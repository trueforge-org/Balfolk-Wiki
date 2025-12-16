#!/usr/bin/env python3
import os
import re
from urllib.parse import unquote

ROOT = os.path.join(os.path.dirname(__file__), '..', 'source', 'web')
ROOT = os.path.abspath(ROOT)

def load_local_htmls():
    return {fn for fn in os.listdir(ROOT) if fn.endswith('.html')}

href_re = re.compile(r'href=("|\')(?P<h>.*?)("|\')', re.IGNORECASE)

def find_html_segment(h):
    # decode percent-encoding
    try:
        dec = unquote(h)
    except Exception:
        dec = h
    # look for .html (case-insensitive)
    idx = dec.lower().find('.html')
    if idx == -1:
        return None
    seg = dec[:idx+5]
    # strip any wrapping parts like https://.../, keep last path component
    return os.path.basename(seg)


def process_file(path, local_htmls):
    with open(path, 'r', encoding='utf-8', errors='surrogatepass') as f:
        s = f.read()

    changed = False

    def repl(m):
        quote = m.group(1)
        h = m.group('h')
        basename = find_html_segment(h)
        if basename and basename in local_htmls:
            # replace href value with just the local basename
            nonlocal changed
            changed = True
            return f'href={quote}{basename}{quote}'
        return m.group(0)

    new = href_re.sub(repl, s)

    if changed:
        # backup
        bak = path + '.bak'
        if not os.path.exists(bak):
            with open(bak, 'w', encoding='utf-8', errors='surrogatepass') as f:
                f.write(s)
        with open(path, 'w', encoding='utf-8', errors='surrogatepass') as f:
            f.write(new)
    return changed


def main():
    local_htmls = load_local_htmls()
    html_files = [os.path.join(ROOT, fn) for fn in os.listdir(ROOT) if fn.endswith('.html')]
    total = 0
    modified = 0
    for path in html_files:
        ok = process_file(path, local_htmls)
        total += 1
        if ok:
            modified += 1
            print('Modified', os.path.basename(path))
    print(f'Done. Scanned {total} files, modified {modified} files.')

if __name__ == '__main__':
    main()
