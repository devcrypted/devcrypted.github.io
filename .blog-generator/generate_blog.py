#!/usr/bin/env python3
"""
Automated Blog Generator using Google Gemini API
Generates technical blog posts about AI, Cloud, Linux, and DevOps
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
TOPICS_COVERED_FILE = SCRIPT_DIR / "topics_covered.json"
POSTS_DIR = SCRIPT_DIR.parent / "_posts"
API_KEY = os.getenv("GEMINI_API_KEY")


def load_config():
    """Load configuration from config.json"""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_topics_covered():
    """Load list of already covered topics"""
    with open(TOPICS_COVERED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_topics_covered(data):
    """Save updated topics covered list"""
    with open(TOPICS_COVERED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_random_uncovered_topic(config, covered_data):
    """Select a random topic that hasn't been covered yet"""
    covered_topics = set(covered_data.get("covered_topics", []))
    available_topics = [t for t in config["topics"] if t not in covered_topics]

    if not available_topics:
        print("⚠️  All topics covered! Resetting topics list...")
        covered_data["covered_topics"] = []
        save_topics_covered(covered_data)
        available_topics = config["topics"]

    return random.choice(available_topics)


def generate_specific_subtopic(topic, config):
    """Generate a specific subtopic for the main topic"""
    content_type = random.choice(config["content_types"])

    # Create more specific prompts based on content type
    subtopic_prompts = {
        "How-to guide": f"a specific how-to guide about {topic}",
        "Tool comparison": f"comparing 2-3 specific tools/services in {topic}",
        "Command reference": f"essential commands for {topic}",
        "Quick tips": f"5-7 practical tips for {topic}",
        "Best practices": f"best practices for {topic}",
        "Configuration guide": f"configuration guide for a specific aspect of {topic}",
        "Troubleshooting guide": f"common issues and solutions in {topic}",
    }

    return subtopic_prompts.get(content_type, f"practical guide about {topic}")


def fix_nested_lists(content):
    """Remove nested list indentation, keep only flat lists"""
    lines = content.split("\n")
    fixed_lines = []
    in_code_block = False

    for line in lines:
        # Track code blocks to avoid modifying them
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            fixed_lines.append(line)
            continue

        if in_code_block:
            fixed_lines.append(line)
            continue

        # Check if line is a bullet point with indentation
        stripped = line.lstrip()
        if stripped.startswith(("-", "*", "•")):
            # Count leading spaces/tabs
            indent = len(line) - len(stripped)

            # If indented more than 4 spaces (nested), reduce to flat
            if indent > 4:
                # Keep it as a flat list item
                fixed_lines.append("- " + stripped[2:].strip())
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def generate_blog_content(topic, config):
    """Generate blog content using Gemini API"""
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    # Configure Gemini
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Generate specific subtopic
    specific_topic = generate_specific_subtopic(topic, config)

    # Create prompt
    system_prompt = config["system_prompt"]
    user_prompt = config["user_prompt_template"].format(topic=specific_topic)

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    print(f"🤖 Generating content for: {specific_topic}")

    # Generate content
    response = model.generate_content(full_prompt)
    content = response.text.strip()

    # Fix any nested lists (remove extra indentation)
    content = fix_nested_lists(content)

    # Generate title - must be specific, accurate, and well-written
    title_prompt = f"""Generate a specific, accurate, and descriptive title for this blog topic: {specific_topic}

Requirements:
- Maximum 80 characters
- Be SPECIFIC (e.g., "Azure Cost Optimization Tips" not "Azure Tips")
- Accurately describe the content
- SEO-friendly and professional
- No generic words like "Hacks", "Tricks" unless appropriate

Return ONLY the title, nothing else."""
    title_response = model.generate_content(title_prompt)
    title = title_response.text.strip().strip('"').strip("'")

    # Generate description
    desc_prompt = f"Generate a one-sentence description (max 150 characters) for this blog topic: {specific_topic}. Return ONLY the description, nothing else."
    desc_response = model.generate_content(desc_prompt)
    description = desc_response.text.strip().strip('"').strip("'")

    return {
        "title": title,
        "description": description,
        "content": content,
        "main_topic": topic,
        "specific_topic": specific_topic,
    }


