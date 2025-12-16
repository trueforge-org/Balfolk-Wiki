#!/usr/bin/env python3
import re
from pathlib import Path

root = Path('source/web')
pattern = re.compile(r'<article\b[^>]*?>.*?</article>', re.IGNORECASE | re.DOTALL)

changed = []
for p in root.rglob('*.html'):
    try:
        text = p.read_text(encoding='utf-8')
    except Exception:
        try:
            text = p.read_text(encoding='latin-1')
        except Exception:
            print(f"Skipping binary/unreadable file: {p}")
            continue
    m = pattern.search(text)
    if m:
        new = m.group(0).strip() + "\n"
    else:
        new = ""  # no article found -> empty file
    if new != text:
        bak = p.with_suffix(p.suffix + '.bak')
        bak.write_text(text, encoding='utf-8')
        p.write_text(new, encoding='utf-8')
        changed.append(str(p))

print(f"Processed {len(list(root.rglob('*.html')))} files. Modified {len(changed)} files:")
for c in changed:
    print(c)
