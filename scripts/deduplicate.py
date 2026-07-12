"""重複除去: URL・content_hash・タイトル類似(rapidfuzz)で既出記事を除外する(設計書14.2)

履歴は data/history/seen.json に保持し、GitHub Actions がコミットすることで
「既読判定・分析済み判定」を実現する(Phase 2 で SQLite へ移行予定)。
"""

from __future__ import annotations

import sys

from rapidfuzz import fuzz, process

from scripts.common import load_json, save_json, today_stamp

# token_set_ratio がこれ以上なら同一記事とみなす。
# 転載時のタイトルは「〜 | メディア名」のような接尾辞が付くことが多く、
# 単純な fuzz.ratio では検出できないためトークンベースで比較する。
TITLE_SIMILARITY_THRESHOLD = 95
MAX_TITLE_HISTORY = 3000  # タイトル類似判定に使う履歴の上限(古いものから破棄)
HISTORY_PATH = "data/history/seen.json"


def empty_history() -> dict:
    return {"urls": {}, "hashes": {}, "titles": {}}


def _is_duplicate_title(title: str, known_titles: list[str]) -> bool:
    if not known_titles:
        return False
    match = process.extractOne(
        title, known_titles, scorer=fuzz.token_set_ratio, score_cutoff=TITLE_SIMILARITY_THRESHOLD
    )
    return match is not None


def dedupe(articles: list[dict], history: dict, today: str) -> tuple[list[dict], dict]:
    """新規記事のみを返し、履歴を更新して返す。バッチ内の重複も除去する。"""
    urls = dict(history.get("urls", {}))
    hashes = dict(history.get("hashes", {}))
    titles = dict(history.get("titles", {}))

    new_articles: list[dict] = []
    for article in articles:
        url = article["url"]
        chash = article["content_hash"]
        title_key = article["title"].strip().lower()
        if url in urls or chash in hashes:
            continue
        if _is_duplicate_title(title_key, list(titles.keys())):
            continue
        new_articles.append(article)
        urls[url] = today
        hashes[chash] = today
        titles[title_key] = today

    if len(titles) > MAX_TITLE_HISTORY:
        # 記録日昇順で古いタイトルから破棄(URL・ハッシュ履歴は保持)
        keep = sorted(titles.items(), key=lambda kv: kv[1])[-MAX_TITLE_HISTORY:]
        titles = dict(keep)

    return new_articles, {"urls": urls, "hashes": hashes, "titles": titles}


def main() -> int:
    stamp = today_stamp()
    data = load_json(f"data/processed/normalized-{stamp}.json")
    if data is None:
        print(f"data/processed/normalized-{stamp}.json がありません。先に normalize.py を実行してください。")
        return 1
    history = load_json(HISTORY_PATH, default=empty_history())
    today = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:]}"
    new_articles, history = dedupe(data.get("articles", []), history, today)
    save_json(HISTORY_PATH, history)
    path = save_json(f"data/processed/deduped-{stamp}.json", {"articles": new_articles})
    print(f"新規 {len(new_articles)} 件 → {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
