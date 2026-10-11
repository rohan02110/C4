/*
 * SHALYA_WHISPER — Ring 5 Reverse Engineering Target
 * Guardian: Shalya (Karna's Charioteer)
 *
 * "The reins of Karna's chariot are in my hands, yet the arrow finds not its mark."
 * Outward compliance concealing an inner cryptographic agenda.
 *
 * Mitigations & Obfuscation:
 * 1. Multi-Stage Anti-Debugging (ptrace TRACEME, /proc/self/status TracerPid, rdtsc timing)
 * 2. Control Flow Flattening (CFF) state machine with opaque predicates
 * 3. Dynamic Feistel / Rolling Decryption of strings in .rodata
 * 4. Self-Integrity verification
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>

#if defined(__linux__)
#include <sys/ptrace.h>
#include <x86intrin.h>
#endif

// Intermediate Flag 5: SHALYA_DISPATCHER_RESOLVED_66a1
// Fragment #2: chakra_shard_
// Token Secret: 3f9a7c2b5d1e4a8b
// Target Port: 9007

// Obfuscated encrypted payloads
static unsigned char enc_flag5[] = {
    0x0a, 0x5d, 0xb5, 0xb8, 0xac, 0xbf, 0x18, 0xcf, 0xe7, 0x9b, 0xca, 0x68, 0xcb, 0x10, 0xba, 0xb5,
    0xb3, 0x35, 0xfd, 0x9f, 0x67, 0x4f, 0x2c, 0x32, 0xc0, 0xcb, 0xbf, 0x5a, 0xff, 0xd4, 0x24, 0x11
};

static unsigned char enc_frag2[] = {
    0x3a, 0x7d, 0x95, 0x9f, 0x87, 0x9f, 0x18, 0xf8, 0xc6, 0xa9, 0xe8, 0x4d, 0xc0, 0x53
};

static unsigned char enc_sanctum[] = {
    0x35, 0x7a, 0x97, 0x95, 0x99, 0x96, 0x28, 0xf8, 0xda, 0xf2, 0xa3, 0x19, 0xaf, 0x64, 0xf2
};

// Anti-debugging verification
static int perform_security_checks(void) {
#if defined(__linux__)
    // 1. Ptrace TRACEME
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        return 0; // Traced!
    }

    // 2. /proc/self/status TracerPid check
    int fd = open("/proc/self/status", O_RDONLY);
    if (fd >= 0) {
        char buf[1024];
        ssize_t bytes = read(fd, buf, sizeof(buf) - 1);
        close(fd);
        if (bytes > 0) {
            buf[bytes] = '\0';
            char *tracer = strstr(buf, "TracerPid:");
            if (tracer) {
                int pid = atoi(tracer + 10);
                if (pid != 0) return 0; // Debugger attached
            }
        }
    }

    // 3. RDTSC Execution Cycle Timing Check
    unsigned long long t1 = __rdtsc();
    for (volatile int i = 0; i < 1000; i++);
    unsigned long long t2 = __rdtsc();
    if ((t2 - t1) > 0x1000000) {
        return 0; // Breakpoint single-stepping detected
    }
#endif
    return 1;
}

// Feistel-inspired rolling state decryptor
static void decrypt_buffer(unsigned char *buf, size_t len, unsigned char key) {
    unsigned char state = key;
    for (size_t i = 0; i < len; i++) {
        unsigned char orig = buf[i];
        buf[i] = orig ^ state;
        // Rolling key schedule
        state = (unsigned char)(((state << 3) | (state >> 5)) + 0x4B + i);
    }
}

int main(int argc, char **argv) {
    printf("====================================================================\n");
    printf("     CHAKRAVYUHA // RING 5: SHALYA'S WHISPER (THE CHARIOTEER)       \n");
    printf("====================================================================\n");

    // Control Flow Flattening State Machine
    int state = 0x1337;
    int checks_passed = 0;
    int is_reveal = (argc > 1 && strcmp(argv[1], "--reveal") == 0);

    while (state != 0xFFFF) {
        // Opaque predicate: (state * (state + 1)) is always even
        int opaque = (state * (state + 1)) % 2;

        switch (state) {
            case 0x1337:
                // State 1: Anti-analysis check
                checks_passed = perform_security_checks();
                if (!checks_passed) {
                    state = 0xDEAD;
                } else {
                    state = (opaque == 0) ? 0x2442 : 0x0000;
                }
                break;

            case 0x2442:
                // State 2: Narrative check
                if (!is_reveal) {
                    printf("[SHALYA]: The reins of Karna's chariot are in my hands,\n");
                    printf("          yet the arrow finds not its mark.\n");
                    printf("          Look deeper into the binary's inner dispatcher (--reveal).\n\n");
                    state = 0xFFFF; // Exit gracefully
                } else {
                    state = 0x3553;
                }
                break;

            case 0x3553:
                // State 3: Decrypt Flag 5 and Fragment 2
                printf("[+] De-flattening dispatch state machine...\n");
                printf("[+] Security checks satisfied. Recovering confidential parameters...\n\n");

                decrypt_buffer(enc_flag5, sizeof(enc_flag5), 0x59);
                decrypt_buffer(enc_frag2, sizeof(enc_frag2), 0x59);
                decrypt_buffer(enc_sanctum, sizeof(enc_sanctum), 0x59);

                printf("--------------------------------------------------------------------\n");
                printf("  [INTERMEDIATE FLAG 5]  : %s\n", enc_flag5);
                printf("  [PASSPHRASE FRAGMENT #2]: %s\n", enc_frag2);
                printf("  [RING 7 TARGET SANCTUM]: %s\n", enc_sanctum);
                printf("  [HMAC TOKEN SECRET]    : 3f9a7c2b5d1e4a8b\n");
                printf("--------------------------------------------------------------------\n");
                printf("\n[*] Use the HMAC Token Secret to authenticate with Ring 7 on port 9007.\n");
                state = 0xFFFF;
                break;

            case 0xDEAD:
                // State Error: Debugger detected
                fprintf(stderr, "[-] Tampering or debugger presence detected. Shalya feigns ignorance.\n");
                _exit(1);
                break;

            default:
                state = 0xFFFF;
                break;
        }
    }

    return 0;
}
