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
import requests
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from google import genai
from PIL import Image
from google.genai import types

BLOG_MODEL_PRIMARY = os.environ.get("GEMINI_BLOG_MODEL_PRIMARY", "gemini-3-pro")
BLOG_MODEL_FALLBACK = os.environ.get("GEMINI_BLOG_MODEL_FALLBACK", "gemini-2.5-pro")
KEYWORD_MODEL = os.environ.get("GEMINI_KEYWORD_MODEL", "gemini-2.5-flash")
IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "imagen-3.0-generate-002")
IMAGE_MODEL_FALLBACKS = [
    m.strip()
    for m in os.environ.get(
        "GEMINI_IMAGE_MODEL_FALLBACKS",
        "imagen-3.0-fast-generate-001,imagen-3.0-generate-001,imagen-2.0-fast-generate-001",
    ).split(",")
    if m.strip()
]
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "img"
TOPICS_DIR = Path(__file__).resolve().parent.parent / "topics"
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
IMAGE_MAX_KB = int(os.environ.get("IMAGE_MAX_KB", "60"))
MAX_DIMENSIONS = (1280, 720)


def placeholder_image_bytes(color: tuple[int, int, int] = (220, 225, 230)) -> bytes:
    placeholder = Image.new("RGB", MAX_DIMENSIONS, color=color)
    return compress_image_to_webp_bytes(placeholder)


def fetch_image(url: str, headers: Dict[str, str] | None = None, timeout: int = 20) -> bytes | None:
    try:
        resp = requests.get(url, headers=headers or {}, timeout=timeout)
        resp.raise_for_status()
        return resp.content
    except Exception as exc:
        print(f"Download failed for {url}: {exc}")
        return None


def compress_image_to_webp_bytes(image: Image.Image, target_kb: int = IMAGE_MAX_KB) -> bytes:
    # Resize to max dimensions while preserving aspect ratio
    img = image.copy()
    img.thumbnail(MAX_DIMENSIONS)
    best_bytes = None
    for quality in (80, 70, 60, 50, 40, 30):
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP", quality=quality, method=6)
        data = buffer.getvalue()
        best_bytes = data
        if len(data) <= target_kb * 1024:
            break
    return best_bytes or b""


def pexels_search_candidates(prompt: str, per_page: int = 6) -> List[Dict[str, Any]]:
    """Return a small list of candidate images (metadata + download url) from Pexels."""
    if not PEXELS_API_KEY:
        return []
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": prompt, "per_page": per_page, "orientation": "landscape"}
    try:
        resp = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        photos = data.get("photos") or []
        results = []
        for photo in photos:
            src = photo.get("src", {})
            # Prefer a ~1k-1.5k wide asset; fallback to anything available
            url = src.get("large2x") or src.get("large") or src.get("original") or src.get("medium") or src.get("small")
            if not url:
                continue
            results.append(
                {
                    "id": photo.get("id"),
                    "alt": photo.get("alt") or "",
                    "photographer": photo.get("photographer") or "",
                    "url": url,
                }
            )
        return results
    except Exception as exc:
        print(f"Pexels search failed: {exc}")
        return []


def unsplash_search(prompt: str) -> bytes | None:
    # Disabled per user request; keep placeholder function for compatibility.
    return None


