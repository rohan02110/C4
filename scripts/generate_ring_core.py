#!/usr/bin/env python3
"""
generate_ring_core.py — Generates encrypted Ring Core artifact (ring_core.enc)
Uses AES-256-CBC with SHA256(Fragment1 + Fragment2 + Fragment3) as the key.
Plaintext is the Final Master Flag:
    KCTF{4\x42HIM4NYU_F0UND_7H3_3XI7_88}
"""

import os
import hashlib
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

FRAGMENT_1 = "k4vach4_"
FRAGMENT_2 = "chakra_shard_"
FRAGMENT_3 = "kund4l4_"
FINAL_FLAG = "KCTF{4\\x42HIM4NYU_F0UND_7H3_3XI7_88}"

# Standard fixed IV for reproducible CTF challenge artifact
STATIC_IV = b"CHAKRAVYUHA_IV01" # 16 bytes

def generate_key() -> bytes:
    combined = (FRAGMENT_1 + FRAGMENT_2 + FRAGMENT_3).encode("utf-8")
    return hashlib.sha256(combined).digest()

def encrypt_core(plaintext: str, key: bytes, iv: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()

def decrypt_core(ciphertext: bytes, key: bytes, iv: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode("utf-8")

def main():
    base_dir = Path(__file__).resolve().parent.parent
    sanctum_dir = base_dir / "rings" / "07-pwn" / "sanctum"
    sanctum_dir.mkdir(parents=True, exist_ok=True)
    out_file = sanctum_dir / "ring_core.enc"

    key = generate_key()
    ciphertext = encrypt_core(FINAL_FLAG, key, STATIC_IV)

    # Write IV (16 bytes) + ciphertext to ring_core.enc
    payload = STATIC_IV + ciphertext
    out_file.write_bytes(payload)
    print(f"[+] Successfully generated: {out_file} ({len(payload)} bytes)")

    # Verify self-test
    iv_read = payload[:16]
    enc_data = payload[16:]
    recovered = decrypt_core(enc_data, key, iv_read)
    assert recovered == FINAL_FLAG, "Decryption verification failed!"
    print(f"[+] Decryption verification successful! Plaintext: {recovered}")

if __name__ == "__main__":
    main()
