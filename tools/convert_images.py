#!/usr/bin/env python3
"""
Standalone image converter: Convert images to WebP format optimized to 45-50KB.
Supports both local file paths and URLs.
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path
from typing import List

import requests
from PIL import Image

DEFAULT_TARGET_KB = 50
MAX_DIMENSIONS = (1280, 720)


def fetch_image_from_url(url: str, timeout: int = 20) -> bytes:
    """Download image from URL."""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.content
    except Exception as exc:
        raise RuntimeError(f"Failed to download image from {url}: {exc}")


def compress_to_webp(image: Image.Image, target_kb: int = DEFAULT_TARGET_KB) -> bytes:
    """Compress image to WebP format with target file size."""
    # Resize to max dimensions while preserving aspect ratio
    img = image.copy().convert("RGB")
    img.thumbnail(MAX_DIMENSIONS, Image.Resampling.LANCZOS)
    
    best_bytes = None
    for quality in (85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30):
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP", quality=quality, method=6)
        data = buffer.getvalue()
        best_bytes = data
        size_kb = len(data) / 1024
        
        # Accept if within target range (target_kb - 5 to target_kb + 5)
        if size_kb <= target_kb + 5:
            print(f"  Optimized to {size_kb:.1f}KB (quality={quality})")
            break
    
    if best_bytes is None:
        raise RuntimeError("Failed to compress image")
    
    return best_bytes


def convert_image(source: str, output_dir: Path | None = None, target_kb: int = DEFAULT_TARGET_KB) -> Path:
    """
    Convert a single image to WebP format.
    
    Args:
        source: Local file path or URL
        output_dir: Output directory (defaults to same as source for files, cwd for URLs)
        target_kb: Target file size in KB
    
    Returns:
        Path to the converted WebP file
    """
    is_url = source.startswith(("http://", "https://"))
    
    if is_url:
        print(f"Downloading: {source}")
        image_data = fetch_image_from_url(source)
        image = Image.open(io.BytesIO(image_data))
        
        # Generate filename from URL
        url_path = source.split("?")[0]  # Remove query params
        original_name = Path(url_path).stem or "image"
        output_name = f"{original_name}.webp"
        
        if output_dir:
            output_path = output_dir / output_name
        else:
            output_path = Path.cwd() / output_name
    else:
        source_path = Path(source).resolve()
        if not source_path.exists():
            raise FileNotFoundError(f"Image not found: {source}")
        
        print(f"Converting: {source_path}")
        image = Image.open(source_path)
        
        # Determine output path
        if output_dir:
            output_name = f"{source_path.stem}.webp"
            output_path = output_dir / output_name
        else:
            output_path = source_path.with_suffix(".webp")
    
    # Convert to WebP
    webp_data = compress_to_webp(image, target_kb)
    
    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(webp_data)
    
    size_kb = len(webp_data) / 1024
    print(f"  Saved: {output_path} ({size_kb:.1f}KB)")
    
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert images to WebP format optimized to 45-50KB",
        epilog="Examples:\n"
               "  %(prog)s image1.jpg image2.png\n"
               "  %(prog)s https://example.com/image.jpg\n"
               "  %(prog)s --output assets/img/ image1.jpg image2.png\n"
               "  %(prog)s --target-kb 60 large-image.jpg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "images",
        nargs="+",
        help="Image file paths or URLs to convert",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory (defaults to same directory as source)",
    )
    parser.add_argument(
        "-t", "--target-kb",
        type=int,
        default=DEFAULT_TARGET_KB,
        help=f"Target file size in KB (default: {DEFAULT_TARGET_KB})",
    )
    
    args = parser.parse_args()
    
    # Validate output directory
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
    
    # Convert all images
    converted: List[Path] = []
    failed: List[str] = []
    
    for source in args.images:
        try:
            output_path = convert_image(source, args.output, args.target_kb)
            converted.append(output_path)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            failed.append(source)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Converted: {len(converted)}/{len(args.images)} images")
    if failed:
        print(f"Failed: {len(failed)} images")
        for img in failed:
            print(f"  - {img}")
    print(f"{'='*60}")
    
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