def choose_image_with_ai(candidates: List[Dict[str, Any]], query: str, title: str) -> Tuple[int | None, str | None]:
    """Ask the text model to pick the best candidate or suggest a better query."""
    if not candidates:
        return None, None
    try:
        text_client = genai.Client(api_key=load_text_key())
        options = [f"{idx}: alt='{c.get('alt','')}' by {c.get('photographer','')}" for idx, c in enumerate(candidates)]
        prompt = (
            "You rank stock photos for a tech blog thumbnail."
            f"\nBlog title: {title}"
            f"\nSearch query used: {query}"
            "\nCandidates (index: alt by photographer):\n" + "\n".join(options) +
            "\nRespond as JSON: {\"choice\": <index or null>, \"new_query\": <string or null>}"
            "\nChoose the best tech-relevant image. If none fit, set choice=null and suggest a better concise query."
        )
        resp = text_client.models.generate_content(
            model=KEYWORD_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        raw = getattr(resp, "text", None)
        if not raw and getattr(resp, "candidates", None):
            parts = getattr(resp.candidates[0].content, "parts", []) if resp.candidates[0].content else []
            if parts and getattr(parts[0], "text", None):
                raw = parts[0].text
        if not raw:
            raise RuntimeError("No JSON response from text model for image ranking.")
        data = json.loads(raw)
        return data.get("choice"), data.get("new_query")
    except Exception as exc:
        print(f"AI ranking failed: {exc}; defaulting to first candidate.")
        return 0, None


def pexels_select_image(prompt: str, title: str) -> bytes | None:
    """Search Pexels, let AI pick/iterate up to 3 tries, and return image bytes if found."""
    if not PEXELS_API_KEY:
        return None
    query = f"{prompt} technology illustration"
    fallback_candidate: Dict[str, Any] | None = None
    for attempt in range(3):
        candidates = pexels_search_candidates(query)
        if candidates:
            if fallback_candidate is None:
                fallback_candidate = candidates[0]
            choice, new_query = choose_image_with_ai(candidates, query, title)
            candidate = None
            if choice is not None and 0 <= choice < len(candidates):
                candidate = candidates[choice]
            elif new_query and attempt < 2:
                query = new_query
                continue
            else:
                candidate = candidates[0]

            data = fetch_image(candidate["url"], headers={"Authorization": PEXELS_API_KEY})
            if data:
                return data
            if new_query and attempt < 2:
                query = new_query
                continue
        elif attempt < 2:
            continue

    if fallback_candidate:
        data = fetch_image(fallback_candidate["url"], headers={"Authorization": PEXELS_API_KEY})
        if data:
            return data
    return None


def load_text_key() -> str:
    key = (
        os.environ.get("GEMINI_TEXT_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
    )
    if not key:
        raise RuntimeError("Set GEMINI_TEXT_API_KEY or GEMINI_API_KEY in the environment.")
    return key


def parse_tags_csv(text: str | None) -> List[str]:
    if not text:
        return []
    return [t.strip().lower() for t in text.split(",") if t.strip()]


def normalize_tags(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(t).strip().lower() for t in value if str(t).strip()]
    if isinstance(value, str):
        return parse_tags_csv(value)
    return []


def parse_resources_csv(text: str | None) -> List[str]:
    if not text:
        return []
    return [r.strip() for r in text.split(",") if r.strip()]


def suggest_metadata(title: str, description: str) -> Dict[str, Any]:
    client = genai.Client(api_key=load_text_key())
    prompt = (
        "You generate concise metadata for a tech blog post."
        f"\nTitle: {title}"
        f"\nDescription: {description}"
        "\nRespond as JSON with keys: category (one short word), tags (3-6 items, kebab-case), permalink_slug (kebab-case), image_prompt (concise), description (<=180 chars)."
    )
    try:
        resp = client.models.generate_content(
            model=KEYWORD_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        raw = getattr(resp, "text", None)
        if not raw and getattr(resp, "candidates", None):
            parts = getattr(resp.candidates[0].content, "parts", []) if resp.candidates[0].content else []
            if parts and getattr(parts[0], "text", None):
                raw = parts[0].text
        if not raw:
            raise RuntimeError("Empty metadata response")
        return json.loads(raw)
    except Exception as exc:
        print(f"Metadata suggestion failed: {exc}; using defaults.")
        return {}


def load_image_key() -> str:
    key = (
        os.environ.get("GEMINI_IMAGE_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
    )
    if not key:
        raise RuntimeError("Set GEMINI_IMAGE_API_KEY or GEMINI_API_KEY in the environment.")
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
        "Follow Jekyll-friendly Markdown: top-level headings must be '# ' and lowest-level headings '###', do not exceed h3.\n"
        "Structure: brief intro, explicit 'What You’ll Get' bullet list, multiple clear sections with h2/h3, small paragraphs, concise bullets.\n"
        "Tone: concise, authoritative, engaging for practitioners.\n"
        "Use research-driven details; avoid fluff.\n"
        "Include varied formats where useful: fenced code blocks, mermaid diagrams for flows/architecture, markdown tables, info blocks/quotes, bold/italic for emphasis, and links to credible sources. Emojis optional; keep tasteful.\n"
        "Prefer examples and code where applicable; keep bullets short.\n"
        "The content should be approximately 700-1200 words. Ensure not to write too long paragraphs\n"
        "Research on what technical audience want from a blog post, I think it's not difficult to find: it's important info, key highlights, small paragraphs, bullet points for clarity, code written within ```lang``` blocks properly, clean steps to follow, pros/cons of topic support that, a brief summary, mermaid high level architect/flow diagrams to understand things better and maybe a few more things, no all blogs support all of the things so use them carefully and ensure you're not making the content too long or unfollowable just because you want to put all stuff, keep precise up to the point and don't overdo things everything should be backed by proper research, no lies but if imaginations could be there indirectly telling that it's imaginations, etc. Rest you take care.\n"
        f"Title: {title}.\n"
        f"Category: {category}. Tags: {', '.join(tags)}.\n"
        f"Writing guidance: {description_prompt}\n"
        f"Reference links to consider (do not copy):\n{resources_block}\n"
        "Do not include YAML. Do not invent media links. Keep text precise and clean."
    )


def request_markdown(client: genai.Client, prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=BLOG_MODEL_PRIMARY,
            contents=prompt,
            config={"response_mime_type": "text/plain"},
        )
    except Exception as primary_exc:
        print(f"Primary blog model '{BLOG_MODEL_PRIMARY}' failed ({primary_exc}); using fallback '{BLOG_MODEL_FALLBACK}'.")
        response = client.models.generate_content(
            model=BLOG_MODEL_FALLBACK,
            contents=prompt,
            config={"response_mime_type": "text/plain"},
        )
    if hasattr(response, "text") and response.text:
        return str(response.text)
    raise RuntimeError("No text response from model.")


def pick_image_model(client: genai.Client) -> Tuple[str | None, List[str]]:
    """Return the first available generateImages-capable model and the full list."""
    available = []
    for model_info in client.models.list():
        methods = getattr(model_info, "supported_generation_methods", []) or []
        if "generateImages" in methods:
            available.append(model_info.name)

    candidates = [IMAGE_MODEL] + [m for m in IMAGE_MODEL_FALLBACKS if m != IMAGE_MODEL]
    for name in candidates:
        if name in available:
            return name, available
    if available:
        return available[0], available
    return None, available


def request_image(client: genai.Client, prompt: str, title: str) -> bytes:
    # model_name, available = pick_image_model(client) ## Uncomment it if you want to use Gemini image generation
    model_name = None
    if model_name:
        print(f"Requesting image from {model_name}...")
        try:
            response = client.models.generate_images(
                model=model_name,
                prompt=prompt,
                config=types.GenerateImagesConfig(number_of_images=1),
            )
            for image_entry in getattr(response, "generated_images", []) or []:
                image_obj = getattr(image_entry, "image", None)
                if image_obj and getattr(image_obj, "image_bytes", None):
                    return bytes(image_obj.image_bytes)
            print("Model call succeeded but no image bytes returned; falling back to stock search.")
        except Exception as exc:
            print(f"Image model '{model_name}' failed ({exc}); falling back to stock search.")
    else:
        print("No image-capable models available on this key; using Pexels search.")

    # Stock photo fallback via Pexels with AI ranking/iteration
    stock_bytes = pexels_select_image(prompt, title)
    if stock_bytes:
        return stock_bytes

    print("Stock photo search failed; using placeholder.")
    return placeholder_image_bytes()

def save_webp(image_bytes: bytes, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    data = compress_image_to_webp_bytes(image)
    destination.write_bytes(data)
    return destination.name


def build_front_matter(title: str, permalink: str, category: str, tags: List[str], image_path: str, description_prompt: str, timestamp: str) -> Dict[str, Any]:
    return {
        "layout": "post",
        "authors": ["devcrypted"],
        "pin": False,
        "mermaid": True,
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
    parser.add_argument("--title", help="Manual mode title (skip topics JSON)")
    parser.add_argument("--description", help="Manual mode description")
    parser.add_argument("--category", help="Override category")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--permalink", help="Override permalink slug")
    parser.add_argument("--image-prompt", dest="image_prompt_override", help="Override image prompt base")
    parser.add_argument("--resources", help="Comma-separated resource links")
    args = parser.parse_args()

    manual_mode = bool(args.title)

    if args.date:
        target_date = date.fromisoformat(args.date)
    else:
        target_date = date.today()

    api_key = load_text_key()
    client = genai.Client(api_key=api_key)

    if manual_mode:
        if not args.description:
            raise SystemExit("--description is required when --title is provided")
        title = str(args.title).strip()
        description_prompt = str(args.description).strip()
        suggested = suggest_metadata(title, description_prompt)
        category = (args.category or suggested.get("category") or "Tech").strip()
        suggested_tags = normalize_tags(suggested.get("tags"))
        tags = parse_tags_csv(args.tags) or suggested_tags
        if not tags:
            tags = slugify(title).split("-")[:6]
        permalink = slugify(args.permalink or suggested.get("permalink_slug") or title)
        image_prompt_base = (args.image_prompt_override or suggested.get("image_prompt") or f"Hero image for {title}").strip()
        description_prompt = suggested.get("description") or description_prompt
        resources = parse_resources_csv(args.resources)
        topic = {
            "title": title,
            "description_prompt": description_prompt,
            "category": category,
            "tags": tags,
            "resources": resources,
            "permalink": permalink,
            "image_prompt": image_prompt_base,
        }
    else:
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
        resources = topic.get("resources") or []

    image_prompt = f"{image_prompt_base}. 1280x720, Nano Banana style, cinematic lighting, detailed."

    body_prompt = build_body_prompt(topic)
    # Generate image first with image-specific key/quota
    image_api_key = load_image_key()
    image_client = genai.Client(api_key=image_api_key)
    image_bytes = request_image(image_client, image_prompt, title)
    image_name = f"{uuid.uuid4().hex}.webp"
    image_path = save_webp(image_bytes, ASSETS_DIR / image_name)

    # Then generate the post body using the text key
    body = request_markdown(client, body_prompt)

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
