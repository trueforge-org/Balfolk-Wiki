#!/usr/bin/env python3
"""Remove leading 'doku.php_id_' from filenames under source/web.

If the target filename already exists, a numeric suffix is appended.
"""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1] / 'source' / 'web'

def main():
    if not ROOT.exists():
        print('source/web not found:', ROOT)
        return 1
    prefix = 'doku.php_id_'
    mappings = []
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_file():
            continue
        name = entry.name
        if not name.startswith(prefix):
            continue
        new_name = name[len(prefix):]
        # avoid empty name
        if new_name == '' or new_name in ('.', '..'):
            new_name = 'index.html'
        target = ROOT / new_name
        base, ext = os.path.splitext(new_name)
        i = 1
        while target.exists():
            target = ROOT / f"{base}_{i}{ext}"
            i += 1
        entry.rename(target)
        mappings.append((name, target.name))
    if mappings:
        print('Renamed files:')
        for old, new in mappings:
            print(f"{old} -> {new}")
    else:
        print('No files with prefix found.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
