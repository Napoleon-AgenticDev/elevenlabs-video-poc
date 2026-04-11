# Welcome to the ElevenLabs Video POC! 📺

This project shows you how to use AI to make videos with cool voices!

## What's This About?

Imagine you want to make a YouTube video or Instagram Reel, but you don't want to record your voice. This project lets you type what you want to say, and the computer reads it out loud in a really nice voice!

We use something called **ElevenLabs** - it's like a super smart robot that can talk like a human!

## What Can You Do With This?

✅ **Make videos with AI voices** - Just type, and it talks!
✅ **Create multi-voice conversations** - Two different voices talking to each other
✅ **Choose different voices** - Fun voice, serious voice, friendly voice, and more!
✅ **Make social media videos** - Perfect for YouTube, Instagram, TikTok

## Quick Start (5 Minutes!)

### Step 1: Get Your Magic Key
You need a special password (called an API key) to use ElevenLabs. Ask your teacher or parent to help you get one from [elevenlabs.io](https://elevenlabs.io)!

### Step 2: Install the Stuff
```bash
pip install requests
```

### Step 3: Make Your First Sound!
```bash
python generate_audio.py --text "Hello world!" --voice brittney --output hello.mp3
```

And that's it! You just made a talking sound! 🎉

## The Files in This Project

| File | What It Does |
|------|--------------|
| `config.py` | Holds all the voice settings and magic keys |
| `generate_audio.py` | The tool that makes the talking sounds |
| `create_video.py` | Turns sounds into actual videos |
| `video-script.md` | The story we tell in our video |
| `docs/` | All the explanations (you're reading one now!) |

## Try It Out!

### Make a voice say something:
```bash
python generate_audio.py --text "I love making videos!" --output myvoice.mp3
```

### List all the voices:
```bash
python generate_audio.py --list-voices
```

### Make two voices talk:
```bash
python generate_audio.py --dialogue --dialogue-input '[{"text":"Hello!","voice_id":"kPzsL2i3teMYv0FxEYQ6"},{"text":"Hi there!","voice_id":"JBFqnCBsd6RMkjVDRZzb"}]' --output conversation.mp3
```

## The Voices You Can Use

| Voice Name | Sounds Like |
|------------|-------------|
| Brittney | Fun friend who tells you about stuff |
| George | Storyteller who reads books |
| Sarah | Professional news reporter |
| Roger | Chill buddy hanging out |
| Matilda | Smart teacher |
| Adam | Boss who means business |

## What's Next?

Now that you know the basics, you can:

1. 📝 **Write your own story** - Edit `video-script.md`
2. 🎬 **Make a video** - Use `create_video.py`
3. 🎨 **Add pictures** - Create images for each scene
4. 📱 **Share it!** - Post to YouTube or Instagram

## Need Help?

Check out these other documents in the `docs/` folder:

- [How It Works](how-it-works.md) - Simple explanation of the technology
- [API Guide](api-guide.md) - How to talk to ElevenLabs
- [Voice Guide](voice-guide.md) - All about choosing voices
- [Troubleshooting](troubleshooting.md) - What to do if something breaks

---

**Made with 💜 using ElevenLabs API**

Now go make something cool! 🚀