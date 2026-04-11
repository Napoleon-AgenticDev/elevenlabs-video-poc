---
name: elevenlabs-video-generator
description: Generate videos with AI voice and images using ElevenLabs API. Creates spectacul videos with expressive voice using v3 Audio Tags and OpenAI image generation.
---

# ElevenLabs Video Generator Skill

## Overview

This skill enables AI coding agents to generate videos with AI-generated voice and images. It combines:
- **ElevenLabs v3** - Text-to-speech with Audio Tags for expressive voice
- **OpenAI GPT Image** - AI-generated cinematic images
- **FFmpeg** - Video compilation

## When to Use

Use this skill when you need to:
- Create social media videos with AI narration
- Generate educational content with voiceover
- Produce marketing videos with custom visuals
- Build video POC demos with AI-generated assets

## Prerequisites

```bash
# Install required tools
pip install requests pillow python-dotenv

# Ensure ffmpeg is installed
brew install ffmpeg  # macOS
# or
sudo apt install ffmpeg  # Linux
```

## Environment Setup

Create a `.env` file:
```bash
ELEVENLABS_API_KEY=your_elevenlabs_key
OPENAI_API_KEY=your_openai_key
```

## Workflow

### 1. Generate Expressive Audio

```python
from generate_spectacular_audio import generate_spectacular_audio

# Generate all 5 scenes
for i in range(1, 6):
    generate_spectacular_audio(i, "output/")
```

### 2. Generate AI Images

```python
from generate_images import generate_scene_images

# Generate cinematic images
generate_scene_images(api_key)
```

### 3. Add Text Overlays

```python
from PIL import Image, ImageDraw, ImageFont

def add_text_overlay(image_path, title, subtitle):
    img = Image.open(image_path).resize((1280, 720))
    draw = ImageDraw.Draw(img)
    # Add text overlays
    img.save("output_with_text.png")
```

### 4. Create Video

```bash
ffmpeg -loop 1 -i image.png -i audio.mp3 \
  -c:v libx264 -c:a aac -shortest output.mp4
```

## Audio Tags Reference (ElevenLabs v3)

Use these tags in your script for expressive voice:

| Tag | Effect |
|-----|--------|
| `[pause]` | Natural pause |
| `[short pause]` | Brief pause |
| `[long pause]` | Extended pause |
| `[shouts]` | Louder delivery |
| `[whispers]` | Quiet delivery |
| `[emphatic]` | Strong emphasis |
| `[excited]` | Enthusiastic tone |
| `[sighs]` | Sighing sound |
| `[slow]` | Slower pace |
| `[fast]` | Faster pace |
| `[dramatic]` | Theatrical delivery |
| `[softly]` | Gentle delivery |

Example script:
```python
SCENES = {
    1: {
        "title": "The Problem",
        "text": """Every developer knows [emphatic] this feeling [long pause]
        You're building an AI system... and it starts spiraling OUT OF CONTROL [shouts]"""
    }
}
```

## Video Generation Script Template

```python
#!/usr/bin/env python3
"""
Video Generator Template
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(".env")
load_dotenv(env_path)

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Your scenes here
SCENES = {
    1: {"title": "Scene 1", "text": "...", "image_prompt": "..."},
    # ...
}

def generate_audio(scene_num):
    """Generate audio with Audio Tags"""
    pass

def generate_image(scene_num):
    """Generate image with OpenAI"""
    pass

def create_video(scene_num):
    """Combine audio + image + text"""
    pass

# Main execution
if __name__ == "__main__":
    for i in range(1, 6):
        generate_audio(i)
        generate_image(i)
        create_video(i)
```

## Best Practices

1. **Use v3 model** for maximum expression
2. **Lower stability** (0.25-0.35) for more variation
3. **Higher style** (0.3-0.5) for emotional range
4. **Include Audio Tags** for dramatic effect
5. **Keep scenes under 30 seconds** for better results

## Output Formats

- Audio: MP3 44100_128
- Images: 1024x1024 (resize to 1280x720)
- Video: MP4, H.264, AAC audio

## Cost Estimate

- ElevenLabs: ~$0.01-0.05 per scene (depends on length)
- OpenAI: ~$0.01-0.05 per image
- Total: ~$0.10-0.30 per minute of video

## Files in This Skill

```
.
├── generate_spectacular_audio.py  # Audio generation with v3 Audio Tags
├── generate_images.py              # AI image generation
├── config.py                       # Configuration and voice settings
├── video-script-enhanced.md        # Example script with Audio Tags
├── image-prompts.md                # Cinematic image prompts
└── .env                            # API keys (local only)
```

## Usage in AI Agents

```bash
# Generate audio
python generate_spectacular_audio.py --scene 1

# Generate all
python generate_spectacular_audio.py --all

# Generate images
python generate_images.py --all --openai-key YOUR_KEY
```

---

**Created for:** buildmotion-ai-agency video POC
**APIs Used:** ElevenLabs v3, OpenAI GPT Image
**Voice:** Brittney (kPzsL2i3teMYv0FxEYQ6)