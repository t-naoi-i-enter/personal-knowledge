"""パイプライン共通ユーティリティ(設定・入出力・日時)"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
JST = timezone(timedelta(hours=9), name="JST")


def load_yaml(path: Path | str) -> Any:
    with open(ROOT / path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path | str, default: Any = None) -> Any:
    p = ROOT / path
    if not p.exists():
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path | str, data: Any) -> Path:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return p


def save_text(path: Path | str, text: str) -> Path:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


def now_jst() -> datetime:
    return datetime.now(JST)


def today_stamp(now: datetime | None = None) -> str:
    """JSTの日付スタンプ(YYYYMMDD)。ファイル名・source_idに使用する。"""
    return (now or now_jst()).strftime("%Y%m%d")
