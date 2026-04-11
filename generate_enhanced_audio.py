#!/usr/bin/env python3
"""
Enhanced Audio Generator with Audio Tags for ElevenLabs v3

This script generates speech using ElevenLabs v3 Audio Tags for:
- Natural pauses: [pause], [short pause], [long pause]
- Emotional expression: [excited], [sad], [angry], [whispers], [shouts]
- Delivery control: [slow], [fast], [emphatic], [softly], [dramatic]

Usage:
    python generate_enhanced_audio.py --scene 1
    python generate_enhanced_audio.py --all
"""

import os
import requests
from pathlib import Path
from config import get_voice

# ElevenLabs v3 Audio Tags enhanced scripts
SCENES = {
    1: {
        "title": "The Problem",
        "voice": "brittney",
        "text": """Every developer knows this feeling [short pause] 
You're building an AI system, and it starts spiraling out of control [long pause] 
Code everywhere [pause] 
No direction [pause] 
Tests failing [emphatic] 
Sound familiar? [short pause]"""
    },
    2: {
        "title": "The Discovery",
        "voice": "brittney",
        "text": """What if there was a better way? [pause] 
What if instead of writing every line of code [pause] 
you could design the specifications [short pause] 
that guide your AI? [emphatic] 

Enter... [long pause] harness engineering [emphatic]. 

It's not about programming the AI directly [softly] 
[pause] 
It's about creating environments, specifications, and feedback loops [emphatic] 
that let agents do reliable work."""
    },
    3: {
        "title": "The Solution",
        "voice": "brittney",
        "text": """Three companies cracked the code [emphatic]. 

OpenAI generated ONE MILLION lines of code [excited] 
with just three engineers [pause] 

LangChain improved their agent by fourteen percentage points [emphatic] 
[pause] 
from fifty-two point eight percent [short pause] 
to sixty-six point five percent [dramatic] 
[pause] 
just by changing the harness [short pause] 
not the model [pause]. 

Anthropic solved the long-running agent problem [emphatic] 
with feature lists [pause] 
and progress tracking [pause]. 

The secret? [long pause] 
Self-verification before exit [emphatic]. 
Incremental progress over scope [pause]. 
Context that the agent can actually see [softly]."""
    },
    4: {
        "title": "The Impact",
        "voice": "brittney",
        "text": """The results speak for themselves [emphatic] [pause]. 

OpenAI reached level four autonomy [emphatic] 
[pause] 
agents that can go from prompt to PR [short pause] 
with minimal human input [pause]. 

LangChain's sandwich approach [pause] 
xhigh reasoning for planning [pause] 
high for implementation [pause] 
xhigh for verification [short pause] 
boosted performance by nearly fourteen points [emphatic] [pause]. 

The shift? [long pause] 
Humans don't write code anymore [emphatic]. 
They design systems [pause]. 
They steer [pause]. 
Agents execute [emphatic]."""
    },
    5: {
        "title": "The Future",
        "voice": "brittney",
        "text": """The future of development isn't about writing more code [emphatic] [pause]. 

It's about creating better specifications [pause]. 
Better feedback loops [pause]. 
Better harnesses [emphatic]. 

Start with your environment [short pause]. 
Add observability [pause]. 
Enforce verification [emphatic]. 

The agents are waiting [long pause]. 
Are you ready to guide them? [emphatic] [short pause]"""
    }
}

# Voice settings optimized for expressive v3
VOICE_SETTINGS = {
    "stability": 0.35,  # Lower for more expression
    "similarity_boost": 0.85,
    "style": 0.3,  # Some style for v3
    "speed": 1.0
}

API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io"

def generate_enhanced_speech(scene_num: int, output_dir: str = ".") -> str:
    """Generate speech with audio tags for a scene"""
    
    if not API_KEY:
        print("Error: ELEVENLABS_API_KEY not set")
        return None
    
    scene = SCENES[scene_num]
    voice_id = get_voice(scene["voice"])
    
    url = f"{BASE_URL}/v1/text-to-speech/{voice_id}"
    
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": scene["text"],
        "voice_settings": VOICE_SETTINGS,
        "model_id": "eleven_v3",
        "output_format": "mp3_44100_128"
    }
    
    print(f"Generating Scene {scene_num}: {scene['title']}...")
    print(f"  Voice: {scene['voice']}")
    print(f"  Model: eleven_v3 (with Audio Tags)")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    output_path = os.path.join(output_dir, f"enhanced_scene{scene_num}.mp3")
    
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    print(f"  Saved to: {output_path}")
    return output_path

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate enhanced audio with v3 Audio Tags")
    parser.add_argument("--scene", type=int, choices=[1,2,3,4,5], help="Scene number")
    parser.add_argument("--all", action="store_true", help="Generate all scenes")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    if args.all:
        for i in range(1, 6):
            generate_enhanced_speech(i, args.output_dir)
    elif args.scene:
        generate_enhanced_speech(args.scene, args.output_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()