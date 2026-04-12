"""
Three-Part Video Series: "The Autonomous Video Generator"
Episode 2: "How does it work?" - Technical deep dive
"""

SCENES = {
    1: {
        "title": "THE RECAP",
        "mood": "continuation",
        "music_genre": "ambient",
        "character": "ARIA - female AI agent, same as before",
        "subject_angle": "medium_shot",
        "script": "We left off with a question. [pause] What is this? [pause] Now... [emphatic] how does it work? [pause] ARIA: Let me show you the architecture. [pause] The producer agent, the scripts, the configuration.",
        "segments": [
            ("We left off with a question.", "quick flashback: last episode thumbnail"),
            ("What is this?", "title: EPISODE 1回顾"),
            ("Now... how does it work?", "transition to EPISODE 2 title"),
            ("ARIA: Let me show you the architecture.", "ARIA gestures to diagrams"),
            ("The producer agent, the scripts, the configuration.", "visual: three pillars")
        ],
        "audio_tags": "clear,introduction",
        "motion": "slow_pan"
    },
    2: {
        "title": "THE PIPELINE",
        "mood": "technical explanation",
        "music_genre": "electronic",
        "character": "ARIA pointing to code",
        "subject_angle": "over_shoulder",
        "script": "The pipeline has five stages. [pause] First: Script generation. [pause] The SCENES dict defines your story. [pause] Second: Voice creation. [pause] ElevenLabs converts text to expressive audio with audio tags for emotion. [slow] Third: Image generation. Gemini creates photorealistic images per segment.",
        "segments": [
            ("The pipeline has five stages.", "diagram: 1→2→3→4→5"),
            ("First: Script generation.", "code: SCENES dict showing script"),
            ("The SCENES dict defines your story.", "close: script text visible"),
            ("Second: Voice creation.", "waveform visualization"),
            ("ElevenLabs converts text to expressive audio.", "API call visual"),
            ("Third: Image generation.", "image appearing"),
            ("Gemini creates photorealistic images per segment.", "gallery of 4 images")
        ],
        "audio_tags": "educational,clear",
        "motion": "tracking"
    },
    3: {
        "title": "THE CONFIGURATION",
        "mood": "technical detail",
        "music_genre": "minimalist",
        "character": "Marcus looking at config",
        "subject_angle": "close_up",
        "script": "Marcus: Wait, how do I customize this? [pause] ARIA: Two ways. [pause] config.yaml for production settings. [pause] And the SCENES dict for your content. [pause] Content rating. Music genre. Camera movement. [emphatic] Even the character appearance.",
        "segments": [
            ("Marcus: Wait, how do I customize this?", "Marcus asking question"),
            ("ARIA: Two ways.", "two options appear on screen"),
            ("config.yaml for production settings.", "yaml file shown"),
            ("And the SCENES dict for your content.", "python code shown"),
            ("Content rating. Music genre. Camera movement.", "settings cycling through"),
            ("Even the character appearance.", "before/after: G vs R rating")
        ],
        "audio_tags": "helpful,detailed",
        "motion": "zoom_in"
    },
    4: {
        "title": "THE PROJECT STRUCTURE",
        "mood": "organized",
        "music_genre": "cinematic",
        "character": "ARIA showing folder structure",
        "subject_angle": "wide_shot",
        "script": "Everything organizes into projects. [pause] Output goes to output/projects/your-project-name. [pause] Each project has scenes, images, audio, video. [pause] Full videos concatenate automatically. [slow] The log tracks everything.",
        "segments": [
            ("Everything organizes into projects.", "folder tree visible"),
            ("Output goes to output/projects/your-project-name.", "path highlighted"),
            ("Each project has scenes, images, audio, video.", "directory structure"),
            ("Full videos concatenate automatically.", "ffmpeg concat visual"),
            ("The log tracks everything.", "log file shown")
        ],
        "audio_tags": "organized,clear",
        "motion": "slow_dissolve"
    },
    5: {
        "title": "THE TEASER",
        "mood": "anticipation",
        "music_genre": "ambient",
        "character": "ARIA addressing camera",
        "subject_angle": "close_up",
        "script": "Now you understand how it works. [pause] But what can it actually create? [emphatic] Stay tuned for our final episode. [pause] We'll showcase real videos, unique features, and the future of automated production.",
        "segments": [
            ("Now you understand how it works.", "summary visual"),
            ("But what can it actually create?", "question to audience"),
            ("Stay tuned for our final episode.", "EPISODE 3 title"),
            ("We'll showcase real videos, unique features...", "preview montage"),
            ("And the future of automated production.", "futuristic view")
        ],
        "audio_tags": "engaging,promo",
        "motion": "slow_dissolve"
    },
}

# Episode metadata
EPISODE = {
    "number": 2,
    "title": "How does it work?",
    "duration_target": "2.5 minutes",
    "characters": ["ARIA", "Marcus"],
    "topic": "Technical architecture and configuration"
}