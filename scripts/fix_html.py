#!/usr/bin/env python3
"""Fix (clean) HTML files under source/web using BeautifulSoup + html5lib.

Usage:
  python3 scripts/fix_html.py [--apply]

Without --apply the script runs in dry-run mode and only reports files that would be changed.
It does not create any backup files.
"""
import argparse
import os
import sys
from bs4 import BeautifulSoup


def clean_content(text):
    soup = BeautifulSoup(text, 'html5lib')
    # html5lib builder produces a parsed tree; decode to string
    return soup.decode()


def process_file(path, apply_changes=False):
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except Exception as e:
        return False, f"read-error: {e}"
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = raw.decode('latin-1')
        except Exception as e:
            return False, f"decode-error: {e}"
    try:
        cleaned = clean_content(text)
    except Exception as e:
        return False, f"parse-error: {e}"
    if cleaned != text:
        if apply_changes:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
            except Exception as e:
                return False, f"write-error: {e}"
        return True, "changed"
    return False, "unchanged"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Actually write fixes to files')
    parser.add_argument('--root', default=os.path.join('source','web'), help='Root folder to scan')
    args = parser.parse_args()

    root = args.root
    if not os.path.isdir(root):
        print(f"ERROR: root folder not found: {root}", file=sys.stderr)
        sys.exit(2)

    total = 0
    changed = []
    errors = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if not fn.lower().endswith('.html'):
                continue
            total += 1
            path = os.path.join(dirpath, fn)
            ok, msg = process_file(path, apply_changes=args.apply)
            if ok:
                changed.append(path)
            else:
                if msg and msg.startswith(('read-error','decode-error','parse-error','write-error')):
                    errors.append((path,msg))
    print(f"Scanned {total} .html files under {root}")
    print(f"Files that would change: {len(changed)}")
    if args.apply and changed:
        print("Files updated:")
        for p in changed:
            print(p)
    elif changed:
        print("Files that would be updated (dry-run):")
        for p in changed:
            print(p)
    if errors:
        print('\nErrors encountered:', file=sys.stderr)
        for p,m in errors:
            print(p + ': ' + m, file=sys.stderr)
        sys.exit(3 if not args.apply else 0)

if __name__ == '__main__':
    main()
