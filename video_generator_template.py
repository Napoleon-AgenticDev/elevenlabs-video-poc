#!/usr/bin/env python3
"""
Video Generator - Complete Reusable Workflow
==========================================
Easily adapt this script for any topic by modifying the SCENES dict.

Usage:
    python video_generator_template.py --scene 1      # Generate single scene
    python video_generator_template.py --all            # Generate all scenes
"""

import os
import sys
import json
import base64
import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()

API_KEYS = {
    "elevenlabs": os.getenv("ELEVENLABS_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY")
}
VOICE_ID = "kPzsL2i3teMYv0FxEYQ6"  # Brittney

SCRIPT_DIR = Path(__file__).parent

# ============================================================================
# CONFIGURE YOUR TOPIC HERE
# ============================================================================

SCENES = {
    1: {
        "title": "The Problem",
        "script": "Every developer knows this feeling. You're building an AI system, and it starts spiraling out of control. Code everywhere. No direction. Tests failing. Sound familiar?",
        "segments": [
            {"text": "Every developer knows this feeling.", "start": 0.0, "end": 2.0},
            {"text": "You're building an AI system, and it starts spiraling out of control.", "start": 2.5, "end": 7.0},
            {"text": "Code everywhere.", "start": 8.0, "end": 9.5},
            {"text": "No direction. Tests failing.", "start": 10.0, "end": 12.5},
            {"text": "Sound familiar?", "start": 13.0, "end": 14.0},
        ],
        "image_prompts": [
            "Developer stressed at multiple monitors showing error messages, dark office night, cinematic lighting",
            "Chaotic code flying everywhere, red X marks, cluttered desk overwhelmed",
            "Developer looking confused at screen with no direction, hopeful eyes",
            "Developer having realization moment, light bulb above head",
        ]
    },
    2: {
        "title": "The Discovery",
        "script": "What if there was a better way? What if you could design the specifications that guide your AI? Enter... harness engineering.",
        "segments": [
            {"text": "What if there was a better way?", "start": 0.0, "end": 2.0},
            {"text": "What if you could design the specifications that guide your AI?", "start": 2.5, "end": 6.0},
            {"text": "Enter... harness engineering.", "start": 7.0, "end": 10.0},
        ],
        "image_prompts": [
            "Eureka moment with glowing blueprint, bright light",
            "Feedback loops glowing green, harness design concept art",
            "Developer holding specification document, modern tech office",
            "AI agents working autonomously with checkmarks, success",
        ]
    },
    3: {
        "title": "The Solution",
        "script": "Three companies cracked the code. OpenAI generated one million lines. LangChain improved by fourteen points. Anthropic solved with verification.",
        "segments": [
            {"text": "Three companies cracked the code.", "start": 0.0, "end": 2.0},
            {"text": "OpenAI generated one million lines of code.", "start": 2.5, "end": 6.0},
            {"text": "LangChain improved by fourteen percentage points.", "start": 7.0, "end": 10.0},
            {"text": "Anthropic solved with feature lists.", "start": 11.0, "end": 14.0},
        ],
        "image_prompts": [
            "Three glowing pillars OpenAI LangChain Anthropic",
            "Code flowing through verification gates, green checkmarks",
            "Feature lists building progress steps",
            "Self-verification loop passing, achievement",
        ]
    },
    4: {
        "title": "The Impact",
        "script": "The results speak for themselves. Level four autonomy achieved. The shift: humans design systems, agents execute.",
        "segments": [
            {"text": "The results speak for themselves.", "start": 0.0, "end": 2.0},
            {"text": "OpenAI reached level four autonomy.", "start": 2.5, "end": 5.5},
            {"text": "Agents that can go from prompt to PR.", "start": 6.0, "end": 9.0},
            {"text": "Humans don't write code anymore. They design systems.", "start": 10.0, "end": 14.0},
        ],
        "image_prompts": [
            "Level 4 autonomy rocket launching into space",
            "Sandwich layers glowing: planning implementation verification",
            "Human designing at command center, AI executing below",
            "Agent delivering completed PR, celebration",
        ]
    },
    5: {
        "title": "The Future",
        "script": "The future isn't about writing more code. It's about creating better specifications. Are you ready to guide them?",
        "segments": [
            {"text": "The future isn't about writing more code.", "start": 0.0, "end": 2.5},
            {"text": "It's about creating better specifications.", "start": 3.0, "end": 5.5},
            {"text": "Better feedback loops. Better harnesses.", "start": 6.0, "end": 9.0},
            {"text": "Are you ready to guide them?", "start": 10.0, "end": 13.0},
        ],
        "image_prompts": [
            "Developer creating beautiful specification blueprint art",
            "Feedback loops as glowing rivers, harness as bridge",
            "Observability dashboard glowing with metrics",
            "Open horizon with AI agent army ready, future arriving",
        ]
    },
}


