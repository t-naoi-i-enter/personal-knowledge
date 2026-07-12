"""静的サイト生成: reports/ と feedback/ 等を GitHub Pages 用HTMLへ変換する

レポート(Daily/Weekly/Monthly/Deep Dive)を閲覧ページにし、
feedback/structured/ の本人コメントを「朱入れ」として各レポートに添える。
仮説・アクション・意思決定の現況をインデックスに表示する。

出力先は _site/(gitignore対象)。デプロイは .github/workflows/pages.yml が行う。
"""

from __future__ import annotations

import html
import re
import shutil
import sys

import markdown as md_lib
import yaml

from scripts.common import ROOT, now_jst

OUTPUT_DIR = ROOT / "_site"
STYLE_SRC = ROOT / "site" / "style.css"
REPO_BLOB_URL = "https://github.com/t-naoi-i-enter/personal-knowledge/blob/main/"

REPORT_TYPES = {
    "daily": {"label": "Daily Brief", "kanji": "日"},
    "weekly": {"label": "Weekly CEO Brief", "kanji": "週"},
    "monthly": {"label": "Monthly Review", "kanji": "月"},
    "deep-dive": {"label": "Deep Dive", "kanji": "深"},
}

GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500'
    "&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Zen+Old+Mincho:wght@600;700;900"
    '&display=swap" rel="stylesheet">'
)

# 朱印風ファビコン(タブで目立つ「知」の印)
FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect x='2' y='2' width='28' height='28' rx='6' fill='%23B3402A'/%3E"
    "%3Ctext x='16' y='23' font-family='serif' font-size='18' font-weight='bold' "
    "fill='%23fff' text-anchor='middle'%3E知%3C/text%3E%3C/svg%3E\">"
)

# ストロークアイコン(feather系、currentColorで着色)
_SVG = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
ICONS = {
    # 仮説 = 羅針盤(探索・検証)
    "hypotheses": _SVG.format(
        '<circle cx="12" cy="12" r="10"/>'
        '<polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88"/>'
    ),
    # アクション = 実行の矢印
    "actions": _SVG.format(
        '<circle cx="12" cy="12" r="10"/><polyline points="12 16 16 12 12 8"/>'
        '<line x1="8" y1="12" x2="16" y2="12"/>'
    ),
    # 意思決定 = 分岐
    "decisions": _SVG.format(
        '<line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/>'
        '<circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>'
    ),
    # 朱入れ = 筆
    "brush": _SVG.format(
        '<path d="M12 20h9"/>'
        '<path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>'
    ),
}

LOGO_SEAL = (
    '<svg class="logo-seal" viewBox="0 0 32 32" aria-hidden="true">'
    '<rect x="1.5" y="1.5" width="29" height="29" rx="6" fill="#B3402A"/>'
    '<text x="16" y="23" font-size="17" font-weight="700" fill="#fff" '
    'text-anchor="middle" style="font-family: \'Zen Old Mincho\', serif;">知</text></svg>'
)

_DATE_PREFIX = re.compile(r"^(\d{4}-W?\d{2}(?:-\d{2})?)")


# ── 解析 ──────────────────────────────────────────────


def parse_report(path, report_type: str) -> dict:
    text = path.read_text(encoding="utf-8")
    stem = path.stem
    title = stem
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    m = _DATE_PREFIX.match(stem)
    return {
        "type": report_type,
        "date": m.group(1) if m else "",
        "stem": stem,
        "title": title,
        "body_md": text,
    }


def match_feedback(report: dict, feedbacks: list[dict]) -> list[dict]:
    """report_type と report_date(YAMLではdate型になりうる)でレポートに紐付ける"""
    return [
        fb
        for fb in feedbacks
        if fb.get("report_type") == report["type"]
        and str(fb.get("report_date") or "") == report["date"]
    ]


def parse_yaml_doc(text: str):
    """仮説・アクション・意思決定ファイル(```yaml フェンス付きMarkdown)をdictにする"""
    body = text.strip()
    if body.startswith("```"):
        lines = body.splitlines()
        lines = [ln for ln in lines if not ln.startswith("```")]
        body = "\n".join(lines)
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


# ── レンダリング ──────────────────────────────────────


def render_markdown_body(md_text: str) -> str:
    return md_lib.markdown(md_text, extensions=["extra", "sane_lists"])


def rewrite_relative_links(html_text: str) -> str:
    """レポート間の相対 .md リンクは .html へ、リポジトリ内ファイルへのリンクはGitHubへ"""
    html_text = re.sub(
        r'href="\.\./(daily|weekly|monthly|deep-dive)/([^"]+)\.md"',
        r'href="../\1/\2.html"',
        html_text,
    )
    html_text = re.sub(
        r'href="\.\./\.\./([^"]+)"',
        lambda m: f'href="{REPO_BLOB_URL}{m.group(1)}"',
        html_text,
    )
    return html_text


