#!/usr/bin/env python3
import os
from pathlib import Path

def replace_in_file(path, replacements):
    text = path.read_text(encoding='utf-8')
    new = text
    for old, new_val in replacements:
        new = new.replace(old, new_val)
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

    # Replacement rules: remove absolute domain for the DansWiki site so links become relative
    replacements = [
        ('https://www.balfolkenschede.nl/danswiki/', ''),
        ('http://www.balfolkenschede.nl/danswiki/', ''),
        ('https://www.balfolkenschede.nl/', ''),
        ('http://www.balfolkenschede.nl/', ''),
    ]

    modified = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if not fn.lower().endswith('.html'):
                continue
            p = Path(dirpath) / fn
            try:
                changed = replace_in_file(p, replacements)
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
