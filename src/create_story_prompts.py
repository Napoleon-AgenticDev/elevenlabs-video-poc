#!/usr/bin/env python3
"""
Story-Grounded Image Prompt Generator
=================================
Analyzes the script/story and creates consistent, grounded image prompts.

Pre-workflow:
1. Analyze the script and determine the story arc
2. Identify recurring visual elements
3. Create a "visual anchor" that grounds all images
4. Generate consistent prompts for each scene

Usage:
    python create_story_prompts.py --script "Your script here"
    python create_story_prompts.py --scene 1
    python create_story_prompts.py --all
"""

import json
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


SCENES = {
    1: {
        "title": "THE PROBLEM",
        "script": "Every developer knows this feeling. You're building an AI system, and it starts spiraling out of control. Code everywhere. No direction. Tests failing. Sound familiar?",
        "segments": [
            {"text": "Every developer knows this feeling.", "emotion": "relatable, slight frustration"},
            {"text": "You're building an AI system, and it starts spiraling out of control.", "emotion": "overwhelmed, chaotic"},
            {"text": "Code everywhere. No direction. Tests failing.", "emotion": "stressed, lost"},
            {"text": "Sound familiar?", "emotion": "hopeful, questioning"},
        ]
    },
    2: {
        "title": "THE DISCOVERY",
        "script": "What if there was a better way? What if you could design the specifications that guide your AI? Enter... harness engineering. It's about creating environments and feedback loops.",
        "segments": [
            {"text": "What if there was a better way?", "emotion": "curious, searching"},
            {"text": "What if you could design the specifications?", "emotion": "contemplative, design-focused"},
            {"text": "Enter... harness engineering.", "emotion": "dramatic, reveal"},
            {"text": "It's about creating environments and feedback loops.", "emotion": "clarity, understanding"},
        ]
    },
    3: {
        "title": "THE SOLUTION",
        "script": "Three companies cracked the code. OpenAI, LangChain, and Anthropic. Self-verification before exit. Incremental progress over scope.",
        "segments": [
            {"text": "Three companies cracked the code.", "emotion": "confident, powerful"},
            {"text": "OpenAI, LangChain, and Anthropic.", "emotion": "professional, credible"},
            {"text": "Self-verification before exit.", "emotion": "methodical, precise"},
            {"text": "Incremental progress over scope.", "emotion": "achievement, success"},
        ]
    },
    4: {
        "title": "THE IMPACT",
        "script": "Level four autonomy achieved. The shift: humans design systems, agents execute. The results speak for themselves.",
        "segments": [
            {"text": "Level four autonomy achieved.", "emotion": "triumphant, epic"},
            {"text": "The shift: humans design systems, agents execute.", "emotion": "transformational, paradigm-shift"},
            {"text": "The results speak for themselves.", "emotion": "confident, prove-it"},
        ]
    },
    5: {
        "title": "THE FUTURE",
        "script": "The future isn't about writing more code. It's about creating better specifications. Are you ready to guide them?",
        "segments": [
            {"text": "The future isn't about writing more code.", "emotion": "visionary, forward-looking"},
            {"text": "It's about creating better specifications.", "emotion": "architectural, design"},
            {"text": "Are you ready to guide them?", "emotion": "empowering, call-to-action"},
        ]
    },
}


def analyze_story():
    """Analyze the full script and extract story elements."""
    
    story_elements = {
        "setting": "Modern tech office/coworking space, realistic professional environment",
        "lighting": "Cinematic natural lighting, some dramatic backlighting, depth of field",
        "people": "Realistic professionals, diverse team, authentic expressions",
        "colors": "Warm earth tones with technical blue accents, professional palette",
        "style": "Photorealistic cinematography, not animated or cartoonish",
        "recurring_elements": [
            "Computers/monitors with code or visualizations",
            "Teams collaborating",
            "Progress indicators (charts, checkmarks)",
            "Architecture diagrams and blueprints",
        ],
        "mood_progression": [
            "Confusion/chaos → Discovery → Clarity → Triumph → Vision",
        ]
    }
    
    visual_anchors = {
        "main_character": "A software developer, mid-30s, diverse, focused expression",
        "environment": "Tech startup office with glass walls, natural light",
        "props": "Laptop, multiple monitors, notebook, coffee cup",
        "color_scheme": "Warm skin tones, cool blue technical accents, green for success",
    }
    
    return {
        "story_elements": story_elements,
        "visual_anchors": visual_anchors,
    }


