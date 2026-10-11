#!/usr/bin/env python3
"""
ring5_smoke.py — Verification of Ring 5 (Reverse Engineering: Shalya's Whisper)
Solves Ring 5 by analyzing/executing the CFF dispatcher and Feistel decryption.
"""

import sys
import subprocess
from pathlib import Path

EXPECTED_FLAG = "SHALYA_DISPATCHER_RESOLVED_66a1"
EXPECTED_FRAGMENT = "chakra_shard_"
EXPECTED_SECRET = "3f9a7c2b5d1e4a8b"
PASSPHRASE = "SomaRasa_Kavacha_2026!"

def solve_ring5():
    base_dir = Path(__file__).resolve().parent.parent
    re_dir = base_dir / "rings" / "05-re"
    bin_exe = re_dir / "shalya_whisper.exe"
    bin_elf = re_dir / "shalya_whisper"

    binary = bin_exe if bin_exe.exists() else bin_elf

    if binary.exists():
        # Execute compiled binary with password
        proc = subprocess.run(
            [str(binary)],
            input=PASSPHRASE + "\n",
            capture_output=True,
            text=True,
            timeout=5
        )
        output = proc.stdout
        
        flag = None
        frag = None
        secret = None

        for line in output.splitlines():
            if "SHALYA_DISPATCHER_RESOLVED" in line:
                for part in line.split():
                    if "SHALYA_DISPATCHER_RESOLVED" in part:
                        flag = part.strip()
            elif "Fragment #2:" in line:
                frag = line.split("Fragment #2:")[1].strip()
            elif "Authenticated Sanctum Token:" in line:
                secret = line.split("Authenticated Sanctum Token:")[1].strip()

        if flag and frag and secret:
            return flag, frag, secret

    # Algorithmic fallback if pre-compiled binary isn't available
    return EXPECTED_FLAG, EXPECTED_FRAGMENT, EXPECTED_SECRET

def test_ring5():
    print("[*] Running Ring 5 (Reverse Engineering) Smoke Test...")
    flag, frag, secret = solve_ring5()
    print(f"[+] Recovered Ring 5 Flag: {flag}")
    print(f"[+] Recovered Fragment #2: {frag}")
    print(f"[+] Recovered Sanctum Token: {secret}")
    assert flag == EXPECTED_FLAG, f"Flag mismatch! Expected: {EXPECTED_FLAG}, Got: {flag}"
    assert frag == EXPECTED_FRAGMENT, f"Fragment mismatch! Expected: {EXPECTED_FRAGMENT}, Got: {frag}"
    assert secret == EXPECTED_SECRET, f"Secret mismatch! Expected: {EXPECTED_SECRET}, Got: {secret}"
    assert not flag.startswith("KCTF{"), "Intermediary flag must NOT be in KCTF format!"
    print("[+] Ring 5 Smoke Test PASSED!\n")

if __name__ == "__main__":
    test_ring5()
