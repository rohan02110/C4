#!/usr/bin/env python3
"""
ring1_smoke.py — Verification of Ring 1 (OSINT: Jayadratha's Gate)
Solves Ring 1 by extracting the concealed perimeter token from staging HTML headers.
"""

import re
from pathlib import Path

EXPECTED_FLAG = "JAYADRATHA_GATE_BYPASS_9a8f27c3e510"

def solve_ring1() -> str:
    base_dir = Path(__file__).resolve().parent.parent
    staging_file = base_dir / "rings" / "01-osint" / "html" / "staging.html"
    
    assert staging_file.exists(), f"Staging file not found: {staging_file}"
    content = staging_file.read_text(encoding="utf-8")
    
    # Extract token from HTTP header comment or meta tag
    # Format: X-Perimeter-Token: JAYADRATHA_GATE_BYPASS_9a8f27c3e510
    match = re.search(r"X-Perimeter-Token:\s*([A-Za-z0-9_]+)", content)
    if not match:
        # Fallback to direct token search
        match = re.search(r"JAYADRATHA_GATE_BYPASS_[a-f0-9]+", content)
        assert match, "Could not locate Jayadratha perimeter token in staging artifact."
        return match.group(0)
        
    return match.group(1)

def test_ring1():
    print("[*] Running Ring 1 (OSINT) Smoke Test...")
    flag = solve_ring1()
    print(f"[+] Recovered Ring 1 Flag: {flag}")
    assert flag == EXPECTED_FLAG, f"Flag mismatch! Expected: {EXPECTED_FLAG}, Got: {flag}"
    # Verify strict intermediary rule: No KCTF prefix
    assert not flag.startswith("KCTF{"), "Intermediary flag must NOT be in KCTF format!"
    print("[+] Ring 1 Smoke Test PASSED!\n")

if __name__ == "__main__":
    test_ring1()
