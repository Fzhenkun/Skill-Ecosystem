# Fallback

Stop at the first failure. Do not edit the script to force success, swap tools, or install guessed packages. Identify the failing line, then apply the matching fix.

## Agent layer
Forbidden: editing `publish_post.py` just to pass, `--force` without approval, pushing without approval, silent skipping.
Required: quote the exact error, classify (path / content / git), fix only the skill's own files, otherwise show the User Fix and wait for "已修复".

## E1 `[FAIL] not a Jekyll blog dir`
User Fix: `Detected: blog dir has no _config.yml. Pass --blog-dir with the correct path. Reply: 已修复`

## E2 `[FAIL] no markdown found`
Check the source path is exact (spaces/Chinese need quotes) and exists.

## E3 `[SKIP] exists`
A post with the same date+slug exists. Ask the user: change `--slug`/`--date`, or approve `--force`.

## E4 `[FAIL] categories/tags must look like [a, b]`
Re-run with e.g. `--tags "[cpp, build]"`.

## E5 `[WARN] image not found`
Not fatal. Tell the user which images are missing; fix paths in the source, then re-run with approved `--force`.

## E6 git failure
```text
Detected: git add/commit/push failed (see output above).
Common causes: not logged in to GitHub, no remote (git remote -v), branch behind (git pull --rebase), no user.name/email.
Fix, then reply: 已修复
```
The post file is already written; retry only the git steps manually or re-run with `--push --force`.

## E7 UnicodeDecodeError
Source is not UTF-8. Ask the user to re-save as UTF-8.

## E8 `[WARN] remote image download failed`
Tell the user which URL failed and the reported reason. The original URL remains in the post, so it may still load externally but is not guaranteed to work after publishing. Check the URL, access restrictions, and whether the response is an image under 20 MiB; then re-run. If the post already exists, ask before using `--force`.
