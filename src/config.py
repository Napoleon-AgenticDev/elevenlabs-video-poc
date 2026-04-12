import os
from pathlib import Path

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

# Configuration file location
CONFIG_DIR = Path(__file__).parent
CONFIG_FILE = CONFIG_DIR / ".env"

# API Configuration
API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://api.elevenlabs.io"

# Voice Configuration
VOICES = {
    "brittney": {
        "id": "kPzsL2i3teMYv0FxEYQ6",
        "name": "Brittney",
        "description": "Fun, Youthful & Informative",
        "use_case": "Primary narrator (social media style)"
    },
    "george": {
        "id": "JBFqnCBsd6RMkjVDRZzb",
        "name": "George",
        "description": "Warm, Captivating Storyteller",
        "use_case": "Dialogue, storytelling"
    },
    "sarah": {
        "id": "EXAVITQu4vr4xnSDxMaL",
        "name": "Sarah",
        "description": "Mature, Reassuring, Confident",
        "use_case": "Dialogue, professional"
    },
    "roger": {
        "id": "CwhRBWXzGAHq8TQ4Fs17",
        "name": "Roger",
        "description": "Laid-Back, Casual, Resonant",
        "use_case": "Casual content"
    },
    "matilda": {
        "id": "XrExE9yKIg1WjnnlVkGX",
        "name": "Matilda",
        "description": "Knowledgeable, Professional",
        "use_case": "Educational"
    },
    "adam": {
        "id": "pNInz6obpgDQGcFmaJgB",
        "name": "Adam",
        "description": "Dominant, Firm",
        "use_case": "Authority"
    }
}

# Model Configuration
MODELS = {
    "eleven_v3": {
        "description": "Most emotionally expressive",
        "char_limit": 5000,
        "latency": "higher"
    },
    "eleven_multilingual_v2": {
        "description": "Best for multilingual",
        "char_limit": 10000,
        "latency": "medium"
    },
    "eleven_flash_v2_5": {
        "description": "Ultra-low latency",
        "char_limit": 40000,
        "latency": "~75ms"
    }
}

# Default Settings
DEFAULT_VOICE = "brittney"
DEFAULT_MODEL = "eleven_v3"

# Voice Settings Presets
VOICE_SETTINGS = {
    "default": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0,
        "speed": 1
    },
    "narrator": {
        "stability": 0.4,
        "similarity_boost": 0.8,
        "style": 0.2,
        "speed": 1
    },
    "energetic": {
        "stability": 0.3,
        "similarity_boost": 0.9,
        "style": 0.5,
        "speed": 1.1
    },
    "calm": {
        "stability": 0.7,
        "similarity_boost": 0.6,
        "style": 0,
        "speed": 0.95
    }
}

# Output Formats
OUTPUT_FORMATS = [
    "mp3_22050_32",
    "mp3_24000_48",
    "mp3_44100_32",
    "mp3_44100_64",
    "mp3_44100_96",
    "mp3_44100_128",
    "mp3_44100_192",
    "pcm_16000",
    "pcm_22050",
    "pcm_24000",
    "wav_44100"
]

DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"

# Helper functions
def get_voice(voice_key: str) -> str:
    """Get voice ID by key"""
    return VOICES.get(voice_key.lower(), VOICES[DEFAULT_VOICE])["id"]

def get_voice_name(voice_key: str) -> str:
    """Get voice name by key"""
    return VOICES.get(voice_key.lower(), VOICES[DEFAULT_VOICE])["name"]

def list_voices() -> list:
    """List all available voices"""
    return [
        {"key": k, **v} for k, v in VOICES.items()
    ]

if __name__ == "__main__":
    print("ElevenLabs Video POC Configuration")
    print("=" * 40)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Base URL: {BASE_URL}")
    print(f"Default Voice: {DEFAULT_VOICE} ({get_voice(DEFAULT_VOICE)})")
    print(f"Default Model: {DEFAULT_MODEL}")
    print("\nAvailable Voices:")
    for v in list_voices():
        print(f"  {v['key']}: {v['name']} - {v['description']}")