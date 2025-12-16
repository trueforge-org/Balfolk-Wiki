#!/usr/bin/env python3
from pathlib import Path

root = Path('source/web/lib')
if not root.exists():
    print('No lib directory found under source/web; nothing to do.')
    raise SystemExit(0)

restored = []
for bak in root.rglob('*.html.bak'):
    orig = bak.with_suffix('')
    try:
        data = bak.read_bytes()
    except Exception as e:
        print(f"Failed to read backup {bak}: {e}")
        continue
    try:
        orig.write_bytes(data)
        bak.unlink()
        restored.append(str(orig))
    except Exception as e:
        print(f"Failed to restore {orig} from {bak}: {e}")

print(f"Restored {len(restored)} files in {root}:")
for r in restored:
    print(r)