# ============================================================================
# GENERATION FUNCTIONS
# ============================================================================

def generate_audio(scene_num, output_dir):
    """Generate audio using ElevenLabs v3"""
    scene = SCENES[scene_num]
    text = scene["script"]
    
    url = f"https://api.elevenlabs.io/v1/text_to_speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEYS["elevenlabs"]}
    data = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.8,
            "style": 0.4
        }
    }
    
    print(f"  Generating audio...")
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    output_file = output_dir / f"scene{scene_num}.mp3"
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"    Saved: {output_file}")
    return output_file


def generate_images(scene_num, output_dir):
    """Generate 4 images using OpenAI GPT Image"""
    scene = SCENES[scene_num]
    prompts = scene["image_prompts"]
    
    url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {API_KEYS['openai']}"}
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, prompt in enumerate(prompts, 1):
        if (output_dir / f"frame_{i}.png").exists():
            print(f"  Skipping frame {i} (exists)")
            continue
            
        print(f"  Generating frame {i}...")
        data = {"model": "gpt-image-1", "prompt": prompt, "size": "1024x1024"}
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        b64 = result["data"][0]["b64_json"]
        
        output_file = output_dir / f"frame_{i}.png"
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"    Saved: {output_file}")


def add_cc_subtitles(image_dir, scene_num):
    """Add CC subtitles to images"""
    scene = SCENES[scene_num]
    segments = scene["segments"]
    
    for i, segment in enumerate(segments, 1):
        image_path = image_dir / f"frame_{i}.png"
        if not image_path.exists():
            continue
            
        output_path = image_dir / f"frame_{i}_cc.png"
        
        img = Image.open(image_path).resize((1280, 720))
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([40, 610, 1240, 800], fill=(0, 0, 0, 180))
        
        text = segment["text"]
        words = text.split()
        lines = []
        line = ''
        for word in words:
            test = line + ' ' + word if line else word
            if len(test) < 55:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        
        y = 635
        for line in lines[:2]:
            draw.text((60, y), line, fill='white')
            y += 30
        
        img.save(output_path)
        print(f"  CC: {output_path}")


def create_video(scene_num, output_dir):
    """Create final video using FFmpeg"""
    audio_file = output_dir / f"scene{scene_num}.mp3"
    image_dir = output_dir / "images" / f"scene{scene_num}"
    
    if not audio_file.exists():
        print(f"  Audio not found: {audio_file}")
        return
    
    output_file = output_dir / f"final_scene{scene_num}.mp4"
    
    frames = [str(image_dir / f"frame_{i}_cc.png") for i in range(1, 5)]
    valid_frames = [f for f in frames if Path(f).exists()]
    
    if not valid_frames:
        print(f"  No CC frames found")
        return
    
    cmd = ["ffmpeg", "-y"]
    
    for frame in valid_frames:
        cmd.extend(["-loop", "1", "-t", "3.5", "-i", frame])
    
    cmd.extend(["-i", str(audio_file)])
    
    n = len(valid_frames)
    filter_complex = "[0:v]"
    for i in range(1, n):
        filter_complex += f"[{i}:v]"
    filter_complex += f"concat=n={n}:v=1:a=0[out];[out]scale=1280:720[out2]"
    
    cmd.extend(["-filter_complex", filter_complex])
    cmd.extend(["-map", "[out2]"])
    cmd.extend(["-map", f"{n}:a"])
    cmd.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "23"])
    cmd.extend(["-c:a", "aac", "-b:a", "128k"])
    cmd.extend(["-shortest"])
    cmd.append(str(output_file))
    
    print(f"  Creating video...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"    Saved: {output_file}")
    else:
        print(f"    Error: {result.stderr[:200]}")


def process_scene(scene_num):
    """Process a single scene through the full pipeline"""
    output_dir = Path("output")
    image_dir = output_dir / "images" / f"scene{scene_num}"
    
    print(f"\n=== Scene {scene_num}: {SCENES[scene_num]['title']} ===")
    
    generate_audio(scene_num, output_dir)
    generate_images(scene_num, image_dir)
    add_cc_subtitles(image_dir, scene_num)
    create_video(scene_num, output_dir)
    
    print(f"  Done!")


def main():
    import requests
    
    parser = argparse.ArgumentParser(description="Video Generator")
    parser.add_argument("--scene", "-s", type=int, help="Scene number (1-5)")
    parser.add_argument("--all", "-a", action="store_true", help="Process all scenes")
    args = parser.parse_args()
    
    if args.all:
        for i in range(1, 6):
            process_scene(i)
    elif args.scene:
        process_scene(args.scene)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()