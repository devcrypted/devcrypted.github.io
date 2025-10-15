#!/usr/bin/env python3
"""
Configuration Manager - Update topics, prompts, and settings
"""

import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"
TOPICS_COVERED_FILE = Path(__file__).parent / "topics_covered.json"

def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print("✅ Configuration saved!")

def load_topics_covered():
    with open(TOPICS_COVERED_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_topics_covered(data):
    with open(TOPICS_COVERED_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("✅ Topics covered data saved!")

def add_topics(new_topics):
    """Add new topics to the configuration"""
    config = load_config()
    added = []

    for topic in new_topics:
        if topic not in config["topics"]:
            config["topics"].append(topic)
            added.append(topic)

    if added:
        save_config(config)
        print(f"✅ Added {len(added)} new topic(s):")
        for topic in added:
            print(f"   - {topic}")
    else:
        print("ℹ️  All topics already exist in configuration")

def remove_topics(topics_to_remove):
    """Remove topics from the configuration"""
    config = load_config()
    removed = []

    for topic in topics_to_remove:
        if topic in config["topics"]:
            config["topics"].remove(topic)
            removed.append(topic)

    if removed:
        save_config(config)
        print(f"✅ Removed {len(removed)} topic(s):")
        for topic in removed:
            print(f"   - {topic}")
    else:
        print("ℹ️  None of the specified topics were found")

def list_topics():
    """List all topics"""
    config = load_config()
    covered_data = load_topics_covered()

    covered_set = set(covered_data.get("covered_topics", []))

    print(f"\n📋 Total Topics: {len(config['topics'])}")
    print(f"✅ Covered: {len(covered_set)}")
    print(f"⏳ Remaining: {len(config['topics']) - len(covered_set)}\n")

    print("All Topics:")
    for i, topic in enumerate(config["topics"], 1):
        status = "✅" if topic in covered_set else "⏳"
        print(f"{i:2d}. {status} {topic}")

def update_system_prompt(new_prompt):
    """Update the system prompt"""
    config = load_config()
    config["system_prompt"] = new_prompt
    save_config(config)
    print("✅ System prompt updated!")

def update_user_prompt_template(new_template):
    """Update the user prompt template"""
    config = load_config()
    config["user_prompt_template"] = new_template
    save_config(config)
    print("✅ User prompt template updated!")

def view_prompts():
    """Display current prompts"""
    config = load_config()
    print("\n" + "="*60)
    print("SYSTEM PROMPT:")
    print("="*60)
    print(config["system_prompt"])
    print("\n" + "="*60)
    print("USER PROMPT TEMPLATE:")
    print("="*60)
    print(config["user_prompt_template"])
    print("="*60 + "\n")

def reset_covered_topics():
    """Reset the list of covered topics"""
    covered_data = load_topics_covered()
    covered_count = len(covered_data.get("covered_topics", []))

    response = input(f"⚠️  This will reset {covered_count} covered topics. Continue? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        covered_data["covered_topics"] = []
        save_topics_covered(covered_data)
        print("✅ Covered topics list has been reset!")
    else:
        print("❌ Operation cancelled")

def add_tags(new_tags):
    """Add new tags to the tags pool"""
    config = load_config()
    added = []

    for tag in new_tags:
        if tag not in config["tags_pool"]:
            config["tags_pool"].append(tag)
            added.append(tag)

    if added:
        save_config(config)
        print(f"✅ Added {len(added)} new tag(s): {', '.join(added)}")
    else:
        print("ℹ️  All tags already exist in configuration")

def show_menu():
    """Display interactive menu"""
    print("\n" + "="*60)
    print("BLOG GENERATOR - CONFIGURATION MANAGER")
    print("="*60)
    print("\n1. List all topics")
    print("2. Add topics")
    print("3. Remove topics")
    print("4. View prompts")
    print("5. Update system prompt")
    print("6. Update user prompt template")
    print("7. Add tags")
    print("8. Reset covered topics")
    print("9. Exit")
    print()

def main():
    """Interactive configuration manager"""
    while True:
        show_menu()
        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            list_topics()

        elif choice == "2":
            print("\nEnter topics (one per line, empty line to finish):")
            topics = []
            while True:
                topic = input("Topic: ").strip()
                if not topic:
                    break
                topics.append(topic)
            if topics:
                add_topics(topics)

        elif choice == "3":
            list_topics()
            print("\nEnter topic numbers to remove (comma-separated):")
            config = load_config()
            numbers = input("Numbers: ").strip()
            try:
                indices = [int(n.strip()) - 1 for n in numbers.split(",")]
                topics_to_remove = [config["topics"][i] for i in indices if 0 <= i < len(config["topics"])]
                remove_topics(topics_to_remove)
            except (ValueError, IndexError):
                print("❌ Invalid input")

        elif choice == "4":
            view_prompts()

        elif choice == "5":
            print("\nEnter new system prompt (or 'cancel' to abort):")
            prompt = input().strip()
            if prompt and prompt.lower() != 'cancel':
                update_system_prompt(prompt)

        elif choice == "6":
            print("\nEnter new user prompt template (use {topic} as placeholder, or 'cancel' to abort):")
            template = input().strip()
            if template and template.lower() != 'cancel':
                update_user_prompt_template(template)

        elif choice == "7":
            print("\nEnter tags (comma-separated):")
            tags_input = input("Tags: ").strip()
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            if tags:
                add_tags(tags)

        elif choice == "8":
            reset_covered_topics()

        elif choice == "9":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
