#!/usr/bin/env python3
"""
Background Music Generator using Mubert API
======================================
Generate royalty-free background music for videos.

Usage:
    python generate_music.py --mood inspiring --duration 30 --output music.mp3
    python generate_music.py --all --duration 15
"""

import os
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

MUBERT_TOKEN = os.getenv("MUBERT_TOKEN", "")

MOODS = {
    "inspiring": "inspiring",
    "calm": "meditative",
    "energetic": "energetic",
    "tech": "techno",
    "corporate": "corporate",
    "cinematic": "cinematic",
    "drama": "dramatic",
    "happy": "happy",
    "sad": "sad",
    "uplifting": "uplifting",
}


def generate_music(mood, duration, output_path, token=None):
    """Generate background music using Mubert API."""
    token = token or MUBERT_TOKEN
    
    if not token:
        print("  No MUBERT_TOKEN found. Using demo mode...")
        return None
    
    url = "https://api.mubert.com/v2/generatetrack"
    
    params = {
        "moods": MOODS.get(mood, "cinematic"),
        "duration": duration,
        "style": "cinematic",
        "tag": mood,
        "format": "mp3",
        "token": token,
    }
    
    response = requests.get(url, params=params, timeout=60)
    
    if response.status_code != 200:
        print(f"  Error: {response.status_code}")
        return None
    
    result = response.json()
    if result.get("status") != 1:
        print(f"  API error: {result}")
        return None
    
    track_url = result.get("data", {}).get("file")
    if not track_url:
        print(f"  No track URL in response")
        return None
    
    audio_resp = requests.get(track_url, timeout=120)
    
    with open(output_path, "wb") as f:
        f.write(audio_resp.content)
    
    print(f"  Saved: {output_path}")
    return output_path


def generate_music_patpat(mood, duration, output_path):
    """Alternative using PatPat API (free tier available)."""
    url = "https://api.patpat.com/api/music"
    
    params = {
        "mood": mood,
        "duration": duration,
        "format": "mp3",
    }
    
    try:
        response = requests.get(url, params=params, timeout=60)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
    except:
        pass
    
    return None


def generate_simple_music(duration, output_path):
    """Generate a simple tone-based background track."""
    import struct
    import math
    
    sample_rate = 44100
    n_samples = sample_rate * duration
    
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        
        freq = 220 + 50 * math.sin(t * 0.5)
        amp = 0.1 * (1 - i / n_samples) * 0.5
        
        sample = int(32767 * amp * math.sin(2 * math.pi * freq * t))
        samples.append(struct.pack("<h", sample))
    
    with open(output_path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + len(b"".join(samples))))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", len(b"".join(samples))))
        f.write(b"".join(samples))
    
    print(f"  Generated simple tone: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate background music")
    parser.add_argument("--mood", "-m", default="cinematic", 
                      choices=list(MOODS.keys()), help="Music mood")
    parser.add_argument("--duration", "-d", type=int, default=15, help="Duration in seconds")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--all", "-a", action="store_true", help="Generate for all scenes")
    parser.add_argument("--token", "-t", help="Mubert token")
    args = parser.parse_args()
    
    if args.all:
        moods = ["inspiring", "inspiring", "cinematic", "uplifting", "cinematic"]
        for i, mood in enumerate(moods, 1):
            output = f"background_music_scene{i}.mp3"
            print(f"Scene {i} ({mood})...")
            generate_music(mood, 15, output, args.token or MUBERT_TOKEN)
    else:
        output = args.output or f"background_music_{args.mood}.mp3"
        generate_music(args.mood, args.duration, output, args.token or MUBERT_TOKEN)


if __name__ == "__main__":
    main()