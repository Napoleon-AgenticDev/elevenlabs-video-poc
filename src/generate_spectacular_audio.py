#!/usr/bin/env python3
"""
Spectacular Audio Generator with Maximum Expression
Using ElevenLabs v3 Audio Tags for dramatic voice inflections
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".env")
load_dotenv(env_path)

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io"

# Spectacular scripts with MAXIMUM expression
SCENES = {
    1: {
        "title": "The Problem",
        "voice_id": "kPzsL2i3teMYv0FxEYQ6",  # Brittney
        "text": """Every developer knows [emphatic] this feeling [long pause] 

You're building [emphatic] an AI system... 
and it starts spiraling [sighs] OUT OF CONTROL [shouts] [long pause] 

Code EVERYWHERE [excited] [short pause] 
No direction [slow] [pause] 
Tests failing [emphatic] [short pause] 

Sound familiar? [emphatic] [short pause]"""
    },
    2: {
        "title": "The Discovery", 
        "voice_id": "kPzsL2i3teMYv0FxEYQ6",
        "text": """What if there was [emphatic] a BETTER [excited] way? [pause]

What if instead of writing every line of code [slow] [pause]
you could design the SPECIFICATIONS [emphatic] [short pause]
that GUIDE your AI? [emphatic] [long pause]

Enter... [dramatic] [long pause]
HARNESS ENGINEERING [excited] [short pause]

It's NOT about programming the AI directly [whispers] [pause]
It's about creating ENVIRONMENTS [emphatic] [pause]
SPECIFICATIONS [emphatic] [pause]
and FEEDBACK LOOPS [excited]
that let agents do RELIABLE [emphatic] work"""
    },
    3: {
        "title": "The Solution",
        "voice_id": "kPzsL2i3teMYv0FxEYQ6",
        "text": """THREE [shouts] companies cracked the CODE [excited] [pause]

OPENAI [emphatic] generated ONE MILLION [emphatic] 
lines of code [excited] with just THREE [emphatic] engineers [pause]

LangChain improved their agent by FOURTEEN [emphatic] PERCENTAGE POINTS [shouts] [long pause]
from fifty-two point eight percent [slow] [pause]
to sixty-six point five percent [emphatic] [dramatic pause]
just by CHANGING [emphatic] the harness [short pause]
NOT the model [pause]

ANTHROPIC [emphatic] solved the long-running agent problem [emphatic]
with FEATURE LISTS [pause] and PROGRESS TRACKING [short pause]

The SECRET? [long pause] [dramatic]
Self-verification BEFORE exit [emphatic] [pause]
Incremental progress OVER scope [pause]
Context that the agent can actually SEE [emphatic] [softly]"""
    },
    4: {
        "title": "The Impact",
        "voice_id": "kPzsL2i3teMYv0FxEYQ6",
        "text": """The RESULTS [shouts] speak for themselves [emphatic] [pause]

OPENAI reached LEVEL FOUR AUTONOMY [excited] [pause]
AGENTS [emphatic] that can go from PROMPT [pause] to PR [short pause]
with MINIMAL human input [pause]

LangChain's SANDWICH APPROACH [emphatic] [pause]
xhigh reasoning for PLANNING [pause]
HIGH for IMPLEMENTATION [short pause]
xhigh for VERIFICATION [short pause]
BOOSTED performance by nearly FOURTEEN POINTS [excited] [pause]

The SHIFT? [dramatic] [long pause]
Humans DON'T write code anymore [emphatic] [pause]
They DESIGN systems [emphatic] [pause]
They STEER [pause]
AGENTS EXECUTE [shouts]"""
    },
    5: {
        "title": "The Future",
        "voice_id": "kPzsL2i3teMYv0FxEYQ6",
        "text": """The FUTURE [emphatic] of development 
isn't about WRITING more code [emphatic] [pause]

It's about creating BETTER [excited] specifications [pause]
BETTER [emphatic] feedback loops [pause]
BETTER [excited] HARNESSES [emphatic] [pause]

Start with your ENVIRONMENT [short pause]
Add OBSERVABILITY [emphatic] [pause]
Enforce VERIFICATION [emphatic] [short pause]

The AGENTS [emphatic] are WAITING [long pause]
Are you READY [shouts] to GUIDE them? [emphatic] [short pause]"""
    }
}

# Optimized for maximum expression
VOICE_SETTINGS = {
    "stability": 0.25,  # Very low for maximum expression
    "similarity_boost": 0.9,
    "style": 0.5,  # High style for v3
    "speed": 1.0
}

def generate_spectacular_audio(scene_num: int, output_dir: str = ".") -> str:
    """Generate spectacular audio with maximum expression"""
    
    scene = SCENES[scene_num]
    voice_id = scene["voice_id"]
    
    url = f"{BASE_URL}/v1/text-to-speech/{voice_id}"
    
    headers = {
        "xi-api-key": ELEVENLABS_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": scene["text"],
        "voice_settings": VOICE_SETTINGS,
        "model_id": "eleven_v3",
        "output_format": "mp3_44100_128"
    }
    
    print(f"Generating SPECTACULAR Scene {scene_num}: {scene['title']}...")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text[:500])
        return None
    
    output_path = os.path.join(output_dir, f"spectacular_scene{scene_num}.mp3")
    
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    print(f"  Saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    for i in range(1, 6):
        generate_spectacular_audio(i, ".")
    print("\n✅ All spectacular audio generated!")