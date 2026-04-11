# ElevenLabs Video POC Configuration

## Environment Variables

```bash
# Copy this to .env file
ELEVENLABS_API_KEY=YOUR_API_KEY_HERE
```

## Voice Configuration

| Voice ID | Name | Description | Use Case |
|----------|------|-------------|----------|
| kPzsL2i3teMYv0FxEYQ6 | Brittney | Fun, Youthful & Informative | Primary narrator (social media style) |
| JBFqnCBsd6RMkjVDRZzb | George | Warm, Captivating Storyteller | Dialogue, storytelling |
| EXAVITQu4vr4xnSDxMaL | Sarah | Mature, Reassuring, Confident | Dialogue, professional |
| CwhRBWXzGAHq8TQ4Fs17 | Roger | Laid-Back, Casual, Resonant | Casual content |
| XrExE9yKIg1WjnnlVkGX | Matilda | Knowledgeable, Professional | Educational |
| pNInz6obpgDQGcFmaJgB | Adam | Dominant, Firm | Authority |

## Model Configuration

| Model ID | Description | Char Limit | Latency |
|----------|-------------|------------|---------|
| eleven_v3 | Most emotionally expressive | 5,000 | Higher |
| eleven_multilingual_v2 | Best for multilingual | 10,000 | Medium |
| eleven_flash_v2_5 | Ultra-low latency | 40,000 | ~75ms |

## Video Settings

- **Output Format**: MP3 44100_128
- **Model**: eleven_v3
- **Voice Settings**: stability=0.4, similarity_boost=0.8

## Available Voices (Full List)

```
kPzsL2i3teMYv0FxEYQ6 - Brittney
JBFqnCBsd6RMkjVDRZzb - George
EXAVITQu4vr4xnSDxMaL - Sarah
CwhRBWXzGAHq8TQ4Fs17 - Roger
pNInz6obpgDQGcFmaJgB - Adam
XrExE9yKIg1WjnnlVkGX - Matilda
```