def generate_grounded_prompt(segment, scene, story_data, frame_num):
    """Generate a story-grounded, consistent image prompt."""
    
    emotion = segment.get("emotion", "neutral")
    
    # Story-grounded prompts with consistent visual anchors
    all_prompts = {
        1: [
            f"Stressed software developer in modern tech office, multiple monitors showing error code, professional lighting, photorealistic style, realistic professional, frustrated expression, cinematic portrait photography, 8k resolution",
            f"Chaotic desk with scattered code printouts, red error messages on screens, overwhelmed developer, office environment, professional lighting, photorealistic, stressed, professional cinematography",
            f"Developer looking at blank screen with no clear direction, hopeful but confused, tech startup environment, natural light from windows, photorealistic, cinematic depth of field",
            f"Developer having realization moment, light bulb icon above head, developer, tech office environment, dramatic lighting, photorealistic, excited, epic shot",
        ],
        2: [
            f"Eureka moment in tech office, developer seeing blueprint, modern office, professional lighting, photorealistic style, curious",
            f"Architectural diagram or specification document in hands, developer studying it, modern office, professional lighting, photorealistic style, contemplative, cinematic",
            f"Feedback loop visualization as glowing circuit or flow, tech environment, professional lighting, photorealistic style, enlightened, digital-physical blend",
            f"Developer with AI agent visualization, tech environment, tech aesthetic, professional lighting, photorealistic style, confident, success visualization",
        ],
        3: [
            f"Three pillars or logos (OpenAI LangChain Anthropic), tech office, professional lighting, photorealistic style, confident, corporate epic",
            f"Code flowing through verification gates with green checkmarks, tech office, professional lighting, photorealistic style, methodical",
            f"Progress staircase or feature list building, developer watching, tech office, professional lighting, photorealistic style, accomplished",
            f"Self-verification loop with checkmarks passing, tech office, professional lighting, photorealistic style, successful",
        ],
        4: [
            f"Level 4 autonomy rocket launching, developer watching, tech office, professional lighting, photorealistic style, triumphant, epic wide shot",
            f"Hierarchical layer visualization (planning/implementation/verification), tech office, professional lighting, photorealistic style, transformational, layered composition",
            f"Human at command center, AI agents executing below, orchestration visualization, tech office, professional lighting, photorealistic style, paradigm-shift",
            f"Agent delivering completed PR or code, celebration moment, tech office, professional lighting, photorealistic style, celebrating, success",
        ],
        5: [
            f"Beautiful specification blueprint as art, developer creating, tech office, professional lighting, photorealistic style, visionary",
            f"Feedback rivers or harness bridges as visualization, tech office, professional lighting, photorealistic style, flowing",
            f"Observability dashboard glowing, developer monitoring, tech office, professional lighting, photorealistic style, controlling",
            f"Open horizon with AI agent army ready, developer as commander, tech office environment, sunrise lighting, photorealistic style, empowered, future vision",
        ],
    }
    
    key = scene
    if key in all_prompts and frame_num <= len(all_prompts[key]):
        return all_prompts[key][frame_num - 1]
    
    return f"Professional tech scene with developer, modern office, photorealistic style"


def generate_scene_prompts(scene_num):
    """Generate the full set of grounded prompts for a scene."""
    
    story_data = analyze_story()
    scene = SCENES[scene_num]
    
    prompts = []
    for i, segment in enumerate(scene["segments"], 1):
        prompt = generate_grounded_prompt(segment, scene_num, story_data, i)
        prompts.append({
            "segment_text": segment["text"],
            "emotion": segment.get("emotion"),
            "frame": i,
            "prompt": prompt
        })
    
    return {
        "scene": scene_num,
        "title": scene["title"],
        "story_data": story_data,
        "prompts": prompts
    }


def generate_all_prompts():
    """Generate prompts for all scenes."""
    all_prompts = {}
    for scene_num in range(1, 6):
        all_prompts[f"scene{scene_num}"] = generate_scene_prompts(scene_num)
    return all_prompts


def main():
    parser = argparse.ArgumentParser(description="Story-grounded image prompts")
    parser.add_argument("--scene", "-s", type=int, help="Scene number (1-5)")
    parser.add_argument("--all", "-a", action="store_true", help="All scenes")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--script", help="Custom script to analyze")
    args = parser.parse_args()
    
    if args.script:
        print("Custom script analysis not implemented - using scene data")
    
    if args.all:
        results = generate_all_prompts()
    elif args.scene:
        results = {"scene": args.scene, **generate_scene_prompts(args.scene)}
    else:
        # Default: all scenes
        results = generate_all_prompts()
    
    output = args.output or "story_prompts.json"
    with open(output, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Saved to {output}")
    
    if args.all or not args.scene:
        for key, data in results.items():
            print(f"\n=== {key}: {data.get('title', '')} ===")
            for p in data.get("prompts", []):
                print(f"  Frame {p['frame']}: {p['prompt'][:70]}...")


if __name__ == "__main__":
    main()