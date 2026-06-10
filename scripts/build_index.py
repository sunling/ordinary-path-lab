#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
import sys
from datetime import datetime
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(SYSTEM_ROOT / "scripts"))
import build_people
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
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            content = value[1:-1].strip()
            return [v.strip().strip('"').strip("'") for v in content.split(",") if v.strip()]
        return [v.strip() for v in value.split(",") if v.strip()]
    return [str(value)]


def parse_additional_themes(text: str) -> list[str]:
    match = FRONTMATTER_RE.match(text)
    body = text[match.end():] if match else text
    heading_match = re.search(r"## 可进入的主题聚合\n+(.*?)(?:\n##|\Z)", body, re.S)
    if not heading_match:
        return []
    themes = []
    for line in heading_match.group(1).splitlines():
        line = line.strip()
        if line.startswith("-"):
            theme = line[1:].strip().strip('"').strip("'")
            if theme:
                themes.append(theme)
    return themes


def record_rows() -> list[dict]:
    rows = []
    for record_dir in RECORD_DIRS:
        if not record_dir.exists():
            continue
        for path in sorted(record_dir.rglob("*.md")):
            file_content = path.read_text(encoding="utf-8")
            data = parse_frontmatter(file_content)
            if not data:
                continue
            rel = path.relative_to(SYSTEM_ROOT)
            record_kind = rel.parts[0]
            
            additional_themes = []
            if record_kind == "03-issue-units":
                additional_themes = parse_additional_themes(file_content)
                
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
                    "additional_themes": additional_themes,
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
    filtered_rows = [{k: v for k, v in r.items() if k in fieldnames} for r in rows]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)


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


def update_section(content: str, heading: str, new_items: list[str]) -> str:
    lines = content.splitlines()
    start_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start_idx = i
            break
    if start_idx == -1:
        return content

    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if lines[i].startswith("## "):
            end_idx = i
            break

    new_section = [heading, ""]
    for item in sorted(new_items):
        new_section.append(f"- `{item}`")
    new_section.append("")

    lines[start_idx:end_idx] = new_section
    return "\n".join(lines) + "\n"


def update_topic_cluster(cluster_path: Path, records: list[str], issues: list[str]) -> None:
    content = cluster_path.read_text(encoding="utf-8")
    content = update_section(content, "## 已有关联记录", records)
    content = update_section(content, "## 已有关联问题单元", issues)
    
    original_content = cluster_path.read_text(encoding="utf-8")
    if content.strip() != original_content.strip():
        content = content.rstrip() + "\n"
        cluster_path.write_text(content, encoding="utf-8")
        print(f"Updated topic cluster: {cluster_path.name}")


def update_all_topic_clusters(rows: list[dict]) -> None:
    theme_to_records = {}
    theme_to_issues = {}

    for row in rows:
        theme = row["primary_theme"]
        kind = row["kind"]
        rec_id = row["id"]
        if not rec_id:
            continue
        if theme:
            if kind == "02-normalized":
                theme_to_records.setdefault(theme, []).append(rec_id)
            elif kind == "03-issue-units":
                theme_to_issues.setdefault(theme, []).append(rec_id)
        
        for add_theme in row.get("additional_themes", []):
            if add_theme != theme:
                if kind == "03-issue-units":
                    theme_to_issues.setdefault(add_theme, []).append(rec_id)

    clusters_dir = SYSTEM_ROOT / "04-topic-clusters"
    if not clusters_dir.exists():
        return

    for path in sorted(clusters_dir.glob("*.md")):
        data = parse_frontmatter(path.read_text(encoding="utf-8"))
        theme = data.get("primary_theme")
        if not theme:
            continue
        
        matching_records = theme_to_records.get(theme, [])
        matching_issues = theme_to_issues.get(theme, [])
        update_topic_cluster(path, matching_records, matching_issues)


def validate_records(rows: list[dict]) -> None:
    errors = []
    
    VALID_THEMES = {
        "文科转码",
        "出国读书和海外求职",
        "早期职业迷茫",
        "学历提升和考研",
        "家庭影响和自我边界",
        "小城市女性职业起步",
        "私域沟通边界",
        "AI学习和AI教育",
        "商业合作和项目邀约",
        "其他"
    }

    VALID_RECORD_TYPES = {
        "qa_thread",
        "consult_call",
        "coaching_session",
        "collaboration",
        "boundary",
        "output",
        "article_draft",
        "other"
    }

    VALID_PRIVACY_LEVELS = {
        "private",
        "anonymized",
        "public_ready"
    }

    VALID_STATUSES = {
        "raw",
        "indexed",
        "normalized",
        "split",
        "clustered",
        "reusable",
        "draft"
    }

    for row in rows:
        path_str = row["record_path"]
        path = Path(path_str)
        
        # 1. Double extension check
        if path_str.endswith(".md.md") or path_str.endswith(".txt.txt"):
            errors.append(f"[{path_str}] Double extension found.")
            
        # 2. ID match check
        expected_id = path.stem
        if row["id"] != expected_id:
            errors.append(f"[{path_str}] ID mismatch. Frontmatter id '{row['id']}' does not match filename stem '{expected_id}'.")
            
        # 3. Theme check
        theme = row["primary_theme"]
        if row["kind"] not in {"05-outputs"}:
            if not theme:
                errors.append(f"[{path_str}] Missing primary_theme.")
            elif theme not in VALID_THEMES:
                errors.append(f"[{path_str}] Invalid primary_theme '{theme}'.")
                
        # 4. Record Type check
        if row["kind"] == "02-normalized":
            rec_type = row["record_type"]
            if not rec_type:
                errors.append(f"[{path_str}] Missing record_type.")
            elif rec_type not in VALID_RECORD_TYPES:
                errors.append(f"[{path_str}] Invalid record_type '{rec_type}'.")
                
        # 5. Privacy Level check
        priv = row["privacy_level"]
        if priv and priv not in VALID_PRIVACY_LEVELS:
            errors.append(f"[{path_str}] Invalid privacy_level '{priv}'.")
            
        # 6. Status check
        status = row["status"]
        if status and status not in VALID_STATUSES:
            errors.append(f"[{path_str}] Invalid status '{status}'.")
            
        # 7. Source Path check
        if row["kind"] == "02-normalized":
            src_path = row["source_path"]
            if not src_path:
                errors.append(f"[{path_str}] Missing source_path.")
            else:
                full_src = SYSTEM_ROOT / "00-inbox" / src_path
                if not full_src.exists():
                    errors.append(f"[{path_str}] source_path points to non-existent file: '00-inbox/{src_path}'.")

    if errors:
        print("\n=== VALIDATION ERRORS ===")
        for err in errors:
            print(f"  ❌ {err}")
        print("=========================\n")
        raise ValueError(f"Validation failed with {len(errors)} errors.")


def main() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    rows = record_rows()
    validate_records(rows)
    write_csv(rows)
    write_json(rows)
    write_markdown(rows)
    write_stats(rows)
    update_all_topic_clusters(rows)
    print(f"Indexed {len(rows)} records")
    try:
        build_people.main()
    except Exception as e:
        print(f"Warning: Failed to rebuild people index: {e}")


if __name__ == "__main__":
    main()


