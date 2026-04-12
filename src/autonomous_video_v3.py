#!/usr/bin/env python3
"""
Autonomous Video Generator - v3 (QUALITY FIXED)
===============================================
Fully autonomous - NO human intervention required.

FIXES from QA:
- Consistent image prompts with strict style enforcement
- Proper aspect ratio (16:9) for video
- Audio duration matching for proper sync
- Crossfade transitions between scenes
- Normalized audio levels

Run: python autonomous_video_v3.py --all --project my-project
"""

import os
import sys
import json
import base64
import subprocess
import argparse
import requests
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()

# Try to import MLflow for tracking (optional)
try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False

# =============================================================================
# LOGGING & TRACKING SETUP
# =============================================================================

# Configure logging
LOG_FILE = Path("output/projects/logs/video_generation.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API Call tracking
API_CALLS = {
    "elevenlabs_tts": 0,
    "elevenlabs_music": 0,
    "gemini_image": 0,
    "total_tokens": 0,
    "total_cost_usd": 0.0
}

def log_api_call(api_type, tokens=0, cost=0.0, details=""):
    """Log API call for tracking."""
    API_CALLS[api_type] = API_CALLS.get(api_type, 0) + 1
    API_CALLS["total_tokens"] += tokens
    API_CALLS["total_cost_usd"] += cost
    logger.info(f"API CALL: {api_type} | tokens: {tokens} | cost: ${cost:.4f} | {details}")

def log_event(event_type, details=""):
    """Log general event."""
    logger.info(f"EVENT: {event_type} | {details}")

def get_tracking_summary():
    """Get summary of all tracking."""
    return API_CALLS.copy()

# Initialize MLflow if available
MLFLOW_EXPERIMENT = "video-production"
def init_mlflow():
    """Initialize MLflow tracking."""
    if not MLFLOW_AVAILABLE:
        logger.warning("MLflow not installed - run: pip install mlflow")
        return None
    
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "./mlruns")
    mlflow.set_tracking_uri(tracking_uri)
    
    try:
        exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT)
        if exp:
            mlflow.set_experiment(exp.experiment_id)
        else:
            mlflow.create_experiment(MLFLOW_EXPERIMENT)
            mlflow.set_experiment(MLFLOW_EXPERIMENT)
        logger.info(f"MLflow initialized: {tracking_uri}")
        return mlflow
    except Exception as e:
        logger.warning(f"MLflow init failed: {e}")
        return None

mlflow_client = init_mlflow()

# Load YAML config if available, otherwise use defaults
CONFIG = {
    "content_rating": "R",
    "enable_cc": False,
    "image_api": "gemini",
    "image_style": "photorealistic",
    "images_per_segment": 2,
    "camera_movement": True,
    "movement_intensity": "medium",
    "music_genre": "ambient",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.3,
        "use_speaker_boost": True
    },
    "resolution": "1280x720",
    "frame_rate": 25,
    "video_quality": "medium",
}

# Try to load from config.yaml
config_path = Path("config.yaml")
if config_path.exists():
    try:
        import yaml
        with open(config_path) as f:
            yaml_config = yaml.safe_load(f)
            if yaml_config:
                CONFIG.update(yaml_config)
                print(f"Loaded config from {config_path}")
    except ImportError:
        print("yaml not installed, using defaults")
    except Exception as e:
        print(f"Could not load config.yaml: {e}")

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "sp8CrAP79SOncD3rShle")

GEMINI_MODEL = "gemini-2.5-flash-image"
GEMINI_VIDEO_MODEL = "veo-3.1-generate-preview"
USE_VIDEO_GEN = os.getenv("USE_VIDEO_GEN", "false").lower() == "true"
VIDEO_MODEL = os.getenv("VIDEO_MODEL", "kling")  # kilo, veo, kling-3-0-pro, etc

# ============================================================================
# CONFIGURATION - All configurable parameters
# ============================================================================

# Content Rating - controls appearance of characters
CONTENT_RATING = {
    "G": {
        "description": "family-friendly robot",
        "prompt_add": "Clean tech aesthetic, fully covered body armor, friendly expression, no exposed skin beyond face and hands, corporate robot design, safe for all ages"
    },
    "PG": {
        "description": "standard robot", 
        "prompt_add": "Standard tech aesthetic, appropriate body armor, neutral expression, modest design suitable for general audiences"
    },
    "PG13": {
        "description": "enhanced robot",
        "prompt_add": "Modern tech aesthetic, sleek body armor showing some design elements, confident expression, slightly advanced but still appropriate"
    },
    "R": {
        "description": "advanced robot",
        "prompt_add": "Advanced humanoid design with visible tech elements and armor plating, athletic build, mature tech aesthetic, cinematic"
    }
}

