"""正規化: data/raw の収集結果を出典メタデータ付きの記事レコードへ整える(設計書8.5・14.2)

- URL正規化(トラッキングパラメータ・フラグメント除去)
- 日付のISO化(python-dateutil)
- 概要のHTML除去と要約長の制限(トークン削減、設計書14.4)
- content_hash生成(重複判定用)
"""

from __future__ import annotations

import hashlib
import html
import re
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dateutil import parser as date_parser
from pydantic import BaseModel, Field

from scripts.common import load_json, now_jst, save_json, today_stamp

SUMMARY_MAX_CHARS = 500
TRACKING_PARAMS = {"fbclid", "gclid", "igshid", "mc_cid", "mc_eid", "ref_src", "cmpid"}


class Article(BaseModel):
    """記事レコード(設計書8.5の出典データモデル+パイプライン拡張)"""

    source_id: str
    title: str
    url: str
    publisher: str = "unknown"
    author: str | None = None
    published_at: str | None = None
    event_date: str | None = None
    collected_at: str
    source_type: str = "unknown"
    language: str = "unknown"
    content_hash: str
    retrieval_status: str = "success"
    summary: str = ""
    category: str | None = None
    priority: str = "medium"
    topics: list[str] = Field(default_factory=list)
    scores: dict[str, int] = Field(default_factory=dict)
    total_score: float = 0.0
    must_include: bool = False


def normalize_url(url: str) -> str:
    """スキーム・ホストの小文字化、フラグメントとトラッキングパラメータの除去、末尾スラッシュ除去"""
    scheme, netloc, path, query, _fragment = urlsplit(url.strip())
    params = [
        (k, v)
        for k, v in parse_qsl(query, keep_blank_values=True)
        if not k.startswith("utm_") and k not in TRACKING_PARAMS
    ]
    if path.endswith("/") and path != "/":
        path = path.rstrip("/")
    return urlunsplit((scheme.lower(), netloc.lower(), path, urlencode(params), ""))


def parse_date(value: str | None) -> str | None:
    """任意形式の日時文字列を YYYY-MM-DD へ。解釈できない場合は None(断定しない)"""
    if not value:
        return None
    try:
        return date_parser.parse(value).date().isoformat()
    except (ValueError, OverflowError):
        return None


def clean_text(text: str) -> str:
    """HTMLタグ除去・実体参照の復元・空白の圧縮"""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def content_hash(title: str, summary: str) -> str:
    """タイトル+概要の空白正規化済みハッシュ(重複判定用、設計書14.4)"""
    normalized = re.sub(r"\s+", " ", f"{title} {summary}").strip().lower()
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def normalize_articles(
    raw_articles: list[dict], collected_at: str, date_stamp: str
) -> list[dict]:
    """収集済みの生記事を正規化済みレコードのリストへ変換する"""
    out: list[dict] = []
    for raw in raw_articles:
        title = clean_text(raw.get("title") or "")
        url = (raw.get("url") or "").strip()
        if not title or not url:
            continue
        summary = clean_text(raw.get("summary") or "")[:SUMMARY_MAX_CHARS]
        article = Article(
            source_id=f"src_{date_stamp}_{len(out) + 1:03d}",
            title=title,
            url=normalize_url(url),
            publisher=raw.get("publisher") or "unknown",
            author=raw.get("author"),
            published_at=parse_date(raw.get("published")),
            collected_at=collected_at,
            source_type=raw.get("source_type") or "unknown",
            language=raw.get("language") or "unknown",
            content_hash=content_hash(title, summary),
            retrieval_status=raw.get("retrieval_status") or "success",
            summary=summary,
            category=raw.get("category"),
            priority=raw.get("priority") or "medium",
        )
        out.append(article.model_dump())
    return out


def main() -> int:
    stamp = today_stamp()
    raw = load_json(f"data/raw/articles-{stamp}.json")
    if raw is None:
        print(f"data/raw/articles-{stamp}.json がありません。先に collect.py を実行してください。")
        return 1
    articles = normalize_articles(raw.get("articles", []), now_jst().isoformat(), stamp)
    path = save_json(f"data/processed/normalized-{stamp}.json", {"articles": articles})
    print(f"{len(articles)} 件を正規化 → {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
