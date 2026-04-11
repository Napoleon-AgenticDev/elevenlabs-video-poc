# Configuration Guide ⚙️

## What's This File?

`config.py` is like the control center of the whole project. It holds all the important settings so you don't have to remember them!

## Quick Overview

```python
# API Configuration
API_KEY = "sk_1818f1c49bcb09529927e0e6f8606d079c232963dbf31632"
BASE_URL = "https://api.elevenlabs.io"

# Voice Configuration
VOICES = { ... }

# Model Configuration  
MODELS = { ... }

# Default Settings
DEFAULT_VOICE = "brittney"
DEFAULT_MODEL = "eleven_v3"
```

## The Parts

### 1. API Configuration 🔑

This is your magic key to use ElevenLabs!

```python
API_KEY = "sk_1818f1c49bcb09529927e0e6f8606d079c232963dbf31632"
BASE_URL = "https://api.elevenlabs.io"
```

**Never share your API key!** It's like a password.

### 2. Voice Configuration 🎤

All the voices you can use are stored here:

```python
VOICES = {
    "brittney": {
        "id": "kPzsL2i3teMYv0FxEYQ6",
        "name": "Brittney",
        "description": "Fun, Youthful & Informative"
    },
    "george": { ... },
    # ... more voices
}
```

**How to use:**
```python
from config import get_voice

voice_id = get_voice("brittney")  # Returns "kPzsL2i3teMYv0FxEYQ6"
```

### 3. Model Configuration 🧠

Different AI brains for different needs:

```python
MODELS = {
    "eleven_v3": {
        "description": "Most emotionally expressive",
        "char_limit": 5000
    },
    "eleven_multilingual_v2": {
        "description": "Best for multilingual",
        "char_limit": 10000
    },
    "eleven_flash_v2_5": {
        "description": "Ultra-low latency",
        "char_limit": 40000
    }
}
```

### 4. Voice Settings 🎛️

Presets for different styles:

```python
VOICE_SETTINGS = {
    "default": {"stability": 0.5, "similarity_boost": 0.75},
    "narrator": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.2},
    "energetic": {"stability": 0.3, "similarity_boost": 0.9, "style": 0.5},
    "calm": {"stability": 0.7, "similarity_boost": 0.6}
}
```

### 5. Helper Functions

```python
# Get voice ID by nickname
get_voice("brittney")  # → "kPzsL2i3teMYv0FxEYQ6"

# Get voice name
get_voice_name("brittney")  # → "Brittney"

# List all voices
list_voices()  # → [{"key": "brittney", "id": "...", "name": "..."}, ...]
```

## Customizing the Config

### Change Default Voice:
```python
DEFAULT_VOICE = "george"  # Change default
```

### Add New Voice:
```python
VOICES = {
    # ... existing voices ...
    "mystery": {
        "id": "YOUR_NEW_VOICE_ID",
        "name": "Mystery Voice",
        "description": "Something cool"
    }
}
```

### Add New Preset:
```python
VOICE_SETTINGS = {
    # ... existing presets ...
    "robotic": {
        "stability": 0.9,
        "similarity_boost": 0.5,
        "style": 0
    }
}
```

## Using with Environment Variables

Create a `.env` file (copy from `.env.example`):

```
ELEVENLABS_API_KEY=sk_1818f1c49bcb09529927e0e6f8606d079c232963dbf31632
DEFAULT_VOICE=brittney
```

Then in Python:
```python
import os
API_KEY = os.getenv("ELEVENLABS_API_KEY")  # Reads from .env
```

## Why Use Config?

✅ **One place to change settings** - Don't hunt through code!
✅ **Easy to share** - Just share the config, not your key
✅ **Consistent** - Same settings everywhere
✅ **Easy to update** - Change once, applies everywhere

---

**Now you're a config pro!** 

Go make something cool! 🚀