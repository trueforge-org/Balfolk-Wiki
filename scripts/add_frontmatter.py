#!/usr/bin/env python3
"""
Add a simple YAML frontmatter with a `title` to Markdown files under src/content/docs
if they don't already start with frontmatter. The title is taken from the first
H1 heading (`# Title`) when present, otherwise from the filename.

Backups are saved with a `.bak` extension next to the original file.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "src" / "content" / "docs"

def has_frontmatter(text: str) -> bool:
    return bool(re.match(r"^---\s*\n", text))

def extract_title(text: str, path: Path) -> str:
    # Look for first level-1 heading
    m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    # fallback: filename without extension
    return path.stem.replace("-"," ").replace("_"," ")

def make_frontmatter(title: str) -> str:
    # Minimal starlight-compatible frontmatter
    fm = ["---"]
    fm.append(f"title: \"{title.replace('"','\'')}\"")
    fm.append("description: \"\"")
    fm.append("draft: false")
    fm.append("---\n\n")
    return "\n".join(fm)

def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if has_frontmatter(text):
        return False
    title = extract_title(text, path)
    fm = make_frontmatter(title)
    # Backup original
    bak = path.with_suffix(path.suffix + ".bak")
    bak.write_text(text, encoding="utf-8")
    path.write_text(fm + text, encoding="utf-8")
    return True

def main():
    changed = []
    if not DOCS_DIR.exists():
        print("Docs directory not found:", DOCS_DIR)
        return
    for p in sorted(DOCS_DIR.rglob("*.md")):
        if process_file(p):
            changed.append(str(p.relative_to(ROOT)))
    if changed:
        print("Updated files:")
        for c in changed:
            print(" -", c)
    else:
        print("No files needed updates.")

if __name__ == "__main__":
    main()
