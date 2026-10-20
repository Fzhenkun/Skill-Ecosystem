---
name: blog-post-publisher
description: MUST USE when the user wants to turn local Markdown/笔记/文档 into a blog post for this Jekyll + Chirpy GitHub Pages blog (非鱼随记) and optionally publish it, or wants to hide/unpublish/re-publish an existing post. Adds Front Matter (title/date/categories/tags/math), renames to YYYY-MM-DD-slug.md, copies local images and downloads HTTP(S) image links into the blog's article-specific assets folder, rewrites them to site paths, strips WYSIWYG `<font>` styling artifacts, can mark a post hidden (`published: false`, excluded entirely from the live site), then can git add/commit/push only with approval. 触发词:发布文章、markdown转博客、把文档放进博客、导入文档、批量导入、上传博客、发文、下载图片、图片本地化、隐藏文章、不公开、不展示、取消发布、下架文章。Do NOT use for creating a new blog site (use personal-website-builder), non-Jekyll sites, or editing the theme/config.
---

# Blog Post Publisher

Routing only. One command does the conversion: `scripts/publish_post.py`.

## Flow

1. Get the source `.md` path (or a directory) from the user; pass it verbatim.
2. Ask only what is missing: categories (max 2 levels), tags (lowercase English). Default categories is `[随记]`. Also ask whether the post should be hidden from the live site for now (`--hidden`); default is no.
3. Preview first: `python scripts/publish_post.py "<src>" --dry-run --categories "[A, B]" --tags "[x, y]"`
4. Run without `--dry-run`; local images are copied and HTTP(S) image links are downloaded into the blog's article-specific assets folder and rewritten for the site. Report every `[WARN]` line (missing local files or failed downloads) to the user.
5. Publishing: only add `--push` after the user explicitly agrees; push triggers a public deployment.
6. Tell the user the post appears in 1-3 minutes at https://fzhenkun.github.io — unless `--hidden` was used, in which case nothing appears there until the `published: false` line is removed from the post's Front Matter and it is pushed again.

## Hiding / re-publishing an existing post

To take an already-published post off the live site (keep it in the repo, just stop showing it), add `published: false` to its Front Matter — no script run needed. To bring it back, delete that line (or set it to `true`). Either way the change only takes effect on the live site after a `git push` (ask for approval before pushing).

## Read when needed

| Need | File |
| --- | --- |
| Options, conversion rules, limitations | `references/usage.md` |
| Any `[FAIL]`, git or script error | `references/fallback.md` |
| Sample invocations | `examples/positive.md`, `examples/negative.md` |

## Hard rules

- Never edit the script to force success; on failure read `references/fallback.md` first.
- Existing posts are skipped unless the user approves `--force`.
- Never push without user approval.
- Audit before delivery (optional, if the skill-lifecycle-engine skill is installed): `python <path>\skill-lifecycle-engine\scripts\maintain_skill.py --skill-dir <this-folder>`
