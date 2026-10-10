"""Render a structured cognition analysis JSON file into a self-contained HTML report."""

import argparse
import json
import sys
from html import escape
from pathlib import Path

LABELS = {
    "zh": {
        "essence": "本质一句话",
        "na": "不适用",
        "conclusion": "综合结论",
        "stance": "建议立场",
        "risks": "主要风险",
        "open": "待验证问题",
        "sources": "参考来源",
        "fact": "事实",
        "inference": "推断",
        "speculation": "推测",
        "high": "高",
        "medium": "中",
        "low": "低",
        "conf": "置信度",
    },
    "en": {
        "essence": "Essence in one sentence",
        "na": "Not applicable",
        "conclusion": "Conclusion",
        "stance": "Recommended stance",
        "risks": "Key risks",
        "open": "Open questions",
        "sources": "Sources",
        "fact": "Fact",
        "inference": "Inference",
        "speculation": "Speculation",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "conf": "Confidence",
    },
}

CSS = """
body{font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;margin:0;background:#f5f6f8;color:#1f2430;line-height:1.65}
main{max-width:920px;margin:0 auto;padding:32px 20px 64px}
h1{margin:0 0 4px;font-size:28px}.sub{color:#5b6475;margin-bottom:20px}
.essence{background:#1f2f5c;color:#fff;border-radius:10px;padding:16px 20px;margin:16px 0 24px}
.essence b{display:block;font-size:12px;opacity:.75;margin-bottom:4px}
section.dim{background:#fff;border-radius:10px;padding:18px 22px;margin:14px 0;box-shadow:0 1px 3px rgba(0,0,0,.08)}
section.dim.na{opacity:.65}
h2{font-size:18px;margin:0 0 6px}.num{display:inline-block;width:26px;height:26px;line-height:26px;text-align:center;border-radius:50%;background:#3b5bdb;color:#fff;font-size:14px;margin-right:8px}
.summary{font-weight:600;margin:4px 0 10px}
ul{padding-left:20px;margin:6px 0}li{margin:6px 0}
.tag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:9px;margin-right:6px;color:#fff}
.fact{background:#2f9e44}.inference{background:#e8890c}.speculation{background:#c92a2a}
.conf{font-size:12px;color:#5b6475}
.concl{background:#fff;border-left:5px solid #3b5bdb;border-radius:6px;padding:16px 22px;margin-top:24px}
"""


def tr(lang: str, key: str) -> str:
    return LABELS[lang].get(key, key)


def render_list(items) -> str:
    return "<ul>" + "".join(f"<li>{escape(str(i))}</li>" for i in items) + "</ul>"


def render_dimension(dim: dict, lang: str) -> str:
    applicable = dim.get("applicable", True)
    parts = [
        f'<section class="dim{"" if applicable else " na"}">',
        f'<h2><span class="num">{escape(str(dim.get("id", "")))}</span>{escape(dim.get("name", ""))}</h2>',
    ]
    if not applicable:
        parts.append(f'<p><b>{tr(lang, "na")}</b>: {escape(dim.get("reason", ""))}</p>')
    else:
        if dim.get("summary"):
            parts.append(f'<div class="summary">{escape(dim["summary"])}</div>')
        parts.append("<ul>")
        for p in dim.get("points", []):
            ptype = p.get("type", "inference")
            if ptype not in ("fact", "inference", "speculation"):
                ptype = "inference"
            conf = p.get("confidence", "medium")
            parts.append(
                f'<li><span class="tag {ptype}">{tr(lang, ptype)}</span>'
                f'{escape(p.get("text", ""))} '
                f'<span class="conf">({tr(lang, "conf")}: {escape(tr(lang, conf))})</span></li>'
            )
        parts.append("</ul>")
    parts.append("</section>")
    return "".join(parts)


def render(data: dict) -> str:
    lang = data.get("language", "zh")
    if lang not in LABELS:
        lang = "zh"
    body = [f'<h1>{escape(data["title"])}</h1>']
    if data.get("subtitle"):
        body.append(f'<div class="sub">{escape(data["subtitle"])}</div>')
    if data.get("essence"):
        body.append(f'<div class="essence"><b>{tr(lang, "essence")}</b>{escape(data["essence"])}</div>')
    body.extend(render_dimension(d, lang) for d in data["dimensions"])

    concl = data.get("conclusion")
    if concl:
        block = [f'<div class="concl"><h2>{tr(lang, "conclusion")}</h2>']
        if concl.get("stance"):
            block.append(f'<p><b>{tr(lang, "stance")}</b>: {escape(concl["stance"])}</p>')
        if concl.get("risks"):
            block.append(f'<b>{tr(lang, "risks")}</b>{render_list(concl["risks"])}')
        if concl.get("open_questions"):
            block.append(f'<b>{tr(lang, "open")}</b>{render_list(concl["open_questions"])}')
        block.append("</div>")
        body.append("".join(block))

    if data.get("sources"):
        body.append(f'<div class="concl"><h2>{tr(lang, "sources")}</h2>{render_list(data["sources"])}</div>')

    return (
        f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{escape(data["title"])}</title><style>{CSS}</style></head>'
        f'<body><main>{"".join(body)}</main></body></html>'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to analysis JSON")
    parser.add_argument("--output", required=True, help="Path to output HTML")
    args = parser.parse_args()

    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
        if "title" not in data or not isinstance(data.get("dimensions"), list):
            raise ValueError("JSON must contain 'title' and a 'dimensions' list")
        html = render(data)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    Path(args.output).write_text(html, encoding="utf-8")
    print(f"Report written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
