"""new_articles 出力: スコア足切り・件数制限をかけ、Claudeが読む入力を生成する(設計書14.1)

- data/new/new_articles.json : /morning-brief がこれだけを読む(トークン削減)
- data/new/new_articles.md   : 人間が中身を目視確認するためのダイジェスト
"""

from __future__ import annotations

import sys

from scripts.common import load_json, load_yaml, now_jst, save_json, save_text, today_stamp


def select_articles(articles: list[dict], cfg: dict) -> list[dict]:
    """しきい値未満を除外(must_includeは残す)し、must_include優先・スコア降順で
    最大 max_export_items 件に絞る。must_include は件数制限でも落とさない。"""
    threshold = cfg["publish_threshold"]
    max_items = cfg["max_export_items"]

    critical = [a for a in articles if a.get("must_include")]
    normal = [
        a for a in articles if not a.get("must_include") and a["total_score"] >= threshold
    ]
    critical.sort(key=lambda a: a["total_score"], reverse=True)
    normal.sort(key=lambda a: a["total_score"], reverse=True)

    remaining = max(0, max_items - len(critical))
    return critical + normal[:remaining]


def render_markdown(articles: list[dict], date_str: str) -> str:
    lines = [
        f"# 新着記事ダイジェスト {date_str}",
        "",
        f"候補 {len(articles)}件。Daily Brief の生成は Claude Code で `/morning-brief` を実行する。",
        "",
    ]
    for a in articles:
        flag = "🚨 " if a.get("must_include") else ""
        lines += [
            f"## {flag}{a['title']}",
            "",
            f"- URL: {a['url']}",
            f"- 発行元: {a['publisher']}(種別: {a.get('source_type', 'unknown')})",
            f"- 公開日: {a.get('published_at') or '不明'}",
            f"- トピック: {', '.join(a.get('topics', []))}",
            f"- 総合スコア: {a['total_score']}",
            "",
            a.get("summary", ""),
            "",
        ]
    return "\n".join(lines)


def main() -> int:
    stamp = today_stamp()
    data = load_json(f"data/processed/scored-{stamp}.json")
    if data is None:
        print(f"data/processed/scored-{stamp}.json がありません。先に score.py を実行してください。")
        return 1
    cfg = load_yaml("config/scoring.yaml")
    selected = select_articles(data.get("articles", []), cfg)
    date_str = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:]}"
    json_path = save_json(
        "data/new/new_articles.json",
        {
            "generated_at": now_jst().isoformat(),
            "date": date_str,
            "count": len(selected),
            "articles": selected,
        },
    )
    save_text("data/new/new_articles.md", render_markdown(selected, date_str))
    print(f"{len(selected)} 件を出力 → {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
