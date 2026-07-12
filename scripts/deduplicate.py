"""重複除去: URL・content_hash・タイトル類似(rapidfuzz)で既出記事を除外する(設計書14.2)

履歴は data/history/seen.json に保持し、GitHub Actions がコミットすることで
「既読判定・分析済み判定」を実現する(Phase 2 で SQLite へ移行予定)。
"""

from __future__ import annotations

import sys
from datetime import date, timedelta

from rapidfuzz import fuzz, process

from scripts.common import load_json, save_json, today_stamp

# token_set_ratio がこれ以上なら同一記事とみなす。
# 転載時のタイトルは「〜 | メディア名」のような接尾辞が付くことが多く、
# 単純な fuzz.ratio では検出できないためトークンベースで比較する。
TITLE_SIMILARITY_THRESHOLD = 95
# ただし token_set_ratio はトークン部分集合("OpenAI" ⊂ 長いタイトル)でも100になるため、
# トークン数が少ないタイトルと、トークン数が大きく異なるペアには適用しない。
# 空白で分割できない日本語タイトルも対象外になるが、URL・ハッシュの重複判定は常に効く。
MIN_TOKENS_FOR_FUZZY = 3
MAX_TOKEN_COUNT_RATIO = 2.0
MAX_TITLE_HISTORY = 3000  # タイトル類似判定に使う履歴の上限(古いものから破棄)
HISTORY_RETENTION_DAYS = 365  # これより古い履歴は破棄(seen.jsonの無制限成長を防ぐ)
HISTORY_PATH = "data/history/seen.json"


def empty_history() -> dict:
    return {"urls": {}, "hashes": {}, "titles": {}}


def _is_duplicate_title(title: str, known_titles: list[str]) -> bool:
    token_count = len(title.split())
    if token_count < MIN_TOKENS_FOR_FUZZY:
        return False
    candidates = [
        t
        for t in known_titles
        if len(t.split()) >= MIN_TOKENS_FOR_FUZZY
        and 1 / MAX_TOKEN_COUNT_RATIO <= len(t.split()) / token_count <= MAX_TOKEN_COUNT_RATIO
    ]
    if not candidates:
        return False
    match = process.extractOne(
        title, candidates, scorer=fuzz.token_set_ratio, score_cutoff=TITLE_SIMILARITY_THRESHOLD
    )
    return match is not None


def _prune_old(entries: dict[str, str], cutoff: str) -> dict[str, str]:
    return {k: v for k, v in entries.items() if v >= cutoff}


def dedupe(articles: list[dict], history: dict, today: str) -> tuple[list[dict], dict]:
    """新規記事のみを返し、履歴を更新して返す。バッチ内の重複も除去する。"""
    cutoff = (date.fromisoformat(today) - timedelta(days=HISTORY_RETENTION_DAYS)).isoformat()
    urls = _prune_old(history.get("urls", {}), cutoff)
    hashes = _prune_old(history.get("hashes", {}), cutoff)
    titles = _prune_old(history.get("titles", {}), cutoff)

    new_articles: list[dict] = []
    for article in articles:
        url = article["url"]
        chash = article["content_hash"]
        title_key = article["title"].strip().lower()
        if url in urls or chash in hashes:
            # 重複でも日付を更新し(last_seen方式)、フィードに載り続ける記事が
            # 保持期限切れ後に新着として再出現しないようにする
            if url in urls:
                urls[url] = today
            if chash in hashes:
                hashes[chash] = today
            if title_key in titles:
                titles[title_key] = today
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
