"""Render a structured cognition JSON file into a readable Markdown report."""

import argparse
import json
import sys
from pathlib import Path


LABELS = {
    "zh": {
        "scope": "界定对象",
        "map": "全局/上下文地图",
        "mechanisms": "关键机制",
        "anomalies": "反常点与历史追溯",
        "boundaries": "边界与代价",
        "verification": "实践验证",
        "lenses": "分析透镜",
        "essence": "本质一句话",
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
    },
    "en": {
        "scope": "Scope",
        "map": "Global/context map",
        "mechanisms": "Key mechanisms",
        "anomalies": "Anomalies and history",
        "boundaries": "Boundaries and costs",
        "verification": "Practice and verification",
        "lenses": "Analytical lenses",
        "essence": "Essence in one sentence",
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
    },
}


def label(lang, key):
    return LABELS.get(lang, LABELS["zh"]).get(key, key)


def claim(text, kind="inference", confidence="medium"):
    return f"- **{label('zh', kind)}**（置信度：{label('zh', confidence)}）：{text}"


def bullet_list(items):
    return "\n".join(f"- {item}" for item in items) if items else "- （无）"


def render_map(context_map):
    if not context_map:
        return "_未提供地图；对简单对象仅保留最小上下文。_\n"
    lines = []
    for key, title in (
        ("scope", "范围"),
        ("components", "组件"),
        ("actors", "参与者/所有者"),
        ("flows", "输入输出与流程"),
        ("dependencies", "依赖"),
        ("lifecycle", "生命周期"),
        ("failure_surface", "失效面"),
    ):
        value = context_map.get(key)
        if not value:
            continue
        lines.append(f"**{title}**")
        if isinstance(value, list):
            lines.append(bullet_list(value))
        else:
            lines.append(str(value))
    return "\n\n".join(lines) + "\n"


def render_claims(points):
    return "\n".join(
        claim(p.get("text", ""), p.get("type", "inference"), p.get("confidence", "medium"))
        for p in points
    ) or "- （无具体结论）"


def render(data):
    lang = data.get("language", "zh")
    lines = [f"# {data['title']}", ""]
    if data.get("subtitle"):
        lines += [data["subtitle"], ""]
    if data.get("complexity"):
        lines += [f"**调查尺度：** `{data['complexity']}`", ""]
    if data.get("scope"):
        lines += [f"## {label(lang, 'scope')}", "", data["scope"], ""]
    if data.get("essence"):
        lines += [f"## {label(lang, 'essence')}", "", data["essence"], ""]

    if "context_map" in data:
        lines += [f"## {label(lang, 'map')}", "", render_map(data.get("context_map")), ""]

    mechanisms = data.get("key_mechanisms", [])
    if mechanisms:
        lines += [f"## {label(lang, 'mechanisms')}", ""]
        for i, item in enumerate(mechanisms, 1):
            lines += [f"### {i}. {item.get('name', '未命名机制')}"]
            if item.get("importance"):
                lines += [f"**为何关键：** {item['importance']}", ""]
            if item.get("chain"):
                lines += [f"**因果链：** `{item['chain']}`", ""]
            lines += [render_claims(item.get("points", [])), ""]

    anomalies = data.get("anomalies", [])
    if anomalies:
        lines += [f"## {label(lang, 'anomalies')}", ""]
        for i, item in enumerate(anomalies, 1):
            lines += [f"### {i}. {item.get('observation', '未命名反常点')}"]
            if item.get("evidence"):
                lines += ["**证据：**", bullet_list(item["evidence"]), ""]
            if item.get("historical_explanation"):
                lines += [f"**历史解释：** {item['historical_explanation']}", ""]
            if item.get("hypotheses"):
                lines += ["**待证假设：**", bullet_list(item["hypotheses"]), ""]
            if item.get("current_constraint"):
                lines += [f"**当前约束：** {item['current_constraint']}", ""]

    if data.get("boundaries"):
        lines += [f"## {label(lang, 'boundaries')}", "", render_claims(data["boundaries"]), ""]

    if data.get("verification"):
        lines += [f"## {label(lang, 'verification')}", ""]
        for i, item in enumerate(data["verification"], 1):
            lines += [f"### {i}. {item.get('check', '未命名检查')}"]
            lines += [f"**预期：** {item.get('expected', '未说明')}"]
            lines += [f"**结果：** {item.get('result', '未执行')}"]
            lines += [f"**限制：** {item.get('limits', '未说明')}", ""]

    # Backward compatibility with the original eight-dimension input.
    dimensions = data.get("dimensions", [])
    lenses = data.get("lenses", []) or dimensions
    if lenses:
        lines += [f"## {label(lang, 'lenses')}", ""]
        for i, item in enumerate(lenses, 1):
            name = item.get("name", f"透镜 {i}")
            lines += [f"### {item.get('id', i)}. {name}"]
            if item.get("summary"):
                lines += [item["summary"], ""]
            if item.get("applicable") is False:
                lines += [f"_不适用：{item.get('reason', '未说明')}_", ""]
            else:
                lines += [render_claims(item.get("points", [])), ""]

    conclusion = data.get("conclusion", {})
    if conclusion:
        lines += [f"## {label(lang, 'conclusion')}", ""]
        if conclusion.get("stance"):
            lines += [f"**{label(lang, 'stance')}：** {conclusion['stance']}", ""]
        if conclusion.get("risks"):
            lines += [f"**{label(lang, 'risks')}：**", bullet_list(conclusion["risks"]), ""]
        if conclusion.get("open_questions"):
            lines += [f"**{label(lang, 'open')}：**", bullet_list(conclusion["open_questions"]), ""]

    if data.get("sources"):
        lines += [f"## {label(lang, 'sources')}", "", bullet_list(data["sources"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to analysis JSON")
    parser.add_argument("--output", required=True, help="Path to output Markdown")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
        if "title" not in data or not isinstance(data.get("dimensions", data.get("lenses", [])), list):
            raise ValueError("JSON must contain 'title' and a list of 'lenses' or 'dimensions'")
        markdown = render(data)
        Path(args.output).write_text(markdown, encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Report written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
