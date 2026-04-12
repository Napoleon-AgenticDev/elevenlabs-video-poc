#!/usr/bin/env python3
"""
Prompt Enhancer using Claude
========================
Enhance raw concept descriptions into optimized prompts for GPT Image.

Usage:
    python enhance_prompts.py --concept "developer stressed at computer"
    python enhance_prompts.py --file prompts.txt
    python enhance_prompts.py --batch scenes.json
"""

import os
import json
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")


SYSTEM_PROMPT = """You are an expert at writing prompts for AI image generation models like DALL-E and GPT Image.
Your job is to transform raw concept descriptions into detailed, high-quality prompts that will generate consistent, cinematic images.

Guidelines:
1. Start with the main subject and action
2. Add specific visual details (lighting, camera angle, composition)
3. Include style references (cinematic, photorealistic, 3D render, illustration)
4. Specify mood/tone (dramatic, hopeful, mysterious)
5. Add technical quality terms (8k, highly detailed, professional photography)
6. Keep prompts under 200 words for consistency

Transform this concept into 4 distinct image prompts that tell a visual story, each highlighting different aspects of the scene."""


def enhance_with_claude(concept, api_key=None):
    """Use Claude API to enhance prompts."""
    key = api_key or ANTHROPIC_KEY
    
    if not key:
        print("  No ANTHROPIC_API_KEY, using local enhancement")
        return enhance_local(concept)
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"Enhance this concept into 4 distinct image prompts: {concept}"}
        ]
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=30)
    
    if response.status_code != 200:
        print(f"  Claude error: {response.status_code}")
        return enhance_local(concept)
    
    result = response.json()
    content = result.get("content", [])
    
    if content:
        prompts = content[0].get("text", "").split("\n")
        return [p.strip() for p in prompts if p.strip()][:4]
    
    return enhance_local(concept)


def enhance_with_chatgpt(concept, api_key=None):
    """Use OpenAI ChatGPT to enhance prompts (fallback)."""
    key = api_key or OPENAI_KEY
    
    if not key:
        return enhance_local(concept)
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o",
        "max_tokens": 1024,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Enhance this concept into 4 distinct image prompts for a video sequence: {concept}"}
        ]
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=30)
    
    if response.status_code != 200:
        return enhance_local(concept)
    
    result = response.json()
    choices = result.get("choices", [])
    
    if choices:
        text = choices[0].get("message", {}).get("content", "")
        prompts = text.split("\n")
        return [p.strip() for p in prompts if p.strip() and not p.startswith("**")][:4]
    
    return enhance_local(concept)


def enhance_local(concept):
    """Local prompt enhancement with templates."""
    base = {
        "developer stressed": [
            "Stressed developer at multiple monitors showing error messages, dark office at night, dramatic cinematic lighting, focused expression",
            "Developer looking overwhelmed with chaotic code flying, red error messages everywhere, cluttered desk, cinematic",
            "Developer silhouette looking at glowing screen, no clear direction, hopeful eyes, dramatic lighting",
            "Developer having realization moment, light bulb above head, determined expression, breakthrough moment",
        ],
        "tech office": [
            "Modern tech office with team collaborating, glass walls, natural lighting, professional",
            "Developer working on holographic display, futuristic interface, AI visualization",
            "Open concept office with standing desks, collaborative environment",
            "Server room with glowing lights, data visualization, tech infrastructure",
        ],
        "ai agents": [
            "AI agents working autonomously in digital space, glowing connections, futuristic",
            "Robot and human collaborating, partnership concept, cinematic lighting",
            "Neural network visualization, glowing nodes, data flowing, abstract tech art",
            "Autonomous agents collaborating on code, digital workspace, success visualization",
        ],
        "harness engineering": [
            "Blueprint and architecture diagram, harness framework visualization",
            "Feedback loops as glowing rivers, system flow visualization",
            "Verification gates with checkmarks, process flow diagram",
            "Observability dashboard, metrics and graphs, control center",
        ],
    }
    
    concept_lower = concept.lower()
    for key, prompts in base.items():
        if key in concept_lower:
            return prompts
    
    return [
        f"{concept}, cinematic lighting, professional photography, 8k",
        f"{concept}, dramatic lighting, emotional tone, highly detailed",
        f"{concept}, wide shot, cinematic composition, photorealistic",
        f"{concept}, close-up detail, professional quality, highly detailed",
    ]


def main():
    parser = argparse.ArgumentParser(description="Enhance image prompts")
    parser.add_argument("--concept", "-c", help="Concept to enhance")
    parser.add_argument("--file", "-f", help="File with concepts (one per line)")
    parser.add_argument("--batch", "-b", help="JSON file with concepts array")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--use-claude", action="store_true", help="Force Claude API")
    parser.add_argument("--api-key", help="API key override")
    args = parser.parse_args()
    
    results = {}
    
    if args.batch:
        with open(args.batch) as f:
            data = json.load(f)
        concepts = data.get("concepts", [])
    elif args.file:
        with open(args.file) as f:
            concepts = [line.strip() for line in f if line.strip()]
    elif args.concept:
        concepts = [args.concept]
    else:
        print("Usage: enhance_prompts.py --concept 'your concept'")
        return
    
    for concept in concepts:
        print(f"Enhancing: {concept[:50]}...")
        
        if args.use_claude or ANTHROPIC_KEY:
            prompts = enhance_with_claude(concept, args.api_key)
        elif OPENAI_KEY:
            prompts = enhance_with_chatgpt(concept, args.api_key)
        else:
            prompts = enhance_local(concept)
        
        results[concept] = prompts
        
        for i, p in enumerate(prompts, 1):
            print(f"  {i}. {p[:60]}...")
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Saved to {args.output}")
    elif len(results) == 1:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()