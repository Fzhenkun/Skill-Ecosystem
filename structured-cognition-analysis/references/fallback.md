# Fallback Rules

| Situation | Action |
| --- | --- |
| `python` unavailable | Tell the user; write the report as a hand-authored single-file HTML using the same section order, and say it was not script-rendered. |
| JSON invalid | Fix the JSON against `report-schema.md`; do not alter analysis content. |
| Evidence is thin or no search tool | Analyze from provided material and general knowledge; mark points as `inference`/`speculation` with low confidence and list gaps under open questions. |
| Subject is trivial | Answer directly; offer a report only if the user insists. |
| Subject ambiguous | Ask one clarifying question about the subject before analyzing. |
| Output path not writable | Report the error; propose an alternate path instead of silently choosing one elsewhere. |

Never invent sources, citations, or data.
