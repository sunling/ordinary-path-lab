#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
INBOX_ROOT = SYSTEM_ROOT / "00-inbox"
VAULT_ROOT = SYSTEM_ROOT.parents[1]
NORMALIZED_DIR = SYSTEM_ROOT / "02-normalized"
PEOPLE_DIR = SYSTEM_ROOT / "07-people"
OUT_CSV = PEOPLE_DIR / "people_candidates.csv"
SOURCE_DIRS = [
    INBOX_ROOT / "一对一咨询",
    INBOX_ROOT / "问答咨询",
    INBOX_ROOT / "人生教练",
]

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SECTION_RE = re.compile(r"^## 她/他是谁\n(.*?)(?=^## |\Z)", re.S | re.M)


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
        if value == "":
            data[key] = ""
            current_key = key
        else:
            data[key] = parse_scalar(value)
            current_key = key
    return data


def as_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [str(value)]


def extract_who_summary(text: str) -> str:
    match = SECTION_RE.search(text)
    if not match:
        return ""
    bullets = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        if "未提及" in line:
            continue
        label, _, value = line[2:].partition("：")
        value = value.strip("。 ")
        if not value:
            continue
        if label in {"年龄", "性别", "所在地/想去的地方", "当前身份", "学历/专业", "工作/行业"}:
            bullets.append(value)
    return "；".join(bullets[:5])


def infer_contact_from_source(source_path: str) -> tuple[str, str, str]:
    """Return contact_channel, contact_value, review_note."""
    filename = Path(source_path).name
    stem = Path(source_path).stem
    if "wx_" in stem:
        match = re.search(r"(wx[_\-][A-Za-z0-9_]+)", stem)
        if match:
            return "wechat_from_filename", match.group(1), "从原始文件名推断，需人工确认"
    return "", "", ""


def make_person_id(record_id: str, alias: str) -> str:
    date_match = re.search(r"(\d{6,8})", record_id)
    date = date_match.group(1) if date_match else "unknown"
    slug_source = alias or record_id
    slug = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", slug_source).strip("-").lower()
    if not slug:
        slug = record_id
    return f"person-{date}-{slug}"


def canonical_name(name: str) -> str:
    return re.sub(r"\s+", "", name or "").lower()


def make_group_person_id(rows: list[dict]) -> str:
    name = rows[0].get("display_name") or "unknown"
    dated = []
    for row in rows:
        for value in (row.get("related_records", ""), row.get("source_path", ""), row.get("person_id", "")):
            match = re.search(r"(\d{6,8})", value)
            if match:
                dated.append(match.group(1))
                break
    date = min(dated) if dated else "unknown"
    slug = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", name).strip("-").lower() or "unknown"
    return f"person-{date}-{slug}"


def infer_alias_from_source_path(path: Path) -> str:
    stem = path.stem
    parts = path.parts
    if "人生教练" in parts:
        idx = parts.index("人生教练")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    if "帮助他人-人生教练" in parts:
        name = re.sub(r"^\d+[-_]", "", stem).strip()
        return name or stem
    if "转写_" in stem:
        name = stem.split("转写_", 1)[1]
        name = re.split(r"\s+_| _ | _|_", name)[0].strip()
        name = re.sub(r"-转写智能优化版.*$", "", name).strip()
        return name or stem
    if "个人会议室" in stem:
        return "个人会议室咨询者"
    if re.match(r"^\d{6}$", stem):
        return ""
    return re.sub(r"^\d+[-_]", "", stem).strip()


def raw_source_candidates(existing_source_paths: set[str]) -> list[dict]:
    rows = []
    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            continue
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
                continue
            rel_source = str(path.relative_to(INBOX_ROOT))
            if rel_source in existing_source_paths:
                continue
            alias = infer_alias_from_source_path(path)
            if not alias:
                continue
            contact_channel, contact_value, contact_note = infer_contact_from_source(rel_source)
            record_seed = path.stem
            rows.append(
                {
                    "person_id": make_person_id(record_seed, alias),
                    "display_name": alias,
                    "real_name": "",
                    "contact_channel": contact_channel,
                    "contact_value": contact_value,
                    "short_intro": "",
                    "primary_theme": "",
                    "tags": "",
                    "related_records": "",
                    "source_path": rel_source,
                    "connection_fit": "unknown",
                    "consent_to_connect": "unknown",
                    "privacy_level": "private",
                    "needs_review": "yes",
                    "notes": contact_note or "由原始文件名/文件夹名推断，尚未关联 normalized 记录",
                }
            )
    return rows


