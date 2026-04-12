#!/usr/bin/env python3
"""
ElevenLabs Image Generator
======================
Generate images using ElevenLabs Image API (via Studio API).

Usage:
    python generate_images_eleven.py --prompt "a developer at computer"
    python generate_images_eleven.py --use_prompts story_prompts.json
    python generate_images_eleven.py --scene 1
"""

import os
import json
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")


def generate_image(prompt, output_path, model="flux-1-dev", width=1024, height=1024):
    """Generate image using ElevenLabs Image API."""
    
    # Try the image generation endpoint
    url = "https://api.elevenlabs.io/v1/generate-image"
    headers = {
        "xi-api-key": ELEVENLABS_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model_id": model,
        "width": width,
        "height": height
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result.get("data", [{}])[0].get("url")
            
            if image_url:
                img_resp = requests.get(image_url)
                with open(output_path, "wb") as f:
                    f.write(img_resp.content)
                print(f"  Saved: {output_path}")
                return output_path
        else:
            print(f"  Error: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"  Exception: {e}")
    
    return None


def generate_with_elevenlabs_client(prompt, output_path):
    """Generate using the ElevenLabs Python client."""
    try:
        from elevenlabs.client import ElevenLabs
        
        client = ElevenLabs(api_key=ELEVENLABS_KEY)
        
        # Try image generation via client
        result = client.image.generate(
            prompt=prompt,
            model="flux-1-dev"
        )
        
        if result:
            with open(output_path, "wb") as f:
                f.write(result.content)
            print(f"  Saved via client: {output_path}")
            return output_path
    except Exception as e:
        print(f"  Client error: {e}")
    
    return None


def generate_with_ playground_api(prompt, output_path):
    """Try using the ElevenLabs Creative Studio API."""
    
    # This is the Studio API approach
    url = "https://api.elevenlabs.io/v1/image/generate"
    headers = {
        "xi-api-key": ELEVENLABS_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "flux-1-dev",
        "aspect_ratio": "16:9",
        "quality": "high"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            image_data = result.get("image")
            
            if image_data:
                import base64
                img_bytes = base64.b64decode(image_data)
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  Saved: {output_path}")
                return output_path
        else:
            print(f"  Status: {response.status_code}")
    except Exception as e:
        print(f"  API error: {e}")
    
    return None


def add_cc_text(image_path, text, output_path):
    """Add CC subtitle text to image."""
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


def main():
    parser = argparse.ArgumentParser(description="Generate images with ElevenLabs")
    parser.add_argument("--prompt", "-p", help="Image prompt")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--scene", "-s", type=int, help="Scene number from story_prompts.json")
    parser.add_argument("--use_prompts", "-f", help="JSON file with prompts")
    parser.add_argument("--add_cc", action="store_true", help="Add CC text")
    parser.add_argument("--model", "-m", default="flux-1-dev", help="Model to use")
    args = parser.parse_args()
    
    if args.scene:
        with open("story_prompts.json") as f:
            data = json.load(f)
        
        scene_key = f"scene{args.scene}"
        if scene_key in data:
            scene_data = data[scene_key]
            prompts = scene_data.get("prompts", [])
            
            output_dir = Path(f"eleven_images/scene{args.scene}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for p in prompts:
                prompt = p.get("prompt", "")
                text = p.get("segment_text", "")
                frame = p.get("frame", 1)
                
                img_path = output_dir / f"frame_{frame}.png"
                
                print(f"Generating frame {frame}...")
                result = generate_image(prompt, img_path, args.model)
                
                if result and args.add_cc:
                    cc_path = output_dir / f"frame_{frame}_cc.png"
                    print(f"  Adding CC...")
                    add_cc_text(result, text, cc_path)
    
    elif args.use_prompts:
        with open(args.use_prompts) as f:
            data = json.load(f)
        
        output_dir = Path("eleven_images")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for key, scene_data in data.items():
            prompts = scene_data.get("prompts", [])
            
            for p in prompts:
                prompt = p.get("prompt", "")
                text = p.get("segment_text", "")
                frame = p.get("frame", 1)
                
                img_path = output_dir / f"{key}_frame_{frame}.png"
                
                print(f"Generating {key} frame {frame}...")
                result = generate_image(prompt, img_path, args.model)
                
                if result and args.add_cc:
                    cc_path = output_dir / f"{key}_frame_{frame}_cc.png"
                    print(f"  Adding CC...")
                    add_cc_text(result, text, cc_path)
    
    elif args.prompt:
        output = args.output or "eleven_image.png"
        generate_image(args.prompt, output, args.model)
    
    else:
        print("Usage:")
        print("  python generate_images_eleven.py --prompt 'your prompt'")
        print("  python generate_images_eleven.py --scene 1 --add_cc")
        print("  python generate_images_eleven.py --use_prompts story_prompts.json")


if __name__ == "__main__":
    main()