def _esc(value) -> str:
    return html.escape(str(value)) if value is not None else ""


def _page(title: str, body: str, css_href: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(title)}</title>
{FAVICON}
{GOOGLE_FONTS}
<link rel="stylesheet" href="{css_href}">
</head>
<body>
{body}
<footer class="site-footer"><div class="wrap">Personal Knowledge OS — 自分専用の Chief of Staff。出典のない情報は掲載しない。</div></footer>
</body>
</html>
"""


def _header(root_prefix: str, active: str = "") -> str:
    stamp = now_jst().strftime("%Y-%m-%d %H:%M JST")
    links = [
        ("index.html", "レポート", "index"),
        ("focus.html", "関心事", "focus"),
        ("lens.html", "収集の観点", "lens"),
    ]
    nav = "".join(
        f'<a href="{root_prefix}{href}"{" class=\"active\"" if key == active else ""}>{label}</a>'
        for href, label, key in links
    )
    return (
        '<header class="site-header"><div class="wrap">'
        f'<a class="brand" href="{root_prefix}index.html">{LOGO_SEAL}'
        '<span class="brand-text"><span class="site-title">Personal Knowledge OS</span>'
        '<span class="site-tagline">朝のブリーフィングデスク — レポートと朱入れの記録</span></span></a>'
        f'<nav class="site-nav">{nav}</nav>'
        f'<span class="build-stamp">build {stamp}</span>'
        "</div></header>"
    )


def _feedback_cards(feedbacks: list[dict]) -> str:
    if not feedbacks:
        return '<p class="fb-empty">このレポートへのフィードバックはまだありません。読了後に /report-feedback で記録できます。</p>'
    cards = []
    for fb in feedbacks:
        labels = "".join(
            f'<span class="fb-label">{_esc(label)}</span>' for label in fb.get("labels") or []
        )
        section = (
            f'<span class="fb-section">{_esc(fb["section_id"])}</span>'
            if fb.get("section_id")
            else ""
        )
        cards.append(
            '<div class="fb-card">'
            f'<div class="fb-meta"><span class="fb-id">{_esc(fb.get("feedback_id"))}</span>{section}</div>'
            f'<p class="fb-comment">{_esc((fb.get("user_comment") or "").strip())}</p>'
            f'<div class="fb-labels">{labels}</div>'
            "</div>"
        )
    return "".join(cards)


def build_report_page(report: dict, feedbacks: list[dict]) -> str:
    info = REPORT_TYPES[report["type"]]
    body_html = rewrite_relative_links(render_markdown_body(report["body_md"]))
    matched = match_feedback(report, feedbacks) if feedbacks else []
    # 呼び出し側が絞り込み済みリストを渡す場合もあるため、一致ゼロなら渡された全件を使う
    shown = matched or feedbacks
    body = f"""{_header("../../", active="index")}
<main class="wrap">
<nav class="crumbs"><a href="../../index.html">← レポート一覧へ戻る</a></nav>
<div class="report-header">
  <div class="meta">
    <span class="seal" title="{_esc(info["label"])}">{info["kanji"]}</span>
    <span class="date-chip">{_esc(report["date"] or report["stem"])}</span>
    <span class="id-chip">{_esc(info["label"])}</span>
  </div>
  <h1>{_esc(report["title"])}</h1>
</div>
<div class="report-layout">
  <article class="report-body">{body_html}</article>
  <aside class="fb-panel">
    <h2>{ICONS["brush"]} 朱入れ — 本人コメント</h2>
    {_feedback_cards(shown)}
  </aside>
