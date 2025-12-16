#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'source' / 'web'

# Patterns to remove
patterns = [
    # Remove anchor wrapping multilingual flag images (any flags/*.gif)
    re.compile(r'<a[^>]*>\s*<img[^>]*flags/[^">]+\.gif"[^>]*>\s*</a>', re.IGNORECASE | re.DOTALL),
    # Remove span.curid that contains a flag img
    re.compile(r'<span[^>]*class=["\']curid["\'][^>]*>.*?<img[^>]*flags/[^">]+\.gif"[^>]*>.*?</span>', re.IGNORECASE | re.DOTALL),
    # Remove list items that include the listed menu texts
    re.compile(r'<li[^>]*>.*?(Toon broncode|Discussion|Oude revisies|Referenties|Hernoem Pagina).*?</li>', re.IGNORECASE | re.DOTALL),
    # Remove 'Referenties en bronnen' anchor in TOC
    re.compile(r'<li[^>]*><a[^>]*href=["\']#referenties_en_bronnen["\'][^>]*>.*?</li>', re.IGNORECASE | re.DOTALL),
    # Remove heading with id referenties_en_bronnen
    re.compile(r'<h[1-6][^>]*id=["\']referenties_en_bronnen["\'][^>]*>.*?</h[1-6]>', re.IGNORECASE | re.DOTALL),
]

# Also remove literal language names occurrences in attributes/text (Deutsch, English, Espa... , Français, Nederlands, Portugu)
lang_words = [
    r'Deutsch', r'English', r'Espa(?:ñ|Ã±)ol', r'Fran[cç]ais', r'Nederlands', r'Portugu[eê]s', r'Toon broncode', r'Discussion', r'Oude revisies', r'Referenties', r'Hernoem Pagina'
]
lang_re = re.compile('|'.join(lang_words), re.IGNORECASE)

changed_files = []
counts = {"files_scanned":0, "files_changed":0, "replacements":0}

for path in ROOT.rglob('*.html'):
    counts["files_scanned"] += 1
    text = path.read_text(encoding='utf-8', errors='ignore')
    original = text

    # Apply structural patterns
    for pat in patterns:
        text, n = pat.subn('', text)
        counts["replacements"] += n

    # Additionally remove inline occurrences that are just language names inside attributes/text
    # but avoid aggressive removal inside main content: only remove within tags (attributes, small spans)
    # We'll remove occurrences inside tags: <...Deutsch...>
    text, n = re.subn(r'(<[^>]{0,200}?)(Deutsch|English|Espa(?:ñ|Ã±)ol|Fran[cç]ais|Nederlands|Portugu[eê]s)([^>]{0,200}?>)', r'\1\3', text, flags=re.IGNORECASE)
    counts["replacements"] += n

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed_files.append(path.relative_to(Path.cwd()))
        counts["files_changed"] += 1

print(f"Scanned {counts['files_scanned']} files, changed {counts['files_changed']} files, replacements: {counts['replacements']}")
for p in changed_files:
    print(p)
