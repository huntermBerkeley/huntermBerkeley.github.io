---
title: "Hello World"
date: "2026-05-06"
summary: "First post — testing the blog setup."
---

This is a test post. To write a new post:

1. Create a new `.md` file in `blog/posts/` named `YYYY-MM-DD-your-slug.md`
2. Add frontmatter at the top (title, date, optional summary)
3. Run `python3 blog/build.py` from the repo root

The script requires `pandoc` — install it with `brew install pandoc`.

## Frontmatter format

```
---
title: "My Post Title"
date: "2026-05-06"
summary: "One-line description shown on the blog index."
---

Post content goes here...
```

## Markdown features

**Bold**, *italic*, `inline code`, [links](https://example.com).

Code blocks with syntax highlighting in the rendered output:

```python
def hello():
    return "world"
```

Blockquotes:

> Research is what I'm doing when I don't know what I'm doing.

Delete this file when you write your first real post.
