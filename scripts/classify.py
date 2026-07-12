"""キーワード分類: config/topics.yaml のキーワードで記事にトピックを付与する(設計書14.2)

AIは使わない機械的分類。どのトピックにも該当しない記事は "uncategorized" となり、
score.py で低スコアになって足切りされる。
"""

from __future__ import annotations

import re
import sys

from scripts.common import load_json, load_yaml, save_json, today_stamp


def _keyword_pattern(keyword: str) -> re.Pattern:
    """英数字キーワードは語境界付きで照合する("mcp" が "pmcportal" に誤マッチしないように)。
    日本語などの非ASCIIキーワードは部分一致。"""
    kw = keyword.lower()
    escaped = re.escape(kw)
    prefix = r"(?<![a-z0-9])" if re.match(r"[a-z0-9]", kw) else ""
    suffix = r"(?![a-z0-9])" if re.match(r"[a-z0-9]", kw[-1]) else ""
    return re.compile(prefix + escaped + suffix)


def classify_article(article: dict, topics_cfg: dict) -> dict:
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    topics = []
    for name, topic in topics_cfg.get("topics", {}).items():
        if any(_keyword_pattern(kw).search(text) for kw in topic.get("keywords", [])):
            topics.append(name)
    article["topics"] = topics or ["uncategorized"]
    return article


def main() -> int:
    stamp = today_stamp()
    data = load_json(f"data/processed/deduped-{stamp}.json")
    if data is None:
        print(f"data/processed/deduped-{stamp}.json がありません。先に deduplicate.py を実行してください。")
        return 1
    topics_cfg = load_yaml("config/topics.yaml")
    articles = [classify_article(a, topics_cfg) for a in data.get("articles", [])]
    path = save_json(f"data/processed/classified-{stamp}.json", {"articles": articles})
    categorized = sum(1 for a in articles if a["topics"] != ["uncategorized"])
    print(f"{len(articles)} 件を分類(トピック該当 {categorized} 件)→ {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
