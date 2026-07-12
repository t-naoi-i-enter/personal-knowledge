"""RSS収集: config/sources.yaml の情報源を取得し data/raw/ へ保存する(設計書13.3・14.2)

- 取得失敗はエラーで止めず failures として記録する(設計書8.1「リンク切れや取得失敗を明示」)
- sources/blocked.yaml に載っている情報源は取得しない(本人承認済みの除外)
"""

from __future__ import annotations

import sys

import feedparser
import httpx

from scripts.common import load_yaml, now_jst, save_json, today_stamp

FETCH_TIMEOUT_SECONDS = 20
USER_AGENT = "personal-knowledge-os/0.1 (+https://github.com/)"


def is_blocked(source: dict, blocked_cfg: dict | None) -> bool:
    entries = (blocked_cfg or {}).get("blocked") or []
    return any(
        source.get("name") == b.get("name") or source.get("url") == b.get("url")
        for b in entries
    )


def parse_feed(content: str | bytes, source: dict) -> list[dict]:
    """フィード本文を記事レコード(生)へ変換する。出典メタデータを引き継ぐ。"""
    feed = feedparser.parse(content)
    articles = []
    for entry in feed.entries:
        link = entry.get("link")
        if not link:
            continue
        articles.append(
            {
                "title": entry.get("title", ""),
                "url": link,
                "summary": entry.get("summary", ""),
                "published": entry.get("published") or entry.get("updated") or None,
                "author": entry.get("author"),
                "publisher": source["name"],
                "category": source.get("category"),
                "priority": source.get("priority", "medium"),
                "source_type": source.get("source_type", "unknown"),
                "language": source.get("language", "unknown"),
                "retrieval_status": "success",
            }
        )
    return articles


def fetch_source(source: dict, client: httpx.Client) -> list[dict]:
    response = client.get(source["url"])
    response.raise_for_status()
    # bytesのまま渡し、XML宣言のencodingをfeedparserに解釈させる
    # (response.textはHTTPヘッダにcharsetがないとUTF-8決め打ちになる)
    return parse_feed(response.content, source)


def collect(sources: list[dict], blocked_cfg: dict | None) -> tuple[list[dict], list[dict]]:
    articles: list[dict] = []
    failures: list[dict] = []
    with httpx.Client(
        timeout=FETCH_TIMEOUT_SECONDS,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        for source in sources:
            if not source.get("enabled", True) or is_blocked(source, blocked_cfg):
                continue
            try:
                fetched = fetch_source(source, client)
                articles.extend(fetched)
                print(f"  {source['name']}: {len(fetched)} 件")
            except Exception as e:  # 個別の取得失敗で全体を止めない
                failures.append(
                    {"name": source["name"], "url": source["url"], "error": str(e)}
                )
                print(f"  {source['name']}: 取得失敗 ({e})")
    return articles, failures


def main() -> int:
    sources = (load_yaml("config/sources.yaml") or {}).get("sources") or []
    blocked_cfg = load_yaml("sources/blocked.yaml")
    print(f"{len(sources)} ソースから収集します。")
    articles, failures = collect(sources, blocked_cfg)
    stamp = today_stamp()
    path = save_json(
        f"data/raw/articles-{stamp}.json",
        {
            "collected_at": now_jst().isoformat(),
            "articles": articles,
            "failures": failures,
        },
    )
    print(f"合計 {len(articles)} 件(失敗 {len(failures)} ソース)→ {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
