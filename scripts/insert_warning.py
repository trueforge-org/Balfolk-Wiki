#!/usr/bin/env python3
import sys
import os

warn = (":::caution\n\nDit bestand is aangevuld middels AI.\u2028Ga er vanuit dat alles hierin onzin is, tenzij bevestigd middels een andere bron.\u2028\u2028Hulp met aanvullen en verbetering word gewaardeerd!\n\n:::\n")

files = sys.stdin.read().splitlines()
if not files:
    print('No files provided on stdin')
    sys.exit(0)

for f in files:
    try:
        with open(f, encoding='utf-8') as fh:
            s = fh.read().splitlines()
    except Exception as e:
        print('ERROR reading', f, e)
        continue
    insert_at = None
    for idx, line in enumerate(s):
        if line.strip().startswith('<!-- source:'):
            insert_at = idx + 1
            break
    if insert_at is None:
        for idx, line in enumerate(s):
            if line.strip().startswith('---'):
                insert_at = idx + 1
                break
    if insert_at is None:
        insert_at = 0
    new = s[:insert_at]
    if new and new[-1].strip() != '':
        new.append('')
    new.append(warn)
    new.append('')
    new.extend(s[insert_at:])
    try:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(new))
        print('Updated', f)
    except Exception as e:
        print('ERROR writing', f, e)
