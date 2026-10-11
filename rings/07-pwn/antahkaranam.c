/*
 * ANTAHKARANAM ("The Inner Chamber") — Ring 7 Binary Exploitation Target
 * Guardian: Brihadbala
 *
 * "Brihadbala was slain, and Abhimanyu breached the heart of the Chakravyuha...
 *  and found himself sealed inside."
 *
 * Vulnerability Architecture:
 * 1. Custom heap chunk table with function pointer dispatch table
 * 2. Use-After-Free: do_free frees chunk data without nulling table[idx]
 * 3. Menu dispatch: ALLOC, WRITE, FREE, SEND
 * 4. Protections: Full RELRO, Canary, PIE, NX enabled
 * 5. Seccomp Sandbox: Blocks execve, requires Open-Read-Write (ORW) ROP
 * 6. In-Process Rekey Timer: alarm(600) on auth success
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#include <sys/types.h>

#if defined(__linux__)
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/syscall.h>
#endif

#define MAX_CHUNKS 16
#define DEFAULT_REKEY_TIMEOUT 600

// Target Artifacts in Container:
// /sanctum/token         -> BRIHADBALA_SANCTUM_COMPROMISED_7714
// /sanctum/ring_core.enc -> AES-256 encrypted payload

typedef struct chunk {
    size_t size;
    void (*on_send)(struct chunk *);
    char *data;
} chunk_t;

static chunk_t *table[MAX_CHUNKS];

static void default_send_handler(chunk_t *c) {
    if (c && c->data) {
        printf("[+] Transmitting chunk [%p]: ", (void *)c);
        write(STDOUT_FILENO, c->data, c->size);
        printf("\n");
    } else {
        printf("[-] Chunk contains uninitialized or stale transmission buffer.\n");
    }
}

// Seccomp BPF Sandbox Filter (Restricts execution to ORW)
static void install_seccomp_sandbox(void) {
#if defined(__linux__) && defined(PR_SET_SECCOMP)
    struct sock_filter filter[] = {
        // Load syscall architecture
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, arch))),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        // Load syscall number
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, nr))),

        // Allow read, write, open, openat, close, exit, exit_group, alarm, fstat
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 8, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_write, 7, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_open, 6, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_openat, 5, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_close, 4, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_exit, 3, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_exit_group, 2, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_alarm, 1, 0),

        // Deny all other syscalls (including execve, fork, clone)
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW)
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == -1) {
        perror("prctl(NO_NEW_PRIVS)");
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog) == -1) {
        perror("prctl(SECCOMP)");
    }
#endif
}

// Rekey Alarm Handler
static void handle_rekey_alarm(int sig) {
    (void)sig;
    const char msg[] = "\n\n[!] FORMATION INTEGRITY ALARM EXPIRED! Keys rotated. Sanctum resealed.\n";
    write(STDOUT_FILENO, msg, sizeof(msg) - 1);
    _exit(0);
}

static void authenticate_live_session(void) {
    char *is_practice = getenv("IS_PRACTICE");
    if (is_practice && strcmp(is_practice, "1") == 0) {
        printf("[*] Ungated Practice Replica. Token gate bypassed.\n");
        return;
    }

    char *expected_secret = getenv("HEAP_TOKEN_SECRET");
    if (!expected_secret) expected_secret = "3f9a7c2b5d1e4a8b";

    printf("====================================================================\n");
    printf("   ANTAHKARANAM // BRIHADBALA'S SANCTUM (TOKEN VERIFICATION)         \n");
    printf("====================================================================\n");
    printf("[?] Enter Ring 5 Discovered Authentication Token: ");
    fflush(stdout);

    char input_token[64];
    if (!fgets(input_token, sizeof(input_token), stdin)) {
        _exit(1);
    }
    input_token[strcspn(input_token, "\r\n")] = '\0';

    if (strcmp(input_token, expected_secret) != 0) {
        printf("[-] Unauthorized challenger. Access to inner sanctum denied.\n");
        _exit(1);
    }

    printf("[+] Authentication accepted. Sanctum gates unsealed.\n");
}

static void do_alloc(void) {
    int idx = -1;
    for (int i = 0; i < MAX_CHUNKS; i++) {
        if (!table[i]) {
            idx = i;
            break;
        }
    }
    if (idx == -1) {
        printf("[-] Chunk table full.\n");
        return;
    }

    printf("[?] Allocation size (16-1024): ");
    size_t sz = 0;
    if (scanf("%zu", &sz) != 1 || sz < 16 || sz > 1024) {
        printf("[-] Invalid size.\n");
        return;
    }

    chunk_t *c = (chunk_t *)malloc(sizeof(chunk_t));
    if (!c) {
        perror("malloc");
        return;
    }
    c->size = sz;
    c->on_send = default_send_handler;
    c->data = (char *)malloc(sz);
    if (!c->data) {
        free(c);
        return;
    }
    memset(c->data, 0, sz);
    table[idx] = c;

    printf("[+] Chunk allocated at index %d [addr: %p, data: %p]\n", idx, (void *)c, (void *)c->data);
}

static void do_write(void) {
    int idx;
    printf("[?] Target index: ");
    if (scanf("%d", &idx) != 1 || idx < 0 || idx >= MAX_CHUNKS || !table[idx]) {
        printf("[-] Invalid index.\n");
        return;
    }

    printf("[?] Payload (raw bytes): ");
    char buf[1024];
    ssize_t n = read(STDIN_FILENO, buf, table[idx]->size);
    if (n > 0 && table[idx]->data) {
        memcpy(table[idx]->data, buf, n);
        printf("[+] %zd bytes written to index %d.\n", n, idx);
    }
}

// THE VULNERABILITY: Use-After-Free
static void do_free(void) {
    int idx;
    printf("[?] Target index to free: ");
    if (scanf("%d", &idx) != 1 || idx < 0 || idx >= MAX_CHUNKS || !table[idx]) {
        printf("[-] Invalid index.\n");
        return;
    }

    // Free data buffer and chunk structure, but DO NOT null table[idx]!
    free(table[idx]->data);
    free(table[idx]);
    // table[idx] = NULL;  <-- DELIBERATE VULNERABILITY: DANGLING POINTER IN TABLE

    printf("[+] Memory released for index %d.\n", idx);
}

static void do_send(void) {
    int idx;
    printf("[?] Target index to dispatch: ");
    if (scanf("%d", &idx) != 1 || idx < 0 || idx >= MAX_CHUNKS || !table[idx]) {
        printf("[-] Invalid index.\n");
        return;
    }

    // Invokes on_send on potentially reclaimed / dangling chunk_t
    table[idx]->on_send(table[idx]);
}

int main(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

#if defined(SIGALRM)
    signal(SIGALRM, handle_rekey_alarm);
#endif

    // Gated token authentication
    authenticate_live_session();

    // In-process 10-minute rekey timer
    char *timeout_str = getenv("REKEY_TIMEOUT_SECONDS");
    int timeout = timeout_str ? atoi(timeout_str) : DEFAULT_REKEY_TIMEOUT;
    if (timeout <= 0) timeout = DEFAULT_REKEY_TIMEOUT;
#if defined(SIGALRM)
    alarm(timeout);
    printf("[*] Formation Rekey Alarm armed: %d seconds remaining.\n", timeout);
#else
    printf("[*] Formation Rekey Alarm configured: %d seconds.\n", timeout);
#endif

    // Install Seccomp sandbox
    install_seccomp_sandbox();

    printf("\n=== CHAKRAVYUHA INNER CHAMBER: ANTAHKARANAM ===\n");
    printf("1. ALLOC chunk\n");
    printf("2. WRITE chunk\n");
    printf("3. FREE chunk (UAF seam)\n");
    printf("4. SEND chunk dispatch\n");
    printf("5. EXIT\n");

    while (1) {
        printf("\n> ");
        int choice;
        if (scanf("%d", &choice) != 1) break;

        switch (choice) {
            case 1: do_alloc(); break;
            case 2: do_write(); break;
            case 3: do_free(); break;
            case 4: do_send(); break;
            case 5: printf("[*] Departing inner sanctum.\n"); return 0;
            default: printf("[-] Unknown command.\n"); break;
        }
    }

    return 0;
}
