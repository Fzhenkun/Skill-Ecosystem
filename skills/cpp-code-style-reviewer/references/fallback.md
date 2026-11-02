# Fallback

If the checker command fails, stop and report the exact command and error. Classify it as path, encoding, permission, or script failure. Read the target file manually if possible, but label all findings as manual and do not pretend the script passed.

If a file is not readable or the path does not exist, ask for a valid path. Preserve the user's literal path in the report.

If project rules conflict with the Google style rules, do not silently choose one. State the project rule, the Google rule, and which one was used for the result.

If automatic repair would require changing names, includes, ownership, casts, macros, or class interfaces, refuse that individual edit and provide a reviewable patch suggestion instead.
