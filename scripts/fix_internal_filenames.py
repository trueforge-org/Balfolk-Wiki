#!/usr/bin/env python3
"""
Normalize malformed internal `doku.php` id links inside HTML files under source/web.

Strategy:
- Find occurrences of `doku.php` (regular or fullwidth variants) with an `id=` parameter.
- For the `id` value: strip any internal `.html` fragments and trailing query params after `&`.
- Ensure the id ends with a single `.html` and preserve anchors after `#`.
- Write a `.bak` copy before changing a file.
"""
from pathlib import Path
import re

ROOT = Path("source/web")

pattern = re.compile(r'(doku\.php[^"\s>]*id=)([^"#\s]+)(#?[^"\s>]*)', flags=re.IGNORECASE)

def normalize_id(id_val: str) -> str:
    # remove query params after '&'
    base = id_val.split('&', 1)[0]
    # remove any occurrences of '.html' embedded in the id
    base = base.replace('.html', '')
    # ensure a single trailing .html
    if not base.endswith('.html'):
        base = base + '.html'
    return base

def replace_in_text(text: str) -> (str, bool):
    changed = False

    def repl(m: re.Match) -> str:
        nonlocal changed
        prefix = m.group(1)
        id_part = m.group(2)
        anchor = m.group(3) or ''
        new_id = normalize_id(id_part)
        new = prefix + new_id + anchor
        if new != m.group(0):
            changed = True
        return new

    new_text = pattern.sub(repl, text)
    return new_text, changed

def process_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    new_text, changed = replace_in_text(text)
    if changed:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(text, encoding='utf-8')
        path.write_text(new_text, encoding='utf-8')
    return changed

def main():
    files = list(ROOT.rglob('*.html'))
    modified = 0
    for f in files:
        if process_file(f):
            modified += 1
            print(f"Modified: {f}")
    print(f"Done. Modified {modified} files.")

if __name__ == '__main__':
    main()
