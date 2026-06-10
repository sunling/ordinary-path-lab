#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SYSTEM_ROOT / "templates" / "normalized-consult.md"
SOUL_PATH = SYSTEM_ROOT / "SOUL.md"
TAXONOMY_PATH = SYSTEM_ROOT / "taxonomy.md"
OUTPUT_DIR = SYSTEM_ROOT / "02-normalized"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_id(text: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    for line in match.group(1).splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            if key.strip() == "id":
                return val.strip().strip('"').strip("'")
    return None


def call_gemini(api_key: str, prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"API Error: {e.read().decode('utf-8')}")
        raise e


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-normalize raw consulting material.")
    parser.add_argument("source_file", help="Path to raw source file inside 00-inbox/")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        print("Please export GEMINI_API_KEY='your_key_here' and try again.")
        return

    src_path = Path(args.source_file)
    if not src_path.exists():
        # Try relative to SYSTEM_ROOT or 00-inbox
        src_path = SYSTEM_ROOT / args.source_file
        if not src_path.exists():
            src_path = SYSTEM_ROOT / "00-inbox" / args.source_file
            if not src_path.exists():
                print(f"Error: Source file '{args.source_file}' not found.")
                return

    print(f"Reading source material from: {src_path.name}...")
    source_content = src_path.read_text(encoding="utf-8")

    # Load context files
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    soul = SOUL_PATH.read_text(encoding="utf-8")
    taxonomy = TAXONOMY_PATH.read_text(encoding="utf-8")

    prompt = f"""You are the processing assistant for the "Ordinary Path Lab" (普通人路径实验室) project.
Your task is to normalize the raw input file into a structured Markdown record following the template, voice, and taxonomy of the project.

Here is the context of the project:

=== SOUL.md ( Philosophy and tone guidelines ) ===
{soul}

=== taxonomy.md ( Category list and privacy rules ) ===
{taxonomy}

=== Template ( Output format ) ===
{template}

=== Raw Input Material (from: {src_path.relative_to(SYSTEM_ROOT)}) ===
{source_content}

=== Instructions ===
1. Analyze the raw input: identify who the person is (age, location, major, status), their core question, their constraints, the response given, and any reusable insights.
2. Structure the output exactly matching the Template headers. Do not modify the headers themselves.
3. Infer the correct target filename ID: "consult-YYYYMMDD-person-topic". If the exact day is unknown, use "consult-YYYYMM-person-topic". Write this ID in the frontmatter `id:` field.
4. Set correct metadata values:
   - `record_type`: choose from taxonomy (e.g. qa_thread, consult_call).
   - `source_path`: write the path relative to 00-inbox (e.g. "一对一咨询/{src_path.name}").
   - `primary_theme`: choose exactly one valid theme from taxonomy.md.
   - `tags`: select matching tags from taxonomy.md.
   - `privacy_level`: default to "private".
5. Keep the tone grounded, empathetic, non-preachy, and objective (reflecting Sun Ling's perspective from SOUL.md).
6. Return only the raw Markdown starting with "---". Do not wrap the output in markdown code blocks (```markdown ... ```).

Now, generate the normalized Markdown record:"""

    print("Querying Gemini API...")
    output = call_gemini(api_key, prompt).strip()

    # Clean markdown formatting if model wrapped it in ```markdown
    if output.startswith("```"):
        # Strip code blocks
        lines = output.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        output = "\n".join(lines).strip()

    rec_id = parse_id(output)
    if not rec_id:
        print("Warning: Could not parse record ID from frontmatter. Using default filename.")
        rec_id = f"consult-{src_path.stem}"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{rec_id}.md"
    
    out_file.write_text(output + "\n", encoding="utf-8")
    print(f"🎉 Success! Generated normalized record at: {out_file.relative_to(SYSTEM_ROOT)}")


if __name__ == "__main__":
    main()
