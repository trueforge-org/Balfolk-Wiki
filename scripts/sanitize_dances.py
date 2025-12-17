#!/usr/bin/env python3
import sys, re, os

PAT_HERK = re.compile(r'^\s*[-*]\s*(Herkomst|herkomst)\s*[:\-]?', re.I)
PAT_MAAT = re.compile(r'^\s*[-*]\s*(Maat/ritme|Maat|maat|ritme)\s*[:\-]?', re.I)
PAT_TIPS = re.compile(r'^\s*(Tips:|\-\s*Tips:|tips:)')

files = sys.stdin.read().splitlines()
if not files:
    print('No files provided on stdin')
    sys.exit(0)

updated = []
for f in files:
    try:
        with open(f, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except Exception as e:
        print('ERROR reading', f, e)
        continue

    new = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        if PAT_HERK.match(line) or PAT_MAAT.match(line) or PAT_TIPS.match(line):
            # skip this line
            changed = True
            i += 1
            # also skip subsequent list lines directly following a Tips: header
            while i < len(lines) and lines[i].strip().startswith('-'):
                i += 1
            continue
        new.append(line)
        i += 1

    # ensure we don't duplicate "Bronnen" placeholder
    content = '\n'.join(new)
    if 'Bronnen:' not in content:
        # append placeholder at end with one blank line before
        if not content.endswith('\n') and len(content) > 0:
            content += '\n'
        content += '\nBronnen:\n\n'
        changed = True

    if changed:
        try:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(content)
            updated.append(f)
            print('Sanitized', f)
        except Exception as e:
            print('ERROR writing', f, e)

print('\nTotal sanitized:', len(updated))
