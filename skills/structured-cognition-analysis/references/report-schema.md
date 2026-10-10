# Report JSON Schema

Input for `scripts/render_report.py`.

```json
{
  "title": "Subject name",
  "subtitle": "optional one-line framing",
  "language": "zh",
  "essence": "One-sentence essence of the subject",
  "dimensions": [
    {
      "id": 1,
      "name": "基石假设 / Foundational assumptions",
      "applicable": true,
      "summary": "Short conclusion for this dimension",
      "points": [
        {"text": "A specific finding", "type": "fact", "confidence": "high"}
      ],
      "reason": "Only when applicable=false: why skipped"
    }
  ],
  "conclusion": {
    "stance": "Recommended stance",
    "risks": ["..."],
    "open_questions": ["..."]
  },
  "sources": ["optional list of references"]
}
```

- `type`: `fact` | `inference` | `speculation`
- `confidence`: `high` | `medium` | `low`
- `language`: `zh` or `en` (affects labels only)
- Only `title` and `dimensions` are required; other fields are optional.
