#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'source' / 'web'

patterns = [
    # Remove @licstart ... @licend blocks
    re.compile(r'@licstart[\s\S]*?@licend', re.IGNORECASE),
    # Remove dw__license div blocks
    re.compile(r'<div[^>]*id=["\']dw__license["\'][\s\S]*?<\/div>\s*', re.IGNORECASE),
    # Remove standalone license divs (class="license")
    re.compile(r'<div[^>]*class=["\']license["\'][\s\S]*?<\/div>\s*', re.IGNORECASE),
    # Remove CC anchor/button images
    re.compile(r'<a[^>]*href=["\']https?://creativecommons\.org/[^"\']+["\'][\s\S]*?<\/a>\s*', re.IGNORECASE),
    # Remove Wayback JavaScript footer lines
    re.compile(r"^.*JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE\..*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^.*ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT.*$", re.IGNORECASE | re.MULTILINE),
]

html_files = list(root.rglob('*.html'))
print(f"Scanning {len(html_files)} HTML files under {root}")
patched = 0
for p in html_files:
    s = p.read_text(encoding='utf-8')
    orig = s
    for pat in patterns:
        s = pat.sub('', s)
    # Trim excessive blank lines
    s = re.sub(r'\n{3,}', '\n\n', s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        patched += 1
        print('Patched:', p)

print('Done. Files patched:', patched)
