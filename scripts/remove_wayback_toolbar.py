#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'source' / 'web'
patterns = [
    re.compile(r"<script[^>]*>.*?__wm\.init\([\s\S]*?<!-- End Wayback Rewrite JS Include -->\s*\n?", re.IGNORECASE | re.DOTALL),
    re.compile(r"<!-- BEGIN WAYBACK TOOLBAR INSERT -->[\s\S]*?<!-- END WAYBACK TOOLBAR INSERT -->\s*\n?", re.IGNORECASE | re.DOTALL),
]

html_files = list(root.rglob('*.html'))
print(f"Found {len(html_files)} HTML files under {root}")

for p in html_files:
    s = p.read_text(encoding='utf-8')
    orig = s
    for pat in patterns:
        s = pat.sub('', s)
    if s != orig:
        backup = p.with_suffix(p.suffix + '.bak')
        backup.write_text(orig, encoding='utf-8')
        p.write_text(s, encoding='utf-8')
        print(f"Patched: {p}")

print("Done.")
