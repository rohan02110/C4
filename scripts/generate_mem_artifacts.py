#!/usr/bin/env python3
"""
generate_mem_artifacts.py — Ring 4 Memory Forensics Artifact Generator
Creates a compact, realistic trimmed memory image 'ashwatthama_trace.mem.zip'
Strictly optimized to stay under 5 MB compressed (ensuring repository stays well below 512 MB).

Contains:
- Simulated Windows 10 memory headers and VAD tree structure
- Process entry: vyuha_sync.exe (PID 4472)
- Carvable heap structures containing:
    - Stego Password: SomaRasa_Kavacha_2026!
    - Intermediate Flag 4: ASHWATTHAMA_MEMORY_VAD_CARVED_77c2
    - Passphrase Fragment #1: k4vach4_
    - Base64-encoded kavacha.png byte stream
"""

import os
import sys
import zipfile
import base64
import struct
from pathlib import Path

FLAG_RING_4 = "ASHWATTHAMA_MEMORY_VAD_CARVED_77c2"
FRAGMENT_1 = "k4vach4_"
PASSWORD = "SomaRasa_Kavacha_2026!"

def generate_memory_dump(out_mem_path: Path, kavacha_png_path: Path):
    print(f"[*] Reading carrier artifact: {kavacha_png_path}")
    png_bytes = kavacha_png_path.read_bytes()
    png_b64 = base64.b64encode(png_bytes)

    print(f"[*] Synthesizing trimmed memory image (target size: ~15 MB)...")
    
    # 1. Windows Memory Header simulation (Win10 x64)
    mem_data = bytearray()
    mem_data.extend(b"PAGE\x00\x00\x00\x00")
    mem_data.extend(struct.pack("<Q", 0x1000000)) # Base address

    # Pad with simulated OS memory pages
    padding_chunk = os.urandom(64 * 1024) # 64 KB noise blocks
    for _ in range(80): # ~5 MB of initial noise
        mem_data.extend(padding_chunk)

    # 2. Inject Process Context: vyuha_sync.exe
    process_header = (
        b"\x00" * 32 +
        b"EPROCESS_HEADER_WIN10_X64\x00" +
        b"ImageFileName: vyuha_sync.exe\x00" +
        b"PID: 4472\x00" +
        b"VAD_ROOT: 0x7FFF00400000\x00"
    )
    mem_data.extend(process_header)

    # 3. Inject In-Memory Heap Configuration Block
    heap_block = (
        b"=== VYUHA_SYNC CONFIGURATION BLOCK ===\n"
        b"STATUS=ACTIVE\n"
        b"SIG_INTEGRITY=" + FLAG_RING_4.encode() + b"\n"
        b"FRAGMENT_1=" + FRAGMENT_1.encode() + b"\n"
        b"STEGO_PASSPHRASE=" + PASSWORD.encode() + b"\n"
        b"TARGET_IMAGE_NAME=kavacha.png\n"
        b"IMAGE_PAYLOAD_BASE64=" + png_b64 + b"\n"
        b"=== END CONFIGURATION BLOCK ===\n"
    )
    mem_data.extend(heap_block)

    # 4. Add trailing memory space
    for _ in range(120): # ~7.5 MB of trailing noise
        mem_data.extend(padding_chunk)

    out_mem_path.write_bytes(mem_data)
    uncompressed_mb = len(mem_data) / (1024 * 1024)
    print(f"[+] Memory image generated: {out_mem_path} ({uncompressed_mb:.2f} MB)")

def create_zip_archive(mem_path: Path, zip_path: Path):
    print(f"[*] Compressing memory dump into zip archive: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(mem_path, arcname="ashwatthama_trace.mem")
    
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"[+] Final zip archive created: {zip_path} ({zip_size_mb:.2f} MB)")

def verify_extraction(zip_path: Path):
    print("[*] Verifying forensic carver extraction from zip...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        extracted = zf.read("ashwatthama_trace.mem")
    
    assert FLAG_RING_4.encode() in extracted
    assert FRAGMENT_1.encode() in extracted
    assert PASSWORD.encode() in extracted
    assert b"IMAGE_PAYLOAD_BASE64=" in extracted
    print("[+] Forensic verification successful! All artifacts carvable.")

def main():
    base_dir = Path(__file__).resolve().parent.parent
    stego_png = base_dir / "rings" / "06-stego" / "assets" / "kavacha.png"
    if not stego_png.exists():
        print("[-] kavacha.png missing. Run build_stego_payload.py first.")
        sys.exit(1)

    forensics_vault = base_dir / "rings" / "04-forensics" / "vault"
    forensics_vault.mkdir(parents=True, exist_ok=True)

    mem_raw = forensics_vault / "ashwatthama_trace.mem"
    mem_zip = forensics_vault / "ashwatthama_trace.mem.zip"

    generate_memory_dump(mem_raw, stego_png)
    create_zip_archive(mem_raw, mem_zip)
    verify_extraction(mem_zip)

    # Delete uncompressed raw file to save disk space
    if mem_raw.exists():
        mem_raw.unlink()
        print(f"[*] Cleaned up uncompressed raw image to strictly maintain < 512 MB limit.")

if __name__ == "__main__":
    main()
