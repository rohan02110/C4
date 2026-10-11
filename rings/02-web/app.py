import os
import json
import base64
import hmac
import hashlib
import socket
import ipaddress
import urllib.parse
from pathlib import Path
from flask import Flask, request, jsonify, Response
import jwt
import requests

app = Flask(__name__)

KEYS_DIR = Path(__file__).resolve().parent / "keys"
RSA_PRIV_KEY = (KEYS_DIR / "portal_priv.pem").read_text()
RSA_PUB_KEY = (KEYS_DIR / "portal_pub.pem").read_text()

FLAG_RING_2 = os.getenv("FLAG_RING_2", "KRIPACHARYA_ADMIN_SEAM_EXPOSED_55d1")

FORBIDDEN_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]

def verify_token(token: str):
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get("alg")
        
        # VULNERABILITY: Algorithm Confusion
        # When alg is HS256, it verifies HMAC using RSA_PUB_KEY as secret
        if alg == "HS256":
            parts = token.split(".")
            if len(parts) == 3:
                signing_input = f"{parts[0]}.{parts[1]}".encode()
                # Pad signature base64 if needed
                sig_b64 = parts[2]
                sig_b64 += "=" * ((4 - len(sig_b64) % 4) % 4)
                sig = base64.urlsafe_b64decode(sig_b64)
                expected_sig = hmac.new(RSA_PUB_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
                if hmac.compare_digest(sig, expected_sig):
                    payload_b64 = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)
                    return json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))
            return None
        elif alg == "RS256":
            return jwt.decode(token, RSA_PUB_KEY, algorithms=["RS256"])
        else:
            raise ValueError(f"Unsupported algorithm {alg}")
    except Exception as e:
        return None


def require_auth(required_role=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or malformed Authorization header"}), 401
            token = auth_header.split(" ", 1)[1].strip()
            claims = verify_token(token)
            if not claims:
                return jsonify({"error": "Invalid token signature or algorithm"}), 401
            if required_role and claims.get("role") != required_role:
                return jsonify({"error": f"Forbidden: '{required_role}' privilege required"}), 403
            request.claims = claims
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks():
    return jsonify({
        "keys": [{
            "kty": "RSA",
            "use": "sig",
            "alg": "RS256",
            "kid": "kripa-portal-key-1",
            "pem": RSA_PUB_KEY
        }]
    })

@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if username == "analyst_sd" and password == "indra2023!":
        payload = {
            "sub": username,
            "role": "analyst",
            "iss": "vyuha-portal",
            "scope": ["view_dashboard", "read_reports"]
        }
        token = jwt.encode(payload, RSA_PRIV_KEY, algorithm="RS256", headers={"kid": "kripa-portal-key-1"})
        return jsonify({
            "status": "authenticated",
            "token": token,
            "role": "analyst"
        })
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/v1/dashboard", methods=["GET"])
@require_auth(required_role=None)
def dashboard():
    claims = request.claims
    role = claims.get("role")
    if role == "admin":
        return jsonify({
            "status": "admin_granted",
            "message": "Welcome Commander Kripacharya.",
            "intermediate_flag_2": FLAG_RING_2,
            "access_features": ["pdf_export", "notes_inspection"]
        })
    return jsonify({
        "status": "analyst_limited",
        "message": "Low privilege session. Switch to admin role to unlock incident export tools.",
        "role": role
    })

@app.route("/api/v1/notes/<int:note_id>", methods=["GET"])
@require_auth(required_role=None)
def get_note(note_id: int):
    if note_id == 4471:
        return jsonify({
            "note_id": 4471,
            "classification": "TOP_SECRET_CORE",
            "title": "Case 4471: Drona Archive Vault Synchronization",
            "content": "Case 4471 contains the Ashwatthama incident trace. Service drona-vault is stationed at http://drona.internal:8080/api/v1/cases/lookup.",
            "status": "PENDING_AUDIT"
        })
    return jsonify({"error": "Note not found"}), 404

@app.route("/api/v1/reports/<int:report_id>/export", methods=["GET"])
@require_auth(required_role="admin")
def export_report(report_id: int):
    source_url = request.args.get("source_url")
    if not source_url:
        return jsonify({"error": "Missing source_url parameter"}), 400

    parsed = urllib.parse.urlparse(source_url)
    if not parsed.scheme or not parsed.hostname:
        return jsonify({"error": "Malformed source_url"}), 400

    # Hardened Anti-SSRF Check:
    # Blocks "internal" string in hostname and direct private IPv4 subnets
    if "internal" in parsed.hostname.lower():
        # Bypassable via decimal/hex IP, redirect, or IPv6 dual-stack encapsulation
        return jsonify({"error": "SSRF Security Filter: Access to *.internal domains blocked"}), 403

    try:
        resolved_ip = socket.gethostbyname(parsed.hostname)
        ip_obj = ipaddress.ip_address(resolved_ip)
        for net in FORBIDDEN_NETWORKS:
            if ip_obj in net:
                return jsonify({"error": f"SSRF Security Filter: Access to private IP {resolved_ip} blocked"}), 403
    except Exception:
        pass # Allow resolving or alternate formats

    try:
        # Fetch content (SSRF exploit point)
        resp = requests.get(source_url, timeout=4)
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type", "text/plain"))
    except Exception as e:
        return jsonify({"error": f"Upstream fetch failure: {str(e)}"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=False)
