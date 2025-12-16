#!/usr/bin/env python3
import re
import os
from pathlib import Path


def to_local_filename(id_value: str) -> str:
    # drop URL params after first &
    id_value = id_value.split('&', 1)[0]
    # preserve anchors if present
    anchor = ''
    if '#' in id_value:
        id_value, anchor = id_value.split('#', 1)
        anchor = '#' + anchor
    # replace normal colon with fullwidth colon used in filenames
    local_id = id_value.replace(':', '﹕')
    return f'doku.php﹖id={local_id}.html{anchor}'


def replace_links(text: str) -> str:
    # pattern for standard doku.php?id=... (with optional domain prefix)
    p1 = re.compile(r'(?:https?://[^/\s]+/[^"\s]*?)?doku\.php\?id=([^"\s\'>]+)')
    # pattern for already converted weird-char form without .html
    p2 = re.compile(r'doku\.php﹖id=([^"\s\'>]+?)(?:\.html)?')

    def repl1(m):
        idv = m.group(1)
        return to_local_filename(idv)

    def repl2(m):
        idv = m.group(1)
        # if it already contains fullwidth colons or .html, normalize
        return to_local_filename(idv)

    text = p1.sub(repl1, text)
    text = p2.sub(repl2, text)
    return text


def replace_in_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    new = replace_links(text)
    if new != text:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(text, encoding='utf-8')
        path.write_text(new, encoding='utf-8')
        return True
    return False


def main():
    root = Path('source/web')
    if not root.exists():
        print('source/web not found')
        return

    modified = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if not fn.lower().endswith('.html'):
                continue
            p = Path(dirpath) / fn
            try:
                changed = replace_in_file(p)
            except Exception as e:
                print(f'ERROR processing {p}: {e}')
                continue
            if changed:
                modified.append(str(p))

    print(f'Modified {len(modified)} files')
    for m in modified:
        print(m)


if __name__ == '__main__':
    main()
