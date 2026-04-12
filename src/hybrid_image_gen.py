#!/usr/bin/env python3
"""
Hybrid Image Generator
=================
Can use ElevenLabs (via Studio) or OpenAI for images.

When ElevenLabs Image API becomes available via API, this will work:
- Set ELEVENLABS_API_KEY and use --elevenlabs flag
- Otherwise uses OpenAI (add credits when needed)

For now, use ElevenLabs Studio directly at:
https://elevenlabs.io/creative/playground

Workflow:
1. Copy prompts from story_prompts.json
2. Generate in ElevenLabs Studio
3. Download images to eleven_images/scene{N}/
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")


def generate_with_openai(prompt, output_path):
    """Generate using OpenAI (when credits available)."""
    import requests
    import base64
    
    url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
    data = {"model": "gpt-image-1", "prompt": prompt, "size": "1024x1024"}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            print(f"  OpenAI error: {response.text[:100]}")
            return None
        
        result = response.json()
        b64 = result["data"][0]["b64_json"]
        
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  Saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"  Error: {e}")
        return None


def add_cc_text(image_path, text, output_path):
    """Add CC subtitle text to image."""
    from PIL import Image, ImageDraw
    
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
    print(f"  CC added: {output_path}")


def create_video_from_images(image_dir, audio_file, output_file):
    """Create video with FFmpeg."""
    images = sorted(Path(image_dir).glob("*_cc.png"))
    
    if not images:
        print(f"  No CC images found in {image_dir}")
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


def print_prompts_for_studio():
    """Print prompts ready for ElevenLabs Studio."""
    
    if not Path("story_prompts.json").exists():
        print("Run create_story_prompts.py first")
        return
    
    with open("story_prompts.json") as f:
        data = json.load(f)
    
    print("\n" + "="*60)
    print("PROMPTS FOR ELEVENLABS STUDIO")
    print("="*60)
    print("\nGo to: https://elevenlabs.io/creative/playground")
    print("Select Image mode, then paste these prompts:\n")
    
    for key, scene_data in data.items():
        title = scene_data.get("title", key)
        prompts = scene_data.get("prompts", [])
        
        print(f"\n--- {title} ---")
        for p in prompts:
            print(f"Frame {p['frame']}: {p['prompt'][:100]}...")


def main():
    parser = argparse.ArgumentParser(description="Hybrid Image Generator")
    parser.add_argument("--scene", "-s", type=int, help="Scene number")
    parser.add_argument("--all", "-a", action="store_true", help="All scenes")
    parser.add_argument("--use_openai", action="store_true", help="Force OpenAI")
    parser.add_argument("--add_cc", action="store_true", help="Add CC text")
    parser.add_argument("--make_video", action="store_true", help="Create video")
    parser.add_argument("--print_prompts", action="store_true", help="Print prompts for Studio")
    args = parser.parse_args()
    
    if args.print_prompts:
        print_prompts_for_studio()
        return
    
    if args.all:
        scenes = range(1, 6)
    elif args.scene:
        scenes = [args.scene]
    else:
        print("Usage:")
        print("  python hybrid_image_gen.py --print_prompts")
        print("  python hybrid_image_gen.py --scene 1 --add_cc")
        print("  python hybrid_image_gen.py --scene 1 --make_video")
        return
    
    for scene_num in scenes:
        print(f"\n=== Scene {scene_num} ===")
        
        image_dir = Path(f"eleven_images/scene{scene_num}")
        
        if args.make_video:
            audio = f"spectacular_scene{scene_num}.mp3"
            if Path(audio).exists():
                create_video_from_images(image_dir, audio, f"final_scene{scene_num}.mp4")
            continue
        
        if not image_dir.exists():
            print(f"Images directory not found: {image_dir}")
            print("1. Run: python hybrid_image_gen.py --print_prompts")
            print("2. Go to ElevenLabs Studio and generate images")
            print(f"3. Put images in {image_dir}/ as frame_1.png, frame_2.png, etc.")
            continue
        
        if args.add_cc:
            import base64
            for img_path in sorted(image_dir.glob("frame_*.png")):
                if "_cc" in img_path.name:
                    continue
                
                # Find matching text
                stem = img_path.stem
                frame_num = int(stem.split("_")[-1])
                
                # Get text from prompts
                with open("story_prompts.json") as f:
                    data = json.load(f)
                
                scene_key = f"scene{scene_num}"
                if scene_key in data:
                    prompts = data[scene_key].get("prompts", [])
                    if frame_num - 1 < len(prompts):
                        text = prompts[frame_num - 1].get("segment_text", "")
                        cc_path = img_path.with_name(f"{stem}_cc.png")
                        add_cc_text(img_path, text, cc_path)


if __name__ == "__main__":
    main()