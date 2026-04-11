#!/usr/bin/env python3
"""
Generate Forced Alignment data from audio files.
Uses ElevenLabs Forced Alignment API to get word-level timestamps.
"""

import os
import json
import sys
from io import BytesIO
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
API_URL = "https://api.elevenlabs.io/v1/forced-alignment"


def format_time_srt(seconds: float) -> str:
    """Format seconds to SRT time format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_time_vtt(seconds: float) -> str:
    """Format seconds to WebVTT time format: HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def create_forced_alignment(audio_path: str, text: str) -> dict:
    """Call ElevenLabs Forced Alignment API with audio file and text."""
    with open(audio_path, "rb") as f:
        audio_data = f.read()

    files = {
        "file": ("audio.mp3", BytesIO(audio_data), "audio/mpeg"),
    }
    data = {
        "text": text,
    }
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
    }

    response = requests.post(API_URL, files=files, data=data, headers=headers)
    response.raise_for_status()
    return response.json()


def alignment_to_srt(alignment: dict) -> str:
    """Convert alignment data to SRT subtitle format."""
    lines = []
    words = alignment.get("words", [])
    
    if not words:
        return ""
    
    subtitle_index = 1
    current_words = []
    current_start = None
    current_end = None
    
    for i, word in enumerate(words):
        word_text = word["text"].strip()
        if not word_text:
            continue
            
        word_start = word["start"]
        word_end = word["end"]
        
        if current_start is None:
            current_start = word_start
            current_end = word_end
            current_words = [word_text]
        elif word_start - current_end < 0.5:
            current_end = word_end
            current_words.append(word_text)
        else:
            if current_words:
                lines.append(str(subtitle_index))
                lines.append(f"{format_time_srt(current_start)} --> {format_time_srt(current_end)}")
                lines.append(" ".join(current_words))
                lines.append("")
                subtitle_index += 1
            
            current_start = word_start
            current_end = word_end
            current_words = [word_text]
    
    if current_words:
        lines.append(str(subtitle_index))
        lines.append(f"{format_time_srt(current_start)} --> {format_time_srt(current_end)}")
        lines.append(" ".join(current_words))
        lines.append("")
    
    return "\n".join(lines)


def alignment_to_vtt(alignment: dict) -> str:
    """Convert alignment data to WebVTT subtitle format."""
    lines = ["WEBVTT", ""]
    words = alignment.get("words", [])
    
    if not words:
        return ""
    
    subtitle_index = 1
    current_words = []
    current_start = None
    current_end = None
    
    for word in words:
        word_text = word["text"].strip()
        if not word_text:
            continue
            
        word_start = word["start"]
        word_end = word["end"]
        
        if current_start is None:
            current_start = word_start
            current_end = word_end
            current_words = [word_text]
        elif word_start - current_end < 0.5:
            current_end = word_end
            current_words.append(word_text)
        else:
            if current_words:
                lines.append(str(subtitle_index))
                lines.append(f"{format_time_vtt(current_start)} --> {format_time_vtt(current_end)}")
                lines.append(" ".join(current_words))
                lines.append("")
                subtitle_index += 1
            
            current_start = word_start
            current_end = word_end
            current_words = [word_text]
    
    if current_words:
        lines.append(str(subtitle_index))
        lines.append(f"{format_time_vtt(current_start)} --> {format_time_vtt(current_end)}")
        lines.append(" ".join(current_words))
        lines.append("")
    
    return "\n".join(lines)


