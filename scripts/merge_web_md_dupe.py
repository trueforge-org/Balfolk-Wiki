#!/usr/bin/env python3
import pathlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source' / 'web-md-dupe'
DST = ROOT / 'done'

def normalize_line(s: str) -> str:
    return s.strip().lower()

def strip_fence(text: str) -> str:
    # Remove surrounding ```markdown fences if present
    if text.startswith('```'):
        parts = text.splitlines()
        if parts and parts[0].startswith('```'):
            # find last fence
            if parts[-1].startswith('```'):
                return '\n'.join(parts[1:-1])
    return text

def merge_file(src_path: Path, dst_path: Path) -> bool:
    src_text = src_path.read_text(encoding='utf-8')
    dst_text = dst_path.read_text(encoding='utf-8')

    src_text = strip_fence(src_text)
    dst_text = strip_fence(dst_text)

    dst_lines = [l.rstrip('\n') for l in dst_text.splitlines()]
    src_lines = [l.rstrip('\n') for l in src_text.splitlines()]

    existing = {normalize_line(l) for l in dst_lines if l.strip()}

    to_append = []
    for l in src_lines:
        nl = normalize_line(l)
        if not l.strip():
            # preserve blank lines only if last appended isn't blank
            if to_append and to_append[-1].strip():
                to_append.append('')
            continue
        if nl not in existing:
            to_append.append(l)
            existing.add(nl)

    if not to_append:
        return False

    # Reconstruct: keep dst original fences if present, else wrap in ```markdown
    dst_has_fence = dst_path.read_text(encoding='utf-8').strip().startswith('```')
    if dst_has_fence:
        # append inside fence: remove final fence, append, re-add fence
        lines = dst_path.read_text(encoding='utf-8').splitlines()
        if lines and lines[-1].startswith('```'):
            body = '\n'.join(lines[1:-1])
            new_body = body + '\n' + '\n'.join(to_append)
            new_text = '```markdown\n' + new_body.strip() + '\n```\n'
        else:
            new_text = dst_path.read_text(encoding='utf-8') + '\n' + '\n'.join(to_append) + '\n'
    else:
        new_text = dst_path.read_text(encoding='utf-8') + '\n\n' + '\n'.join(to_append) + '\n'

    dst_path.write_text(new_text, encoding='utf-8')
    return True

def main():
    updated = []
    for src in SRC.rglob('*.md'):
        rel = src.relative_to(SRC)
        dst = DST / rel
        if dst.exists():
            try:
                changed = merge_file(src, dst)
                if changed:
                    updated.append(str(rel))
            except Exception as e:
                print(f'ERROR merging {rel}: {e}')
        else:
            # no duplicate in done; skip
            continue

    if updated:
        print('Updated files:')
        for u in updated:
            print(' -', u)
    else:
        print('No files needed updating.')

if __name__ == '__main__':
    main()
