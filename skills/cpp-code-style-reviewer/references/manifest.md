# Manifest

## Capabilities

- Review C++ source and header files against the Google C++ Style Guide points represented in the reference image.
- Provide a structured Chinese summary that starts with a global map, then explains key rules, mechanisms, boundaries, historical causes, and verification practices.
- Report findings with file, line, severity, rule, rationale, and an actionable suggestion.
- Read project-specific `.clang-format`, `clang-tidy`, `cpplint`, and repository guidance as higher-priority local constraints.
- Run a dependency-free heuristic checker on individual files or directories.
- Apply only low-risk mechanical fixes when the user explicitly asks for code changes.

## Boundaries

This skill does not replace a compiler, formatter, static analyzer, security review, or runtime debugger. It must not silently change names, ownership, casts, includes, macros, or public interfaces.

## Documentation

- `references/cpp-style-guide-summary.md`: human-readable summary and investigation checklist.
- `reports/cpp-style-guide-analysis.html`: rendered structured analysis report.
