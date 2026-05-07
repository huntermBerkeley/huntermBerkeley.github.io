#!/usr/bin/env python3
"""
Blog build script. Requires pandoc (brew install pandoc).

Usage:
    python3 blog/build.py          # build all posts + regenerate index
    python3 blog/build.py --help
"""

import subprocess
import sys
import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
POSTS_DIR  = SCRIPT_DIR / "posts"
TEMPLATE   = SCRIPT_DIR / "_template.html"


def check_pandoc():
    if subprocess.run(["which", "pandoc"], capture_output=True).returncode != 0:
        print("Error: pandoc not found. Install with:\n  brew install pandoc")
        sys.exit(1)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract --- delimited YAML-ish frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    front = text[3:end]
    body  = text[end + 4:].lstrip("\n")
    meta  = {}
    for line in front.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def md_to_html(markdown: str) -> str:
    result = subprocess.run(
        ["pandoc", "--from=markdown", "--to=html"],
        input=markdown, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc error: {result.stderr.strip()}")
    return result.stdout


def build_post(md_file: Path) -> dict | None:
    text = md_file.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    title   = meta.get("title",   md_file.stem.replace("-", " ").title())
    date    = meta.get("date",    "")
    summary = meta.get("summary", "")

    try:
        html_body = md_to_html(body)
    except RuntimeError as e:
        print(f"  ! {e}")
        return None

    template = TEMPLATE.read_text(encoding="utf-8")
    html = (template
            .replace("{{TITLE}}", title)
            .replace("{{DATE}}",  date)
            .replace("{{BODY}}",  html_body))

    slug    = md_file.stem          # e.g. 2026-05-06-my-post
    out_dir = SCRIPT_DIR / slug
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")

    print(f"  built  → blog/{slug}/index.html")
    return {"title": title, "date": date, "summary": summary, "slug": slug}


def build_index(posts: list[dict]):
    posts.sort(key=lambda p: p["date"], reverse=True)

    if posts:
        items = "\n".join(
            f"""        <li>
            <div class="post-date">{p["date"]}</div>
            <div class="post-title"><a href="{p["slug"]}/">{p["title"]}</a></div>
            {"<div class='post-summary'>" + p["summary"] + "</div>" if p["summary"] else ""}
        </li>"""
            for p in posts
        )
        content = f'<ul class="blog-list">\n{items}\n    </ul>'
    else:
        content = '<p style="color: var(--text-muted); font-size: 0.95em;">No posts yet.</p>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - Hunter McCoy</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <nav>
            <!-- Navigation populated by JavaScript -->
        </nav>
    </header>

    <main>
        <section>
            <h2>Blog</h2>
            {content}
        </section>
    </main>

    <script src="../js/navigation.js"></script>
</body>
</html>
"""
    (SCRIPT_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"  built  → blog/index.html  ({len(posts)} post{'s' if len(posts) != 1 else ''})")


def main():
    check_pandoc()

    if not POSTS_DIR.exists():
        print("No posts/ directory — writing empty index.")
        build_index([])
        return

    md_files = sorted(POSTS_DIR.glob("*.md"))
    if not md_files:
        print("No .md files found in blog/posts/")
        build_index([])
        return

    print(f"Building {len(md_files)} post(s)...")
    posts = [build_post(f) for f in md_files]
    posts = [p for p in posts if p]

    build_index(posts)
    print("Done.")


if __name__ == "__main__":
    main()
