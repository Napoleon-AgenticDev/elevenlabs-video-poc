#!/usr/bin/env python3
"""
Image Generator for Video Scenes

Generates AI images for each scene using OpenAI's gpt-image-1 or DALL-E 3
then adds text overlays for video.

Usage:
    # Generate all 5 scene images
    python generate_images.py --openai-key YOUR_KEY
    
    # Generate specific scene
    python generate_images.py --scene 1 --openai-key YOUR_KEY
    
    # Add text overlay to existing images
    python add_text_overlay.py --scene 1 --title "The Problem"
"""

import argparse
import os
import requests
from pathlib import Path

# Scene configurations
SCENES = {
    1: {
        "title": "The Problem",
        "prompt": """Chaos and disorder visualization: scattered code snippets floating in disarray, 
broken connections, warning symbols, red accent colors mixed with dark background, 
frustrating messy situation, abstract representation of code gone wrong, 
dark navy to deep red gradient, professional presentation style, no text"""
    },
    2: {
        "title": "The Discovery",
        "prompt": """Eureka moment visualization: a bright light illuminating a clear path through complexity, 
blueprint or map emerging from darkness, GPS navigation style, guiding path forward, 
hope and clarity, cyan glow leading the way, dark background with spotlight effect, 
professional presentation style, no text"""
    },
    3: {
        "title": "The Solution",
        "prompt": """Structure and architecture visualization: three pillars or foundation blocks standing strong,
connected nodes forming a network, organized system with clear boundaries, 
blueprints and specifications, building something great, cyan and purple pillars,
dark gradient background, professional presentation style, no text"""
    },
    4: {
        "title": "The Impact",
        "prompt": """Success and achievement visualization: rocketship or upward trajectory, 
trophy or medal concept, level progression steps climbing upward, 
achievement unlocked, green and cyan success colors, dark background,
professional presentation style, no text"""
    },
    5: {
        "title": "The Future",
        "prompt": """Future and possibility visualization: open road or path stretching to horizon,
light at the end of tunnel, sunrise or new dawn, connected network expanding,
possibility and potential, warm cyan to purple gradient, horizon with hope,
professional presentation style, no text"""
    }
}

MASTER_STYLE = """Create a professional tech presentation visual with the following style:
- Modern, sleek dark theme with deep navy (#0a0a1a) to purple (#1a0a2e) gradient background
- Abstract geometric shapes and patterns representing code, AI, and technology
- Soft glowing accents in cyan (#00d4ff) and purple (#7c3aed)
- Clean, minimalist design suitable for a video about software development/AI
- No text in the image - leave space for text overlay
- Professional quality suitable for a corporate/educational video
- Slight 3D depth effect with subtle shadows
- Aspect ratio: 16:9 (1280x720)"""

def generate_image(scene_num: int, api_key: str, output_dir: str = ".") -> str:
    """Generate image for a scene using OpenAI API"""
    
    scene = SCENES[scene_num]
    
    # Combine master style with scene-specific prompt
    full_prompt = f"{MASTER_STYLE}\n\nScene {scene_num} - {scene['title']}: {scene['prompt']}"
    
    url = "https://api.openai.com/v1/images/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-image-1",
        "prompt": full_prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    print(f"Generating image for Scene {scene_num}: {scene['title']}...")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    
    # Get image URL and download
    image_url = data["data"][0]["url"]
    
    # Download image
    img_response = requests.get(image_url)
    
    output_path = os.path.join(output_dir, f"scene{scene_num}_image.png")
    
    with open(output_path, "wb") as f:
        f.write(img_response.content)
    
    print(f"  Saved to: {output_path}")
    return output_path

def generate_with_dalle3(scene_num: int, api_key: str, output_dir: str = ".") -> str:
    """Generate image using DALL-E 3"""
    
    scene = SCENES[scene_num]
    full_prompt = f"{MASTER_STYLE}\n\nScene {scene_num} - {scene['title']}: {scene['prompt']}"
    
    url = "https://api.openai.com/v1/images/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "dall-e-3",
        "prompt": full_prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard"
    }
    
    print(f"Generating DALL-E 3 image for Scene {scene_num}...")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    image_url = data["data"][0]["url"]
    
    img_response = requests.get(image_url)
    output_path = os.path.join(output_dir, f"scene{scene_num}_image.png")
    
    with open(output_path, "wb") as f:
        f.write(img_response.content)
    
    print(f"  Saved to: {output_path}")
    return output_path

def add_text_overlay(image_path: str, title: str, subtitle: str = None, output_path: str = None):
    """Add text overlay to image using PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.open(image_path)
        
        # Resize to 1280x720 if needed
        if img.size != (1280, 720):
            img = img.resize((1280, 720), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fall back to default
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Draw title
        draw.text((640, 340), title, font=title_font, fill="white", anchor="mm")
        
        if subtitle:
            draw.text((640, 420), subtitle, font=subtitle_font, fill="#00d4ff", anchor="mm")
        
        if output_path is None:
            output_path = image_path.replace(".png", "_with_text.png")
        
        img.save(output_path)
        print(f"  Added text overlay: {output_path}")
        return output_path
        
    except ImportError:
        print("PIL not installed. Install with: pip install Pillow")
        return None
    except Exception as e:
        print(f"Error adding text: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate images for video scenes")
    parser.add_argument("--scene", type=int, choices=[1,2,3,4,5], help="Scene number (1-5)")
    parser.add_argument("--all", action="store_true", help="Generate all scenes")
    parser.add_argument("--openai-key", help="OpenAI API key")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument("--add-text", action="store_true", help="Add text overlay to images")
    parser.add_argument("--dalle3", action="store_true", help="Use DALL-E 3 instead of gpt-image-1")
    parser.add_argument("--title", help="Title for text overlay")
    parser.add_argument("--subtitle", help="Subtitle for text overlay")
    
    args = parser.parse_args()
    
    api_key = args.openai_key or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OpenAI API key required. Use --openai-key or set OPENAI_API_KEY environment variable")
        return
    
    if args.all:
        for i in range(1, 6):
            if args.dalle3:
                generate_with_dalle3(i, api_key, args.output_dir)
            else:
                generate_image(i, api_key, args.output_dir)
    elif args.scene:
        if args.dalle3:
            generate_with_dalle3(args.scene, api_key, args.output_dir)
        else:
            generate_image(args.scene, api_key, args.output_dir)
        
        if args.add_text and args.title:
            img_path = os.path.join(args.output_dir, f"scene{args.scene}_image.png")
            add_text_overlay(img_path, args.title, args.subtitle)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()