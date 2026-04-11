# API Guide 📡

## What is an API?

Think of an API like a telephone. You call a number (the API), say what you want (send your text), and get an answer back (the voice audio)!

## The Two Main Ways to Make Voice

### 1. Single Voice (Text to Speech)

One person talking. Like a podcast with one host!

**The Phone Number (Endpoint):**
```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
```

**What You Say (Request):**
```json
{
  "text": "Hello world!",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  },
  "model_id": "eleven_v3"
}
```

### 2. Multiple Voices (Text to Dialogue)

Two or more people talking. Like a conversation!

**The Phone Number:**
```
POST https://api.elevenlabs.io/v1/text-to-dialogue
```

**What You Say:**
```json
{
  "inputs": [
    {"text": "Hello!", "voice_id": "kPzsL2i3teMYv0FxEYQ6"},
    {"text": "Hi there!", "voice_id": "JBFqnCBsd6RMkjVDRZzb"}
  ],
  "model_id": "eleven_v3"
}
```

## The Magic Key (API Key)

Before you can call the API, you need a special password. It's like showing an ID card before entering a building!

Your API key: `YOUR_API_KEY_HERE`

**You need this in every request:**
```
Header: xi-api-key: YOUR_API_KEY_HERE
```

## The Voices You Can Use

| Voice Name | Voice ID | Best For |
|------------|----------|----------|
| Brittney | kPzsL2i3teMYv0FxEYQ6 | Fun, social media |
| George | JBFqnCBsd6RMkjVDRZzb | Storytelling |
| Sarah | EXAVITQu4vr4xnSDxMaL | Professional |
| Roger | CwhRBWXzGAHq8TQ4Fs17 | Casual |
| Matilda | XrExE9yKIg1WjnnlVkGX | Educational |
| Adam | pNInz6obpgDQGcFmaJgB | Authority |

## The Brains (Models)

Different AI "brains" have different strengths!

| Model | What It Does | Best For |
|-------|--------------|----------|
| eleven_v3 | Most expressive, emotional | High quality videos |
| eleven_multilingual_v2 | Speaks many languages | International content |
| eleven_flash_v2_5 | Super fast, low delay | Real-time apps |

## Voice Settings (Make It Sound Different!)

You can change how the voice sounds:

| Setting | What It Does | Range |
|---------|--------------|-------|
| stability | How consistent the voice is | 0.0 - 1.0 |
| similarity_boost | How much it sounds like the original | 0.0 - 1.0 |
| style | How much emotion to add | 0.0 - 1.0 |
| speed | How fast they talk | 0.5 - 2.0 |

**Pro tip:** For narrated videos, use:
```json
{
  "stability": 0.4,
  "similarity_boost": 0.8,
  "style": 0.2
}
```

## Example: Using cURL (Command Line)

### Single Voice:
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/kPzsL2i3teMYv0FxEYQ6" \
  -H "xi-api-key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world!",
    "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
    "model_id": "eleven_v3"
  }' \
  --output hello.mp3
```

### Multiple Voices:
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-dialogue" \
  -H "xi-api-key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {"text": "Hello!", "voice_id": "kPzsL2i3teMYv0FxEYQ6"},
      {"text": "Hi there!", "voice_id": "JBFqnCBsd6RMkjVDRZzb"}
    ]
  }' \
  --output conversation.mp3
```

## Example: Using Python

```python
import requests

# Your settings
API_KEY = "YOUR_API_KEY_HERE"
VOICE_ID = "kPzsL2i3teMYv0FxEYQ6"

# Make the request
response = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": API_KEY},
    json={
        "text": "Hello world!",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
        "model_id": "eleven_v3"
    }
)

# Save the audio
with open("hello.mp3", "wb") as f:
    f.write(response.content)
```

## Output Formats

You can get your audio in different formats:

| Format | What It Is |
|--------|------------|
| mp3_44100_128 | Standard MP3 (best quality/size) |
| mp3_44100_192 | High quality MP3 |
| wav_44100 | Uncompressed audio (bigger file) |
| pcm_16000 | Raw audio for processing |

## Response Headers (Secret Info!)

When you get your audio back, there's hidden info:

- `x-character-count` - How many characters you used (for billing!)
- `request-id` - A unique ID for this request
- `current-concurrent-requests` - How many requests happening now

---

**That's the API!** 

Check out [Voice Guide](voice-guide.md) to learn more about picking the perfect voice! 🎤