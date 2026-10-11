# BUILD_NOTES.md — Chakravyuha: The Seventh Ring

## Architectural Decisions & Build Specifications

### 1. Updated Flag Architecture
- **Intermediary Flags:** In accordance with the revised challenge architecture, all intermediate flags for Rings 1 through 7 are **generic tokens and access seals**, strictly omitting the `KCTF{...}` wrapper:
  - Ring 1 (OSINT): `JAYADRATHA_GATE_BYPASS_9a8f27c3e510`
  - Ring 2 (Web): `KRIPACHARYA_ADMIN_SEAM_EXPOSED_55d1`
  - Ring 3 (SQL Injection): `DRONA_VAULT_QUERY_INJECTED_4471`
  - Ring 4 (Forensics): `ASHWATTHAMA_MEMORY_VAD_CARVED_77c2`
  - Ring 5 (Reverse Engineering): `SHALYA_DISPATCHER_RESOLVED_66a1`
  - Ring 6 (Steganography): `KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9`
  - Ring 7 (Binary Exploitation): `BRIHADBALA_SANCTUM_COMPROMISED_7714`
- **Final Core Exit Flag:** Strictly formatted in `KCTF{...}`:
  `KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}`
  The literal `\x42` is checked as four exact characters without escape-sequence decoding.

### 2. Replacement of LLM Jailbreak with SQL Injection (Ring 3)
- **Guardian:** Drona (Master of Shastras & Astras).
- **Service:** `drona-vault` (FastAPI + PostgreSQL 15).
- **Network Placement:** Strictly internal (`internal` Docker network) at `http://drona.internal:8080`, reachable solely via Ring 2's SSRF exploit.
- **Vulnerability:** AST-evading SQL Injection into case lookup query.
  - Bypasses whitespace filtering via PostgreSQL `%0a`, `%09`, or parenthesis notation.
  - Bypasses string/comment filtering via dollar-quoting (`$$...$$`) or `CHR()` concatenation.
  - Uses stacked queries / database notification triggers (`pg_notify('vault_unlock', 'case=4471')`) to dispatch the webhook to `ashwatthama-host`.

### 3. Elevated Challenge Difficulty & Hardening
- **Ring 1 (OSINT):** Multi-layered passive recon across hardened decoy gate, Certificate Transparency SANs, developer repo commit histories, and geolocated talk slides.
- **Ring 2 (Web):** Dynamic `kid` JWT algorithm confusion (RS256 -> HS256 with public key HMAC) combined with anti-SSRF IP/subnet blacklist bypass via URL parser differentials and dual-stack notation.
- **Ring 4 (Forensics):** Purged PSReadLine history; unmapped VAD descriptor carving in `vyuha_sync.exe`; in-memory decryption of heap structures for Fragment #1 (`k4vach4_`).
- **Ring 5 (RE):** Multi-stage anti-debugging (`ptrace`, `rdtsc` timing check), Control Flow Flattening (CFF) state machine with opaque predicates, Feistel cipher decryption, and self-integrity `.text` hashing for Fragment #2.
- **Ring 6 (Stego):** Custom LSB matrix and polyglot archive embedding Fragment #3 (`kund4l4_`) and the `shalya_whisper` ELF binary, avoiding standard automated steghide extraction.
- **Ring 7 (Pwn):** Menu-driven C service with Use-After-Free in heap chunk dispatch; hardened with Full RELRO, PIE, Canary, NX; strict Seccomp BPF sandbox enforcing Open-Read-Write (ORW) exploitation to read sanctum token and `ring_core.enc`.
- **Rekey Timer:** In-process `alarm(600)` initiated upon successful live token authentication.

### 4. Interactive Battlefield Portal UI
- Interactive frontend built with **Vite** and **Tailwind CSS**.
- Features visual representation of the 7 concentric Chakravyuha rings with animated canvas particle trails, ring status trackers, challenge terminals, and a simulated 10-minute rekey escape countdown console.
