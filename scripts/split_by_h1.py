#!/usr/bin/env python3
import re
from pathlib import Path

src = Path('Danswiki Balfolk.md')
outdir = Path('done')
outdir.mkdir(parents=True, exist_ok=True)

text = src.read_text(encoding='utf-8')
lines = text.splitlines(keepends=True)

sections = []
current_header = None
current_lines = []

for line in lines:
    m = re.match(r'^# (.*)', line)
    if m:
        # start of a new top-level section
        if current_header is not None:
            sections.append((current_header, ''.join(current_lines)))
        current_header = m.group(1).strip()
        current_lines = [line]
    else:
        if current_header is None:
            # content before first H1: accumulate under a special file
            current_header = 'preamble'
            current_lines = [line]
        else:
            current_lines.append(line)

if current_header is not None:
    sections.append((current_header, ''.join(current_lines)))

def sanitize(name: str) -> str:
    s = name.lower()
    # replace non-alphanumeric with hyphens
    s = re.sub(r"[^a-z0-9]+", '-', s)
    s = s.strip('-')
    if not s:
        s = 'section'
    return s + '.md'

created = []
for header, content in sections:
    fname = sanitize(header)
    path = outdir / fname
    path.write_text(content, encoding='utf-8')
    created.append(str(path))

print('Created', len(created), 'files:')
for p in created:
    print('-', p)