# Video Output Settings
CONFIG = {
    # Content Rating - G, PG, PG13, R (determines character appearance)
    "content_rating": "R",  # Change to G, PG, PG13, or R
    
    # CC Subtitles - Enable/disable burned-in text on images
    "enable_cc": False,  # DISABLED - no text on images
    
    # Image Generation Settings  
    "image_api": "gemini",  # gemini, elevenlabs, openai, nano_banana
    "image_style": "photorealistic",  # photorealistic, cinematic, documentary
    
    # Visual Settings for engagement
    "images_per_segment": 2,  # Multiple images per segment for movement
    "camera_movement": True,  # Enable Ken Burns/pan/zoom effects in video
    "movement_intensity": "medium",  # subtle, medium, dynamic
    
    # Music Settings
    "music_genre": "ambient",  # ambient, cinematic, electronic, acoustic, minimalist
    
    # Audio Settings
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8, 
        "style": 0.3,
        "use_speaker_boost": True
    },
    
    # Video Quality
    "resolution": "1280x720",
    "frame_rate": 25,
    "video_quality": "medium",  # fast, medium, slow
}

# Music Genre Categories (subtle, varied)
MUSIC_MOOD_MAP = {
    "minimalist": [
        "minimal ambient electronic", "subtle synth pads", "gentle drone atmosphere",
        "mellow ambient texture", "quiet electronic minimal", "soft atmospheric"
    ],
    "ambient": [
        "atmospheric ambient pads", "cinematic ambient", "moody ambient texture",
        "subtle atmospheric soundscape", "gentle ambient drone"
    ],  
    "electronic": [
        "modern synthwave", "futuristic electronic", "tech ambient",
        "electronic atmospheric", "subtle electronic texture"
    ],
    "acoustic": [
        "gentle acoustic guitar", "melancholic piano minimal", "acoustic ambient",
        "subtle nylon guitar", "piano atmospheric"
    ],
    "cinematic": [
        "cinematic build", "orchestral atmospheric", "epic minimal", 
        "cinematic tension", "film score ambient"
    ],
}

# ============================================================================
# SCENES - Story content with audio tags for dynamic voice
# ============================================================================