</div>
</main>"""
    return _page(report["title"], body, "../../style.css")


def _report_list_items(reports: list[dict]) -> str:
    items = []
    for r in reports:
        fb = (
            f'<span class="fb-count">朱 {r["feedback_count"]}</span>'
            if r.get("feedback_count")
            else ""
        )
        items.append(
            f'<li><a class="report-link" href="reports/{r["type"]}/{_esc(r["stem"])}.html">'
            f'<span class="date-chip">{_esc(r["date"] or r["stem"])}</span>'
            f'<span class="title">{_esc(r["title"])}</span>{fb}</a></li>'
        )
    return "".join(items)


def _rail_items(entries: list[dict], id_key: str, text_of) -> str:
    if not entries:
        return '<div class="empty-note">まだありません</div>'
    rows = []
    for e in entries:
        status = _esc(e.get("status") or "")
        rows.append(
            '<div class="rail-item">'
            f'<span class="status status-{status}">{status}</span>'
            f'<span class="fb-id">{_esc(e.get(id_key))}</span><br>{_esc(text_of(e))}'
            "</div>"
        )
    return "".join(rows)


def build_index_page(reports: list[dict], extras: dict) -> str:
    reports = sorted(reports, key=lambda r: (r["date"], r["stem"]), reverse=True)
    hero_html = ""
    if reports:
        latest = reports[0]
        info = REPORT_TYPES[latest["type"]]
        fb = (
            f'<span class="fb-count">朱入れ {latest["feedback_count"]}件</span>'
            if latest.get("feedback_count")
            else ""
        )
        hero_html = f"""<div class="hero">
<p class="hero-eyebrow">LATEST BRIEF</p>
<a class="hero-card" href="reports/{latest["type"]}/{_esc(latest["stem"])}.html" data-kanji="{info["kanji"]}">
  <div class="hero-meta"><span class="seal">{info["kanji"]}</span>
  <span class="date-chip">{_esc(latest["date"])}</span>{fb}</div>
  <h2>{_esc(latest["title"])}</h2>
</a></div>"""

    sections = []
    for rtype, info in REPORT_TYPES.items():
        of_type = [r for r in reports if r["type"] == rtype]
        body = (
            f'<ul class="report-list">{_report_list_items(of_type)}</ul>'
            if of_type
            else '<div class="empty-note">まだありません</div>'
        )
        sections.append(
            f'<div class="section-title"><span class="seal">{info["kanji"]}</span>'
            f'{_esc(info["label"])} <span class="section-count">{len(of_type)}件</span></div>{body}'
        )

    rail = f"""<div class="rail-panel"><h3>{ICONS["hypotheses"]} HYPOTHESES — 仮説</h3>
{_rail_items(extras.get("hypotheses") or [], "hypothesis_id", lambda e: e.get("statement") or "")}</div>
<div class="rail-panel"><h3>{ICONS["actions"]} ACTIONS — アクション</h3>
{_rail_items(extras.get("actions") or [], "action_id", lambda e: (e.get("proposal") or {}).get("title") or "")}</div>
<div class="rail-panel"><h3>{ICONS["decisions"]} DECISIONS — 意思決定</h3>
{_rail_items(extras.get("decisions") or [], "decision_id", lambda e: e.get("title") or "")}</div>"""

    body = f"""{_header("", active="index")}
<main class="wrap">
{hero_html}
<div class="columns">
  <div>{"".join(sections)}</div>
  <aside>{rail}</aside>
</div>
</main>"""
    return _page("Personal Knowledge OS", body, "style.css")


def build_focus_page(focus_md: str, interests_md: str) -> str:
    """関心事ページ: self/current-focus.md と self/interests.md を並べる"""
    body = f"""{_header("", active="focus")}
<main class="wrap">
<div class="page-title"><h1>関心事</h1>
<p class="page-lead">日々の選別とレポート生成の基準になる、今の重点と関心の履歴。更新は本人承認制(evolution/proposed/ 経由)。</p></div>
<div class="columns">
  <article class="report-body">{render_markdown_body(focus_md)}</article>
  <article class="report-body">{render_markdown_body(interests_md)}</article>
</div>
</main>"""
    return _page("関心事 | Personal Knowledge OS", body, "style.css")


def _keyword_chips(keywords: list) -> str:
    return "".join(f'<span class="kw">{_esc(kw)}</span>' for kw in keywords if kw)


def build_lens_page(topics_cfg: dict, sources_cfg: dict, scoring_cfg: dict) -> str:
    """収集の観点ページ: テーマ・情報源・評価ルールを可視化する"""
    topic_cards = []
    for name, topic in (topics_cfg.get("topics") or {}).items():
        topic_cards.append(
            '<div class="topic-card">'
            '<div class="topic-head">'
            f'<span class="topic-label">{_esc(topic.get("label") or name)}</span>'
            f'<span class="id-chip">{_esc(name)}</span>'
            f'<span class="weight-chip">重み {_esc(topic.get("weight"))}</span>'
            f'<span class="date-chip">{_esc(topic.get("frequency"))}</span>'
            "</div>"
            f'<div class="kw-list">{_keyword_chips(topic.get("keywords") or [])}</div>'
            "</div>"
        )

    source_rows = []
    for src in (sources_cfg.get("sources") or []):
        enabled = src.get("enabled", True)
        state = "" if enabled else '<span class="status status-rejected">停止中</span>'
        source_rows.append(
            "<tr>"
            f'<td><a href="{_esc(src.get("url"))}">{_esc(src.get("name"))}</a> {state}</td>'
            f'<td class="mono">{_esc(src.get("category"))}</td>'
            f'<td class="mono">{_esc(src.get("priority"))}</td>'
            f'<td class="mono">{_esc(src.get("source_type"))}</td>'
            f'<td class="mono">{_esc(src.get("language"))}</td>'
            "</tr>"
        )

    weight_rows = "".join(
        f'<tr><td>{_esc(k)}</td><td class="mono">{_esc(v)}</td></tr>'
        for k, v in (scoring_cfg.get("weights") or {}).items()
    )
    must_chips = _keyword_chips(scoring_cfg.get("must_include_keywords") or [])

    body = f"""{_header("", active="lens")}
