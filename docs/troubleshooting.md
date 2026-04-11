# Troubleshooting 🔧

## Oh no! Something broke! Don't worry, we've got you!

## Common Problems and Fixes

### Problem: "Voice not found" Error

**What it looks like:**
```
{"detail":{"status":"voice_not_found","message":"Voice(s) not found: xyz123"}}
```

**What it means:** You're using a voice ID that doesn't exist or isn't in your account.

**How to fix:**
1. Run `--list-voices` to see what voices you have access to
2. Make sure you're using the correct voice ID
3. Some voices are only available on paid plans

```bash
python generate_audio.py --list-voices
```

---

### Problem: "API key invalid" Error

**What it looks like:**
```
401 Unauthorized
```

**What it means:** Your API key is wrong or expired.

**How to fix:**
1. Check your API key in `config.py`
2. Make sure it starts with `sk_`
3. Get a new key from [elevenlabs.io/app/api](https://elevenlabs.io/app/api)

---

### Problem: "Too many characters" Error

**What it looks like:**
```
{"detail":{"status":"text_limit_exceeded"}}
```

**What it means:** Your text is too long for the model!

**How to fix:**

| Model | Max Characters |
|-------|-----------------|
| eleven_v3 | 5,000 |
| eleven_multilingual_v2 | 10,000 |
| eleven_flash_v2_5 | 40,000 |

**Solution:** Split your text into smaller pieces!

```python
# Instead of one long text...
long_text = "This is a very long text..."

# Split it!
chunks = long_text.split(".")
for i, chunk in enumerate(chunks):
    if chunk.strip():
        # Generate each chunk separately
        generate_speech(chunk, output_file=f"part{i}.mp3")
```

---

### Problem: "Connection timeout" or "Network error"

**What it means:** Your internet is being slow or ElevenLabs is busy.

**How to fix:**
1. Try again in a few seconds
2. Check your internet connection
3. Add a timeout to your requests:

```python
import requests

response = requests.post(
    url, 
    headers=headers, 
    json=data,
    timeout=30  # Wait up to 30 seconds
)
```

---

### Problem: Video file is too big or takes forever

**What it means:** Your video is huge!

**How to fix:**
- Use smaller image files
- Use MP3 instead of WAV
- Reduce video resolution in ffmpeg:

```bash
ffmpeg -i input.mp4 -vf scale=1280:-2 -c:v libx264 -crf 23 output.mp4
```

---

### Problem: "ffmpeg not found" when making video

**What it means:** You don't have ffmpeg installed!

**How to fix:**

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

---

### Problem: Audio plays too fast or too slow

**What it means:** The speed setting is wrong!

**How to fix:**
In `config.py`, change the speed:

```python
"narrator": {
    "speed": 0.95  # Slightly slower
}
```

Or in your request:
```json
{"voice_settings": {"speed": 0.9}}
```

---

### Problem: Different voice every time

**What it means:** The stability is too low!

**How to fix:**
```json
{"voice_settings": {"stability": 0.7}}
```

Higher stability = more consistent voice!

---

## Getting More Help

### Check the Status
Sometimes ElevenLabs has outages. Check:
- https://status.elevenlabs.io

### Look at the Docs
ElevenLabs has official docs:
- https://elevenlabs.io/docs

### Ask Questions
- GitHub Issues: https://github.com/Napoleon-AgenticDev/elevenlabs-video-poc/issues

---

## Error Codes Quick Reference

| Code | Meaning |
|------|---------|
| 200 | Success! 🎉 |
| 400 | Bad request - check your JSON |
| 401 | Wrong API key |
| 422 | Validation error - missing something |
| 429 | Too many requests - wait a bit |
| 500 | ElevenLabs server problem |

---

**Still stuck?** That's okay! Try:
1. Restart your computer
2. Check your internet
3. Try a simpler command
4. Ask for help!

Remember: Every expert was once a beginner! 🌟