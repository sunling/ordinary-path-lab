#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
INBOX_ROOT = SYSTEM_ROOT / "00-inbox"
INDEX_DIR = SYSTEM_ROOT / "01-source-index"
SOURCE_DIRS = [
    INBOX_ROOT / "问答咨询",
    INBOX_ROOT / "一对一咨询",
    INBOX_ROOT / "人生教练",
]
EXTENSIONS = {".md", ".txt"}


def guess_kind(path: Path) -> str:
    parts = set(path.parts)
    if "问答咨询" in parts:
        return "qa"
    if "一对一咨询" in parts:
        return "one_on_one"
    if "人生教练" in parts:
        return "life_coaching"
    return "other"


def main() -> None:
    rows = []
    counts = Counter()
    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            continue
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            rel = path.relative_to(INBOX_ROOT)
            kind = guess_kind(path)
            size_kb = path.stat().st_size / 1024
            counts[kind] += 1
            rows.append((str(rel), kind, path.suffix.lower(), size_kb))

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    out = INDEX_DIR / "source_inventory.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 咨询原始材料清单",
        "",
        f"Generated: {now}",
        "",
        "## 统计",
        "",
    ]
    for kind, count in sorted(counts.items()):
        lines.append(f"- {kind}: {count}")
    lines.extend(
        [
            f"- total: {len(rows)}",
            "",
            "## 文件",
            "",
            "| source_path | kind | ext | size_kb |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for rel, kind, ext, size_kb in rows:
        lines.append(f"| {rel} | {kind} | {ext} | {size_kb:.1f} |")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Sources: {len(rows)}")


if __name__ == "__main__":
    main()
