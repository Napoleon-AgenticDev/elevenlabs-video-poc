#!/usr/bin/env python3
"""
Video Creator - Combine audio files with images to create video

This script creates a video by combining:
- Audio files (MP3) for each scene
- Image files (PNG/JPG) for each scene
- Text overlays for titles

Requirements:
    pip install Pillow requests

Usage:
    python create_video.py --audio-dir ./ --image-dir ./images/ --output video.mp4
"""

import argparse
import os
import subprocess
from pathlib import Path
from config import VOICES, DEFAULT_VOICE, get_voice

# Scene configuration - maps audio files to images and durations
SCENES = {
    "scene1": {
        "audio": "brittney_scene1.mp3",
        "image": "scene1_chaos.png",  # Image showing chaos/breaking code
        "title": "The Problem",
        "text": "Every developer knows this feeling...",
        "duration_offset": 0  # Start time offset
    },
    "scene2": {
        "audio": "brittney_scene2.mp3",
        "image": "scene2_discovery.png",  # Image showing lightbulm/idea
        "title": "The Discovery",
        "text": "What if there was a better way?",
        "duration_offset": 0
    },
    "scene3": {
        "audio": "brittney_scene3.mp3",
        "image": "scene3_solution.png",  # Image showing pillars/solution
        "title": "The Solution",
        "text": "Three companies cracked the code...",
        "duration_offset": 0
    },
    "scene4": {
        "audio": "brittney_scene4.mp3",
        "image": "scene4_impact.png",  # Image showing transformation
        "title": "The Impact",
        "text": "The results speak for themselves...",
        "duration_offset": 0
    },
    "scene5": {
        "audio": "brittney_scene5.mp3",
        "image": "scene5_future.png",  # Image showing future/road
        "title": "The Future",
        "text": "The agents are waiting...",
        "duration_offset": 0
    }
}

def get_audio_duration(audio_file: str) -> float:
    """Get duration of audio file in seconds using ffprobe"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
             "-of", "default=noprint_wrappers=1:nokey=1", audio_file],
            capture_output=True, text=True, check=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Warning: Could not get duration for {audio_file}: {e}")
        return 10.0  # Default fallback

def create_image_with_text(image_path: str, text: str, output_path: str, width: int = 1280, height: int = 720):
    """Create an image with text overlay using PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create gradient background
        img = Image.new('RGB', (width, height), color=(20, 20, 40))
        
        # Draw simple gradient
        draw = ImageDraw.Draw(img)
        for i in range(height):
            color = int(20 + (i / height) * 30)
            draw.line([(0, i), (width, i)], fill=(color, color, color + 20))
        
        # Draw text (simplified - no font file needed)
        # In production, you'd use a proper font file
        text_color = (255, 255, 255)
        
        # Save temporary image
        img.save(output_path)
        print(f"Created placeholder image: {output_path}")
        return True
    except ImportError:
        print("PIL not installed. Using solid color background.")
        # Create simple colored image with ffmpeg instead
        return False
    except Exception as e:
        print(f"Error creating image: {e}")
        return False

def create_video_with_ffmpeg(audio_file: str, image_file: str, output_file: str, 
                             duration: float = None, text: str = None):
    """Create video from audio and image using ffmpeg"""
    
    if duration is None:
        duration = get_audio_duration(audio_file)
    
    # Create simple black image if no image provided
    if not os.path.exists(image_file):
        placeholder = os.path.splitext(image_file)[0] + "_temp.png"
        # Create a simple solid color image
        subprocess.run([
            "ffmpeg", "-f", "lavfi", "-i", f"color=c=black:s=1280x720:d={duration}",
            "-frames:v", "1", "-y", placeholder
        ], capture_output=True)
        image_file = placeholder
    
    # Build ffmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_file,
        "-i", audio_file,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_file
    ]
    
    # Add text overlay if provided
    if text:
        # Escape text for ffmpeg
        escaped_text = text.replace("'", "\\'").replace(":", "\\:")
        cmd.insert(4, "-vf")
        cmd.insert(5, f"drawtext=text='{escaped_text}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2")
    
    print(f"Running: {' '.join(cmd[:12])}...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    print(f"Created: {output_file}")
    return True

def concatenate_videos(video_files: list, output_file: str):
    """Concatenate multiple videos into one"""
    
    # Create concat file
    concat_file = "concat_list.txt"
    with open(concat_file, "w") as f:
        for vfile in video_files:
            f.write(f"file '{vfile}'\n")
    
    # Run ffmpeg concat
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Cleanup
    os.remove(concat_file)
    
    if result.returncode != 0:
        print(f"Error concatenating: {result.stderr}")
        return False
    
    print(f"Final video: {output_file}")
    return True

def create_video(audio_dir: str = ".", image_dir: str = None, output: str = "output.mp4"):
    """Main function to create video from scenes"""
    
    if image_dir is None:
        image_dir = audio_dir
    
    video_files = []
    
    print("Creating videos for each scene...")
    
    for scene_id, scene_config in SCENES.items():
        audio_path = os.path.join(audio_dir, scene_config["audio"])
        
        if image_dir:
            image_path = os.path.join(image_dir, scene_config["image"])
        else:
            image_path = scene_config["image"]
        
        output_video = f"temp_{scene_id}.mp4"
        
        if os.path.exists(audio_path):
            create_video_with_ffmpeg(
                audio_path, 
                image_path if os.path.exists(image_path) else "",
                output_video,
                text=scene_config.get("title", "")
            )
            video_files.append(output_video)
        else:
            print(f"Warning: Audio file not found: {audio_path}")
    
    if video_files:
        concatenate_videos(video_files, output)
        
        # Cleanup temp files
        for f in video_files:
            if os.path.exists(f):
                os.remove(f)
        
        print(f"\nDone! Video created: {output}")
    else:
        print("No videos created. Check audio files.")

def main():
    parser = argparse.ArgumentParser(description="Create video from audio and images")
    parser.add_argument("--audio-dir", default=".", help="Directory containing audio files")
    parser.add_argument("--image-dir", default=None, help="Directory containing images")
    parser.add_argument("--output", default="output.mp4", help="Output video file")
    
    args = parser.parse_args()
    
    create_video(args.audio_dir, args.image_dir, args.output)

if __name__ == "__main__":
    main()