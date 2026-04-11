# Video Production Workflow

## Complete 5-Step Pipeline for Any Topic

### Step 1: Write Your Script

Create 5 scenes, each 10-20 seconds:
- Scene 1: Problem/Hook
- Scene 2: Discovery/Question
- Scene 3: Solution/Answer
- Scene 4: Impact/Evidence
- Scene 5: Call to Action/Future

Each scene needs:
- `title`: Scene title
- `script`: The script (50-100 words)
- `segments`: Array of {text, start, end}
- `image_prompts`: 4 contextual prompts

### Step 2: Generate Audio

```python
python video_generator_template.py --scene 1
# Or all scenes:
python video_generator_template.py --all
```

Uses ElevenLabs v3 with voice Brittney (kPzsL2i3teMYv0FxEYQ6).

### Step 3: Generate Image Alignment

```bash
python generate_alignment.py
```

This creates word-level timestamps for syncing.

### Step 4: Create Images with CC

```python
# Add CC subtitles to images
from PIL import Image, ImageDraw
# See video_generator_template.py for full code
```

### Step 5: Assemble Video

```bash
ffmpeg -loop 1 -t 3.5 -i frame_1_cc.png \
       -loop 1 -t 3.5 -i frame_2_cc.png \
       -loop 1 -t 3.5 -i frame_3_cc.png \
       -loop 1 -t 3.5 -i frame_4_cc.png \
       -i audio.mp3 \
       -filter_complex "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[out]" \
       -map "[out]" -map 4:a -c:v libx264 -c:a aac -shortest output.mp4
```

## Key Files

| File | Purpose |
|------|---------|
| `video_generator_template.py` | Main reusable script |
| `generate_alignment.py` | Word timestamps |
| `create_synced_video.py` | Video assembly |
| `production_scene*.mp4` | Individual final videos |
| `full_video_v2.mp4` | Full concatenated video |

## Customizing for a New Topic

1. Edit `SCENES` dict in `video_generator_template.py`
2. Update each scene's `script` and `image_prompts`
3. Run `python video_generator_template.py --all`
4. Concatenate with concat file

## Cost Estimate (per video)

- ElevenLabs audio: ~$0.02/scene
- OpenAI images: ~$0.08/scene (4 images)
- Total: ~$0.50/minute

## Best Practices

1. Keep scripts 10-20 seconds each
2. Use 4 images per scene for variety
3. Match CC text to what's being said
4. Add transitions between key moments
5. Use v3 model for expressive voice