#!/usr/bin/env python3
"""
ElevenLabs Video POC - Audio Generator

Usage:
    python generate_audio.py --text "Hello world" --voice brittney
    python generate_audio.py --text "Hello world" --voice george --model eleven_v3
    python generate_audio.py --scene 1 --output ./output/
"""

import argparse
import json
import sys
import requests
from pathlib import Path
from config import (
    API_KEY, BASE_URL, VOICES, MODELS, DEFAULT_VOICE, DEFAULT_MODEL,
    VOICE_SETTINGS, DEFAULT_OUTPUT_FORMAT, get_voice, get_voice_name
)

def generate_speech(text: str, voice_key: str = None, model: str = None, 
                    output_file: str = None, settings_preset: str = "narrator") -> bytes:
    """Generate speech using ElevenLabs API"""
    
    voice_key = voice_key or DEFAULT_VOICE
    model = model or DEFAULT_MODEL
    voice_id = get_voice(voice_key)
    voice_name = get_voice_name(voice_key)
    
    settings = VOICE_SETTINGS.get(settings_preset, VOICE_SETTINGS["default"])
    
    url = f"{BASE_URL}/v1/text-to-speech/{voice_id}"
    
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "voice_settings": settings,
        "model_id": model,
        "output_format": DEFAULT_OUTPUT_FORMAT
    }
    
    print(f"Generating speech...")
    print(f"  Voice: {voice_name} ({voice_id})")
    print(f"  Model: {model}")
    print(f"  Text: {text[:50]}{'...' if len(text) > 50 else ''}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    if output_file:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"  Saved to: {output_file}")
    
    return response.content

def generate_dialogue(inputs: list, model: str = None, output_file: str = None) -> bytes:
    """Generate multi-voice dialogue using ElevenLabs API"""
    
    model = model or DEFAULT_MODEL
    
    url = f"{BASE_URL}/v1/text-to-dialogue"
    
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": inputs,
        "model_id": model
    }
    
    print(f"Generating dialogue...")
    print(f"  Model: {model}")
    print(f"  Inputs: {len(inputs)} lines")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    if output_file:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"  Saved to: {output_file}")
    
    return response.content

def get_available_voices() -> dict:
    """Fetch all available voices from API"""
    
    url = f"{BASE_URL}/v1/voices"
    
    headers = {
        "xi-api-key": API_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching voices: {response.status_code}")
        return {}
    
    voices = {}
    for v in response.json().get("voices", []):
        voices[v["voice_id"]] = v.get("name", "Unknown")
    
    return voices

def main():
    parser = argparse.ArgumentParser(description="ElevenLabs Audio Generator")
    parser.add_argument("--text", help="Text to generate speech for")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Voice key (brittney, george, sarah, etc.)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model ID")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--dialogue", action="store_true", help="Use dialogue mode (requires --dialogue-input)")
    parser.add_argument("--dialogue-input", type=json.loads, help="JSON array of {text, voice_id} objects")
    
    args = parser.parse_args()
    
    if args.list_voices:
        print("Configured Voices:")
        for key, voice in VOICES.items():
            print(f"  {key}: {voice['name']} - {voice['description']}")
        
        print("\nFetching all available voices from API...")
        api_voices = get_available_voices()
        print("\nAPI Voices:")
        for vid, name in api_voices.items():
            print(f"  {vid}: {name}")
        return
    
    if args.dialogue and args.dialogue_input:
        generate_dialogue(args.dialogue_input, args.model, args.output)
    elif args.text:
        generate_speech(args.text, args.voice, args.model, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()