#!/usr/bin/env python3
from pathlib import Path

root = Path('source/web')
removed = []
for p in root.rglob('*.html'):
    try:
        text = p.read_text(encoding='utf-8')
    except Exception:
        try:
            text = p.read_text(encoding='latin-1')
        except Exception:
            continue
    if text.strip() == '':
        p.unlink()
        removed.append(str(p))

print(f"Removed {len(removed)} empty .html files:")
for r in removed:
    print(r)