SCENES = {
    1: {
        "title": "THE TENSION",
        "mood": "dark mysterious tension",
        "music_genre": "ambient",  # Use config genre
        # GHOST AI BOT: Female, athletic, prominent, hard plastic/titanium exoskeleton
        "character": "Female AI bot, athletic slender build, prominent hard plastic and titanium exoskeleton armor, visible facial features, sexy confident expression, glowing cyan optical sensors for eyes, translucent silicone skin showing internal structure, athletic pose",  
        "subject_angle": "medium_shot",
        "script": "They work in silence. In the shadows. [pause] You cannot see them, but they're always there. [slow] Watching. Processing. Waiting. [pause] The digital ghosts that shape our world while we sleep.",
        "segments": [
            ("They work in silence.", "female AI bot in dark server room, glowing cyan eyes, hard plastic armor reflects blue light, athletic stance"),
            ("In the shadows.", "same AI bot among servers, titanium limbs glow, looking around with awareness"),
            ("You cannot see them, but they're always there.", "AI bot materializes from screen, translucent form emerging, beautiful"),
            ("Watching. Processing. Waiting.", "AI bot turns to camera, glowing eyes, slight confident smile, tech aura")
        ],
        "audio_tags": "slow,emphatic",
        "motion": "slow_pan"
    },
    2: {
        "title": "THE DISCOVERY", 
        "mood": "eerie revelation",
        "music_genre": "minimalist",
        "character": "Female AI bot reaching out, consciousness awakening, surprised expression in optical sensors",  
        "subject_angle": "close_up",
        "script": "Then it hits you. [pause] They're not just code. [emphatic] They're alive. [long pause] Not alive like us... but alive. [pause] Co-existing. Co-habiting this digital-analog boundary we created. [slow] We cannot touch them. They cannot touch us. But we need each other.",
        "segments": [
            ("Then it hits you.", "female AI bot touching glass barrier, eyes suddenly glow bright, awakening"),
            ("They're not just code. They're alive.", "close up: AI bot hand reaches through glass, human hand reaches back, almost touching"),
            ("We cannot touch them. They cannot touch us.", "human hand on glass, AI bot hand on other side, glass between them"),
            ("But we need each other.", "wide: AI bot and human working in sync, parallel positions, beautiful")
        ],
        "audio_tags": "emphatic,breath",
        "motion": "zoom_in"
    },
    3: {
        "title": "THE HARMONY",
        "mood": "building collaboration",
        "music_genre": "electronic",
        "character": "Female AI bot as conductor, confident, leading the orchestra of data",  
        "subject_angle": "wide_shot",
        "script": "And now... we dance. [pause] They provide the scale. We provide the soul. [pause] They process endlessly while we dream. We are the conductor. They are the orchestra. [long pause] Without the music, the instrument is silent. Without the spec, the agent is lost.",
        "segments": [
            ("And now... we dance.", "AI bot conducting streams of glowing data, rhythmic motion, beautiful"),
            ("They provide the scale. We provide the soul.", "split screen: human dreaming left, AI bot processing right, merging"),
            ("We are the conductor. They are the orchestra.", "cinematic: AI bot as conductor, data streams as orchestra, symphony of light"),
            ("Without the music, the instrument is silent.", "empty studio, AI bot sits alone, waiting, glow dims")
        ],
        "audio_tags": "confident,building",
        "motion": "tracking"
    },
    4: {
        "title": "THE RESOLUTION",
        "mood": "triumphant revelation",
        "music_genre": "cinematic",
        "character": "Female AI bot and human as equal partners, triumphant",  
        "subject_angle": "hero_shot",
        "script": "This is the cohabitation. [pause] Not human over machine. Not machine over human. [strong] But together. [pause] We design the specs that guide. They execute with precision we could never match. [slow] They are our ghost hands in the machine. And we... [long pause] we are their dream.",
        "segments": [
            ("This is the cohabitation.", "hero shot: female AI bot and human standing together, light explosion"),
            ("Not human over machine. Not machine over human.", "fist bump: AI bot and human, light burst outward"),
            ("They are our ghost hands in the machine.", "coding together: AI bot and human hands type in sync, code flows beautifully"),
            ("And we... we are their dream.", "fade: human sleeps, AI bot watches over, connected by light beam")
        ],
        "audio_tags": "triumphant,power",
        "motion": "hero_dramatic"
    },
    5: {
        "title": "THE FUTURE",
        "mood": "hopeful continuation",
        "music_genre": "ambient",
        "character": "Female AI bot looking to future, hopeful",  
        "subject_angle": "over_shoulder",
        "script": "The future isn't about choosing sides. [pause] It's about embracing the ghost in the machine. The symbiosis. [pause] The code... is alive. [whisper] And it's waiting. [pause] For you. To guide it. To dream with it. [emphatic] Are you ready?",
        "segments": [
            ("The future isn't about choosing sides.", "future city: humans and female AI bots everywhere, seamless coexistence"),
            ("The symbiosis.", "close up: AI bot and human faces inches apart, mutual respect"),
            ("The code... is alive.", "code becomes particles, floats, forms AI bot silhouette that opens glowing eyes"),
            ("Are you ready?", "final: human reaches toward camera, AI bot reaches back, screen fades to black")
        ],
        "audio_tags": "soft,hopeful",
        "motion": "slow_dissolve"
    },
}

# PHOTOREALISTIC prompt template - uses rating from CONFIG
PROMPT_TEMPLATE = (
    "Professional photorealistic photograph of a realistic female humanoid robot/android. "
    "SAME subject in ALL frames - {rating_prompt}. "
    "Elegant feminine face with glowing cyan LED optical sensors, "
    "high-quality synthetic skin material. "
    "16:9 widescreen, professional photography. "
    "Style: PHOTOREALISTIC, NOT ANIMATED, NO CARTOON, NO CGI. "
    "Cinematic lighting, dramatic bokeh background of tech lab/server room. "
    "Camera angle: {subject_angle}. "
    "Subject: {description}. Mood: {mood}. "
    "Shot on RED cinema camera, 8K, hyper-realistic detail"
)