SCENE_TRANSCRIPTS = {
    "scene1": """Every developer knows this feeling. You're building an AI system, and it starts spiraling out of control. Code everywhere. No direction. Tests failing. Sound familiar?""",
    "scene2": """What if there was a better way? What if instead of writing every line of code you could design the specifications that guide your AI? Enter, harness engineering. It's not about programming the AI directly. It's about creating environments, specifications, and feedback loops that let agents do reliable work.""",
    "scene3": """Three companies cracked the code. OpenAI generated ONE MILLION lines of code with just three engineers. LangChain improved their agent by fourteen percentage points from fifty-two point eight percent to sixty-six point five percent just by changing the harness, not the model. Anthropic solved the long-running agent problem with feature lists and progress tracking. The secret? Self-verification before exit. Incremental progress over scope. Context that the agent can actually see.""",
    "scene4": """The results speak for themselves. OpenAI reached level four autonomy, agents that can go from prompt to PR with minimal human input. LangChain's sandwich approach for planning, for implementation, for verification boosted performance by nearly fourteen points. The shift? Humans don't write code anymore. They design systems. They steer. Agents execute.""",
    "scene5": """The future of development isn't about writing more code. It's about creating better specifications. Better feedback loops. Better harnesses. Start with your environment. Add observability. Enforce verification. The agents are waiting. Are you ready to guide them?""",
}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Forced Alignment for audio files")
    parser.add_argument("--audio", "-a", help="Audio file path")
    parser.add_argument("--text", "-t", help="Text transcript")
    parser.add_argument("--scene", "-s", choices=["scene1", "scene2", "scene3", "scene4", "scene5"],
                        help="Use preset scene transcript")
    parser.add_argument("--output", "-o", help="Output JSON file for alignment data")
    parser.add_argument("--srt", help="Output SRT file")
    parser.add_argument("--vtt", help="Output VTT file")
    parser.add_argument("--print", action="store_true", help="Print alignment data")
    args = parser.parse_args()
    
    if not args.audio:
        print("Processing all spectacular scenes...")
        for scene_name, transcript in SCENE_TRANSCRIPTS.items():
            audio_path = f"spectacular_{scene_name}.mp3"
            if not os.path.exists(audio_path):
                print(f"  Skipping {audio_path} (not found)")
                continue
                
            print(f"  Processing {audio_path}...")
            try:
                alignment = create_forced_alignment(audio_path, transcript)
                
                output_json = f"{scene_name}_alignment.json"
                with open(output_json, "w") as f:
                    json.dump(alignment, f, indent=2)
                print(f"    Saved alignment to {output_json}")
                
                srt_content = alignment_to_srt(alignment)
                output_srt = f"{scene_name}.srt"
                with open(output_srt, "w") as f:
                    f.write(srt_content)
                print(f"    Saved SRT to {output_srt}")
                
                vtt_content = alignment_to_vtt(alignment)
                output_vtt = f"{scene_name}.vtt"
                with open(output_vtt, "w") as f:
                    f.write(vtt_content)
                print(f"    Saved VTT to {output_vtt}")
                
                if args.print:
                    print(f"\n  Words ({len(alignment['words'])}):")
                    for word in alignment["words"][:10]:
                        print(f"    {word['text']}: {word['start']:.2f}s - {word['end']:.2f}s (loss: {word['loss']:.3f})")
                    print("    ...")
                    
            except Exception as e:
                print(f"    Error: {e}")
                
        print("\nDone!")
        return
        
    if not args.text and not args.scene:
        print("Error: Must provide --text or --scene")
        sys.exit(1)
    
    text = args.text or SCENE_TRANSCRIPTS[args.scene]
    print(f"Transcript: {text[:100]}...")
    
    alignment = create_forced_alignment(args.audio, text)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(alignment, f, indent=2)
        print(f"Saved alignment to {args.output}")
    
    if args.srt:
        srt_content = alignment_to_srt(alignment)
        with open(args.srt, "w") as f:
            f.write(srt_content)
        print(f"Saved SRT to {args.srt}")
    
    if args.vtt:
        vtt_content = alignment_to_vtt(alignment)
        with open(args.vtt, "w") as f:
            f.write(vtt_content)
        print(f"Saved VTT to {args.vtt}")
    
    if args.print or not any([args.output, args.srt, args.vtt]):
        print("\nAlignment data:")
        print(json.dumps(alignment, indent=2))
    
    print(f"\nWords: {len(alignment['words'])}")
    print(f"Characters: {len(alignment['characters'])}")
    print(f"Average loss: {alignment['loss']:.4f}")
    
    print("\nWord timings (first 10):")
    for word in alignment["words"][:10]:
        print(f"  {word['text']}: {word['start']:.3f}s - {word['end']:.3f}s")


if __name__ == "__main__":
    main()