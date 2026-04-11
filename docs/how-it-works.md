# How It Works 🔍

## The Complete AI Video Pipeline

This project combines TWO powerful AI services to create SPECTACULAR videos:

```
YOUR SCRIPT
    ↓
    ├─→ ElevenLabs v3 (Voice) + Audio Tags
    │       ↓
    │    MP3 AUDIO
    │
    └─→ OpenAI GPT Image (Images)
            ↓
         PNG IMAGES
              ↓
         FFmpeg (Combine)
              ↓
         FINAL VIDEO 🎬
```

## Part 1: ElevenLabs v3 - Expressive Voice AI

### How Voice AI Works

Imagine you have a robot friend. You write what you want to say, the robot reads it out loud with EXPRESSION. That's ElevenLabs!

### The Magic: Audio Tags!

ElevenLabs v3 understands special tags that control emotion:

```
"CODE EVERYWHERE [shouts]" 
     ↓
AI adds loud, emphasized pronunciation

"the secret is [emphatic] self-verification"
     ↓  
AI adds strong emphasis on "self-verification"

"are you ready [long pause] to guide them?"
     ↓
AI adds dramatic pause before ending
```

### Why Does It Sound So Real?

ElevenLabs learned from millions of voice recordings and knows:
- 🔊 How voices change with emotion
- 🎯 How to pronounce anything
- ⏱️ When to pause naturally
- 💫 How to add drama and excitement

## Part 2: OpenAI GPT Image - Cinematic Images

### How Image AI Works

You describe what you want to see, AI generates a real image:

```
YOUR PROMPT: "Cinematic dark tech visualization, chaotic code fragments..."
     ↓
OpenAI GPT Image
     ↓
BEAUTIFUL IMAGE (1024x1024)
```

### Our Cinematic Prompts

Each scene has a specialized prompt:
- Scene 1: Chaos, dark void, red accents
- Scene 2: Light revealing path, hope
- Scene 3: Three pillars, structure
- Scene 4: Rocket ascending, success
- Scene 5: Future horizon, sunrise

## Part 3: FFmpeg - Video Assembly

FFmpeg is the magic tool that combines everything:
- Takes one image and loops it
- Adds the audio track
- Outputs a watchable video!

```bash
ffmpeg -loop 1 -i image.png -i audio.mp3 -shortest output.mp4
```

## The Full Workflow

```
1. WRITE SCRIPT with Audio Tags
       ↓
2. GENERATE AUDIO with v3
       ↓
3. GENERATE IMAGES with OpenAI
       ↓
4. ADD TEXT OVERLAYS
       ↓
5. CREATE VIDEO with FFmpeg
       ↓
6. UPLOAD to GitHub Release!
```

## Key Words To Remember

| Term | What It Does |
|------|--------------|
| **Audio Tags** | Special commands like [shouts], [emphatic] that control voice expression |
| **v3 Model** | ElevenLabs' most expressive AI voice model |
| **GPT Image** | OpenAI's AI image generator |
| **FFmpeg** | Tool that combines images + audio = video |
| **API** | The "window" that lets computers talk to AI services |

## Why This Is Special

1. **No recording needed** - Just type your script
2. **Expressive voice** - Audio Tags make it sound REAL
3. **Custom images** - Describe what you want, get it
4. **Professional quality** - Cinematic look with text overlays

---

**Now you understand the COMPLETE pipeline!**

Next, check out the [API Guide](api-guide.md) to learn both APIs in detail! 🎮