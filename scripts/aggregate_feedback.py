"""フィードバック集計: feedback/structured/ を機械集計しレポート品質指標を出す(設計書11章)

AIを使わない件数集計のみ(設計書14.2)。傾向の解釈・改善提案は /feedback-analyzer が行う。
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from scripts.common import ROOT, save_json, save_text, today_stamp

USEFUL_LABELS = {"important", "useful", "insightful", "actionable", "well_connected"}
NOISE_LABELS = {"not_relevant", "already_known"}
ACTION_ADOPTED = {"will_do", "already_doing"}


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 3) if denominator else 0.0


def compute_metrics(feedbacks: list[dict]) -> dict:
    useful_count = 0
    noise_count = 0
    action_proposals = 0
    action_adopted = 0
    by_topic: dict[str, dict[str, int]] = {}

    for fb in feedbacks:
        labels = set(fb.get("labels") or [])
        is_useful = bool(labels & USEFUL_LABELS)
        is_noise = bool(labels & NOISE_LABELS)
        useful_count += is_useful
        noise_count += is_noise

        topic = (fb.get("topic") or {}).get("primary") or "unknown"
        tally = by_topic.setdefault(topic, {"items": 0, "useful": 0, "noise": 0})
        tally["items"] += 1
        tally["useful"] += is_useful
        tally["noise"] += is_noise

        status = (fb.get("action_feedback") or {}).get("status")
        if status:
            action_proposals += 1
            action_adopted += status in ACTION_ADOPTED

    total = len(feedbacks)
    return {
        "total_items": total,
        "useful_count": useful_count,
        "noise_count": noise_count,
        "action_proposals": action_proposals,
        "action_adopted": action_adopted,
        "useful_item_rate": _rate(useful_count, total),
        "noise_rate": _rate(noise_count, total),
        "action_conversion_rate": _rate(action_adopted, action_proposals),
        "by_topic": by_topic,
    }


def load_structured_feedback(directory: Path) -> list[dict]:
    feedbacks = []
    for path in sorted(directory.glob("*.yaml")) + sorted(directory.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            feedbacks.append(data)
        elif isinstance(data, list):
            feedbacks.extend(d for d in data if isinstance(d, dict))
    return feedbacks


def render_markdown(metrics: dict, stamp: str) -> str:
    lines = [
        f"# レポート品質指標 {stamp}",
        "",
        f"- 集計対象: {metrics['total_items']} 件",
        f"- Useful Item Rate: {metrics['useful_item_rate']}(有益 {metrics['useful_count']} 件)",
        f"- Noise Rate: {metrics['noise_rate']}(不要・既知 {metrics['noise_count']} 件)",
        f"- Action Conversion Rate: {metrics['action_conversion_rate']}"
        f"(採用 {metrics['action_adopted']} / 提案 {metrics['action_proposals']})",
        "",
        "## テーマ別",
        "",
    ]
    for topic, tally in metrics["by_topic"].items():
        lines.append(
            f"- {topic}: {tally['items']} 件(有益 {tally['useful']} / 不要 {tally['noise']})"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    feedbacks = load_structured_feedback(ROOT / "feedback" / "structured")
    metrics = compute_metrics(feedbacks)
    stamp = today_stamp()
    save_json(f"feedback/metrics/metrics-{stamp}.json", metrics)
    save_text(f"feedback/metrics/metrics-{stamp}.md", render_markdown(metrics, stamp))
    print(
        f"{metrics['total_items']} 件を集計: useful={metrics['useful_item_rate']} "
        f"noise={metrics['noise_rate']} action={metrics['action_conversion_rate']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
