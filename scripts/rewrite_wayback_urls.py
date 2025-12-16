#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'source' / 'web'
pattern1 = re.compile(r'https?://web\.archive\.org/web/[^/]+/(http[s]?://[^"\' >]+)')
pattern2 = re.compile(r'https?://web\.archive\.org/web/[^"\' >]*/')

html_files = list(root.rglob('*.html'))
print(f"Scanning {len(html_files)} HTML files under {root}")
patched = 0
for p in html_files:
    s = p.read_text(encoding='utf-8')
    orig = s
    s = pattern1.sub(r'\1', s)
    s = pattern2.sub('', s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        patched += 1
        print('Patched:', p)

print('Done. Files patched:', patched)
