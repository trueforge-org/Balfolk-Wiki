#!/usr/bin/env python3
"""
Map `doku.php` id links to actual filenames in the same folder when possible.

For each `doku.php` link found in an HTML file, if the linked id filename
doesn't exist in the same directory, try to find the best-matching file
in that directory (based on token presence) and replace the link to point
to that existing filename.
"""
from pathlib import Path
import re

ROOT = Path("source/web")
pattern = re.compile(r'(doku\.php[^"\s>]*id=)([^"#\s]+)(#?[^"\s>]*)', flags=re.IGNORECASE)

def tokens_from_id(id_str: str):
    base = id_str.split('&',1)[0]
    base = base.replace('.html','')
    # split on fullwidth or ascii colon
    toks = re.split('[﹕:]', base)
    return [t for t in toks if t]

def best_match_file(dirpath: Path, id_str: str):
    toks = tokens_from_id(id_str)
    candidates = list(dirpath.iterdir())
    best = None
    best_score = 0
    for c in candidates:
        if not c.is_file():
            continue
        name = c.name.lower()
        score = sum(1 for t in toks if t.lower() in name)
        if score > best_score:
            best_score = score
            best = c
    # accept only if at least one token matched
    if best_score > 0:
        return best.name
    return None

def replace_in_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    changed = 0

    def repl(m: re.Match) -> str:
        nonlocal changed
        prefix = m.group(1)
        id_part = m.group(2)
        anchor = m.group(3) or ''
        # check if file exists in same dir
        target = Path(path).parent / id_part
        if target.exists():
            return m.group(0)
        # try best match
        candidate_name = best_match_file(Path(path).parent, id_part)
        if candidate_name:
            changed += 1
            return prefix + candidate_name + anchor
        return m.group(0)

    new_text = pattern.sub(repl, text)
    if changed:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(text, encoding='utf-8')
        path.write_text(new_text, encoding='utf-8')
    return changed

def main():
    files = list(Path('source/web').rglob('*.html'))
    total = 0
    for f in files:
        c = replace_in_file(f)
        if c:
            print(f"Updated {c} links in {f}")
            total += c
    print(f"Done. Remapped {total} links.")

if __name__ == '__main__':
    main()
