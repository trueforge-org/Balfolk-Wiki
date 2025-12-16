#!/usr/bin/env python3
"""Move files with specific prefixes into subfolders and remove the prefix.

Prefixes handled: 'algemeen_', 'bands_', 'dansen_', 'event_', 'events_', 'muziek_'
For each matching file in source/web, create the subfolder (if needed), move
the file into it and remove the prefix from the filename. Avoid collisions by
appending numeric suffixes when necessary.
"""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1] / 'source' / 'web'
PREFIXES = ['algemeen_', 'bands_', 'dansen_', 'event_', 'events_', 'muziek_']

def move_file(entry: Path, prefix: str):
    rel = entry.name[len(prefix):]
    if rel == '' or rel in ('.', '..'):
        rel = 'index.html'
    folder = ROOT / prefix[:-1]  # remove trailing underscore
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / rel
    base, ext = os.path.splitext(rel)
    i = 1
    while target.exists():
        target = folder / f"{base}_{i}{ext}"
        i += 1
    entry.rename(target)
    return entry.name, str(target.relative_to(ROOT))

def main():
    if not ROOT.exists():
        print('source/web not found:', ROOT)
        return 1
    mappings = []
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_file():
            continue
        if entry.name in ('.DS_Store', 'doku.php.html'):
            continue
        for prefix in PREFIXES:
            if entry.name.startswith(prefix):
                mappings.append(move_file(entry, prefix))
                break
    if mappings:
        print('Moved files:')
        for old, new in mappings:
            print(f"{old} -> {new}")
    else:
        print('No files matched prefixes.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
