#!/usr/bin/env python3
"""Sanitize filenames under source/web by replacing unsafe chars with underscores.

Rules:
- Replace any character not in [A-Za-z0-9._-] with '_'.
- Collapse consecutive '_' to a single '_'.
- Strip leading/trailing '_'.
- Preserve file extension.
- If a target filename already exists, append a numeric suffix to avoid collision.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'source' / 'web'

def sanitize(name: str) -> str:
    # preserve extension
    p = Path(name)
    stem = p.stem
    suffix = p.suffix
    # replace unsafe chars
    cleaned = re.sub(r'[^A-Za-z0-9._-]+', '_', stem)
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.strip('_')
    if cleaned == '':
        cleaned = 'file'
    return cleaned + suffix

def main():
    if not ROOT.exists():
        print('source/web directory not found:', ROOT)
        return 1
    mappings = []
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_file():
            continue
        if entry.name == '.DS_Store':
            continue
        new_name = sanitize(entry.name)
        # if name unchanged, skip
        if new_name == entry.name:
            continue
        target = ROOT / new_name
        base, ext = os.path.splitext(new_name)
        i = 1
        while target.exists():
            target = ROOT / f"{base}_{i}{ext}"
            i += 1
        entry.rename(target)
        mappings.append((entry.name, target.name))
    if mappings:
        print('Renamed files:')
        for old, new in mappings:
            print(f"{old} -> {new}")
    else:
        print('No files needed renaming.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
