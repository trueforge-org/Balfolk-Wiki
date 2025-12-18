#!/usr/bin/env python3
import os
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path('src/content/docs')
ALL_MD = list(ROOT.rglob('*.md'))
ALL_PATHS = [p.resolve() for p in ALL_MD]

link_re = re.compile(r"\[([^\]]+)\]\((?!https?:\/\/)([^)]+)\)")

# helper normalize

def norm(s):
    return re.sub(r"[^a-z0-9]+","-", s.lower())

# try to resolve a target string to one of ALL_MD paths
def resolve_target(target, src_path):
    t = target.strip()
    t = unquote(t)
    # ignore anchors
    if t.startswith('#'):
        return None
    # remove surrounding <> if present
    if t.startswith('<') and t.endswith('>'):
        t = t[1:-1]
    # If it's already a path to md inside docs
    cand = (src_path.parent / t).resolve()
    if cand.exists() and cand.suffix in ('.md','.MD'):
        return cand
    # If t ends with .html, try replacing with .md
    tnohtml = re.sub(r"\.html?$","", t, flags=re.I)
    # split by various separators to tokens
    tokens = re.split(r"[:\uFE56/\\]+", tnohtml)
    # remove empty and leading 'doku.php' or 'id' tokens
    tokens = [x for x in tokens if x and not x.lower().startswith('doku.php') and not x.lower().startswith('id=')]
    if not tokens:
        tokens = [tnohtml]
    # try path by tokens
    for i in range(1, len(tokens)+1):
        cand_path = ROOT.joinpath(*tokens[-i:])
        for ext in ('','.md','.MD'):
            p = Path(str(cand_path) + ext)
            if p.exists():
                return p.resolve()
    # fallback: use last token as slug and search filenames
    slug = tokens[-1]
    slug_norm = norm(slug)
    candidates = []
    for p in ALL_PATHS:
        name = p.stem
        if slug_norm in norm(name):
            candidates.append(p)
        elif slug_norm in norm(str(p)):
            candidates.append(p)
    if len(candidates)==1:
        return candidates[0]
    if len(candidates)>1:
        # prefer same directory siblings
        for c in candidates:
            if c.parent == src_path.parent.resolve():
                return c
        # else return first
        return candidates[0]
    return None

changes = []
summary = {'fixed':0,'removed':0,'scanned':0}
for path in ALL_MD:
    src = path
    text = src.read_text(encoding='utf-8')
    new_text = text
    offs = 0
    for m in link_re.finditer(text):
        summary['scanned'] += 1
        full = m.group(0)
        label = m.group(1)
        target = m.group(2).strip()
        resolved = resolve_target(target, src)
        if resolved:
            # compute relative path between files
            relpath = os.path.relpath(str(resolved), start=str(src.parent))
            relpath = relpath.replace('\\','/')
            # ensure leading ./ if in same dir? no, just use relative
            replacement = f'[{label}]({relpath})'
            if replacement != full:
                new_text = new_text.replace(full, replacement)
                changes.append((src, full, replacement))
                summary['fixed'] += 1
        else:
            # remove link markup, keep label
            replacement = label
            new_text = new_text.replace(full, replacement)
            changes.append((src, full, replacement))
            summary['removed'] += 1
    if new_text != text:
        src.write_text(new_text, encoding='utf-8')

print(f"Scanned links: {summary['scanned']}")
print(f"Fixed links: {summary['fixed']}")
print(f"Removed broken links: {summary['removed']}")

# print brief list of changed files
files_changed = sorted({str(c[0]) for c in changes})
print(f"Files changed: {len(files_changed)}")
for f in files_changed:
    print(f)

# exit with non-zero if nothing changed
if not files_changed:
    print('No changes made.')
