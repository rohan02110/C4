#!/usr/bin/env python3
"""
full_chain_e2e.py — Master End-to-End Solver & Verification Bot
Simulates a top-tier CTF team breaching all 7 concentric rings of the Chakravyuha:
1. Ring 1 (OSINT) -> Jayadratha's Gate Bypass Token
2. Ring 2 (Web) -> Kripacharya's Admin Seam (JWT Algorithm Confusion)
3. Ring 3 (SQLi) -> Drona's Vault Query Injection (AST/Whitespace bypass)
4. Ring 4 (Forensics) -> Ashwatthama's Memory VAD Carving (Fragment #1)
5. Ring 5 (Reverse Eng) -> Shalya's Whisper CFF Feistel Decryption (Fragment #2 + Auth Secret)
6. Ring 6 (Stego) -> Karna's Armor Polyglot Extraction (Fragment #3)
7. Ring 7 (Pwn) -> Brihadbala's Sanctum Compromise (Sanctum Payload)
8. Core Cryptographic Assembly -> AES-256-CBC Decryption yielding Final Exit Flag:
   KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}
"""

import sys
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Import individual ring solvers
from tests.ring1_smoke import solve_ring1
from tests.ring2_smoke import solve_ring2
from tests.ring3_smoke import solve_ring3
from tests.ring4_smoke import solve_ring4
from tests.ring5_smoke import solve_ring5
from tests.ring6_smoke import solve_ring6
from tests.ring7_smoke import solve_ring7

FINAL_MASTER_FLAG_EXPECTED = "KCTF{4\\x42HIM4NYU_F0UND_7H3_3XI7_88}"

def decrypt_core_artifact(core_path: Path, passphrase: str) -> str:
    raw_data = core_path.read_bytes()
    iv = raw_data[:16]
    ciphertext = raw_data[16:]

    key = hashlib.sha256(passphrase.encode("utf-8")).digest()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext_bytes = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext_bytes.decode("utf-8")

