#!/usr/bin/env python3
"""
Create synchronized video with multiple images, transitions, and CC subtitles.
Uses FFmpeg to create professional video with:
- Multiple images per scene (synced to dialogue)
- Transitions between images (fade, wipeleft, etc.)
- CC subtitles showing spoken dialogue
"""

import os
import json
import subprocess
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VIDEO_DIR = Path(".")

IMAGE_TRANSITIONS = ["fade", "dissolve", " wipeleft", "slideleft", "fadeblack"]


def parse_args():
    parser = argparse.ArgumentParser(description="Create synced video with transitions")
    parser.add_argument("--scene", "-s", type=int, help="Scene number (1-5)")
    parser.add_argument("--all", "-a", action="store_true", help="Process all scenes")
    parser.add_argument("--images", "-i", action="store_true", help="Generate images first")
    parser.add_argument("--video", "-v", action="store_true", help="Create video")
    parser.add_argument("--openai-key", type=str, help="OpenAI API key")
    return parser.parse_args()


def get_scene_segment_times(scene_num):
    """Get dialogue segment timings from alignment data."""
    alignment_file = VIDEO_DIR / f"scene{scene_num}_alignment.json"
    if not alignment_file.exists():
        print(f"  Alignment file not found: {alignment_file}")
        return []
    
    with open(alignment_file) as f:
        alignment = json.load(f)
    
    words = alignment.get("words", [])
    segments = []
    
    current_text = []
    current_start = None
    current_end = None
    
    for word in words:
        text = word["text"].strip()
        if not text:
            continue
        
        if current_start is None:
            current_start = word["start"]
        
        if text in [".", ",", "?", "!"]:
            if current_text:
                current_text[-1] += text
                current_end = word["end"]
        elif current_end is not None and word["start"] - current_end > 1.0:
            if current_text and current_start is not None and current_end is not None:
                text_joined = " ".join(current_text).strip()
                if text_joined:
                    segments.append({
                        "text": text_joined,
                        "start": current_start,
                        "end": current_end
                    })
            current_text = [text]
            current_start = word["start"]
            current_end = word["end"]
        else:
            current_text.append(text)
            current_end = word["end"]
    
    if current_text and current_start is not None and current_end is not None:
        text = " ".join(current_text).strip()
        if text:
            segments.append({
                "text": text,
                "start": current_start,
                "end": current_end
            })
    
    return segments


def get_segment_image_prompts(scene_num, segments):
    """Generate contextual image prompts for each dialogue segment."""
    
    SCENE_CONTEXTS = {
        1: {
            "title": "THE PROBLEM",
            "segments": [
                "Close-up of stressed software developer staring at multiple failing screens",
                "Chaotic server room with code streaming on walls, developer overwhelmed",
                "Flying code documents scattered everywhere, test failures displayed",
                "Developer looking confused at error messages",
            ]
        },
        2: {
            "title": "THE DISCOVERY",
            "segments": [
                "Light bulb moment, developer discovers blueprint",
                "Hands holding architecture diagram with AI agent connections",
                "Clean organized system with feedback loops flowing smoothly",
                "Developer smiling at harness design principles",
            ]
        },
        3: {
            "title": "THE SOLUTION",
            "segments": [
                "Three pillars: OpenAI, LangChain, Anthropic logos emerging",
                "Code flowing smoothly through verification gates",
                "Feature lists building progress step by step",
                "Checkmarks passing self-verification",
            ]
        },
        4: {
            "title": "THE IMPACT",
            "segments": [
                "Autonomous agent going from prompt to PR successfully",
                "Sandwich approach layers: planning, implementation, verification",
                "Human designing systems, agent executing work",
                "Level 4 autonomy achievement",
            ]
        },
        5: {
            "title": "THE FUTURE",
            "segments": [
                "Developer creating better specifications",
                "Feedback loops visualized as glowing paths",
                "Observed harness with clear verification gates",
                "Open horizon with agent army ready",
            ]
        }
    }
    
    context = SCENE_CONTEXTS.get(scene_num, {"title": f"SCENE {scene_num}", "segments": []})
    prompts = context.get("segments", [])
    
    result = []
    for i, seg in enumerate(segments):
        prompt = prompts[i] if i < len(prompts) else prompts[-1]
        result.append({
            "text": seg["text"],
            "start": seg["start"],
            "end": seg["end"],
            "image_prompt": prompt
        })
    
    return result


