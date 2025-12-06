#!/usr/bin/env python3
"""
Generate a Chirpy-friendly draft with YAML front matter using Gemini.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import yaml
from google import genai

DEFAULT_MODEL = os.environ.get("GEMINI_TEXT_MODEL", "gemini-2.5-pro")
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"


def load_api_key() -> str:
    key = (
        os.environ.get("GEMINI_TEXT_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
    )
    if not key:
        raise RuntimeError("Set GEMINI_TEXT_API_KEY or GEMINI_API_KEY.")
    return key


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return cleaned or "post"


def ensure_unique_path(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    for index in range(1, 100):
        candidate = base_path.with_name(f"{base_path.stem}-{index}{base_path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("Could not find a unique filename after 99 attempts.")


def split_front_matter(markdown: str) -> Tuple[Dict[str, Any], str]:
    if markdown.startswith("---"):
        parts = markdown.split("---", 2)
        if len(parts) >= 3:
            front_matter = yaml.safe_load(parts[1]) or {}
            body = parts[2].lstrip("\n")
            return front_matter, body
    return {}, markdown


def build_prompt(topic: str, category: str, timestamp: str, context: str | None) -> str:
    context_block = f"\nContext to respect:\n{context}\n" if context else ""
    return (
        "You are a Senior Technical Writer who produces Markdown for the Jekyll Chirpy theme.\n"
        "Write a concise, technically accurate blog post with clear headings and code blocks where relevant.\n"
        "Return the result as full Markdown with a YAML front matter block.\n"
        "Use the provided timestamp verbatim for the date field.\n"
        "Front matter keys: title, date, categories (list), tags (list), image (object with path and lqip), description.\n"
        "Leave image.path and image.lqip empty.\n"
        f"Timestamp to use: {timestamp}.\n"
        f"Primary category: {category}.\n"
        f"Topic: {topic}.\n"
        f"{context_block}"
        "Body guidelines: keep paragraphs short, include a brief intro, actionable steps, and a closing summary."
    )


def request_markdown(client: genai.Client, prompt: str) -> str:
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config={"response_mime_type": "text/plain"},
    )
    if hasattr(response, "text") and response.text:
        return str(response.text)
    raise RuntimeError("No text response from model.")


def normalize_front_matter(raw_front_matter: Dict[str, Any], topic: str, category: str, timestamp: str) -> Dict[str, Any]:
    front_matter = dict(raw_front_matter)
    title = str(front_matter.get("title") or topic).strip()
    front_matter["title"] = title
    front_matter["date"] = timestamp
    front_matter.setdefault("layout", "post")
    front_matter["categories"] = front_matter.get("categories") or [category]
    tags = front_matter.get("tags") or slugify(title).split("-")
    front_matter["tags"] = tags

    image_value = front_matter.get("image")
    if isinstance(image_value, dict):
        image_value.setdefault("path", "")
        image_value.setdefault("lqip", "")
        front_matter["image"] = image_value
    else:
        front_matter["image"] = {"path": "", "lqip": ""}

    if not front_matter.get("description"):
        front_matter["description"] = f"A walkthrough on {title}."
    return front_matter


def write_post(path: Path, front_matter: Dict[str, Any], body: str) -> None:
    yaml_block = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=False)
    content = f"---\n{yaml_block}---\n\n{body.strip()}\n"
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Chirpy-compatible draft using Gemini.")
    parser.add_argument("--topic", required=True, help="Topic for the blog post")
    parser.add_argument("--category", default="Tech", help="Primary category")
    parser.add_argument("--context-file", help="Optional path to additional context text")
    args = parser.parse_args()

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    now = datetime.now().astimezone()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S %z")

    context_text = None
    if args.context_file:
        context_path = Path(args.context_file)
        if context_path.is_file():
            context_text = context_path.read_text(encoding="utf-8")
        else:
            raise RuntimeError(f"Context file not found: {context_path}")

    prompt = build_prompt(args.topic, args.category, timestamp, context_text)
    markdown = request_markdown(client, prompt)
    front_matter_raw, body = split_front_matter(markdown)

    front_matter = normalize_front_matter(front_matter_raw, args.topic, args.category, timestamp)

    slug = slugify(front_matter.get("title", args.topic))
    filename = f"{now.strftime('%Y-%m-%d')}-{slug}.md"
    destination = ensure_unique_path(POSTS_DIR / filename)

    write_post(destination, front_matter, body)
    print(f"Generated draft: {destination}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - surface errors for CI logs
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
