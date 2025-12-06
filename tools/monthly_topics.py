#!/usr/bin/env python3
"""
Generate a month-long topic plan using Gemini 3 Pro and save to topics/MM-YYYY.json.
"""
from __future__ import annotations

import argparse
import calendar
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, List

from google import genai

DEFAULT_MODEL = os.environ.get("GEMINI_TEXT_MODEL", "gemini-2.5-pro")
TOPICS_DIR = Path(__file__).resolve().parent.parent / "topics"


def load_api_key() -> str:
    key = (
        os.environ.get("GEMINI_TEXT_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
    )
    if not key:
        raise RuntimeError("Set GEMINI_TEXT_API_KEY or GEMINI_API_KEY in the environment.")
    return key


def slugify(text: str, max_length: int = 60) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_length] or "topic"


@dataclass
class Topic:
    title: str
    description_prompt: str
    image_prompt: str
    tags: List[str]
    category: str
    permalink: str
    resources: List[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description_prompt": self.description_prompt,
            "image_prompt": self.image_prompt,
            "tags": self.tags,
            "category": self.category,
            "permalink": self.permalink,
            "resources": self.resources,
        }


def build_prompt(month_name: str, year: int, days: int, last_month_name: str) -> str:
    return (
        "You are a senior technical content strategist with internet research skills.\n"
        "Create a JSON array with exactly one entry per day of the month.\n"
        f"Target month: {month_name} {year} (days: {days}). Use insights from {last_month_name} trends.\n"
        "Allowed domains/topics to mix: AI, Azure, AWS, Linux, Terraform, OpenTofu, new technology news,\n"
        "popular tools, cloud networking, Ansible, Kubernetes, Docker, VSCode, antigravity, Gemini/Copilot/GPT/Claude,\n"
        "DevSecOps, DevOps, platform engineering, security tooling.\n"
        "Requirements for each array item: {\n"
        "  title: string (concise, refined, click-worthy occasionally),\n"
        "  description_prompt: detailed guidance for Gemini to write the blog (what to cover, key points, engagement cues),\n"
        "  image_prompt: a vivid 1280x720 prompt tailored for Nano Banana/Gemini image gen,\n"
        "  tags: 4-8 lowercase strings,\n"
        "  category: 1-2 word category,\n"
        "  permalink: max 60 chars, lowercase, hyphenated,\n"
        "  resources: 3-6 authoritative links for further reading\n"
        "}.\n"
        "Do not include date fields. Do not include code fences. Output only valid JSON array with length equal to days.\n"
        "Ensure titles are unique and not copies of existing articles; vary focus and angles."
    )


def request_topics(client: genai.Client, prompt: str) -> list[Any]:
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    raw = response.text if hasattr(response, "text") else None
    if not raw:
        raise RuntimeError("No response from model.")
    return json.loads(raw)


def normalize_topic(entry: Any) -> Topic:
    if not isinstance(entry, dict):
        raise ValueError("Topic entry must be an object")

    title = str(entry.get("title") or "Untitled").strip()
    description_prompt = str(entry.get("description_prompt") or "Outline the topic clearly.").strip()
    image_prompt = str(entry.get("image_prompt") or f"Hero image for {title}").strip()
    tags_raw = entry.get("tags") or []
    tags = [str(tag).lower().strip() for tag in tags_raw if str(tag).strip()]
    if not tags:
        tags = slugify(title).split("-")[:6]
    category = str(entry.get("category") or "Tech").strip()
    permalink_raw = entry.get("permalink") or slugify(title)
    permalink = slugify(permalink_raw)
    resources_raw = entry.get("resources") or []
    resources = [str(url).strip() for url in resources_raw if str(url).strip()]

    return Topic(
        title=title,
        description_prompt=description_prompt,
        image_prompt=image_prompt,
        tags=tags,
        category=category,
        permalink=permalink,
        resources=resources,
    )


def ensure_length(topics: list[Topic], desired: int) -> list[Topic]:
    if len(topics) >= desired:
        return topics[:desired]
    fallback_title = "Cloud engineering insights"
    while len(topics) < desired:
        topics.append(
            Topic(
                title=fallback_title,
                description_prompt="Summarize emerging practices in cloud engineering and reliability.",
                image_prompt="Isometric cloud infrastructure diagram with vibrant lighting, 1280x720",
                tags=["cloud", "engineering", "devops"],
                category="Cloud",
                permalink=slugify(fallback_title),
                resources=["https://cloud.google.com/architecture", "https://aws.amazon.com/whitepapers"],
            )
        )
    return topics


def write_topics_file(path: Path, topics: list[Topic]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [topic.to_dict() for topic in topics]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate monthly topics JSON using Gemini.")
    parser.add_argument("--month", type=int, help="Month number (1-12). Defaults to current month.")
    parser.add_argument("--year", type=int, help="Year (e.g., 2025). Defaults to current year.")
    args = parser.parse_args()

    today = date.today()
    month = args.month or today.month
    year = args.year or today.year
    days = calendar.monthrange(year, month)[1]
    last_month_num = 12 if month == 1 else month - 1
    last_month_year = year - 1 if month == 1 else year

    month_name = calendar.month_name[month]
    last_month_name = f"{calendar.month_name[last_month_num]} {last_month_year}"

    output_path = TOPICS_DIR / f"{month:02d}-{year}.json"
    if output_path.exists():
        print(f"Topics already exist for {month:02d}-{year}: {output_path}. Skipping generation.")
        return

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    prompt = build_prompt(month_name, year, days, last_month_name)
    raw_topics = request_topics(client, prompt)

    topics: list[Topic] = []
    if not isinstance(raw_topics, list):
        raise RuntimeError("Model response is not a list")

    for entry in raw_topics:
        try:
            topics.append(normalize_topic(entry))
        except Exception as exc:  # pragma: no cover
            print(f"Skipping malformed topic: {exc}", file=sys.stderr)

    topics = ensure_length(topics, days)
    write_topics_file(output_path, topics)
    print(f"Wrote topics: {output_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
