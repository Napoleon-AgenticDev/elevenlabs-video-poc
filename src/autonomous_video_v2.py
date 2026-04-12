#!/usr/bin/env python3
"""
Autonomous Video Generator - Full Pipeline v2
===============================================
Fully autonomous - NO human intervention required.

Uses:
- ElevenLabs TTS (voice) ✓
- ElevenLabs Music (background) ✓  
- Gemini 2.5 Flash Image (images) ✓

Run: python autonomous_video_v2.py --all
"""

import os
import sys
import json
import base64
import subprocess
import argparse
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "kPzsL2i3teMYv0FxEYQ6")  # From .env

# Gemini model for images - using v1beta
GEMINI_MODEL = "gemini-2.5-flash-image"

SCENES = {
    1: {
        "title": "The Problem",
        "script": "Every developer knows this feeling. You're building an AI system, and it starts spiraling out of control. Code everywhere. No direction. Tests failing. Sound familiar?",
        "segments": [
            "Every developer knows this feeling.",
            "You're building an AI system, and it starts spiraling out of control.",
            "Code everywhere. No direction. Tests failing.",
            "Sound familiar?"
        ],
        "music_mood": "stressed electronic conflict"
    },
    2: {
        "title": "The Discovery",
        "script": "What if there was a better way? What if you could design the specifications that guide your AI? Enter... harness engineering.",
        "segments": [
            "What if there was a better way?",
            "What if you could design the specifications?",
            "Enter... harness engineering."
        ],
        "music_mood": "hopeful discovery building"
    },
    3: {
        "title": "The Solution",
        "script": "Three companies cracked the code. OpenAI, LangChain, and Anthropic. Self-verification before exit. Incremental progress.",
        "segments": [
            "Three companies cracked the code.",
            "OpenAI, LangChain, and Anthropic.",
            "Self-verification before exit."
        ],
        "music_mood": "triumphant building achieving"
    },
    4: {
        "title": "The Impact",
        "script": "Level four autonomy achieved. The shift: humans design systems, agents execute. The results speak for themselves.",
        "segments": [
            "Level four autonomy achieved.",
            "The shift: humans design systems, agents execute.",
            "The results speak for themselves."
        ],
        "music_mood": "epic triumphant success"
    },
    5: {
        "title": "The Future",
        "script": "The future isn't about writing more code. It's about creating better specifications. Are you ready to guide them?",
        "segments": [
            "The future isn't about writing more code.",
            "It's about creating better specifications.",
            "Are you ready to guide them?"
        ],
        "music_mood": "visionary hopeful inspiring"
    },
}


def check_deps():
    """Install required dependencies."""
    try:
        import google.genai
    except ImportError:
        print("Installing google-genai...")
        subprocess.run([sys.executable, "-m", "pip", "install", "google-genai", "-q"], check=True)
    try:
        import elevenlabs
    except ImportError:
        print("Installing elevenlabs...")
        subprocess.run([sys.executable, "-m", "pip", "install", "elevenlabs", "-q"], check=True)


def generate_voice(text, output_path):
    """Generate voice using ElevenLabs."""
    import requests
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_KEY}
    data = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.3, "similarity_boost": 0.8, "style": 0.4}
    }
    
    print(f"  Generating voice...")
    response = requests.post(url, json=data, headers=headers, timeout=60)
    
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"    Voice saved: {output_path}")
        return output_path
    else:
        print(f"    Voice error: {response.status_code}")
        return None


def generate_music(mood, duration_ms, output_path):
    """Generate background music using ElevenLabs Music API."""
    from elevenlabs.client import ElevenLabs
    
    print(f"  Generating music...")
    try:
        client = ElevenLabs(api_key=ELEVENLABS_KEY)
        
        audio = client.music.compose(
            prompt=mood,
            music_length_ms=duration_ms,
            force_instrumental=True
        )
        
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"    Music saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"    Music error: {e}")
        return None


