#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = SYSTEM_ROOT / "07-people"
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


def main() -> None:
    if not PEOPLE_DIR.exists():
        print(f"Directory {PEOPLE_DIR} does not exist.")
        return

    rows = []
    for path in sorted(PEOPLE_DIR.glob("person-*.md")):
        if path.name == "person-template.md":
            continue

        data = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not data:
            continue

        tags_str = ", ".join(as_list(data.get("tags")))
        related_str = "; ".join(as_list(data.get("related_records")))

        rows.append(
            {
                "person_id": data.get("person_id", ""),
                "display_name": data.get("display_name", ""),
                "real_name": data.get("real_name", ""),
                "contact_channel": data.get("contact_channel", ""),
                "contact_value": data.get("contact_value", ""),
                "short_intro": data.get("short_intro", ""),
                "primary_theme": data.get("primary_theme", ""),
                "tags": tags_str,
                "related_records": related_str,
                "connection_fit": data.get("connection_fit", "maybe"),
                "consent_to_connect": data.get("consent_to_connect", "unknown"),
                "privacy_level": data.get("privacy_level", "private"),
                "last_contacted": data.get("last_contacted", ""),
                "notes": data.get("notes", ""),
                "created": data.get("created", ""),
                "updated": data.get("updated", ""),
            }
        )

    out = PEOPLE_DIR / "people.csv"
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
        "connection_fit",
        "consent_to_connect",
        "privacy_level",
        "last_contacted",
        "notes",
        "created",
        "updated",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {out} with {len(rows)} people records.")


if __name__ == "__main__":
    main()