def select_category_and_tags(main_topic, config):
    """Select appropriate category and tags based on topic"""
    topic_lower = main_topic.lower()

    # Category mapping
    category_map = {
        "azure": "Microsoft Azure",
        "aws": "Amazon Web Services",
        "linux": "Linux Administration",
        "devops": "DevOps Tools",
        "ai": "Artificial Intelligence",
        "machine learning": "Artificial Intelligence",
        "docker": "DevOps Tools",
        "kubernetes": "Container Orchestration",
        "terraform": "Infrastructure as Code",
        "ansible": "Infrastructure as Code",
        "python": "Automation",
        "powershell": "Automation",
        "cloud": "Cloud Engineering",
    }

    # Find matching category
    category = "Cloud Engineering"  # Default
    for key, cat in category_map.items():
        if key in topic_lower:
            category = cat
            break

    # Select relevant tags (3-5 tags)
    tags = []
    for tag in config["tags_pool"]:
        if tag.lower() in topic_lower or any(
            word in tag.lower() for word in topic_lower.split()
        ):
            tags.append(tag)

    # If no tags matched, add some default ones based on category
    if not tags:
        if "Azure" in category:
            tags = ["Azure", "Cloud"]
        elif "AWS" in category:
            tags = ["AWS", "Cloud"]
        elif "Linux" in category:
            tags = ["Linux"]
        elif "DevOps" in category:
            tags = ["DevOps", "Automation"]
        else:
            tags = ["Cloud Engineering"]

    # Limit to 3-5 tags
    tags = tags[:5] if len(tags) > 5 else tags
    if len(tags) < 3:
        tags.append("Tutorial")

    return category, tags


def create_blog_post(blog_data, config):
    """Create blog post markdown file with frontmatter"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    # Create filename-friendly title (CamelCase for filename)
    filename_title = "".join(
        c for c in blog_data["title"] if c.isalnum() or c in (" ", "-")
    ).strip()
    filename_title = filename_title.replace(" ", "")

    # Find next available number
    existing_posts = list(POSTS_DIR.glob(f"{date_str}-*.md"))
    post_number = len(existing_posts) + 1

    filename = f"{date_str}-{filename_title}.md"
    filepath = POSTS_DIR / filename

    # Select category and tags
    category, tags = select_category_and_tags(blog_data["main_topic"], config)

    # Create permalink - properly dash-separated, lowercase
    permalink_base = "".join(
        c if c.isalnum() or c == " " else " " for c in blog_data["title"]
    )
    permalink = "-".join(permalink_base.lower().split())

    # Create frontmatter
    frontmatter = f"""---
layout: post
authors: ["kamal"]
media_subpath: /assets/img/
pin: false

# Should be changed according to post
published: true
title: "{blog_data['title']}"
permalink: {permalink}
date: {today.strftime('%Y-%m-%d %H:%M %z')}
categories: ["{category}"]
tags: {json.dumps(tags)}
description: {blog_data['description']}
---

"""

    # Add AI generation notice
    ai_notice = """<!-- This blog post was automatically generated using AI -->

---

"""

    # Combine everything
    full_content = frontmatter + ai_notice + blog_data["content"]

    # Write file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"✅ Blog post created: {filename}")
    return filename


def main():
    """Main execution function"""
    print("🚀 Starting Automated Blog Generator...")

    # Load configuration
    config = load_config()
    covered_data = load_topics_covered()

    # Select topic
    topic = get_random_uncovered_topic(config, covered_data)
    print(f"📌 Selected topic: {topic}")

    # Generate content
    try:
        blog_data = generate_blog_content(topic, config)

        # Create blog post
        filename = create_blog_post(blog_data, config)

        # Update covered topics
        covered_data["covered_topics"].append(topic)
        covered_data["last_generated"] = datetime.now().isoformat()
        covered_data["total_generated"] = covered_data.get("total_generated", 0) + 1
        save_topics_covered(covered_data)

        print(f"✨ Successfully generated blog post!")
        print(f"📊 Total posts generated: {covered_data['total_generated']}")
        print(
            f"📝 Topics remaining: {len(config['topics']) - len(covered_data['covered_topics'])}"
        )

    except Exception as e:
        print(f"❌ Error generating blog: {str(e)}")
        raise


if __name__ == "__main__":
    main()
