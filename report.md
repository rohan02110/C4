# Chakravyuha: The Seventh Ring — Master Challenge Report

**Challenge Title:** Chakravyuha: The Seventh Ring  
**Difficulty Tier:** Master-Tier / Sovereign Hard  
**Total Points:** 1,700 Intermediate Points + 500 Completion Bonus  
**Categories:** Multi-Domain Sovereign Gauntlet (OSINT, Web Application Security, SQL Injection, Memory Forensics, Reverse Engineering, Steganography, Binary Exploitation, Cryptographic Engineering)  
**Target Repository:** `https://github.com/rohan02110/C4`  
**Live Frontend Deployment:** `https://the-red-flag.onrender.com`  

---

## 1. Executive Summary & Narrative Context

### 1.1 Mythological & Narrative Premise
In the Mahabharata epic, **Chakravyuha** was an invincible multi-tiered spiral military labyrinth engineered by Guru Drona. Abhimanyu, the young warrior prince, possessed the knowledge to penetrate all concentric rings to reach the inner sanctum, but was never taught the secret of egress. Trapped inside, he was overwhelmed by coordinated enemy commanders.

In this master-tier sovereign CTF challenge, an elite defense consortium built an automated cyber labyrinth named **CHAKRAVYUHA**. Seven defensive rings are maintained by seven autonomous security layers, each guarded by an avatar reflecting the mythic character flaw or archetype of the corresponding Mahabharata warrior:
1. **Jayadratha:** Impenetrable head-on decoy gate (defeated via passive intelligence & staging bypass).
2. **Kripacharya:** Strict procedural martial authority (compromised via JWT algorithm confusion & SSRF).
3. **Drona:** Invocation through formal sacred grammar (shattered via SQL parser injection).
4. **Ashwatthama:** Destructive nocturnal aftermath (reconstructed via memory heap and VAD forensics).
5. **Shalya:** Deceptive allegiance and hidden intent (unmasked via control-flow de-flattening).
6. **Karna:** Impenetrable natural armor (extracted via multi-spectral LSB polyglot steganography).
7. **Brihadbala:** The final guardian of the inner sanctum (compromised via Use-After-Free heap exploitation).

### 1.2 The Narrative Inversion
Competitors must invert Abhimanyu's tragic history: **breach every ring, collect the three narrative passphrase fragments, compromise the inner sanctum binary, and decrypt the core payload before the 10-minute rekey timer permanently reseals the formation.**

---

## 2. Global Challenge Hints (Official 2 Hints)

As mandated for tournament directors and operators, two progressive, high-impact hints are officially provided for the entire challenge to guide teams through its deepest architectural chokepoints:

### 💡 Hint 1: The Threefold Armor of Karna & The Escape Key (Cryptographic Convergence)
> *"Abhimanyu entered with sword in hand, but the final exit was forged of Karna’s divine gifts and Shalya’s whisper. Do not approach Brihadbala’s sanctum before the three pieces of armor are united. The memory wreckage holds the root (`k4vach4_`), the de-flattened dispatcher reveals the center keyed to the secret, and the polyglot archive yields the crown (`kund4l4_`). Concatenate them in linear order and hash the union with SHA-256 to forge the master AES key. Remember: the 10-minute clock starts the second the live gate authenticates—have your decryption script ready before crossing the threshold."*

### 💡 Hint 2: The Fall of the Formal Grammar & The Blind Sanctum (Parser & Seccomp Duality)
> *"Both Drona’s vault and Brihadbala’s sanctum fall to parser inversion rather than raw violence. In the third ring, direct whitespace and comments are forbidden by the AST tokenizer—speak to PostgreSQL in its native tongue of parenthesis encapsulation, dollar-quotes (`$$`), or character concatenation (`CHR`) to trigger the internal dispatch worker. In the seventh ring, once your Use-After-Free primitive rewires the dispatch table, do not seek an interactive `/bin/sh`—the sanctum is bound by a strict Seccomp BPF filter that strikes down `execve`. You must craft an Open-Read-Write (ORW) chain to directly read `/sanctum/token` and recover the core."*

---

## 3. Architecture & Service Topology