<main class="wrap">
<div class="page-title"><h1>収集の観点</h1>
<p class="page-lead">RSS収集の対象と、掲載可否を決めるルールベース評価(AIを使わない足切り)。変更は config/ で管理し、テーマの重みは本人承認制。</p></div>

<div class="section-title">収集テーマとキーワード <span class="section-count">config/topics.yaml</span></div>
{"".join(topic_cards)}

<div class="section-title">情報源 <span class="section-count">config/sources.yaml</span></div>
<div class="report-body lens-table"><table>
<thead><tr><th>情報源</th><th>テーマ</th><th>優先度</th><th>種別</th><th>言語</th></tr></thead>
<tbody>{"".join(source_rows)}</tbody></table></div>

<div class="section-title">評価の重み <span class="section-count">config/scoring.yaml</span></div>
<div class="columns">
<div class="report-body lens-table"><table>
<thead><tr><th>観点</th><th>重み</th></tr></thead><tbody>{weight_rows}</tbody></table>
<p class="page-lead">総合スコア {_esc(scoring_cfg.get("publish_threshold"))} 未満は掲載しない(重大情報を除く)。</p></div>
<div class="report-body"><h3>スコアに関係なく掲載する重大キーワード</h3>
<div class="kw-list kw-must">{must_chips}</div></div>
</div>
</main>"""
    return _page("収集の観点 | Personal Knowledge OS", body, "style.css")


# ── 収集と出力 ────────────────────────────────────────


def _load_feedbacks() -> list[dict]:
    feedbacks = []
    directory = ROOT / "feedback" / "structured"
    if not directory.exists():
        return feedbacks
    for path in sorted(directory.glob("*.yaml")) + sorted(directory.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            feedbacks.append(data)
    return feedbacks


def _load_yaml_dir(base: str) -> list[dict]:
    entries = []
    root = ROOT / base
    if not root.exists():
        return entries
    for path in sorted(root.rglob("*.md")):
        data = parse_yaml_doc(path.read_text(encoding="utf-8"))
        if data:
            data.setdefault("status", path.parent.name)
            entries.append(data)
    return entries


def main() -> int:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    shutil.copy(STYLE_SRC, OUTPUT_DIR / "style.css")

    feedbacks = _load_feedbacks()
    reports = []
    for rtype in REPORT_TYPES:
        for path in sorted((ROOT / "reports" / rtype).glob("*.md")):
            report = parse_report(path, rtype)
            matched = match_feedback(report, feedbacks)
            report["feedback_count"] = len(matched)
            out = OUTPUT_DIR / "reports" / rtype / f"{report['stem']}.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(build_report_page(report, matched), encoding="utf-8", newline="\n")
            reports.append(report)

    extras = {
        "hypotheses": _load_yaml_dir("hypotheses"),
        "actions": _load_yaml_dir("actions"),
        "decisions": _load_yaml_dir("decisions"),
    }
    (OUTPUT_DIR / "index.html").write_text(
        build_index_page(reports, extras), encoding="utf-8", newline="\n"
    )
    (OUTPUT_DIR / "focus.html").write_text(
        build_focus_page(
            (ROOT / "self" / "current-focus.md").read_text(encoding="utf-8"),
            (ROOT / "self" / "interests.md").read_text(encoding="utf-8"),
        ),
        encoding="utf-8",
        newline="\n",
    )
    (OUTPUT_DIR / "lens.html").write_text(
        build_lens_page(
            yaml.safe_load((ROOT / "config" / "topics.yaml").read_text(encoding="utf-8")),
            yaml.safe_load((ROOT / "config" / "sources.yaml").read_text(encoding="utf-8")),
            yaml.safe_load((ROOT / "config" / "scoring.yaml").read_text(encoding="utf-8")),
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"{len(reports)} レポート + index/focus/lens を生成 → {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
