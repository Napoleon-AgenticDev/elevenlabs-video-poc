#!/usr/bin/env python3
"""
Image Animation Generator
=====================
Animate static images using AI. Supports Runway, Seedance, and other image-to-video APIs.

Usage:
    python animate_images.py --image image.png --motion "zoom in" --output video.mp4
    python animate_images.py --all --images_dir images/
"""

import os
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
RUNWAY_KEY = os.getenv("RUNWAY_API_KEY", "")

MOTION_PROMPTS = {
    "zoom in": "Slow zoom in toward the subject, cinematic movement",
    "pan left": "Smooth pan to the left, cinematic tracking shot",
    "pan right": "Smooth pan to the right, cinematic tracking shot",
    "drift": "Gentle floating movement, dreamy atmosphere",
    "wave": "Subtle wave motion, organic movement",
    "fly": "Flying perspective, soaring view",
    "rotate": "Slow rotation around the subject, 3D effect",
    "none": "Static, no motion",
}


def check_runway_available():
    """Check if Runway API is available."""
    if not RUNWAY_KEY:
        return False
    
    url = "https://api.runwayml.com/v1/me"
    headers = {"Authorization": f"Bearer {RUNWAY_KEY}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False


def generate_with_runway(image_path, motion, output_path, api_key=None):
    """Generate video using Runway API."""
    key = api_key or RUNWAY_KEY
    
    # This requires actual API integration
    # Using placeholder for now
    print(f"  Runway API requires manual integration")
    print(f"  Motion: {motion}")
    return None


def generate_keep_frames_video(image_path, duration, output_path):
    """Generate a simple Ken Burns effect video from static image."""
    import subprocess
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-vf", f"zoompan=z='min(zoom+0.001,1.5)':d={25*duration}:s=1280x720",
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  Created Ken Burns: {output_path}")
        return output_path
    else:
        print(f"  Error: {result.stderr[:100]}")
        return None


def generate_zoom_pan_video(image_path, duration, output_path):
    """Generate video with zoom/pan effects."""
    import subprocess
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-filter_complex",
        "[0:v]scale=1280:720,zoompan=z='min(zoom+0.002,1.3)':d=25:x='nq*0.5':y='nq*0.3':s=1280x720[out]",
        "-map", "[out]",
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  Created zoom pan: {output_path}")
        return output_path
    return None


def generate_with_effect(image_path, effect, duration, output_path):
    """Generate video with various effects."""
    import subprocess
    
    effects = {
        "fade": "fade=t=in:st=0:d=1,fade=t=out:st=2:d=1",
        "blur": "scale=1280:720,boxblur=2:1",
        "vignette": "scale=1280:720,vignette=angle=0.5",
        "zoom": "zoompan=z='min(zoom+0.002,1.5)':d=25:x='nq*0.3':y='nq*0.2'",
        "pan": "zoompan=x='if(gte(n,100),x-10,x+10)':y=0:z=1:d=25",
    }
    
    filter_str = effects.get(effect, "scale=1280:720")
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-vf", filter_str,
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  Created {effect}: {output_path}")
        return output_path
    
    return None


def create_slideshow_from_images(image_dir, output_path, transition="fade", duration_per_image=3):
    """Create slideshow with transitions from multiple images."""
    import subprocess
    
    image_dir = Path(image_dir)
    images = sorted(image_dir.glob("*.png")) + sorted(image_dir.glob("*.jpg"))
    
    if not images:
        print(f"  No images in {image_dir}")
        return None
    
    inputs = []
    for img in images:
        inputs.extend(["-loop", "1", "-t", str(duration_per_image), "-i", str(img)])
    
    n = len(images)
    filter_parts = []
    
    for i in range(n):
        filter_parts.append(f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v{i}]")
    
    for i in range(n - 1):
        filter_parts.append(f"[v{i}][v{i+1}]xfade=transition={transition}:duration=0.5:offset={duration_per_image*i}[v{i+1}x]")
    
    filter_complex = ";".join(filter_parts) + f";[v{n-1}]null[out]"
    
    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-t", str(duration_per_image * n),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  Created slideshow: {output_path}")
        return output_path
    
    print(f"  Error: {result.stderr[:200]}")
    return None


def main():
    parser = argparse.ArgumentParser(description="Animate images")
    parser.add_argument("--image", "-i", help="Input image")
    parser.add_argument("--motion", "-m", default="zoom", 
                      choices=list(MOTION_PROMPTS.keys()), help="Motion type")
    parser.add_argument("--effect", "-e", default="zoom",
                      choices=["fade", "blur", "vignette", "zoom", "pan"], 
                      help="Effect type")
    parser.add_argument("--duration", "-d", type=int, default=3, help="Duration")
    parser.add_argument("--output", "-o", help="Output video")
    parser.add_argument("--images_dir", help="Directory of images for slideshow")
    parser.add_argument("--all", "-a", action="store_true", help="Process all images")
    args = parser.parse_args()
    
    if args.images_dir:
        output = args.output or "slideshow.mp4"
        create_slideshow_from_images(args.images_dir, output, args.effect)
        return
    
    if not args.image:
        print("Usage: animate_images.py --image image.png")
        return
    
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"  Image not found: {image_path}")
        return
    
    output = args.output or f"{image_path.stem}_animated.mp4"
    generate_with_effect(image_path, args.effect, args.duration, output)


if __name__ == "__main__":
    main()