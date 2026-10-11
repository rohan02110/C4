#!/usr/bin/env python3
"""
check_size.py — Repository Size & Quota Verifier
Checks that the challenge repository strictly adheres to the 512 MB ceiling.
"""

from pathlib import Path

MAX_ALLOWED_MB = 512.0

def get_dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())

def main():
    root = Path(__file__).resolve().parent.parent
    total_bytes = get_dir_size(root)
    total_mb = total_bytes / (1024 * 1024)

    print("=" * 60)
    print("      CHAKRAVYUHA DEPLOYMENT QUOTA INSPECTOR (MAX: 512 MB)     ")
    print("=" * 60)

    for item in sorted(root.iterdir()):
        if item.is_dir():
            dir_mb = get_dir_size(item) / (1024 * 1024)
            pct = (dir_mb / MAX_ALLOWED_MB) * 100
            print(f"  - {item.name:22} : {dir_mb:6.2f} MB ({pct:4.1f}% of quota)")
        elif item.is_file():
            file_kb = item.stat().st_size / 1024
            print(f"  - {item.name:22} : {file_kb:6.2f} KB")

    print("-" * 60)
    print(f"TOTAL REPOSITORY SIZE    : {total_mb:.2f} MB / {MAX_ALLOWED_MB:.1f} MB")
    print(f"AVAILABLE HEADROOM       : {(MAX_ALLOWED_MB - total_mb):.2f} MB")
    print(f"QUOTA STATUS             : {'OK - FULLY DEPLOYABLE' if total_mb <= MAX_ALLOWED_MB else 'EXCEEDED'}")
    print("=" * 60)

    assert total_mb <= MAX_ALLOWED_MB, f"Total size ({total_mb:.2f} MB) exceeds {MAX_ALLOWED_MB} MB limit!"

if __name__ == "__main__":
    main()