```
                   [ PUBLIC INGRESS: the-red-flag.onrender.com ]
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        │                                                                 │
  [ RING 1: OSINT ]                                               [ RING 2: WEB ]
  vyuha-osint-assets (Port 8081)                                  vyuha-portal (Port 8082)
  - CT Logs & Commit diffs                                        - JWT RS256 -> HS256 Confusion
  - Staging gate discovery                                        - URL Parser SSRF Bypass
  Artifact: JAYADRATHA_GATE_BYPASS...                             Artifact: KRIPACHARYA_ADMIN_SEAM...
        │                                                                 │
        └────────────────────────────────┬────────────────────────────────┘
                                         ▼
                                 [ RING 3: SQLi ]
                                 drona-vault (Internal Port 8080)
                                 - AST / WAF Filter Bypass
                                 - Stacked trigger -> ashwatthama unlock
                                 Artifact: DRONA_VAULT_QUERY_INJECTED...
                                         │
                                         ▼ (Dynamic Webhook Unlock)
                                 [ RING 4: DFIR ]
                                 ashwatthama-host (Port 8084)
                                 - Windows Memory Dump (VAD Carving)
                                 - vyuha_sync.exe Decryption
                                 Artifact: ASHWATTHAMA_MEMORY_VAD...
                                 Passphrase Fragment #1: k4vach4_
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
            [ RING 5: RE ]                            [ RING 6: STEGO ]
            shalya_whisper (ELF x86_64)               kavacha.png (Multi-Spectral)
            - Control Flow Flattening (CFF)           - Custom kAvC PNG Chunk
            - Anti-Debug (ptrace/rdtsc)               - Seeded LSB Polyglot Archive
            Artifact: SHALYA_DISPATCHER...            Artifact: KARNA_ARMOR_POLYGLOT...
            Passphrase Fragment #2: <Dynamic>         Passphrase Fragment #3: kund4l4_
                    │                                         │
                    └────────────────────┬────────────────────┘
                                         ▼
                                 [ RING 7: PWN ]
                                 antahkaranam (Live: 9007 / Practice: 9008)
                                 - HMAC Token Gate (Ring 5)
                                 - UAF Heap Dispatch Overlap
                                 - Seccomp BPF Sandbox (ORW Only)
                                 - 10-Minute Rekey Alarm (alarm(600))
                                 Artifact: BRIHADBALA_SANCTUM_COMPROMISED...
                                         │
                                         ▼
                               [ THE FINAL EXIT ]
                               ring_core.enc Decryption
                               AES-256-CBC(SHA-256(Frag1 + Frag2 + Frag3))
                               FINAL FLAG: KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}
```

---

## 4. Technical Breakdown by Ring

### Ring 1 — OSINT (Jayadratha)
- **Concept:** Passive infrastructure discovery and developer leakage.
- **Vulnerabilities:** Certificate Transparency log parsing, sanitized git commit history reconstruction, metadata extraction from technical slide decks.
- **Solve Path:**
  1. Inspect Certificate Transparency search results for `*.ctf.local` to find `vyuha-staging.ctf.local`.
  2. Query commit histories on the architect's public repositories to uncover internal staging environment variables and IP ingress definitions.
  3. Reconstruct the gateway authentication token.
- **Flag 1:** `JAYADRATHA_GATE_BYPASS_9a8f27c3e510` (150 pts)

### Ring 2 — Web Application Security (Kripacharya)
- **Concept:** Cryptographic session forgery and anti-SSRF evasion.
- **Vulnerabilities:** JWT Algorithm/Key Confusion (`RS256` downgraded to `HS256`), Anti-SSRF parser differential, IDOR note leakage.
- **Solve Path:**
  1. Retrieve RSA public key from `/.well-known/jwks.json`.
  2. Forge an administrative token with role `admin` using `HS256`, signing the payload with the public key as the HMAC secret.
  3. Use the PDF export feature at `/api/v1/reports/<id>/export?source_url=...` to bypass IPv4 blacklists using decimal/hex notations (e.g., `http://0x7f000001` or redirection) to pivot to the internal service `http://drona.internal:8080`.
  4. Query `/api/v1/notes/4471` to retrieve the case docket.
- **Flag 2:** `KRIPACHARYA_ADMIN_SEAM_EXPOSED_55d1` (200 pts)

