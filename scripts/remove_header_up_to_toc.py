#!/usr/bin/env python3
"""
Strip everything above the first "" marker in files under source/web.
Does in-place edits without creating backups.
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), '..')
WEB_DIR = os.path.normpath(os.path.join(ROOT, 'source', 'web'))

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    marker = ''
    idx = data.find(marker)
    if idx == -1:
        return False
    # Keep marker and everything after it
    new = data[idx:]
    if new == data:
        return False
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new)
    return True

def main():
    changed = []
    for dirpath, dirs, files in os.walk(WEB_DIR):
        for name in files:
            if not name.lower().endswith('.html'):
                continue
            path = os.path.join(dirpath, name)
            try:
                if process_file(path):
                    changed.append(os.path.relpath(path))
            except Exception as e:
                print(f'ERROR processing {path}: {e}')
    if changed:
        print('Modified files:')
        for p in changed:
            print(p)
    else:
        print('No files changed.')

if __name__ == '__main__':
    main()