def generate_image(api_key, prompt, output_path, size="landscape"):
    """Generate an image using OpenAI GPT Image API."""
    import requests
    
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=120)
    response.raise_for_status()
    
    result = response.json()
    image_url = result["data"][0]["url"]
    
    image_response = requests.get(image_url)
    with open(output_path, "wb") as f:
        f.write(image_response.content)
    
    return output_path


def generate_images_for_scene(scene_num, segments, api_key):
    """Generate images for all segments in a scene."""
    output_dir = VIDEO_DIR / f"image_segments/scene{scene_num}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, seg in enumerate(segments):
        output_path = output_dir / f"segment_{i+1}.png"
        if output_path.exists():
            print(f"  Skipping segment {i+1} (exists)")
            continue
            
        print(f"  Generating segment {i+1}: {seg['image_prompt'][:50]}...")
        generate_image(api_key, seg["image_prompt"], output_path)
    
    return output_dir


def generate_srt_for_segments(segments):
    """Generate SRT subtitles for all segments."""
    lines = []
    index = 1
    
    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        
        start_h = int(start // 3600)
        start_m = int((start % 3600) // 60)
        start_s = int(start % 60)
        start_ms = int((start % 1) * 1000)
        
        end_h = int(end // 3600)
        end_m = int((end % 3600) // 60)
        end_s = int(end % 60)
        end_ms = int((end % 1) * 1000)
        
        lines.append(str(index))
        lines.append(f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03f} --> {end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03f}")
        lines.append(seg["text"])
        lines.append("")
        index += 1
    
    return "\n".join(lines)


def create_video_with_transitions(scene_num, segments, image_dir, audio_file, output_file):
    """Create video with multiple images, transitions, and CC subtitles."""
    
    srt_content = generate_srt_for_segments(segments)
    srt_file = VIDEO_DIR / f"scene{scene_num}_segments.srt"
    with open(srt_file, "w") as f:
        f.write(srt_content)
    
    duration_file = VIDEO_DIR / f"scene{scene_num}_duration.txt"
    total_duration = segments[-1]["end"] if segments else 10
    with open(duration_file, "w") as f:
        f.write(str(total_duration))
    
    filter_complex = []
    inputs = []
    
    for seg in segments:
        img_path = image_dir / f"segment_{segments.index(seg)+1}.png"
        if not img_path.exists():
            print(f"  Warning: {img_path} not found")
            continue
    
    image_files = [image_dir / f"segment_{i+1}.png" for i in range(len(segments))]
    valid_image_files = [f for f in image_files if f.exists()]
    
    if not valid_image_files:
        print(f"  No images found in {image_dir}")
        return
    
    duration = total_duration
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(valid_image_files[0]),
        "-i", str(audio_file),
    ]
    
    filter_parts = [
        f"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
        f"setpts=pts={0}/{duration}",
    ]
    
    for i, img_file in enumerate(valid_image_files[1:], 1):
        cmd.extend(["-loop", "1", "-i", str(img_file)])
        segment_duration = segments[i]["end"] - segments[i]["start"]
        filter_parts.append(
            f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setpts=pts={segments[i]['start']}/{duration}[v{i}]"
        )
    
    filter_str = ";".join(filter_parts)
    cmd.extend([
        "-filter_complex", filter_str,
        "-map", "0:a",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        str(output_file)
    ])
    
    print(f"  Running: {' '.join(cmd[:12])}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Error: {result.stderr[:500]}")
    
    print(f"  Created: {output_file}")
    return output_file


def create_simple_video(scene_num):
    """Create a simple video with the existing approach but better."""
    
    audio_file = VIDEO_DIR / f"spectacular_scene{scene_num}.mp3"
    alignment_file = VIDEO_DIR / f"scene{scene_num}_alignment.json"
    
    if not audio_file.exists():
        print(f"  Audio not found: {audio_file}")
        return
    
    if not alignment_file.exists():
        print(f"  Alignment not found: {alignment_file}")
        return
    
    with open(alignment_file) as f:
        alignment = json.load(f)
    
    segments = []
    words = alignment.get("words", [])
    
    current_text = []
    current_start = None
    current_end = None
    min_segment_duration = 2.5
    
    for word in words:
        text = word["text"].strip()
        if not text or text == " ":
            continue
        
        if current_start is None:
            current_start = word["start"]
        
        if text in [".", "?", "!"]:
            if current_text:
                current_text[-1] += text
                current_end = word["end"]
                if current_end - current_start >= min_segment_duration:
                    segments.append({
                        "text": " ".join(current_text).strip(),
                        "start": current_start,
                        "end": current_end
                    })
                    current_text = []
                    current_start = None
                    current_end = None
        else:
            if word["start"] - (current_end or 0) > 0.8 and current_text:
                if current_end - current_start >= min_segment_duration:
                    segments.append({
                        "text": " ".join(current_text).strip(),
                        "start": current_start,
                        "end": current_end
                    })
                current_text = []
                current_start = word["start"]
            
            current_text.append(text)
            current_end = word["end"]
    
    if current_text and current_start and current_end and current_end - current_start >= min_segment_duration:
        segments.append({
            "text": " ".join(current_text).strip(),
            "start": current_start,
            "end": current_end
        })
    
    segment_prompts = get_segment_image_prompts(scene_num, segments)
    
    for i, seg in enumerate(segment_prompts):
        seg["start"] = segments[i]["start"]
        seg["end"] = segments[i]["end"]
    
    srt_content = generate_srt_for_segments(segment_prompts)
    srt_file = VIDEO_DIR / f"scene{scene_num}_cc.srt"
    with open(srt_file, "w") as f:
        f.write(srt_content)
    print(f"  Created CC subtitles: {srt_file}")
    
    output_file = VIDEO_DIR / f"synced_scene{scene_num}.mp4"
    
    max_segments = min(4, len(segment_prompts))
    if max_segments < len(segment_prompts):
        segment_prompts = segment_prompts[:max_segments]
    
    image_dir = VIDEO_DIR / f"synced_images/scene{scene_num}"
    image_dir.mkdir(parents=True, exist_ok=True)
    
    image_files = []
    for i in range(max_segments):
        img_file = image_dir / f"frame_{i+1}.png"
        image_files.append(str(img_file))
    
    input_parts = []
    filter_parts = []
    
    for i, img_file in enumerate(image_files):
        input_parts.extend(["-loop", "1", "-i", img_file])
        
        start_time = segment_prompts[i]["start"]
        end_time = segment_prompts[i]["end"]
        duration = end_time - start_time
    
    if not image_files:
        print(f"  No images found in {image_dir}")
        return None
    
    cmd = ["ffmpeg", "-y"]
    
    for img in image_files:
        cmd.extend(["-loop", "1", "-i", img])
    
    cmd.extend(["-i", str(audio_file)])
    
    filter_complex = ""
    for i in range(len(image_files)):
        filter_complex += f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}];"
    
    for i in range(len(image_files) - 1):
        start = segment_prompts[i]["start"]
        end = segment_prompts[i+1]["start"]
        duration = end - start
        filter_complex += f"[v{i}][v{i+1}]xfade=transition=fade:duration=0.5:offset={start}[v{i+1}t];"
    
    filter_complex += f"[v{len(image_files)-1}]subtitles='{srt_file}'[out]"
    
    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", f"{len(image_files)}:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        str(output_file)
    ])
    
    try:
        print(f"  Running FFmpeg with {len(image_files)} images and transitions...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"  FFmpeg error: {result.stderr[:300]}")
        else:
            print(f"  Created: {output_file}")
    except subprocess.TimeoutExpired:
        print(f"  Timeout - video may be too long")
    except Exception as e:
        print(f"  Error: {e}")
    
    return output_file


def main():
    args = parse_args()
    
    api_key = args.openai_key or OPENAI_API_KEY
    
    if args.all:
        scenes = range(1, 6)
    elif args.scene:
        scenes = [args.scene]
    else:
        print("Usage: create_synced_video.py --scene N or --all")
        return
    
    for scene_num in scenes:
        print(f"\n=== Scene {scene_num} ===")
        
        segments = get_scene_segment_times(scene_num)
        print(f"  Found {len(segments)} dialogue segments")
        
        if args.images:
            segment_prompts = get_segment_image_prompts(scene_num, segments)
            image_dir = VIDEO_DIR / f"synced_images/scene{scene_num}"
            image_dir.mkdir(parents=True, exist_ok=True)
            
            for i, seg in enumerate(segment_prompts[:4]):
                img_path = image_dir / f"frame_{i+1}.png"
                if img_path.exists():
                    print(f"  Skipping frame {i+1} (exists)")
                    continue
                print(f"  Generating: {seg['image_prompt'][:60]}...")
                try:
                    generate_image(api_key, seg["image_prompt"], img_path)
                except Exception as e:
                    print(f"  Error: {e}")
        
        if args.video or args.all:
            create_simple_video(scene_num)


if __name__ == "__main__":
    main()