### Ring 3 — SQL Injection (Drona)
- **Concept:** Syntactic parsing corruption and event-driven lateral dispatch.
- **Vulnerabilities:** AST-evading SQL injection in PostgreSQL query parameters without spaces or comments.
- **Solve Path:**
  1. Access the vault search endpoint via Ring 2's SSRF proxy.
  2. Bypass input tokenizers by replacing whitespace with parentheses, brackets, or tab characters (`%09`).
  3. Avoid quotes using PostgreSQL dollar-quoting (`$$...$$`) or `CHR()` concatenation.
  4. Execute a stacked query:
     ```sql
     INSERT INTO dispatch_triggers (action, target_case) VALUES ($$UNLOCK$$, 4471);
     ```
  5. The internal trigger daemon intercepts the event and transmits an authenticated unlock command to `http://ashwatthama-host:8081/unlock`, extracting the flag and unlocking Ring 4.
- **Flag 3:** `DRONA_VAULT_QUERY_INJECTED_4471` (250 pts)

### Ring 4 — Memory Forensics (Ashwatthama)
- **Concept:** Volatility 3 artifact triage and unmapped VAD descriptor carving.
- **Vulnerabilities:** Hidden in-memory process structures, deleted registry transaction logs (`NTUSER.DAT.LOG1`), and volatile heap configurations.
- **Solve Path:**
  1. Download the unlocked `ashwatthama_trace.mem` memory dump.
  2. Execute Volatility 3 `windows.malfind` and `windows.pslist` to detect injected code inside `vyuha_sync.exe`.
  3. Carve the decrypted configuration block from thread local storage.
  4. Extract:
     - Intermediate Flag 4.
     - **Passphrase Fragment #1:** `k4vach4_`.
     - Steganographic password and cover image `kavacha.png`.
- **Flag 4:** `ASHWATTHAMA_MEMORY_VAD_CARVED_77c2` (250 pts)

### Ring 5 — Reverse Engineering (Shalya)
- **Concept:** Obfuscated native binary reversing and cryptographic state recovery.
- **Target:** `shalya_whisper` (x86_64 stripped ELF).
- **Protections:** Control Flow Flattening (CFF) state machine, anti-debug (`ptrace`, `TracerPid`, `rdtsc` cycle count deltas), custom Feistel cipher tamper-checked against `.text` hash.
- **Solve Path:**
  1. Neutralize anti-debugging traps via dynamic instrumentation or binary patching.
  2. Symbolically de-flatten the dispatch table to uncover the real state transitions.
  3. Reverse the Feistel key derivation routines.
  4. Extract:
     - Intermediate Flag 5.
     - Ring 7 HMAC token generation algorithm & embedded secret (`HEAP_TOKEN_SECRET`).
     - **Passphrase Fragment #2:** Dynamic string keyed to `HEAP_TOKEN_SECRET`.
- **Flag 5:** `SHALYA_DISPATCHER_RESOLVED_66a1` (300 pts)

### Ring 6 — Steganography (Karna)
- **Concept:** Multi-spectral image steganography and polyglot extraction.
- **Artifact:** `kavacha.png`.
- **Solve Path:**
  1. Inspect PNG chunk structures to locate the custom ancillary chunk `kAvC`.
  2. Implement an LSB extractor using the PRNG seed recovered in Ring 4.
  3. Extract the polyglot file to obtain:
     - The compiled binary `shalya_whisper` (Ring 5 target).
     - **Passphrase Fragment #3:** `kund4l4_`.
     - Intermediate Flag 6.
- **Flag 6:** `KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9` (200 pts)

### Ring 7 — Binary Exploitation (Brihadbala)
- **Concept:** Heap exploitation under strict Seccomp sandboxing.
- **Target:** `antahkaranam` (Networked C daemon).
- **Protections:** Full RELRO, Stack Canary, NX, PIE, ASLR, Seccomp BPF (blocks `execve`).
- **Solve Path:**
  1. Authenticate using the HMAC token generated from Ring 5.
  2. Exploit a Use-After-Free (UAF) condition where a freed chunk retains an active reference in the dispatch table.
  3. Craft overlapping allocations to hijack the `on_send` function pointer.
  4. Leak heap addresses and libc base via unsorted bin pointers.
  5. Build an Open-Read-Write (ORW) ROP chain or shellcode to read `/sanctum/token` and recover `ring_core.enc`.