def normalized_candidates() -> list[dict]:
    rows = []
    for path in sorted(NORMALIZED_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        data = parse_frontmatter(text)
        if not data:
            continue
        record_id = data.get("id", path.stem)
        alias = data.get("person_alias", "")
        source_path = data.get("source_path", "")
        contact_channel, contact_value, contact_note = infer_contact_from_source(source_path)
        short_intro = extract_who_summary(text)
        rows.append(
            {
                "person_id": make_person_id(record_id, alias),
                "display_name": alias,
                "real_name": "",
                "contact_channel": contact_channel,
                "contact_value": contact_value,
                "short_intro": short_intro,
                "primary_theme": data.get("primary_theme", ""),
                "tags": ", ".join(as_list(data.get("tags"))),
                "related_records": record_id,
                "source_path": source_path,
                "connection_fit": "maybe" if "connection" in as_list(data.get("layers")) else "unknown",
                "consent_to_connect": "unknown",
                "privacy_level": "private",
                "needs_review": "yes",
                "notes": contact_note or "由 normalized 记录生成，需人工确认联系方式和连接意愿",
            }
        )
    return rows


def merge_people(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        key = canonical_name(row.get("display_name"))
        if not key:
            key = row.get("person_id", "")
        grouped[key].append(row)

    merged_rows = []
    for _, group in grouped.items():
        group = sorted(group, key=lambda row: (row.get("source_path", ""), row.get("related_records", "")))
        base = max(group, key=lambda row: len(row.get("short_intro", "")))
        related_records = sorted({r for row in group for r in row.get("related_records", "").split("; ") if r})
        source_paths = sorted({row.get("source_path", "") for row in group if row.get("source_path", "")})
        tags = sorted({tag.strip() for row in group for tag in row.get("tags", "").split(",") if tag.strip()})
        themes = [row.get("primary_theme", "") for row in group if row.get("primary_theme", "")]
        primary_theme = base.get("primary_theme", "") or (themes[0] if themes else "")
        contact_rows = [row for row in group if row.get("contact_value")]
        contact = contact_rows[0] if contact_rows else base
        connection_values = {row.get("connection_fit", "") for row in group}
        connection_fit = "maybe" if "maybe" in connection_values else "unknown"
        notes = []
        if len(group) > 1:
            notes.append(f"已合并 {len(group)} 条候选记录")
        contact_note = contact.get("notes", "")
        if contact_note and "从原始文件名推断" in contact_note:
            notes.append(contact_note)
        notes.append("需人工确认联系方式、重复合并和连接意愿")
        merged_rows.append(
            {
                "person_id": make_group_person_id(group),
                "display_name": base.get("display_name", ""),
                "real_name": "",
                "contact_channel": contact.get("contact_channel", ""),
                "contact_value": contact.get("contact_value", ""),
                "short_intro": base.get("short_intro", ""),
                "primary_theme": primary_theme,
                "tags": ", ".join(tags),
                "related_records": "; ".join(related_records),
                "source_path": "; ".join(source_paths),
                "connection_fit": connection_fit,
                "consent_to_connect": "unknown",
                "privacy_level": "private",
                "needs_review": "yes",
                "notes": "；".join(notes),
            }
        )
    return sorted(merged_rows, key=lambda row: (row["display_name"].lower(), row["person_id"]))


def main() -> None:
    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    rows = normalized_candidates()
    existing_source_paths = {row["source_path"] for row in rows if row["source_path"]}
    rows.extend(raw_source_candidates(existing_source_paths))
    rows = merge_people(rows)
    fieldnames = [
        "person_id",
        "display_name",
        "real_name",
        "contact_channel",
        "contact_value",
        "short_intro",
        "primary_theme",
        "tags",
        "related_records",
        "source_path",
        "connection_fit",
        "consent_to_connect",
        "privacy_level",
        "needs_review",
        "notes",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} people candidates to {OUT_CSV.relative_to(VAULT_ROOT)}")


if __name__ == "__main__":
    main()
