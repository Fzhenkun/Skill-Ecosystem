#!/usr/bin/env python3
"""Convert local Markdown into a Jekyll/Chirpy post, copy images, optionally git push."""
import argparse
import datetime as dt
import hashlib
import mimetypes
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote, unquote
from urllib.parse import urlsplit

DEFAULT_BLOG = str(Path(__file__).resolve().parents[4])  # <repo>/.github/skills/<name>/scripts/
MAX_IMAGE_BYTES = 20 * 1024 * 1024
IMAGE_TIMEOUT_SECONDS = 20
IMG_MD = re.compile(r'(!\[[^\]]*\]\()(<[^>]+>|[^)\s]+)((?:\s+"[^"]*")?\))')
IMG_HTML = re.compile(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'])', re.I)
FENCE = re.compile(r"^\s*(```|~~~)")
# WYSIWYG exports (e.g. Yuque) wrap plain text in <font color/background-color> spans;
# Chirpy has no use for them, so unwrap to the inner text and keep any surrounding backticks intact.
FONT_TAG = re.compile(r"<font\b[^>]*>(.*?)</font>", re.I)


def split_front_matter(text):
    if text.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
        if m:
            return m.group(1), text[m.end():]
    return "", text


def parse_fm(raw):
    fm, extra = {}, []
    for line in raw.splitlines():
        m = re.match(r"^(title|date|categories|tags|math|mermaid|published):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
        elif line.strip():
            extra.append(line)
    return fm, extra


def make_slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if len(s) >= 3:
        return s[:60]
    return "post-" + hashlib.md5(name.encode("utf-8")).hexdigest()[:6]


def is_remote(p):
    return re.match(r"^(https?:|data:|//|/|#)", p, re.I) is not None


def remote_filename(url, content_type=""):
    parsed = urlsplit(url)
    basename = unquote(parsed.path).rsplit("/", 1)[-1]
    stem = Path(basename).stem
    suffix = Path(basename).suffix
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip(".-_") or "image"
    if not re.fullmatch(r"\.[A-Za-z0-9]{1,10}", suffix):
        suffix = ""
    if not suffix and content_type:
        suffix = mimetypes.guess_extension(content_type, strict=False) or ""
        if suffix == ".jpe":
            suffix = ".jpg"
    suffix = suffix.lower() or ".img"
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    return f"{stem[:80]}-{digest}{suffix}"


def download_remote_image(url):
    request = urllib.request.Request(url, headers={"User-Agent": "blog-post-publisher/1.0"})
    with urllib.request.urlopen(request, timeout=IMAGE_TIMEOUT_SECONDS) as response:
        content_type = response.headers.get_content_type().lower()
        data = response.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError(f"image exceeds {MAX_IMAGE_BYTES // (1024 * 1024)} MiB limit")
    if not data:
        raise ValueError("image response is empty")
    if not content_type.startswith("image/"):
        raise ValueError(f"response content type is not an image: {content_type}")
    return data, content_type


def convert(src, blog, args, dry_run=False):
    text = src.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    raw_fm, body = split_front_matter(text)
    fm, extra = parse_fm(raw_fm)

    title = fm.get("title", "").strip("\"'")
    in_fence, out, h1_done = False, [], False
    for line in body.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
        # The theme renders the title itself, so drop the first H1.
        if not in_fence and not h1_done and re.match(r"^# +\S", line):
            h1_done = True
            if not title:
                title = line[2:].strip()
            if line[2:].strip() == title:
                continue
        out.append(line)
    title = title or src.stem

    date_str = args.date or fm.get("date")
    if not date_str:
        date_str = dt.datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S +0800")
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        date_str += " 12:00:00 +0800"
    day = date_str[:10]
    slug = args.slug or make_slug(src.stem)

    img_dir = blog / "assets" / "img" / "posts" / slug
    copied, warnings, remote_count = [], [], 0

    def fix(path_str):
        nonlocal remote_count
        p = path_str.strip("<>")
        if re.match(r"^data:", p, re.I) or p.startswith(("/", "#")):
            return path_str
        if p.startswith("//"):
            url = "https:" + p
        elif re.match(r"^https?://", p, re.I):
            url = p
        else:
            url = None

        if url:
            remote_count += 1
            parsed = urlsplit(url)
            if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
                warnings.append(f"remote image URL is invalid: {url}")
                return path_str
            download_url = parsed._replace(fragment="").geturl()
            if dry_run:
                filename = remote_filename(download_url)
            else:
                try:
                    data, content_type = download_remote_image(download_url)
                except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                    warnings.append(f"remote image download failed: {url} ({exc})")
                    return path_str
                filename = remote_filename(download_url, content_type)
                img_dir.mkdir(parents=True, exist_ok=True)
                (img_dir / filename).write_bytes(data)
            copied.append(filename)
            return f"/assets/img/posts/{slug}/{quote(filename)}"

        if is_remote(p):
            return path_str
        cand = Path(unquote(p))
        if not cand.is_absolute():
            cand = src.parent / cand
        if not cand.is_file():
            warnings.append(f"image not found: {p}")
            return path_str
        if not dry_run:
            img_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(cand, img_dir / cand.name)
        copied.append(cand.name)
        return f"/assets/img/posts/{slug}/{quote(cand.name)}"

    in_fence, res = False, []
    for line in out:
        if FENCE.match(line):
            in_fence = not in_fence
        if not in_fence:
            line = IMG_MD.sub(lambda m: m.group(1) + fix(m.group(2)) + m.group(3), line)
            line = IMG_HTML.sub(lambda m: m.group(1) + fix(m.group(2)) + m.group(3), line)
            line = FONT_TAG.sub(lambda m: m.group(1), line)
        res.append(line)
    body_out = "\n".join(res).lstrip("\n")
    # Collapse blank lines left behind by now-empty <font></font> tags.
    body_out = re.sub(r"\n{3,}", "\n\n", body_out)

    cats = args.categories or fm.get("categories") or "[随记]"
    tags = args.tags or fm.get("tags") or "[]"
    for v in (cats, tags):
        if not v.startswith("["):
            sys.exit(f"[FAIL] categories/tags must look like [a, b]: {v}")

    head = ["---", f"title: {title}", f"date: {date_str}", f"categories: {cats}", f"tags: {tags}"]
    stripped = re.sub(r"```.*?```", "", body_out, flags=re.S)
    if fm.get("math") or re.search(r"\$\$|(?<![\\$])\$[^$\n]+\$", stripped):
        head.append("math: true")
    if fm.get("mermaid") or re.search(r"^```mermaid", body_out, re.M):
        head.append("mermaid: true")
    # `published: false` tells Jekyll to skip the post entirely (no page, no listing, no feed/search entry).
    if args.hidden or fm.get("published", "").strip().lower() == "false":
        head.append("published: false")
    head += extra + ["---", ""]
    target = blog / "_posts" / f"{day}-{slug}.md"
    return target, "\n".join(head) + "\n" + body_out.rstrip("\n") + "\n", copied, warnings, remote_count


def git(blog, *a):
    r = subprocess.run(["git", "-C", str(blog), *a], capture_output=True, text=True)
    print(r.stdout + r.stderr, end="")
    if r.returncode:
        sys.exit(f"[FAIL] git {' '.join(a)} exited {r.returncode}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", help="a .md file or a directory of .md files")
    ap.add_argument("--blog-dir", default=DEFAULT_BLOG)
    ap.add_argument("--slug")
    ap.add_argument("--date", help="YYYY-MM-DD or full datetime")
    ap.add_argument("--categories", help='e.g. "[C++, 编译优化]"')
    ap.add_argument("--tags", help='e.g. "[cpp, build]"')
    ap.add_argument("--force", action="store_true", help="overwrite existing post")
    ap.add_argument("--hidden", action="store_true", help="add published: false (post is kept in the repo but Jekyll skips it entirely: no page, no listing, no feed/search entry)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--push", action="store_true", help="git add/commit/push (needs user approval)")
    args = ap.parse_args()

    blog = Path(args.blog_dir)
    if not (blog / "_config.yml").is_file():
        sys.exit(f"[FAIL] not a Jekyll blog dir: {blog}")
    src = Path(args.src)
    files = sorted(src.glob("*.md")) if src.is_dir() else [src]
    if not files or not all(f.is_file() for f in files):
        sys.exit(f"[FAIL] no markdown found: {src}")
    if len(files) > 1 and args.slug:
        sys.exit("[FAIL] --slug only valid for a single file")

    written = []
    for f in files:
        target, content, copied, warnings, remote_count = convert(f, blog, args, dry_run=True)
        if target.exists() and not args.force:
            print(f"[SKIP] exists (use --force): {target}")
            continue
        if args.dry_run:
            print(f"[OK] {f.name} -> {target.name}; images to copy/download: {len(copied)}")
            if remote_count:
                print(f"[INFO] remote images to download: {remote_count}")
        else:
            target, content, copied, warnings, _ = convert(f, blog, args)
            print(f"[OK] {f.name} -> {target.name}; images copied/downloaded: {len(copied)}")
            target.write_text(content, encoding="utf-8", newline="\n")
            written.append(target)
        for warning in warnings:
            print(f"[WARN] {warning}")

    if args.push and written and not args.dry_run:
        git(blog, "add", "-A")
        git(blog, "commit", "-m", f"新增文章:{', '.join(p.stem[11:] for p in written)}")
        git(blog, "push")
        print("[OK] pushed; Actions will deploy in 1-3 minutes")


if __name__ == "__main__":
    main()
