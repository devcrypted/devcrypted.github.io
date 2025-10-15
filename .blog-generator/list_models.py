#!/usr/bin/env python3
"""
List available Gemini models to find the correct model name
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GEMINI_API_KEY not found in environment variables")
    exit(1)

genai.configure(api_key=API_KEY)

print("📋 Available Gemini Models:\n")
for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print()
