# Marketing Workflow Engine - Specification

## Goal

Build an **autonomous daily content engine** that:
1. Runs daily (cron)
2. Generates video content on topics
3. Creates professional videos (voice + images + music)
4. Publishes to social media

## Current State

`autonomous_video_v3.py` provides:
- Script generation with emotional arc (ghost agents story)
- Voice (ElevenLabs TTS)
- Music (ElevenLabs Music)
- Images (Gemini) 
- Video assembly (FFmpeg)

## Target State

```
Daily Schedule
├── Topic selection (manual or AI)
├── Script generation
├── Video pipeline
│   ├── Voice tracks
│   ├── Image generation
│   ├── Music generation
│   └── Video assembly
├── Post-processing
│   ├── Quality check
│   └── Review (optional)
└── Publishing
    ├── Twitter/X
    ├── LinkedIn
    ├── Instagram
    ├── TikTok
    └── YouTube Shorts
```

## Existing Tools (Evaluate)

| Tool | What | Link |
|------|------|------|
| OpenMontage | Agentic video - 11 pipelines | github.com/calesthio/OpenMontage |
| ClawdAgent | Video → 9 platforms | github.com/47thstreet/ClawdAgent |

## Next Steps

1. [ ] Scheduling - cron/DAG for daily runs
2. [ ] Social publishing integration
3. [ ] Topic/content curation
4. [ ] Quality automation

## Files

- `autonomous_video_v3.py` - Core video generation
- `output_v3/` - Generated assets
- `index.html` - Preview/landing page