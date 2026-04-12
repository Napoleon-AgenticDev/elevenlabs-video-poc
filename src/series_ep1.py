"""
Three-Part Video Series: "The Autonomous Video Generator"
Episode 1: "What is this?" - Introduction to the repo
"""

SCENES = {
    1: {
        "title": "THE INTRODUCTION",
        "mood": "curious discovery",
        "music_genre": "ambient",
        "character": "ARIA - female AI agent with silver titanium exoskeleton, glowing cyan LED eyes, athletic build, helpful mysterious presence",
        "subject_angle": "medium_shot",
        "script": "Marcus sits at his desk, scrolling through GitHub. [pause] A new repository catches his eye. [pause] Autonomous Video Generator. [slow] He clicks. The readme loads. [pause] But something else catches his attention... [pause] A translucent figure beside him. [emphatic] ARIA: I can help you understand what this does.",
        "segments": [
            ("Marcus sits at his desk, scrolling through GitHub.", "human developer at laptop late at night, looking curious, tech office"),
            ("A new repository catches his eye.", "screen shows GitHub repository with code"),
            ("Autonomous Video Generator.", "text on screen reveals: elevenlabs-video-poc repository"),
            ("A translucent figure beside him.", "female AI bot ARIA materializes beside the developer, glowing cyan eyes"),
            ("ARIA: I can help you understand what this does.", "ARIA addresses camera with confident smile, tech aura")
        ],
        "audio_tags": "curious,emphatic",
        "motion": "slow_pan"
    },
    2: {
        "title": "THE REVEAL", 
        "mood": "explanation",
        "music_genre": "minimalist",
        "character": "ARIA - same AI agent, explaining",
        "subject_angle": "close_up",
        "script": "She gestures to the screen. [pause] ARIA: This is a fully autonomous video production system. [pause] No humans needed after setup. [pause] It writes scripts, generates voice, creates images, adds music... [emphatic] And builds the final video. All by itself.",
        "segments": [
            ("She gestures to the screen.", "ARIA points to screen, elegant motion"),
            ("This is a fully autonomous video production system.", "wide shot: ARIA and Marcus looking at code together"),
            ("No humans needed after setup.", "split: human typing vs AI working independently"),
            ("It writes scripts, generates voice, creates images, adds music...", "montage: voice waveform, image generation, music notes"),
            ("And builds the final video. All by itself.", "final video thumbnail appears, ARIA smiles")
        ],
        "audio_tags": "clear,confident",
        "motion": "tracking"
    },
    3: {
        "title": "THE POSSIBILITY",
        "mood": "inspiration",
        "music_genre": "cinematic",
        "character": "ARIA and Marcus both in frame",
        "subject_angle": "hero_shot",
        "script": "Marcus leans back. [pause] Marcus: So I just... give it a topic? [pause] ARIA: And it creates the video. [slow] Every single day if you want. [pause] Marketing content. Product demos. Educational. [pause] The future of video production is here.",
        "segments": [
            ("Marcus leans back, impressed.", "Marcus has amazed expression, looking at ARIA"),
            ("So I just... give it a topic?", "human questioning, hopeful"),
            ("And it creates the video.", "ARIA gestures to show finished video appearing"),
            ("Every single day if you want.", "calendar/timeline visualization, daily content"),
            ("The future of video production is here.", "hero shot: both ARIA and Marcus, light burst, title card")
        ],
        "audio_tags": "hopeful,triumphant",
        "motion": "hero_dramatic"
    },
    4: {
        "title": "THE TEASER",
        "mood": "curiosity",
        "music_genre": "ambient",
        "character": "ARIA turning to camera",
        "subject_angle": "close_up",
        "script": "ARIA turns to face the camera directly. [pause] But how does it actually work? [long pause] [emphatic] Join us for part two. [pause] We'll dive into the code, the configuration, and the workflow.",
        "segments": [
            ("ARIA turns to face the camera directly.", "direct address, engaging"),
            ("But how does it actually work?", "thoughtful question to audience"),
            ("Join us for part two.", "promo text: EPISODE 2"),
            ("We'll dive into the code, the configuration, and the workflow.", "preview: code snippets, config files, diagrams")
        ],
        "audio_tags": "engaging,mysterious",
        "motion": "zoom_in"
    },
}

# Episode metadata
EPISODE = {
    "number": 1,
    "title": "What is this?",
    "duration_target": "2.5 minutes",
    "characters": ["ARIA", "Marcus"],
    "topic": "Repository introduction and overview"
}