# Description Patterns

## Goal

Write frontmatter descriptions that trigger on the right requests and stay out of the way of unrelated work.

## Length Limit (mandatory)

- Hard maximum: **1024 characters** (VS Code Agent Skills). Over the limit, the skill may fail to load.
- Target: **300-800 characters**. Too short is vague; too long dilutes key signals.
- Count the final text including Chinese and spaces; `scripts/maintain_skill.py` reports the count and fails above 1024.
- Prefer a single-line quoted string so the counted text equals the loaded text.
- To shorten: merge duplicated bilingual sentences, cut repeated synonyms, drop prose. Never drop the "when to use" or "do not use" parts.

## Strong Description Formula

Include all of the following:

1. What the skill does (positive enumeration of concrete scenarios).
2. When it must be used.
3. Strong signals first: special nouns, domain terms, protocol keywords.
4. Keyword carpet: synonyms, abbreviations, English aliases.
5. Reverse exclusion: what it must not be used for.
6. Strong imperative tone ("MUST USE", "immediately", "必须使用", "立即触发").
7. Bilingual trigger words when the working environment is bilingual.

Then put the trigger scenarios into a three-column table in `SKILL.md` (scenario, typical request, trigger keywords), not prose.

## Patterns

### Positive enumeration

List the exact scenarios that should trigger the skill.

Example:

```text
MUST USE when the user wants to create a new skill, repair a partial skill, optimize skill triggering, split a large skill into references, or establish a maintenance workflow.
```

### Keyword carpet

Add synonyms, abbreviations, and alternate phrasings that real users may use.

Example concepts:

- skill creation
- skill packaging
- SKILL.md
- trigger optimization
- reference routing
- maintain skill
- 优化技能
- 创建技能
- 维护 skill

### Reverse exclusion

State what not to use the skill for.

Example:

```text
Do NOT use for ordinary application coding unless the task is specifically about skill construction or maintenance.
```

## Anti-Patterns

Avoid:

- vague descriptions such as "help with automation"
- body-only trigger guidance that never appears in frontmatter
- long unstructured paragraphs with no concrete scenarios
- descriptions that overlap heavily with unrelated skills
- descriptions longer than 1024 characters
- multi-paragraph bilingual descriptions that repeat the same content twice
