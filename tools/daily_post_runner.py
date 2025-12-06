#!/usr/bin/env python3
"""
Generate a daily Chirpy blog post from monthly topics and create a thumbnail image.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from google import genai
from PIL import Image

TEXT_MODEL = os.environ.get("GEMINI_TEXT_MODEL", "gemini-3-pro-preview")
IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "img"
TOPICS_DIR = Path(__file__).resolve().parent.parent / "topics"


def load_api_key() -> str:
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Set GEMINI_API_KEY or GOOGLE_API_KEY in the environment.")
    return key


def slugify(text: str, max_length: int = 60) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_length] or "post"


def ensure_unique_path(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    for idx in range(1, 100):
        candidate = base_path.with_name(f"{base_path.stem}-{idx}{base_path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("Unable to create a unique filename after 99 attempts.")


def read_topics(month: int, year: int) -> List[Dict[str, Any]]:
    path = TOPICS_DIR / f"{month:02d}-{year}.json"
    if not path.exists():
        raise FileNotFoundError(f"Topics file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Topics file must contain a JSON array")
    return data


def pick_topic(topics: List[Dict[str, Any]], day: int) -> Dict[str, Any]:
    index = day - 1
    if index < 0 or index >= len(topics):
        raise IndexError(f"No topic entry for day {day}")
    return topics[index]


def build_body_prompt(topic: Dict[str, Any]) -> str:
    title = topic.get("title", "Technical Insight")
    description_prompt = topic.get("description_prompt", "Provide a concise overview.")
    resources = topic.get("resources", [])
    tags = topic.get("tags", [])
    category = topic.get("category", "Tech")
    resources_block = "\n".join(str(r) for r in resources)
    return (
        "Act as an experienced technical writer with internet research skills.\n"
        "Write a full Markdown article (no YAML front matter).\n"
        "Structure: brief intro, multiple clear sections with h2/h3, actionable steps, examples, and a conclusion.\n"
        "Tone: concise, authoritative, engaging for practitioners.\n"
        "Use research-driven details; avoid fluff.\n"
        f"Title: {title}.\n"
        f"Category: {category}. Tags: {', '.join(tags)}.\n"
        f"Writing guidance: {description_prompt}\n"
        f"Reference links to consider (do not copy):\n{resources_block}\n"
        "Do not include YAML. Do not invent media links. Use fenced code blocks where relevant."
    )


def request_markdown(client: genai.Client, prompt: str) -> str:
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=[{"role": "user", "parts": [prompt]}],
        config={"response_mime_type": "text/plain"},
    )
    if hasattr(response, "text") and response.text:
        return str(response.text)
    raise RuntimeError("No text response from model.")


def request_image(client: genai.Client, prompt: str) -> bytes:
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[{"role": "user", "parts": [prompt]}],
        config={"response_mime_type": "image/png"},
    )
    if hasattr(response, "binary") and response.binary:
        return bytes(response.binary)
    if hasattr(response, "data") and response.data:
        return bytes(response.data)
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", []) if content else []
        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data and getattr(inline_data, "data", None):
                return bytes(inline_data.data)
    raise RuntimeError("No image bytes returned from model.")


def save_webp(image_bytes: bytes, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image.save(destination, format="WEBP", quality=85)
    return f"/assets/img/{destination.name}"


def build_front_matter(title: str, permalink: str, category: str, tags: List[str], image_path: str, description_prompt: str, timestamp: str) -> Dict[str, Any]:
    return {
        "layout": "post",
        "authors": ["devcrypted"],
        "pin": False,
        "video_prefix": "https://youtu.be/",
        "playlist_prefix": "https://youtube.com/playlist?list=",
        "github_prefix": "https://github.com/devcrypted/",
        "published": True,
        "title": title,
        "permalink": permalink,
        "media_subpath": "/assets/img",
        "date": timestamp,
        "categories": [category],
        "tags": tags,
        "image": image_path,
        "description": description_prompt[:180],
        "video_id": "",
        "playlist_id": "",
        "github_repo": "",
    }


def write_post(path: Path, front_matter: Dict[str, Any], body: str, resources: List[str]) -> None:
    yaml_block = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=False)
    extra = ""
    if resources:
        links = "\n".join(f"- {url}" for url in resources)
        extra = f"\n\n## Further Reading\n\n{links}\n"
    content = f"---\n{yaml_block}---\n\n{body.strip()}\n{extra}"
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate daily blog post and thumbnail from topics JSON.")
    parser.add_argument("--date", help="ISO date (YYYY-MM-DD). Defaults to today.")
    args = parser.parse_args()

    if args.date:
        target_date = date.fromisoformat(args.date)
    else:
        target_date = date.today()

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    topics = read_topics(target_date.month, target_date.year)
    topic = pick_topic(topics, target_date.day)

    title = str(topic.get("title") or "Technical Insight").strip()
    permalink = slugify(topic.get("permalink") or title)
    category = str(topic.get("category") or "Tech").strip()
    tags = [str(t).lower().strip() for t in topic.get("tags", []) if str(t).strip()]
    if not tags:
        tags = slugify(title).split("-")[:6]
    description_prompt = str(topic.get("description_prompt") or "Concise overview.").strip()
    image_prompt_base = str(topic.get("image_prompt") or f"Hero image for {title}").strip()
    image_prompt = f"{image_prompt_base}. 1280x720, Nano Banana style, cinematic lighting, detailed."
    resources = topic.get("resources") or []

    body_prompt = build_body_prompt(topic)
    body = request_markdown(client, body_prompt)

    image_bytes = request_image(client, image_prompt)
    image_name = f"{uuid.uuid4().hex}.webp"
    image_path = save_webp(image_bytes, ASSETS_DIR / image_name)

    now = datetime.now().astimezone()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S %z")

    front_matter = build_front_matter(title, permalink, category, tags, image_path, description_prompt, timestamp)

    filename = f"{target_date.strftime('%Y-%m-%d')}-{slugify(title)}.md"
    destination = ensure_unique_path(POSTS_DIR / filename)
    write_post(destination, front_matter, body, resources)
    print(f"Generated post: {destination}")
    print(f"Thumbnail: {image_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
