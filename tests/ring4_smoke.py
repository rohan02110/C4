#!/usr/bin/env python3
"""
ring4_smoke.py — Verification of Ring 4 (Memory Forensics: Ashwatthama's Host)
Solves Ring 4 by carving the memory dump for unmapped VAD descriptor structures in vyuha_sync.exe.
"""

import re
import zipfile
import base64
from pathlib import Path

EXPECTED_FLAG = "ASHWATTHAMA_MEMORY_VAD_CARVED_77c2"
EXPECTED_FRAGMENT = "k4vach4_"
EXPECTED_PASSWORD = "SomaRasa_Kavacha_2026!"

def solve_ring4():
    base_dir = Path(__file__).resolve().parent.parent
    zip_path = base_dir / "rings" / "04-forensics" / "vault" / "ashwatthama_trace.mem.zip"
    
    assert zip_path.exists(), f"Forensic artifact missing: {zip_path}"

    with zipfile.ZipFile(zip_path, "r") as zf:
        mem_data = zf.read("ashwatthama_trace.mem")

    # Forensic carving: Locate the configuration block
    config_match = re.search(
        rb"=== VYUHA_SYNC CONFIGURATION BLOCK ===(.*?)=== END CONFIGURATION BLOCK ===",
        mem_data,
        re.DOTALL
    )
    assert config_match, "Configuration block not found in memory dump!"
    block = config_match.group(1).decode("utf-8", errors="ignore")

    flag_match = re.search(r"SIG_INTEGRITY=([A-Za-z0-9_]+)", block)
    frag_match = re.search(r"FRAGMENT_1=([A-Za-z0-9_]+)", block)
    pwd_match = re.search(r"STEGO_PASSPHRASE=([^\r\n]+)", block)
    img_match = re.search(r"IMAGE_PAYLOAD_BASE64=([A-Za-z0-9+/=]+)", block)

    assert flag_match, "SIG_INTEGRITY (Flag 4) missing from carved block"
    assert frag_match, "FRAGMENT_1 missing from carved block"
    assert pwd_match, "STEGO_PASSPHRASE missing from carved block"
    assert img_match, "IMAGE_PAYLOAD_BASE64 missing from carved block"

    flag = flag_match.group(1)
    frag = frag_match.group(1)
    pwd = pwd_match.group(1)

    # Verify extracted PNG
    png_bytes = base64.b64decode(img_match.group(1))
    assert png_bytes.startswith(b"\x89PNG\r\n\x1a\n"), "Extracted image payload is not valid PNG!"

    return flag, frag, pwd

def test_ring4():
    print("[*] Running Ring 4 (Memory Forensics) Smoke Test...")
    flag, frag, pwd = solve_ring4()
    print(f"[+] Recovered Ring 4 Flag: {flag}")
    print(f"[+] Recovered Fragment #1: {frag}")
    print(f"[+] Recovered Stego Password: {pwd}")
    assert flag == EXPECTED_FLAG, f"Flag mismatch! Expected: {EXPECTED_FLAG}, Got: {flag}"
    assert frag == EXPECTED_FRAGMENT, f"Fragment mismatch! Expected: {EXPECTED_FRAGMENT}, Got: {frag}"
    assert pwd == EXPECTED_PASSWORD, f"Password mismatch! Expected: {EXPECTED_PASSWORD}, Got: {pwd}"
    assert not flag.startswith("KCTF{"), "Intermediary flag must NOT be in KCTF format!"
    print("[+] Ring 4 Smoke Test PASSED!\n")

if __name__ == "__main__":
    test_ring4()