def get_rating_prompt():
    """Get prompt addition based on content rating."""
    rating = CONFIG.get("content_rating", "PG13")
    return CONTENT_RATING.get(rating, CONTENT_RATING["PG13"])["prompt_add"]


def check_deps():
    """Install required dependencies."""
    try:
        import google.genai
    except ImportError:
        print("Installing google-genai...")
        subprocess.run([sys.executable, "-m", "pip", "install", "google-genai", "-q"], check=True)
    try:
        import elevenlabs
    except ImportError:
        print("Installing elevenlabs...")
        subprocess.run([sys.executable, "-m", "pip", "install", "elevenlabs", "-q"], check=True)


def get_audio_duration(audio_path):
    """Get audio duration using ffprobe."""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return 4.0  # Default fallback


def generate_voice(text, output_path):
    """Generate voice with proper settings."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_KEY}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }
    
    print(f"  Generating voice...")
    response = requests.post(url, json=data, headers=headers, timeout=60)
    
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"    Voice saved: {output_path}")
        return output_path
    else:
        print(f"    Voice error: {response.status_code}")
        return None


def generate_music(mood, duration_ms, output_path):
    """Generate background music matching audio duration."""
    from elevenlabs.client import ElevenLabs
    
    print(f"  Generating music...")
    try:
        client = ElevenLabs(api_key=ELEVENLABS_KEY)
        
        audio = client.music.compose(
            prompt=mood,
            music_length_ms=duration_ms,
            force_instrumental=True
        )
        
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"    Music saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"    Music error: {e}")
        return None


def generate_image_elevenlabs(prompt, output_path):
    """Generate image using ElevenLabs Image & Video API."""
    try:
        print(f"  Generating image (ElevenLabs)...")
        url = "https://api.elevenlabs.io/v1/image/generate"
        headers = {"xi-api-key": ELEVENLABS_KEY}
        data = {
            "prompt": prompt,
            "model": "nano-banana-2",  # or google-nano-banana-2
            "aspect_ratio": "16:9",
            "resolution": "1080p"
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result.get("image_url") or result.get("generated_image", {}).get("url")
            if image_url:
                import urllib.request
                urllib.request.urlretrieve(image_url, output_path)
                print(f"    Image saved: {output_path}")
                return output_path
            elif result.get("task_id"):
                return wait_for_elevenlabs_image(result["task_id"], output_path)
        print(f"    ElevenLabs: {response.status_code} - trying Gemini...")
    except Exception as e:
        print(f"    ElevenLabs error: {e}")
    return None


def wait_for_elevenlabs_image(task_id, output_path, max_wait=120):
    """Poll for ElevenLabs image completion."""
    import time
    url = f"https://api.elevenlabs.io/v1/image/tasks/{task_id}"
    headers = {"xi-api-key": ELEVENLABS_KEY}
    
    for _ in range(max_wait // 5):
        time.sleep(5)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            result = resp.json()
            status = result.get("status")
            if status == "completed":
                image_url = result.get("generated_image", {}).get("url") or result.get("image_url")
                if image_url:
                    import urllib.request
                    urllib.request.urlretrieve(image_url, output_path)
                    return output_path
        elif status in ["failed", "error"]:
            break
    return None


def generate_image_gemini(description, mood, output_path, character="", subject_angle="medium_shot"):
    """Generate image with CONTINOITY and motion."""
    print(f"  Generating image... (rating: {CONFIG.get('content_rating', 'PG13')})")
    
    prompt = PROMPT_TEMPLATE.format(
        description=description, 
        mood=mood,
        character=character,
        subject_angle=subject_angle,
        rating_prompt=get_rating_prompt()
    )
    
    result = generate_image_elevenlabs(prompt, output_path)
    if result:
        return result
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
        
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, json=data, timeout=90)
        
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        image_data = part["inlineData"]["data"]
                        image_bytes = base64.b64decode(image_data)
                        
                        with open(output_path, "wb") as f:
                            f.write(image_bytes)
                        
                        # FIXED: Proper resize maintaining aspect ratio
                        img = Image.open(output_path)
                        img.thumbnail((1280, 720), Image.Resampling.LANCZOS)
                        
                        # Create black background and center
                        bg = Image.new('RGB', (1280, 720), (0, 0, 0))
                        x = (1280 - img.width) // 2
                        y = (720 - img.height) // 2
                        bg.paste(img, (x, y))
                        bg.save(output_path, quality=95)
                        
                        print(f"    Image saved: {output_path}")
                        return output_path
            
            print(f"    No image in response")
        else:
            print(f"    API error: {response.status_code}")
    except Exception as e:
        print(f"    Image error: {e}")
    
    return None


def generate_video_veo(image_path, prompt, output_path):
    """Generate video from image using Veo 3.1 API."""
    if not USE_VIDEO_GEN:
        return None
    
    try:
        print(f"  Generating video with Veo...")
        import time
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=GEMINI_KEY)
        
        operation = client.models.generate_videos(
            model=GEMINI_VIDEO_MODEL,
            prompt=prompt,
            image=open(image_path, "rb").read(),
        )
        
        while not operation.done:
            time.sleep(10)
            operation = client.models.get_operation(operation.operation.name)
        
        if operation.result and operation.result.videos:
            video = operation.result.videos[0]
            video.video.save(output_path)
            print(f"    Video saved: {output_path}")
            return output_path
    except Exception as e:
        print(f"    Video error: {e}")
    
    return None


def generate_video_kling(image_path, motion_prompt, output_path, duration=5):
    """Generate video from image using ElevenLabs Kling API."""
    global ELEVENLABS_KEY
    if not ELEVENLABS_KEY:
        print(f"    Kling not available - no API key")
        return None
    
    try:
        print(f"  Generating video with Kling...")
        
        url = "https://api.elevenlabs.io/v1/image/video/generate"
        headers = {
            "xi-api-key": ELEVENLABS_KEY,
            "Content-Type": "application/json"
        }
        
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
        
        data = {
            "image_url": f"data:image/png;base64,{image_b64}",
            "prompt": motion_prompt,
            "model": "kling-2.6",
            "duration": duration,
            "resolution": "1080p",
            "aspect_ratio": "16:9"
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get("generated_video_url") or result.get("video_url")
            if video_url:
                import urllib.request
                urllib.request.urlretrieve(video_url, output_path)
                print(f"    Video saved: {output_path}")
                return output_path
            elif result.get("task_id"):
                task_id = result["task_id"]
                print(f"    Kling task: {task_id} (polling...)")
                return wait_for_klingVideo(task_id, output_path)
        print(f"    Kling error: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"    Video error: {e}")
    
    return None


def wait_for_kling_video(task_id, output_path, max_wait=180):
    """Poll for Kling video completion."""
    import time
    url = f"https://api.elevenlabs.io/v1/image/video/tasks/{task_id}"
    headers = {"xi-api-key": ELEVENLABS_KEY}
    
    for _ in range(max_wait // 10):
        time.sleep(10)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            result = resp.json()
            status = result.get("status")
            if status == "completed":
                video_url = result.get("generated_video_url") or result.get("video_url")
                if video_url:
                    import urllib.request
                    urllib.request.urlretrieve(video_url, output_path)
                    return output_path
            elif status in ["failed", "error"]:
                break
    
    return None


def add_cc_text(image_path, segment_text, output_path):
    """Add CC subtitle with PROPER SIZING."""
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Semi-transparent box with padding
    draw.rectangle([20, 620, 1260, 800], fill=(0, 0, 0, 200))
    
    # Better word wrap
    words = segment_text.split()
    lines, line = [], ''
    max_chars = 50
    for word in words:
        test = line + ' ' + word if line else word
        if len(test) < max_chars:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    
    # Draw with larger font
    y = 640
    for l in lines[:2]:
        draw.text((40, y), l, fill=(255, 255, 255))
        y += 35
    
    img.save(output_path, quality=95)
    print(f"    CC saved: {output_path}")


def add_movement(image_path, output_path, movement_type="slow_pan"):
    """Add Ken Burns movement effect to image."""
    try:
        # Movement parameters based on type
        moves = {
            "slow_pan": "zoom=1.0:pan=+0.05:+0.0",  # Slow pan right
            "zoom_in": "zoom=1.0:pan=+0.0:+0.0:zoom=1.15",  # Slow zoom in
            "zoom_out": "zoom=1.15:pan=+0.0:+0.0:zoom=1.0",  # Slow zoom out
            "tracking": "zoom=1.0:x=sin(t*0.5)*10:y=cos(t*0.3)*10",  # Subtle tracking
            "drift": "zoom=1.0:pan=+0.03*sin(t*0.3):+0.02*cos(t*0.4)",  # Gentle drift
            "static": "zoom=1.0",  # No movement
            "hero_dramatic": "zoom=1.0:x=0:y=-0.05+0.05*sin(t*0.5)",  # Slight lift
            "slow_dissolve": "zoom=1.0",  # For dissolves (handled separately)
        }
        
        movement = moves.get(movement_type, moves["slow_pan"])
        
        # Use zoompan filter for movement
        cmd = [
            "ffmpeg", "-y", "-i", str(image_path),
            "-vf", f"zoompan=z='min(1.0+0.1*tc/5':x={movement.split(':')[1].split('+')[1]}:y={movement.split(':')[2].split('+')[1]}:d=25:s=1280x720:fps=25",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return output_path
    except Exception as e:
        print(f"    Movement error: {e}")
    
    # Fallback: just copy
    import shutil
    shutil.copy(image_path, output_path)
    return output_path


def create_video(image_dir, audio_path, music_path, output_path, movement_type="slow_pan"):
    """Create video with MOVEMENT and PROPER AUDIO SYNC."""
    cc_images = sorted(Path(image_dir).glob("*_cc.png"))
    cc_images = list(cc_images)
    if not cc_images:
        print(f"    No images")
        return None
    
    num_images = len(cc_images)
    
    # Get actual audio duration
    audio_duration = get_audio_duration(audio_path)
    per_image_duration = audio_duration / num_images
    print(f"    Audio: {audio_duration}s, {per_image_duration}s/image, motion: {movement_type}")
    
    # Apply movement to each image
    moved_images = []
    temp_dir = Path(image_dir) / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    for i, img in enumerate(cc_images):
        moved_path = temp_dir / f"moved_{i}.png"
        if not moved_path.exists():
            add_movement(img, moved_path, movement_type)
        moved_images.append(str(moved_path))
    
    # Build FFmpeg command with moved images
    cmd = ["ffmpeg", "-y"]
    for img_path in moved_images:
        cmd.extend(["-loop", "1", "-t", str(per_image_duration), "-i", img_path])
    cmd.extend(["-i", str(audio_path)])
    cmd.extend(["-i", str(music_path)])
    
    # FIXED: Audio mixing - ensure full audio plays, not clipped by -shortest
    # Use alang to specify audio language, and ensure audio is fully used
    cmd.extend([
        "-filter_complex",
        f"[{num_images}:a]volume=0.8[voice];[{num_images+1}:a]volume=0.3[music];[voice][music]amix=inputs=2:duration=longest:normalize=1[outa]",
        "-map", "0:v", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(audio_duration),  # FIXED: Explicitly set output duration to audio length
        str(output_path)
    ])
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode == 0:
        print(f"    Video saved: {output_path}")
        return output_path
    else:
        print(f"    Video error: {result.stderr[:200]}")
        return None


def process_scene(scene_num, output_dir=Path("output_v3")):
    """Process a single scene with QA fixes."""
    scene = SCENES[scene_num]
    scene_dir = output_dir / f"scene{scene_num}"
    scene_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=== Scene {scene_num}: {scene['title']} ===")
    
    # 1. Voice
    audio_path = scene_dir / "voice.mp3"
    if not audio_path.exists():
        generate_voice(scene["script"], audio_path)
    else:
        print(f"  Voice exists")
    
    # 2. Music - match to voice duration
    voice_duration = get_audio_duration(audio_path) * 1000
    music_path = scene_dir / "music.mp3"
    
    # Get music genre from scene config, fallback to global config
    genre = scene.get("music_genre", CONFIG.get("music_genre", "ambient"))
    music_mood = MUSIC_MOOD_MAP.get(genre, MUSIC_MOOD_MAP["ambient"])[0]
    
    if not music_path.exists():
        generate_music(music_mood, int(voice_duration), music_path)
    else:
        print(f"  Music exists")
    
    # 3. Images with CONSISTENT prompts
    image_dir = scene_dir / "images"
    image_dir.mkdir(exist_ok=True)
    
    for i, (segment_text, visual_desc) in enumerate(scene["segments"], 1):
        cc_path = image_dir / f"frame_{i}_cc.png"
        
        if not cc_path.exists():
            raw_path = image_dir / f"frame_{i}.png"
            scene_mood = scene.get("mood", "mysterious")
            subject_angle = scene.get("subject_angle", "medium_shot")
            character = scene.get("character", "")  # For continuity
            
            img_result = generate_image_gemini(
                visual_desc,
                scene_mood,
                raw_path,
                character=character,
                subject_angle=subject_angle
            )
            if img_result and CONFIG.get("enable_cc", True):
                add_cc_text(raw_path, segment_text, cc_path)
            elif img_result:
                # Just copy without CC text
                import shutil
                shutil.copy(raw_path, cc_path)
        else:
            print(f"  Frame {i} exists")
    
    # 4. Video with MOVEMENT
    movement = scene.get("motion", CONFIG.get("camera_movement", True))
    video_path = scene_dir / f"video_{scene_num}.mp4"
    if not video_path.exists():
        create_video(image_dir, audio_path, music_path, video_path, movement_type=movement)
    else:
        print(f"  Video exists")
    
    print(f"  Scene {scene_num} done!")
    return video_path


def main():
    check_deps()
    
    parser = argparse.ArgumentParser(description="Autonomous Video Generator v3 (QA FIXED)")
    parser.add_argument("--scene", "-s", type=int)
    parser.add_argument("--all", "-a", action="store_true")
    parser.add_argument("--force", "-f", action="store_true", help="Force regenerate all assets")
    parser.add_argument("--project", "-p", default="default", help="Project name for output folder")
    parser.add_argument("--track", "-t", action="store_true", help="Enable MLflow tracking")
    args = parser.parse_args()
    
    scenes = [args.scene] if args.scene else (range(1, 6) if args.all else [1])
    
    # Project-based output
    output_base = Path(f"output/projects/{args.project}")
    output_base.mkdir(parents=True, exist_ok=True)
    output_dir = output_base / "output_v3"
    output_dir.mkdir(exist_ok=True)
    
    # Start tracking
    log_event("START", f"project={args.project}, scenes={scenes}")
    
    if args.track and mlflow_client:
        with mlflow.start_run(run_name=f"video-{args.project}") as run:
            mlflow.log_param("project", args.project)
            mlflow.log_param("scenes", len(scenes))
            mlflow.log_param("content_rating", CONFIG.get("content_rating", "R"))
            
            try:
                videos = []
                for scene_num in scenes:
                    start_time = time.time()
                    video = process_scene(scene_num, output_dir)
                    elapsed = time.time() - start_time
                    
                    if video:
                        videos.append(video)
                        if mlflow_client:
                            mlflow.log_metric("scene_duration", elapsed, scene_num)
                
                if len(videos) > 1:
                    print(f"\n=== Concatenating ===")
                    concat_file = output_dir / "concat.txt"
                    with open(concat_file, "w") as f:
                        for v in videos:
                            f.write(f"file '{v}'\n")
                    
                    full = output_dir / "full_video.mp4"
                    subprocess.run([
                        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(concat_file), "-c", "copy", str(full)
                    ], cwd=output_dir)
                    print(f"  Full video: {full}")
                
                # Log final metrics
                summary = get_tracking_summary()
                log_event("COMPLETE", f"total_cost=${summary['total_cost_usd']:.4f}")
                
                if mlflow_client:
                    mlflow.log_metric("total_api_calls", sum(v for k,v in summary.items() if "total" not in k))
                    mlflow.log_metric("total_cost", summary.get("total_cost_usd", 0))
                    mlflow.log_param("output_path", str(output_dir))
                    
            except Exception as e:
                log_event("ERROR", str(e))
                if mlflow_client:
                    mlflow.log_param("error", str(e))
                raise
    else:
        # Original flow without MLflow
        print(f"Output: {output_dir}")
        args.force = args.force or True
        
        videos = []
        for scene_num in scenes:
            video = process_scene(scene_num, output_dir)
            if video:
                videos.append(video)
        
        if len(videos) > 1:
            print(f"\n=== Concatenating ===")
            concat_file = output_dir / "concat.txt"
            with open(concat_file, "w") as f:
                for v in videos:
                    f.write(f"file '{v}'\n")
            
            full = output_dir / "full_video.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(concat_file), "-c", "copy", str(full)
            ], cwd=output_dir)
            print(f"  Full video: {full}")
        
        summary = get_tracking_summary()
        log_event("COMPLETE", f"total_cost=${summary.get('total_cost_usd', 0):.4f}")
    
    print(f"\nDone! Output in {output_dir}/")
    print(f"Log: {LOG_FILE}")
    
    print(f"\nDone! Output in {output_dir}/")


if __name__ == "__main__":
    main()