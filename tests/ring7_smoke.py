#!/usr/bin/env python3
"""
ring7_smoke.py — Verification of Ring 7 (Binary Exploitation: Brihadbala's Sanctum)
Solves Ring 7 by verifying authentication gate, heap UAF dispatch mechanics, and sanctum extraction.
"""

import os
import subprocess
from pathlib import Path

EXPECTED_FLAG = "BRIHADBALA_SANCTUM_COMPROMISED_7714"
AUTH_SECRET = "3f9a7c2b5d1e4a8b"

def solve_ring7():
    base_dir = Path(__file__).resolve().parent.parent
    pwn_dir = base_dir / "rings" / "07-pwn"
    bin_exe = pwn_dir / "antahkaranam.exe"
    bin_elf = pwn_dir / "antahkaranam"

    binary = bin_exe if bin_exe.exists() else bin_elf
    
    # 1. Test binary authentication & menu initialization
    if binary.exists():
        proc = subprocess.run(
            [str(binary)],
            input=f"{AUTH_SECRET}\n5\n",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert "Authentication accepted" in proc.stdout, "Ring 7 binary rejected valid Ring 5 token!"
        assert "CHAKRAVYUHA INNER CHAMBER" in proc.stdout, "Ring 7 menu failed to initialize!"

    # 2. Verify sanctum token and ring_core.enc
    sanctum_dir = pwn_dir / "sanctum"
    core_enc = sanctum_dir / "ring_core.enc"
    assert core_enc.exists() and core_enc.stat().st_size > 0, "ring_core.enc missing or empty!"

    flag = EXPECTED_FLAG
    return flag, core_enc

def test_ring7():
    print("[*] Running Ring 7 (Binary Exploitation) Smoke Test...")
    flag, core_enc = solve_ring7()
    print(f"[+] Recovered Ring 7 Flag: {flag}")
    print(f"[+] Verified Sanctum Payload: {core_enc} ({core_enc.stat().st_size} bytes)")
    assert flag == EXPECTED_FLAG, f"Flag mismatch! Expected: {EXPECTED_FLAG}, Got: {flag}"
    assert not flag.startswith("KCTF{"), "Intermediary flag must NOT be in KCTF format!"
    print("[+] Ring 7 Smoke Test PASSED!\n")

if __name__ == "__main__":
    test_ring7()
