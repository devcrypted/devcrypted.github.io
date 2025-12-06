#!/usr/bin/env python3
"""
Generate header images for posts missing image metadata.
"""
from __future__ import annotations

import argparse
import base64
import io
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

import yaml
from google import genai
from PIL import Image, ImageFilter

POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"
HEADERS_DIR = Path(__file__).resolve().parent.parent / "assets" / "img" / "headers"
DEFAULT_IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
DEFAULT_STYLE = "Nano Banana style, 3D isometric, clay material, high fidelity, cinematic lighting"


@dataclass
class Post:
    path: Path
    front_matter: Dict[str, Any]
    body: str


def load_api_key() -> str:
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Set GOOGLE_API_KEY or GEMINI_API_KEY.")
    return key


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return cleaned or "post"


def split_front_matter(markdown: str) -> Tuple[Dict[str, Any], str]:
    if markdown.startswith("---"):
        parts = markdown.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}, parts[2].lstrip("\n")
    return {}, markdown


def parse_post(path: Path) -> Post:
    raw = path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(raw)
    return Post(path=path, front_matter=front_matter, body=body)


def needs_image(front_matter: Dict[str, Any]) -> bool:
    if "image" not in front_matter:
        return True
    image_val = front_matter["image"]
    if isinstance(image_val, dict):
        return not image_val.get("path")
    if isinstance(image_val, str):
        return False
    return True


def summarize_text(text: str, limit: int = 1000) -> str:
    return " ".join(text.strip().split())[:limit]


def extract_image_bytes(response: Any) -> bytes:
    for attr in ("binary", "data", "bytes"):
        candidate = getattr(response, attr, None)
        if isinstance(candidate, (bytes, bytearray)):
            return bytes(candidate)

    media_list = getattr(response, "media", None)
    if media_list:
        for media in media_list:
            data = getattr(media, "data", None)
            if isinstance(data, (bytes, bytearray)):
                return bytes(data)

    candidates = getattr(response, "candidates", [])
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts: Iterable[Any] = getattr(content, "parts", []) if content else []
        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data and getattr(inline_data, "data", None):
                return bytes(inline_data.data)

    raise RuntimeError("Could not extract image bytes from response.")


def request_image(client: genai.Client, prompt: str, model: str) -> bytes:
    response = client.models.generate_content(
        model=model,
        contents=[{"role": "user", "parts": [prompt]}],
        config={"response_mime_type": "image/png"},
    )
    return extract_image_bytes(response)


def save_webp(image_bytes: bytes, destination: Path) -> Image.Image:
    HEADERS_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="WEBP", quality=85)
    return image


def generate_lqip(image: Image.Image) -> str:
    preview = image.copy()
    preview.thumbnail((20, 20))
    preview = preview.filter(ImageFilter.GaussianBlur(radius=1.5))
    buffer = io.BytesIO()
    preview.save(buffer, format="WEBP", quality=50)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def update_front_matter(front_matter: Dict[str, Any], webp_path: str, lqip: str) -> Dict[str, Any]:
    updated = dict(front_matter)
    updated["image"] = {"path": webp_path, "lqip": lqip}
    return updated


def write_post(post: Post, front_matter: Dict[str, Any]) -> None:
    yaml_block = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=False)
    content = f"---\n{yaml_block}---\n\n{post.body.strip()}\n"
    post.path.write_text(content, encoding="utf-8")


def process_post(client: genai.Client, post: Post, style: str, model: str) -> None:
    if not needs_image(post.front_matter):
        print(f"Skipping (image exists): {post.path}")
        return

    slug_source = post.front_matter.get("title") or post.path.stem
    slug = slugify(slug_source)
    header_path = HEADERS_DIR / f"{slug}.webp"
    web_path = f"/assets/img/headers/{header_path.name}"

    summary = summarize_text(post.body)
    prompt = f"{style}. Create a header image for: {summary}"
    image_bytes = request_image(client, prompt, model)

    final_image = save_webp(image_bytes, header_path)
    lqip_value = generate_lqip(final_image)

    updated_front_matter = update_front_matter(post.front_matter, web_path, f"data:image/webp;base64,{lqip_value}")
    write_post(post, updated_front_matter)
    print(f"Updated image for: {post.path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Nano Banana style images for posts without images.")
    parser.add_argument("--limit", type=int, default=0, help="Maximum number of posts to process (0 = all)")
    parser.add_argument("--style", default=DEFAULT_STYLE, help="Style prompt prefix")
    parser.add_argument("--model", default=DEFAULT_IMAGE_MODEL, help="Gemini model for image generation")
    args = parser.parse_args()

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    processed = 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        if args.limit and processed >= args.limit:
            break
        post = parse_post(path)
        try:
            process_post(client, post, args.style, args.model)
            processed += 1
        except Exception as exc:  # pragma: no cover - log and continue
            print(f"Error processing {path}: {exc}", file=sys.stderr)

    print(f"Processed {processed} post(s).")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
