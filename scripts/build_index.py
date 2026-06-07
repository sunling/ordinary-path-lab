#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = SYSTEM_ROOT / "01-source-index"
RECORD_DIRS = [
    SYSTEM_ROOT / "02-normalized",
    SYSTEM_ROOT / "03-issue-units",
    SYSTEM_ROOT / "04-topic-clusters",
    SYSTEM_ROOT / "05-outputs",
    SYSTEM_ROOT / "06-article-drafts",
]
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_scalar(value: str):
    value = value.strip()
    if value == "":
        return ""
    if value in {"[]", "null", "None"}:
        return []
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = {}
    current_key = None
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip():
            continue
        if raw_line.startswith("  - ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(parse_scalar(raw_line[4:]))
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "[]":
            data[key] = []
        elif value == "":
            data[key] = ""
            current_key = key
        else:
            data[key] = parse_scalar(value)
            current_key = key
    return data


def as_list(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [str(value)]


def record_rows() -> list[dict]:
    rows = []
    for record_dir in RECORD_DIRS:
        if not record_dir.exists():
            continue
        for path in sorted(record_dir.rglob("*.md")):
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
            if not data:
                continue
            rel = path.relative_to(SYSTEM_ROOT)
            record_kind = rel.parts[0]
            rows.append(
                {
                    "id": data.get("id", ""),
                    "kind": record_kind,
                    "record_type": data.get("record_type", ""),
                    "title": data.get("title", ""),
                    "primary_theme": data.get("primary_theme", ""),
                    "tags": ", ".join(as_list(data.get("tags"))),
                    "layers": ", ".join(as_list(data.get("layers"))),
                    "status": data.get("status", ""),
                    "privacy_level": data.get("privacy_level", ""),
                    "source_path": data.get("source_path", ""),
                    "source_consult_id": data.get("source_consult_id", ""),
                    "record_path": str(rel),
                }
            )
    return rows


def write_csv(rows: list[dict]) -> None:
    out = INDEX_DIR / "records.csv"
    fieldnames = [
        "id",
        "kind",
        "record_type",
        "title",
        "primary_theme",
        "tags",
        "layers",
        "privacy_level",
        "status",
        "source_path",
        "source_consult_id",
        "record_path",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict]) -> None:
    out = INDEX_DIR / "records.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(rows: list[dict]) -> None:
    out = INDEX_DIR / "records.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 咨询整理记录索引",
        "",
        f"Generated: {now}",
        "",
        "| id | kind | title | primary_theme | layers | status | record_path |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {id} | {kind} | {title} | {primary_theme} | {layers} | {status} | {record_path} |".format(**row)
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_stats(rows: list[dict]) -> None:
    out = INDEX_DIR / "stats.md"
    by_kind = Counter(row["kind"] for row in rows if row["kind"])
    by_record_type = Counter(row["record_type"] for row in rows if row["record_type"])
    by_theme = Counter(row["primary_theme"] for row in rows if row["primary_theme"])
    by_layer = Counter(layer for row in rows for layer in as_list(row["layers"]))
    by_tag = Counter(tag for row in rows for tag in as_list(row["tags"]))
    sections = [
        ("kind", by_kind),
        ("record_type", by_record_type),
        ("primary_theme", by_theme),
        ("layers", by_layer),
        ("tags", by_tag),
    ]
    lines = ["# 咨询整理记录统计", ""]
    for title, counter in sections:
        lines.extend([f"## {title}", ""])
        if not counter:
            lines.append("- 暂无")
        else:
            for key, count in counter.most_common():
                lines.append(f"- {key}: {count}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    rows = record_rows()
    write_csv(rows)
    write_json(rows)
    write_markdown(rows)
    write_stats(rows)
    print(f"Indexed {len(rows)} records")


if __name__ == "__main__":
    main()
