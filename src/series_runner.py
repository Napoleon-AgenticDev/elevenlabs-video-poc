#!/usr/bin/env python3
"""
Series Runner - Run any episode of the video series
Usage: python series_runner.py --episode 1 --project my-series
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import episode configurations
from series_ep1 import SCENES as EP1, EPISODE as META1
from series_ep2 import SCENES as EP2, EPISODE as META2
from series_ep3 import SCENES as EP3, EPISODE as META3

EPISODES = {
    1: {"scenes": EP1, "meta": META1},
    2: {"scenes": EP2, "meta": META2},
    3: {"scenes": EP3, "meta": META3},
}

def get_episode_script(episode_num):
    """Get the full script for an episode by combining scenes."""
    ep = EPISODES.get(episode_num)
    if not ep:
        raise ValueError(f"Episode {episode_num} not found")
    
    full_script = ""
    for scene_num, scene_data in ep["scenes"].items():
        if full_script:
            full_script += " "
        full_script += scene_data["script"]
    
    return full_script

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Series Runner")
    parser.add_argument("--episode", "-e", type=int, required=True, help="Episode number (1, 2, or 3)")
    parser.add_argument("--project", "-p", help="Project name")
    parser.add_argument("--track", "-t", action="store_true", help="Enable MLflow tracking")
    args = parser.parse_args()
    
    if args.episode not in [1, 2, 3]:
        print("Episode must be 1, 2, or 3")
        return
    
    meta = EPISODES[args.episode]["meta"]
    project_name = args.project or f"series-ep{args.episode}-{meta['title'].lower().replace(' ', '-')}"
    
    print(f"=== Episode {args.episode}: {meta['title']} ===")
    print(f"Project: {project_name}")
    print(f"Target duration: {meta['duration_target']}")
    print(f"Characters: {', '.join(meta['characters'])}")
    print(f"Topic: {meta['topic']}")
    
    # For now, run the main script with the episode's scenes
    # In production, we'd inject these scenes into the CONFIG
    print(f"\nTo generate this episode, update SCENES in autonomous_video_v3.py with the content from series_ep{args.episode}.py")
    print(f"\nRun: python src/autonomous_video_v3.py --all --project {project_name}")

if __name__ == "__main__":
    main()