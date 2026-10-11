# CHAKRAVYUHA: THE SEVENTH RING

> *"Abhimanyu knew how to enter the Chakravyuha. He was never taught how to leave."*  
> Complete what the myth could not: breach all seven rings, recover the passphrase fragments, compromise the core sanctum, and extract the payload before the formation reseals.

---

## 1. Challenge Architecture & Rings

| Ring | Guardian | Domain | Target Service | Flag Type | Points | Flag / Identifier |
|---|---|---|---|---|---|---|
| **1** | Jayadratha | OSINT | `vyuha-osint-assets` | Generic Token | 150 | `JAYADRATHA_GATE_BYPASS_9a8f27c3e510` |
| **2** | Kripacharya | Web Security | `vyuha-portal` | Generic Token | 200 | `KRIPACHARYA_ADMIN_SEAM_EXPOSED_55d1` |
| **3** | Drona | SQL Injection | `drona-vault` (Internal) | Generic Token | 250 | `DRONA_VAULT_QUERY_INJECTED_4471` |
| **4** | Ashwatthama | Forensics | `ashwatthama-host` | Generic Token | 250 | `ASHWATTHAMA_MEMORY_VAD_CARVED_77c2` |
| **5** | Shalya | Reverse Eng. | `shalya_whisper` | Generic Token | 300 | `SHALYA_DISPATCHER_RESOLVED_66a1` |
| **6** | Karna | Steganography | `kavacha.png` pipeline | Generic Token | 200 | `KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9` |
| **7** | Brihadbala | Binary Exploit | `antahkaranam` (UAF Heap) | Generic Token | 350 | `BRIHADBALA_SANCTUM_COMPROMISED_7714` |
| **EXIT**| Abhimanyu | Cryptographic Escape | `ring_core.enc` | **KCTF Format** | **Bonus** | `KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}` |

---

## 2. Flag Submission Rules & Platform Policy

1. **Intermediate Flags (Stages 1–6 / Rings 1–6):**
   - Non-KCTF generic token format (e.g. `JAYADRATHA_...`, `KRIPACHARYA_...`).
   - Verified and accepted automatically on the Command Portal website across Stages 1 to 6.
2. **Stage 7 & Final Sovereign Flag Submission (Admin Manual Evaluation):**
   - **No automated text box** is provided on the portal for Stage 7 / the final submission.
   - The final exit flag (`KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}`) and Ring 7 pwn exploit must be submitted directly to the **CTF Administrator** for manual verification and registration.
3. **No Hints & Clean UI:**
   - No hints are displayed on the portal. All hint mechanisms and points counters have been completely removed from the frontend.
4. **The 10-Minute Rekey Alarm:**
   - On successful live token authentication to `antahkaranam` (Ring 7), a 10-minute countdown starts (`alarm(600)`).
   - If `ring_core.enc` is not decrypted and the final flag submitted within 10 minutes, the process resets.

---

## 3. Cryptographic Assembly (Passphrase Fragments)

The final core payload `ring_core.enc` is encrypted with AES-256-CBC:
```python
key = sha256(fragment_1 + fragment_2 + fragment_3).digest()
# Fragment 1 (Ring 4): k4vach4_
# Fragment 2 (Ring 5): <derived from HEAP_TOKEN_SECRET>
# Fragment 3 (Ring 6): kund4l4_
```
IV is the first 16 bytes of `ring_core.enc`.

---

## 4. Quickstart & Deployment

### Local Replica Setup:
```bash
cp .env.example .env
make build
make up
```

### Accessing the Rings:
- **Chakravyuha Command Portal (UI):** `http://localhost:5173` (Vite + Tailwind frontend)
- **Ring 1 (OSINT & Staging Gate):** `http://localhost:8081`
- **Ring 2 (Web Portal):** `http://localhost:8082`
- **Ring 3 (Drona Vault):** Internal only (`http://drona.internal:8080`, accessible via SSRF)
- **Ring 4 (Forensics Host):** `http://localhost:8084` (unlocked dynamically by Ring 3)
- **Ring 7 (Brihadbala Pwn - Live):** `localhost:9007` (Token-gated)
- **Ring 7 Practice Replica (Ungated):** `localhost:9008` (`docker compose -f docker-compose.practice.yml up`)
- **Scoring Engine:** `http://localhost:8000`

---

## 5. Operator Runbook

- `make up`: Start all production services with network isolation.
- `make down`: Stop all services.
- `make reset-ring7`: Respawn the pwn container for a clean heap state.
- `make logs-ring N`: View container logs for ring `N`.
- `make rotate-secrets`: Regenerate `HEAP_TOKEN_SECRET` and AES fragment material.
- `make test`: Run automated smoke tests and solver bots across all 7 rings.