def main():
    print("=" * 72)
    print("       CHAKRAVYUHA: THE SEVENTH RING — MASTER END-TO-END SOLVER       ")
    print("=" * 72)

    total_points = 0

    # -------------------------------------------------------------
    # RING 1: OSINT (Jayadratha's Gate)
    # -------------------------------------------------------------
    print("\n[+] BREACHING RING 1: JAYADRATHA'S GATE (OSINT)...")
    flag1 = solve_ring1()
    print(f"    --> Flag 1 Captured: {flag1}")
    assert not flag1.startswith("KCTF{"), "Ring 1 flag must not have KCTF wrapper"
    total_points += 150

    # -------------------------------------------------------------
    # RING 2: WEB (Kripacharya's Seam)
    # -------------------------------------------------------------
    print("\n[+] BREACHING RING 2: KRIPACHARYA'S SEAM (WEB APPLICATION)...")
    flag2 = solve_ring2()
    print(f"    --> Flag 2 Captured: {flag2}")
    assert not flag2.startswith("KCTF{"), "Ring 2 flag must not have KCTF wrapper"
    total_points += 200

    # -------------------------------------------------------------
    # RING 3: SQL INJECTION (Drona's Vault)
    # -------------------------------------------------------------
    print("\n[+] BREACHING RING 3: DRONA'S VAULT (SQL INJECTION)...")
    flag3 = solve_ring3()
    print(f"    --> Flag 3 Captured: {flag3}")
    assert not flag3.startswith("KCTF{"), "Ring 3 flag must not have KCTF wrapper"
    total_points += 250

    # -------------------------------------------------------------
    # RING 4: FORENSICS (Ashwatthama's Host)
    # -------------------------------------------------------------
    print("\n[+] BREACHING RING 4: ASHWATTHAMA'S MEMORY ISOLATION (FORENSICS)...")
    flag4, frag1, pwd = solve_ring4()
    print(f"    --> Flag 4 Captured: {flag4}")
    print(f"    --> Discovered Passphrase Fragment #1: '{frag1}'")
    print(f"    --> Discovered Stego Password: '{pwd}'")
    assert not flag4.startswith("KCTF{"), "Ring 4 flag must not have KCTF wrapper"
    total_points += 250

    # -------------------------------------------------------------
    # RING 5: REVERSE ENGINEERING (Shalya's Whisper)
    # -------------------------------------------------------------
    print("\n[+] BREACHING RING 5: SHALYA'S WHISPER (REVERSE ENGINEERING)...")
    flag5, frag2, auth_token = solve_ring5()
    print(f"    --> Flag 5 Captured: {flag5}")
    print(f"    --> Discovered Passphrase Fragment #2: '{frag2}'")
    print(f"    --> Discovered Sanctum Auth Token: '{auth_token}'")
    assert not flag5.startswith("KCTF{"), "Ring 5 flag must not have KCTF wrapper"
    total_points += 300

    # -------------------------------------------------------------
    # RING 6: STEGANOGRAPHY (Karna's Armor)
    # -------------------------------------------------------------
    print("\n[+] BREACHING RING 6: KARNA'S ARMOR (STEGANOGRAPHY)...")
    flag6, frag3, embedded_bin = solve_ring6()
    print(f"    --> Flag 6 Captured: {flag6}")
    print(f"    --> Discovered Passphrase Fragment #3: '{frag3}'")
    assert not flag6.startswith("KCTF{"), "Ring 6 flag must not have KCTF wrapper"
    total_points += 350

    # -------------------------------------------------------------
    # RING 7: BINARY EXPLOITATION (Brihadbala's Sanctum)
    # -------------------------------------------------------------
    print("\n[+] BREACHING RING 7: BRIHADBALA'S SANCTUM (BINARY EXPLOITATION)...")
    flag7, core_enc_path = solve_ring7()
    print(f"    --> Flag 7 Captured: {flag7}")
    print(f"    --> Sanctum Sealed Core Infiltrated: {core_enc_path.name}")
    assert not flag7.startswith("KCTF{"), "Ring 7 flag must not have KCTF wrapper"
    total_points += 500

    # -------------------------------------------------------------
    # FINAL EXIT DISCOVERY: CRYPTOGRAPHIC PASSAGE ASSEMBLY
    # -------------------------------------------------------------
    print("\n" + "=" * 72)
    print("       FINAL REVELATION: ASSEMBLING PASSPHRASE FRAGMENTS        ")
    print("=" * 72)
    assembled_passphrase = frag1 + frag2 + frag3
    print(f"[*] Fragment 1: '{frag1}'")
    print(f"[*] Fragment 2: '{frag2}'")
    print(f"[*] Fragment 3: '{frag3}'")
    print(f"[+] Concatenated Master Passphrase: '{assembled_passphrase}'")

    print("[*] Decrypting sanctum ring_core.enc via AES-256-CBC...")
    decrypted_flag = decrypt_core_artifact(core_enc_path, assembled_passphrase)
    print(f"\n[!!!] FINAL CORE EXIT FLAG RECOVERED: {decrypted_flag}")
    
    # Verification of final requirements
    assert decrypted_flag == FINAL_MASTER_FLAG_EXPECTED, f"Final flag mismatch! Got: {decrypted_flag}"
    assert decrypted_flag.startswith("KCTF{") and decrypted_flag.endswith("}"), "Final flag MUST be in strict KCTF{...} format!"
    assert r"\x42" in decrypted_flag, r"Final flag must contain literal \x42"

    print("\n" + "=" * 72)
    print("       CHAKRAVYUHA COMPLETION: ALL 7 RINGS COMPROMISED         ")
    print(f"       SCORE: {total_points} / 2000 POINTS (100% BREACH)       ")
    print("=" * 72)
    print("\n[SUCCESS] ABHIMANYU HAS FOUND THE EXIT AND SURVIVED THE 13TH DAY.\n")

if __name__ == "__main__":
    main()
