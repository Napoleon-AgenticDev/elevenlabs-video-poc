# API Guide 📡

## Overview

This project uses TWO powerful AI APIs:

| API | What It Does | Docs |
|-----|--------------|------|
| **ElevenLabs** | AI voice generation with Audio Tags | [elevenlabs.io/docs](https://elevenlabs.io/docs) |
| **OpenAI** | AI image generation | [platform.openai.com/docs](https://platform.openai.com/docs) |

---

## Part 1: ElevenLabs API

### Authentication

```python
# Header required for all requests
headers = {
    "xi-api-key": "YOUR_ELEVENLABS_API_KEY",
    "Content-Type": "application/json"
}
```

### 1. Text to Speech with Audio Tags (Recommended!)

**Endpoint:** `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`

**Request:**
```json
{
  "text": "Hello world [emphatic] with expression! [shouts]",
  "voice_settings": {
    "stability": 0.25,
    "similarity_boost": 0.9,
    "style": 0.5
  },
  "model_id": "eleven_v3",
  "output_format": "mp3_44100_128"
}
```

**Audio Tags in text:**
```
"CODE [shouts] everywhere!"           → Loud emphasis
"the secret [emphatic] is..."          → Strong emphasis
"wait [long pause] what?"               → Dramatic pause
"not telling anyone [whispers]"        → Quiet delivery
```

### 2. Text to Dialogue (Multi-Voice)

**Endpoint:** `POST https://api.elevenlabs.io/v1/text-to-dialogue`

**Request:**
```json
{
  "inputs": [
    {"text": "Hello!", "voice_id": "kPzsL2i3teMYv0FxEYQ6"},
    {"text": "Hi there!", "voice_id": "JBFqnCBsd6RMkjVDRZzb"}
  ],
  "model_id": "eleven_v3"
}
```

### Voice Settings for Expression

| Setting | For Drama | For Narration |
|---------|-----------|----------------|
| stability | 0.25 | 0.4 |
| similarity_boost | 0.9 | 0.8 |
| style | 0.5 | 0.2 |
| speed | 1.0 | 1.0 |

---

## Part 2: OpenAI API (Images)

### Authentication

```python
headers = {
    "Authorization": "Bearer YOUR_OPENAI_API_KEY",
    "Content-Type": "application/json"
}
```

### Generate Image

**Endpoint:** `POST https://api.openai.com/v1/images/generations`

**Request:**
```json
{
  "model": "gpt-image-1",
  "prompt": "Cinematic dark tech visualization, chaotic code fragments, dramatic lighting",
  "n": 1,
  "size": "1024x1024"
}
```

### Response
```json
{
  "data": [
    {"url": "https://..."}  // Download this URL
  ]
}
```

---

## Complete Python Example

```python
import os
import requests
from dotenv import load_dotenv

# Load API keys
load_dotenv()
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# 1. Generate Audio
audio_response = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/kPzsL2i3teMYv0FxEYQ6",
    headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
    json={
        "text": "Every developer knows [emphatic] this feeling [long pause]",
        "voice_settings": {"stability": 0.25, "similarity_boost": 0.9, "style": 0.5},
        "model_id": "eleven_v3"
    }
)
with open("audio.mp3", "wb") as f:
    f.write(audio_response.content)

# 2. Generate Image
image_response = requests.post(
    "https://api.openai.com/v1/images/generations",
    headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
    json={
        "model": "gpt-image-1",
        "prompt": "Cinematic dark tech visualization",
        "n": 1,
        "size": "1024x1024"
    }
)
image_url = image_response.json()["data"][0]["url"]

# Download image
img = requests.get(image_url).content
with open("image.png", "wb") as f:
    f.write(img)

# 3. Create Video (requires ffmpeg)
# ffmpeg -loop 1 -i image.png -i audio.mp3 -shortest output.mp4
```

---

## API Endpoints Summary

| Service | Endpoint | Purpose |
|---------|-----------|---------|
| ElevenLabs | `POST /v1/text-to-speech/{voice_id}` | Single voice |
| ElevenLabs | `POST /v1/text-to-dialogue` | Multi-voice |
| OpenAI | `POST /v1/images/generations` | AI images |

---

## Cost Estimates

| Operation | Cost |
|-----------|------|
| ElevenLabs v3 audio (per minute) | ~$0.01-0.05 |
| OpenAI GPT Image (per image) | ~$0.01-0.05 |
| **Total per 2-min video** | **~$0.10-0.30** |

---

**Now you can use both APIs!** 

Check out [voice-guide.md](voice-guide.md) for the full Audio Tags reference! 🎤