def generate_image_gemini(prompt, output_path):
    """Generate image using Gemini 2.5 Flash Image."""
    import requests
    
    print(f"  Generating image...")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        response = requests.post(url, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            # Look for image in response
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        image_data = part["inlineData"]["data"]
                        image_bytes = base64.b64decode(image_data)
                        
                        with open(output_path, "wb") as f:
                            f.write(image_bytes)
                        
                        # Resize
                        img = Image.open(output_path)
                        img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                        img.save(output_path)
                        
                        print(f"    Image saved: {output_path}")
                        return output_path
            
            print(f"    No image in response: {result}")
        else:
            print(f"    API error: {response.status_code} - {response.text[:150]}")
    except Exception as e:
        print(f"    Image error: {e}")
    
    return None


def add_cc_text(image_path, text, output_path):
    """Add CC subtitle overlay."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((1280, 720))
    draw = ImageDraw.Draw(img)
    
    # Semi-transparent box
    draw.rectangle([40, 610, 1240, 800], fill=(0, 0, 0, 180))
    
    # Word wrap
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
    for l in lines[:2]:
        draw.text((60, y), l, fill='white')
        y += 30
    
    img.save(output_path)
    print(f"    CC saved: {output_path}")


def create_video(image_dir, audio_path, music_path, output_path):
    """Create video with FFmpeg."""
    cc_images = sorted(Path(image_dir).glob("*_cc.png"))
    if not cc_images:
        print(f"    No images")
        return None
    
    cmd = ["ffmpeg", "-y"]
    for img in cc_images:
        cmd.extend(["-loop", "1", "-t", "4", "-i", str(img)])
    cmd.extend(["-i", str(audio_path)])
    cmd.extend(["-i", str(music_path)])
    
    n = len(list(cc_images))
    
    # Mix voice (70%) with music (30%)
    cmd.extend([
        "-filter_complex",
        f"[{n}:a]volume=0.7[voice];[{n+1}:a]volume=0.3[music];[voice][music]amix=inputs=2:duration=first[outa]",
        "-map", "0:v", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(output_path)
    ])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"    Video saved: {output_path}")
        return output_path
    else:
        print(f"    Video error")
        return None


def process_scene(scene_num):
    """Process a single scene fully autonomously."""
    scene = SCENES[scene_num]
    output_dir = Path(f"output_v2/scene{scene_num}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== Scene {scene_num}: {scene['title']} ===")
    
    # 1. Voice
    audio_path = output_dir / "voice.mp3"
    if not audio_path.exists():
        generate_voice(scene["script"], audio_path)
    else:
        print(f"  Voice exists")
    
    # 2. Music  
    music_path = output_dir / "music.mp3"
    if not music_path.exists():
        generate_music(scene["music_mood"], 15000, music_path)
    else:
        print(f"  Music exists")
    
    # 3. Images
    image_dir = output_dir / "images"
    image_dir.mkdir(exist_ok=True)
    
    for i, segment in enumerate(scene["segments"], 1):
        cc_path = image_dir / f"frame_{i}_cc.png"
        
        if not cc_path.exists():
            # Generate contextual prompt
            prompt = (
                f"Professional software developer in modern tech office during '{scene['title'].lower()}' scenario. "
                f"Scene: {segment[:50]}. Photorealistic, cinematic lighting, widescreen, "
                f"professional quality, realistic, not animated"
            )
            
            raw_path = image_dir / f"frame_{i}.png"
            img_result = generate_image_gemini(prompt, raw_path)
            if img_result:
                add_cc_text(raw_path, segment, cc_path)
        else:
            print(f"  Frame {i} exists")
    
    # 4. Video
    video_path = output_dir / f"video_{scene_num}.mp4"
    if not video_path.exists():
        create_video(image_dir, audio_path, music_path, video_path)
    else:
        print(f"  Video exists")
    
    print(f"  Scene {scene_num} done!")
    return video_path


def main():
    check_deps()
    
    parser = argparse.ArgumentParser(description="Autonomous Video Generator v2")
    parser.add_argument("--scene", "-s", type=int)
    parser.add_argument("--all", "-a", action="store_true")
    args = parser.parse_args()
    
    scenes = [args.scene] if args.scene else (range(1, 6) if args.all else [1])
    
    Path("output_v2").mkdir(exist_ok=True)
    
    videos = []
    for scene_num in scenes:
        video = process_scene(scene_num)
        if video:
            videos.append(video)
    
    # Concatenate
    if len(videos) > 1:
        print(f"\n=== Concatenating ===")
        concat_file = Path("output_v2/concat.txt")
        with open(concat_file, "w") as f:
            for v in videos:
                f.write(f"file '{v}'\n")
        
        full = Path("output_v2/full_video.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_file), "-c", "copy", str(full)
        ])
        print(f"  Full video: {full}")
    
    print(f"\nDone! Output in output_v2/")


if __name__ == "__main__":
    main()