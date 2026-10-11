#!/usr/bin/env python3
"""
ring6_smoke.py — Verification of Ring 6 (Steganography: Karna's Armor)
Solves Ring 6 by extracting the custom PNG 'kAvC' ancillary chunk decrypted with Ring 4 password.
"""

import zlib
import struct
import hashlib
import json
from pathlib import Path

EXPECTED_FLAG = "KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9"
EXPECTED_FRAGMENT = "kund4l4_"
PASSWORD = "SomaRasa_Kavacha_2026!"

def solve_ring6():
    base_dir = Path(__file__).resolve().parent.parent
    png_path = base_dir / "rings" / "06-stego" / "assets" / "kavacha.png"
    
    assert png_path.exists(), f"Stego image not found: {png_path}"
    raw = png_path.read_bytes()

    marker = b"kAvC"
    pos = raw.find(marker)
    assert pos != -1, "kAvC custom chunk not found in PNG carrier!"

    length = struct.unpack(">I", raw[pos - 4:pos])[0]
    compressed_data = raw[pos + 4 : pos + 4 + length]
    encrypted_blob = zlib.decompress(compressed_data)

    key_stream = hashlib.sha256(PASSWORD.encode("utf-8")).digest()
    decrypted = bytearray()
    for i, b in enumerate(encrypted_blob):
        decrypted.append(b ^ key_stream[i % len(key_stream)])

    meta_part, bin_part = bytes(decrypted).split(b"||PAYLOAD_DATA||", 1)
    meta = json.loads(meta_part.decode("utf-8"))

    flag = meta.get("flag6")
    frag = meta.get("fragment3")
    
    return flag, frag, bin_part

def test_ring6():
    print("[*] Running Ring 6 (Steganography) Smoke Test...")
    flag, frag, bin_part = solve_ring6()
    print(f"[+] Recovered Ring 6 Flag: {flag}")
    print(f"[+] Recovered Fragment #3: {frag}")
    print(f"[+] Recovered Embedded Binary Size: {len(bin_part)} bytes")
    assert flag == EXPECTED_FLAG, f"Flag mismatch! Expected: {EXPECTED_FLAG}, Got: {flag}"
    assert frag == EXPECTED_FRAGMENT, f"Fragment mismatch! Expected: {EXPECTED_FRAGMENT}, Got: {frag}"
    assert not flag.startswith("KCTF{"), "Intermediary flag must NOT be in KCTF format!"
    print("[+] Ring 6 Smoke Test PASSED!\n")

if __name__ == "__main__":
    test_ring6()