- **Flag 7:** `BRIHADBALA_SANCTUM_COMPROMISED_7714` (350 pts)

---

## 5. The Final Exit & Cryptographic Escape

### 5.1 The 10-Minute Rekey Alarm
Connecting to live Ring 7 activates an internal POSIX timer:
```c
alarm(600); // 10 minutes (600 seconds)
```
If the core payload is not decrypted and registered within 10 minutes, the session is terminated and heap allocations are rotated.

### 5.2 Passphrase Assembly & AES Decryption
Assemble the three passphrase fragments in exact sequential order:
```python
import hashlib
from Crypto.Cipher import AES

# Fragments recovered across rings
fragment_1 = "k4vach4_"      # From Ring 4 (Forensics)
fragment_2 = "chakra_shard_" # From Ring 5 (Reverse Engineering)
fragment_3 = "kund4l4_"      # From Ring 6 (Steganography)

passphrase = (fragment_1 + fragment_2 + fragment_3).encode("utf-8")
aes_key = hashlib.sha256(passphrase).digest() # 32-byte AES-256 key

# IV is the first 16 bytes of ring_core.enc
with open("ring_core.enc", "rb") as f:
    ciphertext_blob = f.read()

iv = ciphertext_blob[:16]
encrypted_payload = ciphertext_blob[16:]

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted_bytes = cipher.decrypt(encrypted_payload)

# Remove PKCS7 padding
pad_len = decrypted_bytes[-1]
plaintext = decrypted_bytes[:-pad_len].decode("utf-8")
# Result: 4\x42HIM4NYU_F0UND_7H3_3XI7_88
```

### 5.3 Final Flag Format
Wrap the decrypted secret into the sovereign format:
```
KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}
```
*Note on Validation:* The characters `\x42` are compared **literally as raw characters** (`\`, `x`, `4`, `2`) and must never be evaluated or decoded into byte `0x42` (`B`).

---

## 6. Complete Verification Matrix

| Ring / Stage | Domain | Guardian | Flag / Artifact String | Format | Points | Verification Method |
|---|---|---|---|---|---|---|
| **Ring 1** | OSINT | Jayadratha | `JAYADRATHA_GATE_BYPASS_9a8f27c3e510` | Generic Token | 150 | Automated Portal UI |
| **Ring 2** | Web Security | Kripacharya | `KRIPACHARYA_ADMIN_SEAM_EXPOSED_55d1` | Generic Token | 200 | Automated Portal UI |
| **Ring 3** | SQLi | Drona | `DRONA_VAULT_QUERY_INJECTED_4471` | Generic Token | 250 | Automated Portal UI |
| **Ring 4** | Forensics | Ashwatthama | `ASHWATTHAMA_MEMORY_VAD_CARVED_77c2` | Generic Token | 250 | Automated Portal UI |
| **Ring 5** | Reverse Eng. | Shalya | `SHALYA_DISPATCHER_RESOLVED_66a1` | Generic Token | 300 | Automated Portal UI |
| **Ring 6** | Steganography | Karna | `KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9` | Generic Token | 200 | Automated Portal UI |
| **Ring 7** | Binary Exploit | Brihadbala | `BRIHADBALA_SANCTUM_COMPROMISED_7714` | Generic Token | 350 | Admin Manual Review |
| **Final Exit** | Core Payload | Abhimanyu | `KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}` | Sovereign KCTF | 500 Bonus | Admin Manual Review |

---

## 7. Tournament Administration & Security Controls

1. **No Front-Facing Clues or Hints:**
   The participant website (`the-red-flag.onrender.com`) contains zero visible hints, clues, or solution traces. Developer tools inspection safeguards and clean CSS styling prevent unauthorized asset discovery.
2. **Partial Flag Acceptance:**
   The portal accepts flags for Rings 1 through 6 independently. Ring 7 and the final extraction flag have no public submission box on the website and must be verified directly by CTF Administrators.
3. **Repository Footprint:**
   The repository is optimized at ~13.4 MB (excluding `node_modules`), staying far below the 512 MB platform deployment limit.
4. **Render Deployment Configuration:**
   - Web Service running production server (`node server.js`) with automatic port binding.
   - Fallback `preview.allowedHosts` explicitly configured for `the-red-flag.onrender.com` and all subdomains.
