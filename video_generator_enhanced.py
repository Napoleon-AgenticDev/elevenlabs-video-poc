#!/usr/bin/env python3
"""
Enhanced Video Generator - V3
============================
Complete production pipeline with:
- Claude prompt enhancement
- ElevenLabs v3 audio
- OpenAI GPT Image  
- Background music (Mubert)
- Image animation/effects
- CC subtitles
- Transitions

Usage:
    python video_generator_enhanced.py --scene 1
    python video_generator_enhanced.py --all --with_music --animate
"""

import os
import sys
import json
import requests
import base64
import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()

API_KEYS = {
    "elevenlabs": os.getenv("ELEVENLABS_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    "mubert": os.getenv("MUBERT_TOKEN", ""),
}
VOICE_ID = "kPzsL2i3teMYv0FxEYQ6"

SCENES = {
    1: {
        "title": "THE PROBLEM",
        "script": "Every developer knows this feeling. You're building an AI system, and it starts spiraling out of control. Code everywhere. No direction. Tests failing. Sound familiar?",
        "concept": "developer stressed confused overwhelmed",
        "segments": [
            "Every developer knows this feeling.",
            "You're building an AI system, and it starts spiraling out of control.",
            "Code everywhere. No direction. Tests failing.",
            "Sound familiar?",
        ]
    },
    2: {
        "title": "THE DISCOVERY",
        "script": "What if there was a better way? What if you could design the specifications that guide your AI? Enter... harness engineering.",
        "concept": "eureka moment blueprint architecture",
        "segments": [
            "What if there was a better way?",
            "What if you could design the specifications?",
            "Enter... harness engineering.",
        ]
    },
    3: {
        "title": "THE SOLUTION",
        "script": "Three companies cracked the code. OpenAI, LangChain, and Anthropic. Self-verification before exit. Incremental progress over scope.",
        "concept": "three pillars verification progress",
        "segments": [
            "Three companies cracked the code.",
            "OpenAI, LangChain, and Anthropic.",
            "Self-verification before exit.",
            "Incremental progress over scope.",
        ]
    },
    4: {
        "title": "THE IMPACT",
        "script": "Level four autonomy achieved. The shift: humans design systems, agents execute. The results speak for themselves.",
        "concept": "autonomy achievement success",
        "segments": [
            "Level four autonomy achieved.",
            "The shift: humans design systems, agents execute.",
            "The results speak for themselves.",
        ]
    },
    5: {
        "title": "THE FUTURE",
        "script": "The future isn't about writing more code. It's about creating better specifications. Are you ready to guide them?",
        "concept": "future horizon AI army ready",
        "segments": [
            "The future isn't about writing more code.",
            "It's about creating better specifications.",
            "Are you ready to guide them?",
        ]
    },
}


def enhance_prompt(concept):
    """Enhance concept into 4 image prompts."""
    if API_KEYS.get("anthropic"):
        return enhance_with_claude(concept)
    elif API_KEYS.get("openai"):
        return enhance_with_chatgpt(concept)
    return enhance_local(concept)


def enhance_with_claude(concept):
    """Use Claude to enhance prompts."""
    from enhance_prompts import enhance_with_claude as clau
    return clau(concept, API_KEYS.get("anthropic"))


def enhance_with_chatgpt(concept):
    """Use ChatGPT to enhance prompts."""  
    from enhance_prompts import enhance_with_chatgpt as chat
    return chat(concept, API_KEYS.get("openai"))


def enhance_local(concept):
    """Local prompt enhancement."""
    concept_lower = concept.lower()
    return [
        f"{title}, cinematic lighting, professional photography, 8k highly detailed",
        f"{title}, dramatic lighting, emotional tone, highly detailed, photorealistic",
        f"{title}, wide shot, cinematic composition, professional",
        f"{title}, close-up detail, professional quality, highly detailed",
    ]


def generate_audio(text, output_file):
    """Generate voice using ElevenLabs v3."""
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
    response = requests.post(url, json=data, headers=headers, timeout=60)
    
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"  Audio: {output_file}")


