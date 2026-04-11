# Welcome to the ElevenLabs Video POC! 📺

This project shows you how to use AI to make SPECTACULAR videos with AI voices and images!

## What's This About?

Imagine you want to make a YouTube video or Instagram Reel, but you don't want to record your voice or create images. This project does it ALL with AI:
- **AI Voice** - Type what you want, it talks with EXPRESSION
- **AI Images** - Describe what you want, it generates cinematic images
- **Video** - Combines everything into a real video!

We use:
- **ElevenLabs v3** - The most expressive AI voice with Audio Tags
- **OpenAI GPT Image** - AI-generated cinematic images
- **FFmpeg** - Video compilation

## What Can You Do With This?

✅ **Make videos with AI voices** - Just type, and it talks!
✅ **Add voice inflections** - Use [shouts], [whispers], [emphatic] for drama
✅ **Generate AI images** - Describe your scene, get a cinematic image
✅ **Create full videos** - Audio + images + text = professional video
✅ **Multi-voice dialogue** - Two or more AI voices talking

## Quick Start (10 Minutes!)

### Step 1: Get Your Magic Keys
You need two API keys:
- **ElevenLabs** - Get from [elevenlabs.io/app/api](https://elevenlabs.io/app/api)
- **OpenAI** - Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Step 2: Set Up
```bash
# Create .env file with your keys
ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Step 3: Generate Spectacular Audio!
```bash
# Creates audio with dramatic voice inflections
python generate_spectacular_audio.py
```

### Step 4: Generate Images
```bash
# Creates cinematic AI images
python generate_images.py --all
```

### Step 5: Create Video
```bash
# Combines audio + images + text into video
ffmpeg -loop 1 -i scene1_with_text.png -i audio.mp3 -shortest output.mp4
```

## The Files in This Project

| File | What It Does |
|------|--------------|
| `config.py` | Holds all settings, voices, API keys |
| `generate_spectacular_audio.py` | ⭐ Audio with voice inflections (v3 Audio Tags) |
| `generate_images.py` | ⭐ AI image generation with OpenAI |
| `generate_enhanced_audio.py` | Audio with expressive tags |
| `create_video.py` | Turns everything into video |
| `SKILL.md` | 📚 Complete skill for AI agents |
| `video-script-enhanced.md` | Example script with Audio Tags |
| `image-prompts.md` | Cinematic image prompts |
| `docs/` | All the explanations |

## ✨ New: Audio Tags (v3 Expressive Voice)

Add DRAMA to your voice with these tags:

| Tag | Example |
|-----|---------|
| `[shouts]` | "CODE EVERYWHERE [shouts]" |
| `[whispers]` | "It's not about programming directly [whispers]" |
| `[emphatic]` | "The SECRET is [emphatic] self-verification" |
| `[excited]` | "ONE MILLION lines [excited] with 3 engineers!" |
| `[long pause]` | "The shift? [long pause] Humans don't write code anymore" |
| `[sighs]` | "It started spiraling out of control [sighs]" |
| `[slow]` | "...into the darkness [slow]" |

**Full list in:** [Voice Guide](voice-guide.md)

## Try It Out!

### Make a voice say something with expression:
```bash
python generate_spectacular_audio.py --scene 1
```

### List all available voices:
```bash
python generate_audio.py --list-voices
```

### Generate all 5 scenes:
```bash
python generate_spectacular_audio.py --all
```

### Generate cinematic images:
```bash
python generate_images.py --all
```

## The Voices You Can Use

| Voice Name | Sounds Like | Best For |
|------------|-------------|----------|
| Brittney ⭐ | Fun, youthful | Social media, vlogs |
| George | Warm storyteller | Narratives |
| Sarah | Professional | Business, tutorials |
| Roger | Chill, casual | Podcasts |
| Matilda | Knowledgeable | Educational |
| Adam | Dominant | Action, drama |

## What's Next?

Now that you know the basics, you can:

1. 📝 **Write your own story** - Edit scripts with Audio Tags
2. 🎬 **Make a spectacular video** - Run generate_spectacular_audio.py
3. 🎨 **Create AI images** - Use prompts from image-prompts.md
4. 📱 **Share it!** - Post to YouTube or Instagram
5. 🤖 **Use in AI agents** - Import SKILL.md into Claude/OpenCode

## Need Help?

- [How It Works](how-it-works.md) - Simple explanation
- [API Guide](api-guide.md) - ElevenLabs & OpenAI APIs
- [Voice Guide](voice-guide.md) - All about Audio Tags
- [Video Script Guide](video-script-guide.md) - Writing with expression
- [Troubleshooting](troubleshooting.md) - Fix common issues

---

**Made with 💜 using ElevenLabs v3 + OpenAI GPT Image**

Now go make something SPECTACULAR! 🚀