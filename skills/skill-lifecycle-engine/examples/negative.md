# Negative Examples

## Example 1

User request:

```text
Build a React dashboard for inventory tracking.
```

Why this skill should not trigger:

- application development task
- no skill construction or maintenance requested

## Example 2

User request:

```text
Write a Python script that renames image files in a folder.
```

Why this skill should not trigger:

- standalone scripting task
- not about a skill package

## Example 3

User request:

```text
Explain how YAML frontmatter works in Markdown.
```

Why this skill should not trigger by default:

- general explanation request
- only trigger if the broader task is to build or repair a skill

## Counter-example: rewriting user text

User gives `C:\Users\me\Desktop\skills工程\x.txt`. Writing "the notes file on the desktop" into the skill or command is wrong; use the path verbatim.
