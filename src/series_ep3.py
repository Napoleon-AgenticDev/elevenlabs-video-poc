"""
Three-Part Video Series: "The Autonomous Video Generator"
Episode 3: "What can it create?" - Capabilities and future
"""

SCENES = {
    1: {
        "title": "THE TRANSITION",
        "mood": "reveal",
        "music_genre": "cinematic",
        "character": "ARIA with finished video",
        "subject_angle": "hero_shot",
        "script": "We've explored what this is. [pause] We've learned how it works. [slow] Now... [emphatic] let's see what it creates. [pause] ARIA gestures and the screen fills with scenes from our ghost-in-machine video.",
        "segments": [
            ("We've explored what this is.", "episode 1 thumbnail"),
            ("We've learned how it works.", "episode 2 thumbnail"),
            ("Now... let's see what it creates.", "title reveal: EPISODE 3"),
            ("ARIA gestures and the screen fills with scenes.", "montage of generated videos"),
            ("Ghost-in-machine video playing.", "片段 playing")
        ],
        "audio_tags": "grand,revealing",
        "motion": "hero_dramatic"
    },
    2: {
        "title": "THE DEMO",
        "mood": "showcase",
        "music_genre": "electronic",
        "character": "Videos on screen with ARIA voiceover",
        "subject_angle": "wide_shot",
        "script": "This system produced this entire video. [pause] Every scene. [pause] The dialogue. [pause] The images. [pause] The music. [emphatic] The transitions. [pause] All automated. [slow] All tracked for cost and performance.",
        "segments": [
            ("This system produced this entire video.", "full video playing"),
            ("Every scene.", "individual scenes cycling"),
            ("The dialogue.", "voice waveform visualization"),
            ("The images.", "image gallery"),
            ("The music.", "music track visualization"),
            ("The transitions.", "crossfade moments"),
            ("All automated.", "automation icon"),
            ("All tracked for cost and performance.", "MLflow metrics visible")
        ],
        "audio_tags": "proud,showcasing",
        "motion": "tracking"
    },
    3: {
        "title": "THE USE CASES",
        "mood": "inspiration",
        "music_genre": "ambient",
        "character": "ARIA listing use cases",
        "subject_angle": "medium_shot",
        "script": "What can you create? [pause] Marketing campaigns running daily. [pause] Product demos on demand. [pause] Educational content. [pause] Social media series. [emphatic] Even personalized messages at scale. [pause] The only limit is your imagination.",
        "segments": [
            ("What can you create?", "question to audience"),
            ("Marketing campaigns running daily.", "marketing dashboard visualization"),
            ("Product demos on demand.", "product demo thumbnail"),
            ("Educational content.", "tutorial style video"),
            ("Social media series.", "multiple videos in grid"),
            ("Even personalized messages at scale.", "mass personalization concept"),
            ("The only limit is your imagination.", "creative burst visual")
        ],
        "audio_tags": "inspiring,list",
        "motion": "slow_pan"
    },
    4: {
        "title": "THE SKILL",
        "mood": "professional",
        "music_genre": "cinematic",
        "character": "ARIA in OpenCode context",
        "subject_angle": "close_up",
        "script": "This is packaged as an OpenCode skill. [pause] Any AI agent can load it. [pause] Use it with Claude, with OpenCode, with your own automation. [pause] The skill includes scripts, configuration, references. [slow] Everything you need to start.",
        "segments": [
            ("This is packaged as an OpenCode skill.", "skill structure shown"),
            ("Any AI agent can load it.", "skill tool loading"),
            ("Use it with Claude, with OpenCode, with your own automation.", "multiple tools logos"),
            ("The skill includes scripts, configuration, references.", "skill components listing"),
            ("Everything you need to start.", "get started button")
        ],
        "audio_tags": "professional,helpful",
        "motion": "zoom_in"
    },
    5: {
        "title": "THE CLOSE",
        "mood": "conclusion",
        "music_genre": "ambient",
        "character": "ARIA and Marcus together",
        "subject_angle": "hero_shot",
        "script": "Marcus: So this is the future of video? [pause] ARIA: This is A version of the future. [slow] [emphatic] And it keeps evolving. [pause] Thanks for watching this three-part series. [pause] Now go create something. [pause] The machine is ready.",
        "segments": [
            ("Marcus: So this is the future of video?", "Marcus closing question"),
            ("ARIA: This is A version of the future.", "ARIA thoughtful response"),
            ("And it keeps evolving.", "code being written visual"),
            ("Thanks for watching this three-part series.", "credits roll style"),
            ("Now go create something.", "call to action"),
            ("The machine is ready.", "final shot: ARIA and Marcus, screen showing terminal")
        ],
        "audio_tags": "warm,conclusion,triumphant",
        "motion": "hero_dramatic"
    },
}

# Episode metadata
EPISODE = {
    "number": 3,
    "title": "What can it create?",
    "duration_target": "2.5 minutes",
    "characters": ["ARIA", "Marcus"],
    "topic": "Capabilities, use cases, and future"
}