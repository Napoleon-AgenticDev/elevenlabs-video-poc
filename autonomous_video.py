#!/usr/bin/env python3
"""
Autonomous Video Generator - Full Pipeline
=======================================
Generates complete videos WITHOUT human intervention.

Uses:
- ElevenLabs TTS (voice) - WORKING
- ElevenLabs Music (background) - WORKING  
- OpenAI or alternative (images) - Try best available

Run: python autonomous_video.py --topic "Your Topic"
"""

import os
import sys
import requests
import json
import time
import base64
import subprocess
import argparse
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Voice ID - stored in .env as ELEVENLABS_VOICE_ID
# Default: Brittney (Social Media Voice)
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "kPzsL2i3teMYv0FxEYQ6")

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


def check_and_install_deps():
    """Ensure dependencies are installed."""
    try:
        import elevenlabs
    except ImportError:
        print("Installing elevenlabs...")
        subprocess.run([sys.executable, "-m", "pip", "install", "elevenlabs", "-q"])
    print("  Dependencies ready.")


def generate_voice(text, output_path):
    """Generate voice using ElevenLabs."""
    print(f"  Generating voice...")
    
    url = f"https://api.elevenlabs.io/v1/text_to_speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_KEY}
    data = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.3, "similarity_boost": 0.8, "style": 0.4}
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=60)
    
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"    Voice: {output_path}")
        return output_path
    else:
        print(f"    Voice error: {response.status_code}")
        return None


def generate_background_music(mood, duration_ms, output_path):
    """Generate background music using ElevenLabs Music API."""
    print(f"  Generating music...")
    
    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=ELEVENLABS_KEY)
        
        audio = client.music.compose(
            prompt=mood,
            music_length_ms=duration_ms,
            force_instrumental=True
        )
        
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"    Music: {output_path}")
        return output_path
    except Exception as e:
        print(f"    Music error: {e}")
        return None


def generate_image_fallback(prompt, output_path):
    """Generate image - tries multiple APIs."""
    
    # Try OpenAI first
    if OPENAI_KEY:
        try:
            import requests
            url = "https://api.openai.com/v1/images/generations"
            headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
            data = {"model": "gpt-image-1", "prompt": prompt, "size": "1024x1024"}
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                b64 = result["data"][0]["b64_json"]
                
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"    Image (OpenAI): {output_path}")
                return output_path
        except Exception as e:
            print(f"    OpenAI error: {e}")
    
    print(f"    No image API available. Using placeholder.")
    return create_placeholder_image(prompt, output_path)


def create_placeholder_image(prompt, output_path):
    """Create a placeholder image with text."""
    img = Image.new('RGB', (1024, 1024), color=(30, 30, 50))
    draw = ImageDraw.Draw(img)
    
    prompt_short = prompt[:50] + "..." if len(prompt) > 50 else prompt
    draw.text((100, 500), prompt_short, fill='white')
    draw.text((100, 550), "(Generate in ElevenLabs Studio)", fill='gray')
    
    img.save(output_path)
    print(f"    Placeholder: {output_path}")
    return output_path


def add_cc_to_image(image_path, text, output_path):
    """Add CC text overlay."""
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
    for l in lines[:2]:
        draw.text((60, y), l, fill='white')
        y += 30
    
    img.save(output_path)


def create_video(image_dir, audio_path, music_path, output_path):
    """Create final video with FFmpeg."""
    
    cc_images = sorted(Path(image_dir).glob("*_cc.png"))
    if not cc_images:
        print(f"    No CC images found")
        return None
    
    # Build FFmpeg command
    cmd = ["ffmpeg", "-y"]
    for img in cc_images:
        cmd.extend(["-loop", "1", "-t", "4", "-i", str(img)])
    cmd.extend(["-i", str(audio_path)])
    cmd.extend(["-i", str(music_path)])
    
    n = len(list(cc_images))
    
    # Mix voice with music
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
        print(f"    Video: {output_path}")
        return output_path
    else:
        print(f"    Video error: {result.stderr[:100]}")
        return None


def process_scene_autonomous(scene_num):
    """Fully autonomous scene processing."""
    scene = SCENES[scene_num]
    output_dir = Path(f"output_autonomous/scene{scene_num}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== Scene {scene_num}: {scene['title']} ===")
    
    # 1. Generate Voice
    audio_path = output_dir / "voice.mp3"
    if not audio_path.exists():
        generate_voice(scene["script"], audio_path)
    else:
        print(f"  Voice exists")
    
    # 2. Generate Music
    music_path = output_dir / "music.mp3"
    if not music_path.exists():
        generate_background_music(scene["music_mood"], 15000, music_path)
    else:
        print(f"  Music exists")
    
    # 3. Generate Images for each segment
    image_dir = output_dir / "images"
    image_dir.mkdir(exist_ok=True)
    
    for i, segment in enumerate(scene["segments"], 1):
        img_path = image_dir / f"frame_{i}.png"
        cc_path = image_dir / f"frame_{i}_cc.png"
        
        if not cc_path.exists():
            # Generate contextual prompt
            prompt = f"Professional software developer in modern tech office, {scene['title'].lower()} scene, photorealistic, cinematic lighting, {segment[:30]}..."
            
            generate_image_fallback(prompt, img_path)
            add_cc_to_image(img_path, segment, cc_path)
        else:
            print(f"  Frame {i} exists")
    
    # 4. Create video
    video_path = output_dir / f"video_{scene_num}.mp4"
    if not video_path.exists():
        create_video(image_dir, audio_path, music_path, video_path)
    else:
        print(f"  Video exists")
    
    print(f"  Scene {scene_num} complete!")
    return video_path


def main():
    import requests
    
    check_and_install_deps()
    
    parser = argparse.ArgumentParser(description="Autonomous Video Generator")
    parser.add_argument("--scene", "-s", type=int, help="Scene number")
    parser.add_argument("--all", "-a", action="store_true", help="All scenes")
    args = parser.parse_args()
    
    if args.all:
        scenes = range(1, 6)
    elif args.scene:
        scenes = [args.scene]
    else:
        scenes = range(1, 6)  # Default: all
    
    Path("output_autonomous").mkdir(exist_ok=True)
    
    for scene_num in scenes:
        process_scene_autonomous(scene_num)
    
    # Concatenate all videos
    print(f"\n=== Creating full video ===")
    full_path = Path("output_autonomous/full_video.mp4")
    
    # Simple concat
    concat_list = Path("output_autonomous/concat.txt")
    with open(concat_list, "w") as f:
        for i in scenes:
            video = Path(f"output_autonomous/scene{i}/video_{i}.mp4")
            if video.exists():
                f.write(f"file '{video}'\n")
    
    if concat_list.exists():
        result = subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
            "-i", str(concat_list), "-c", "copy", str(full_path)
        ], capture_output=True)
        
        if result.returncode == 0:
            print(f"  Full video: {full_path}")
    
    print(f"\nDone! Output in output_autonomous/")


if __name__ == "__main__":
    main()