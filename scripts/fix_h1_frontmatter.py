#!/usr/bin/env python3
"""
Remove leading H1 headings from Markdown files under src/content/docs and ensure
YAML frontmatter `title` matches the removed H1. Backups are saved with `.bak`.
"""
import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "src" / "content" / "docs"


def extract_title_from_text(text: str) -> Optional[str]:
    m = re.search(r"^\s*#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def extract_title_from_filename(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ")


def make_frontmatter(title: str, other_lines: Optional[list[str]] = None) -> str:
    escaped = title.replace('"', '\\"')
    lines = ["---", f'title: "{escaped}"']
    if other_lines:
        lines.extend(other_lines)
    else:
        lines.append('description: ""')
        lines.append('draft: false')
    lines.append("---\n")
    return "\n".join(lines) + "\n"


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if fm_match:
        fm_body = fm_match.group(1)
        rest = text[fm_match.end():]
    else:
        fm_body = None
        rest = text

    h1_title = extract_title_from_text(rest)

    if fm_body is None and not h1_title:
        title = extract_title_from_filename(path)
        fm = make_frontmatter(title)
        bak = path.with_suffix(path.suffix + ".bak")
        bak.write_text(text, encoding="utf-8")
        path.write_text(fm + text, encoding="utf-8")
        return True

    changed = False

    if h1_title:
        rest_new = re.sub(r"^\s*#\s+.+?\s*\n(?:\s*\n)?", "", rest, count=1, flags=re.MULTILINE)
    else:
        rest_new = rest

    if fm_body is None:
        title = h1_title or extract_title_from_filename(path)
        fm = make_frontmatter(title)
        new_text = fm + rest_new
        changed = True
    else:
        fm_lines = [l for l in fm_body.splitlines() if not re.match(r"^\s*title\s*:\s*", l, flags=re.I)]
        if h1_title:
            title_to_use = h1_title
            changed = True
        else:
            m = re.search(r"^\s*title\s*:\s*(?:\"|\')?(.*?)(?:\"|\')?\s*$", fm_body, flags=re.I | re.M)
            if m:
                title_to_use = m.group(1).strip()
            else:
                title_to_use = extract_title_from_filename(path)
                changed = True

        fm = make_frontmatter(title_to_use, fm_lines)
        new_text = fm + rest_new

    if changed:
        bak = path.with_suffix(path.suffix + ".bak")
        bak.write_text(text, encoding="utf-8")
        path.write_text(new_text, encoding="utf-8")
        return True

    return False


if __name__ == "__main__":
    if not DOCS_DIR.exists():
        print("Docs directory not found:", DOCS_DIR)
        raise SystemExit(1)
    updated = []
    for p in sorted(DOCS_DIR.rglob("*.md")):
        if process_file(p):
            updated.append(str(p.relative_to(ROOT)))
    if updated:
        print("Updated files:")
        for u in updated:
            print(" -", u)
    else:
        print("No files changed.")
