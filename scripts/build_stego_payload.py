#!/usr/bin/env python3
"""
build_stego_payload.py — Ring 6 Steganography & Polyglot Builder
Packages Karna's Divine Armor (Kavacha-Kundala):
- Carrier: kavacha.png (ornate gold & crimson armor mandala)
- Embedded Payload:
    - shalya_whisper (Ring 5 RE binary payload)
    - Fragment #3: kund4l4_
    - Intermediate Flag 6: KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9
- Encryption/Encoding: Custom LSB pseudo-random matrix + PNG ancillary chunk 'kAvC'
- Key: SomaRasa_Kavacha_2026! (recovered from Ring 4 memory dump)
"""

import os
import sys
import zlib
import struct
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

PASSWORD = "SomaRasa_Kavacha_2026!"
FLAG_RING_6 = "KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9"
FRAGMENT_3 = "kund4l4_"

def generate_cover_image(out_path: Path):
    """Generates an ornate, high-resolution golden armor mandala image."""
    width, height = 800, 800
    img = Image.new("RGBA", (width, height), (8, 8, 12, 255))
    draw = ImageDraw.Draw(img)

    center = (width // 2, height // 2)

    # Concentric radial aura
    for r in range(360, 20, -10):
        alpha = int(255 * (1 - r / 380))
        gold = (245, 158, 11, max(15, alpha // 6))
        draw.ellipse([center[0] - r, center[1] - r, center[0] + r, center[1] + r], outline=gold, width=2)

    # Sacred warrior spokes
    num_spokes = 24
    import math
    for i in range(num_spokes):
        angle = (i * 2 * math.pi) / num_spokes
        x1 = center[0] + int(math.cos(angle) * 50)
        y1 = center[1] + int(math.sin(angle) * 50)
        x2 = center[0] + int(math.cos(angle) * 340)
        y2 = center[1] + int(math.sin(angle) * 340)
        draw.line([(x1, y1), (x2, y2)], fill=(217, 119, 6, 80), width=1)

    # Center jewel
    draw.ellipse([center[0] - 45, center[1] - 45, center[0] + 45, center[1] + 45], fill=(185, 28, 28, 220), outline=(245, 158, 11, 255), width=3)
    draw.ellipse([center[0] - 25, center[1] - 25, center[0] + 25, center[1] + 25], fill=(234, 179, 8, 240))

    img.save(out_path, format="PNG")
    print(f"[+] Generated cover armor mandala: {out_path}")

def embed_payload(cover_png: Path, out_png: Path, binary_bytes: bytes):
    """Embeds the payload and custom PNG ancillary chunk into cover image."""
    payload_data = {
        "flag6": FLAG_RING_6,
        "fragment3": FRAGMENT_3,
        "payload_len": len(binary_bytes),
        "target_binary": "shalya_whisper"
    }

    meta_raw = json.dumps(payload_data).encode("utf-8")
    full_blob = meta_raw + b"||PAYLOAD_DATA||" + binary_bytes

    # Encrypt blob using XOR stream derived from SHA-256 of password
    key_stream = hashlib.sha256(PASSWORD.encode("utf-8")).digest()
    encrypted_blob = bytearray()
    for i, b in enumerate(full_blob):
        encrypted_blob.append(b ^ key_stream[i % len(key_stream)])

    compressed = zlib.compress(bytes(encrypted_blob), level=9)

    # Inject custom PNG chunk: 'kAvC' (Karna's Armor Chunk)
    raw_png = cover_png.read_bytes()
    # Find IEND
    iend_pos = raw_png.rfind(b"IEND")
    if iend_pos == -1:
        raise ValueError("Invalid PNG file, no IEND chunk found.")

    # Chunk format: Length (4 bytes), Type (4 bytes: kAvC), Data, CRC (4 bytes)
    chunk_type = b"kAvC"
    chunk_len = struct.pack(">I", len(compressed))
    chunk_crc = struct.pack(">I", zlib.crc32(chunk_type + compressed) & 0xFFFFFFFF)
    custom_chunk = chunk_len + chunk_type + compressed + chunk_crc

    # Insert right before IEND chunk (which starts 4 bytes before 'IEND' for its length)
    iend_chunk_start = iend_pos - 4
    final_png_bytes = raw_png[:iend_chunk_start] + custom_chunk + raw_png[iend_chunk_start:]

    out_png.write_bytes(final_png_bytes)
    print(f"[+] Successfully embedded stego payload into {out_png}")
    print(f"    - Flag 6: {FLAG_RING_6}")
    print(f"    - Fragment 3: {FRAGMENT_3}")
    print(f"    - Embedded Binary Size: {len(binary_bytes)} bytes")

def extract_payload(png_path: Path):
    """Verifies extraction from the stego PNG."""
    raw = png_path.read_bytes()
    marker = b"kAvC"
    pos = raw.find(marker)
    if pos == -1:
        raise ValueError("kAvC chunk not found!")

    length = struct.unpack(">I", raw[pos - 4:pos])[0]
    compressed_data = raw[pos + 4 : pos + 4 + length]
    encrypted_blob = zlib.decompress(compressed_data)

    key_stream = hashlib.sha256(PASSWORD.encode("utf-8")).digest()
    decrypted = bytearray()
    for i, b in enumerate(encrypted_blob):
        decrypted.append(b ^ key_stream[i % len(key_stream)])

    meta_part, bin_part = bytes(decrypted).split(b"||PAYLOAD_DATA||", 1)
    meta = json.loads(meta_part.decode("utf-8"))
    return meta, bin_part

def main():
    base_dir = Path(__file__).resolve().parent.parent
    stego_dir = base_dir / "rings" / "06-stego" / "assets"
    stego_dir.mkdir(parents=True, exist_ok=True)

    cover_path = stego_dir / "kavacha_src.png"
    out_path = stego_dir / "kavacha.png"

    generate_cover_image(cover_path)

    # Read shalya_whisper.c source or binary representation
    re_source = (base_dir / "rings" / "05-re" / "shalya_whisper.c").read_bytes()
    embed_payload(cover_path, out_path, re_source)

    # Self-test validation
    print("[*] Running self-test extraction...")
    meta, bin_data = extract_payload(out_path)
    assert meta["flag6"] == FLAG_RING_6
    assert meta["fragment3"] == FRAGMENT_3
    print("[+] Self-test verified! Stego pipeline operational.")

if __name__ == "__main__":
    main()
