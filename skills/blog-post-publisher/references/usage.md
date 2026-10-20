# Usage

```powershell
python scripts/publish_post.py <src> [--blog-dir DIR] [--slug S] [--date D] [--categories "[A, B]"] [--tags "[x]"] [--force] [--hidden] [--dry-run] [--push]
```

`<src>` is a file or a directory (non-recursive, `*.md`). `--blog-dir` defaults to the repository root (resolved from the script location).

## What it does

| Step | Rule |
| --- | --- |
| Title | Front Matter `title`, else first H1 (removed from body, theme renders it), else filename |
| Date | `--date`, else Front Matter, else file mtime (+0800) |
| File name | `_posts/YYYY-MM-DD-slug.md`; slug from ASCII filename, else `post-<hash>` (use `--slug` for readable URLs) |
| Categories/tags | Args > Front Matter > `[随记]` / `[]`; must be `[a, b]` form |
| Math / Mermaid | `math: true` if `$..$`/`$$` outside code fences; `mermaid: true` if a mermaid fence exists |
| Visibility | `--hidden`, or a source Front Matter `published: false`, adds `published: false` to the post. Jekyll then skips it entirely (no generated page, not in home/archive/categories/tags/search/RSS); re-publish later by removing that line (or re-running without `--hidden` and `--force`). |
| Images | Local `![](x)` and `<img src>` copied to `assets/img/posts/<slug>/`; HTTP(S) and protocol-relative image URLs downloaded there with stable URL-hash filenames. Links are rewritten to `/assets/img/posts/<slug>/<name>` so the published site serves local copies. `data:`, root-relative, and fragment sources stay unchanged. |
| `<font>` cleanup | `<font style="...">text</font>` spans (common in Yuque/WYSIWYG exports) are unwrapped to their inner text outside code fences, so styled-but-empty markup never leaks into the post as literal tags or stray inline code. |
| Other Front Matter keys | Preserved |
| Push | `git add -A`, commit `新增文章:<slug>`, push |

## Limitations

- Same-named images from different folders collide (last wins).
- Remote image downloads are limited to 20 MiB per image and 20 seconds; failed requests or non-image responses leave the original URL unchanged and print `[WARN]`. Preview (`--dry-run`) reports planned downloads without making network requests.
- Only inline Markdown images (`![](...)`) and HTML `<img src>` are converted; reference-style Markdown image definitions are not supported.
- `<font>` stripping only unwraps the tag; other inline styling tags (`<span style=...>`, etc.) are left as-is.
- Multi-line Front Matter lists for title/categories/tags are not parsed; use `[a, b]` single-line.
- Word/PDF must be converted to Markdown first (e.g. `pandoc x.docx -o x.md --extract-media=./media`).
- Images are not compressed; keep each under ~500KB.
- Wiki-links (`[[x]]`) and Obsidian callouts are not converted.