def generate_image(prompt, output_file):
    """Generate image using OpenAI GPT Image."""
    url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {API_KEYS['openai']}"}
    data = {"model": "gpt-image-1", "prompt": prompt, "size": "1024x1024"}
    
    print(f"  Generating: {prompt[:40]}...")
    response = requests.post(url, headers=headers, json=data, timeout=60)
    result = response.json()
    b64 = result["data"][0]["b64_json"]
    
    with open(output_file, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"  Image: {output_file}")


def generate_music(duration, output_file, mood="cinematic"):
    """Generate background music using Mubert."""
    if not API_KEYS.get("mubert"):
        print(f"  No MUBERT_TOKEN, skipping music")
        return None
    
    from generate_music import generate_music as mubert
    return mubert(mood, duration, output_file, API_KEYS["mubert"])


def add_cc(image_path, text, output_path):
    """Add CC subtitles to image."""
    img = Image.open(image_path).resize((1280, 720))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([40, 610, 1240, 800], fill=(0, 0, 0, 180))
    
    words = text.split()
    lines, line = [], ''
    for word in words:
        test = line + ' ' + word if line else word
        if len(test) < 55:
            line = test
        else:
            lines.append(line)
            line = word
    if line: lines.append(line)
    
    y = 635
    for line_text in lines[:2]:
        draw.text((60, y), line_text, fill='white')
        y += 30
    
    img.save(output_path)


def create_video(image_dir, audio_file, output_file):
    """Create video with transitions."""
    images = sorted(Path(image_dir).glob("*_cc.png"))
    
    if not images:
        print(f"  No CC images found")
        return
    
    cmd = ["ffmpeg", "-y"]
    for img in images:
        cmd.extend(["-loop", "1", "-t", "3.5", "-i", str(img)])
    cmd.extend(["-i", str(audio_file)])
    
    n = len(list(images))
    cmd.extend([
        "-filter_complex", 
        f"[0:v][1:v][2:v][3:v]concat=n={n}:v=1:a=0[out];[out]scale=1280:720[out2]",
        "-map", "[out2]", "-map", f"{n}:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(output_file)
    ])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  Video: {output_file}")
    else:
        print(f"  Error: {result.stderr[:100]}")


def add_music_to_video(video_path, music_path, output_path):
    """Add background music to video."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(music_path),
        "-filter_complex", "[1:a]volume=0.3[music]",
        "-map", "0:v", "-map", "0:a", "-map", "[music]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  Final: {output_path}")
    else:
        print(f"  Error: {result.stderr[:100]}")


def process_scene(scene_num, with_music=False, animate=False):
    """Process a single scene."""
    scene = SCENES[scene_num]
    output_dir = Path(f"output_v3/scene{scene_num}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== Scene {scene_num}: {scene['title']} ===")
    
    audio_file = output_dir / "audio.mp3"
    if not audio_file.exists():
        generate_audio(scene["script"], audio_file)
    
    prompts = enhance_prompt(scene["concept"])
    
    image_dir = output_dir / "images"
    image_dir.mkdir(exist_ok=True)
    
    for i, prompt in enumerate(prompts[:4], 1):
        img_file = image_dir / f"frame_{i}.png"
        if not img_file.exists():
            generate_image(prompt, img_file)
        
        cc_file = image_dir / f"frame_{i}_cc.png"
        if not cc_file.exists() and i <= len(scene["segments"]):
            add_cc(img_file, scene["segments"][i-1], cc_file)
    
    video_file = output_dir / "video.mp4"
    if not video_file.exists():
        create_video(image_dir, audio_file, video_file)
    
    if with_music:
        music_file = output_dir / "music.mp3"
        if not music_file.exists():
            generate_music(15, music_file, "cinematic")
        
        final_file = output_dir / "final.mp4"
        if video_file.exists() and music_file.exists():
            add_music_to_video(video_file, music_file, final_file)
    
    print(f"  Done!")


def main():
    import requests
    
    parser = argparse.ArgumentParser(description="Enhanced Video Generator V3")
    parser.add_argument("--scene", "-s", type=int, help="Scene number")
    parser.add_argument("--all", "-a", action="store_true", help="All scenes")
    parser.add_argument("--music", "-m", action="store_true", help="Add background music")
    parser.add_argument("--animate", action="store_true", help="Add animations")
    args = parser.parse_args()
    
    if args.all:
        for i in range(1, 6):
            process_scene(i, args.music, args.animate)
    elif args.scene:
        process_scene(args.scene, args.music, args.animate)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()