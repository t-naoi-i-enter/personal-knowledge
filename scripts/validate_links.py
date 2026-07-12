"""リンク検証: reports/ 配下のMarkdownに含まれるURLの生存確認(設計書8.1・13.2)

出典のリンク切れを検出して明示する。壊れたリンクがあっても exit 0 とし、
結果は標準出力と data/history/link-check-YYYYMMDD.md に残す。
"""

from __future__ import annotations

import re
import sys

import httpx

from scripts.common import ROOT, save_text, today_stamp

URL_PATTERN = re.compile(r"https?://[^\s)\]>\"'`]+")
TRAILING_PUNCTUATION = ".,;:!?。、"
CHECK_TIMEOUT_SECONDS = 15


def extract_urls(markdown_text: str) -> list[str]:
    """Markdown本文からURLを抽出する(順序保持・重複除去・末尾の句読点除去)"""
    urls: list[str] = []
    for match in URL_PATTERN.findall(markdown_text or ""):
        url = match.rstrip(TRAILING_PUNCTUATION)
        if url and url not in urls:
            urls.append(url)
    return urls


def check_url(url: str, client: httpx.Client) -> tuple[bool, str]:
    try:
        response = client.head(url)
        if response.status_code in (405, 403, 501):  # HEAD非対応サイトはGETで再確認
            response = client.get(url)
        ok = response.status_code < 400
        return ok, str(response.status_code)
    except Exception as e:
        return False, type(e).__name__


def main() -> int:
    reports = sorted((ROOT / "reports").rglob("*.md"))
    url_locations: dict[str, list[str]] = {}
    for report in reports:
        for url in extract_urls(report.read_text(encoding="utf-8")):
            url_locations.setdefault(url, []).append(
                report.relative_to(ROOT).as_posix()
            )

    print(f"{len(reports)} レポートから {len(url_locations)} URLを確認します。")
    broken: list[tuple[str, str, list[str]]] = []
    with httpx.Client(
        timeout=CHECK_TIMEOUT_SECONDS,
        follow_redirects=True,
        headers={"User-Agent": "personal-knowledge-os/0.1 link-checker"},
    ) as client:
        for url, locations in url_locations.items():
            ok, status = check_url(url, client)
            if not ok:
                broken.append((url, status, locations))
                print(f"  NG [{status}] {url}")

    stamp = today_stamp()
    lines = [f"# リンク確認 {stamp}", "", f"- 確認URL数: {len(url_locations)}", f"- リンク切れ: {len(broken)}", ""]
    for url, status, locations in broken:
        lines.append(f"- [{status}] {url}(使用箇所: {', '.join(locations)})")
    save_text(f"data/history/link-check-{stamp}.md", "\n".join(lines) + "\n")
    print(f"リンク切れ {len(broken)} 件。結果 → data/history/link-check-{stamp}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
