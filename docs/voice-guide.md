# Voice Guide 🎤

## Meet the Voices!

Think of these like different characters in a movie. Each one has their own personality!

## The Voices in Our Project

### Brittney (kPzsL2i3teMYv0FxEYQ6) ⭐ PRIMARY
- **Personality:** Fun, youthful, informative
- **Sounds like:** That friend who always tells you about cool new stuff
- **Best for:** YouTube videos, social media, educational content
- **Vibe:** Energetic and friendly!

**Example:** "Hey guys! Today we're going to talk about something super cool..."

---

### George (JBFqnCBsd6RMkjVDRZzb)
- **Personality:** Warm, captivating storyteller
- **Sounds like:** A grandpa telling stories by the fireplace
- **Best for:** Narratives, stories, explainer videos
- **Vibe:** Comforting and engaging!

**Example:** "Once upon a time, in a land far away..."

---

### Sarah (EXAVITQu4vr4xnSDxMaL)
- **Personality:** Mature, reassuring, confident
- **Sounds like:** A professional news anchor or teacher
- **Best for:** Business videos, tutorials, presentations
- **Vibe:** Professional and trustworthy!

**Example:** "In today's lesson, we will cover the fundamentals of..."

---

### Roger (CwhRBWXzGAHq8TQ4Fs17)
- **Personality:** Laid-back, casual, resonant
- **Sounds like:** That chill friend who's always relaxed
- **Best for:** Podcasts, casual content, comedy
- **Vibe:** Easy-going and relatable!

**Example:** "So yeah, I was thinking about this the other day..."

---

### Matilda (XrExE9yKIg1WjnnlVkGX)
- **Personality:** Knowledgeable, professional
- **Sounds like:** A smart professor who knows everything
- **Best for:** Educational content, documentaries, non-fiction
- **Vibe:** Smart and authoritative!

**Example:** "The research indicates that..."

---

### Adam (pNInz6obpgDQGcFmaJgB)
- **Personality:** Dominant, firm
- **Sounds like:** A strong leader or boss
- **Best for:** Action content, sports, dramatic moments
- **Vibe:** Powerful and commanding!

**Example:** "This is how we get it done!"

---

## How to Pick the Right Voice

Ask yourself these questions:

| Question | Best Voice |
|----------|-------------|
| Is it fun/social media? | Brittney |
| Is it a story? | George |
| Is it professional? | Sarah |
| Is it casual/chill? | Roger |
| Is it educational? | Matilda |
| Is it action/dramatic? | Adam |

## Voice Settings Deep Dive 🎛️

You can make each voice sound different by changing settings:

### Stability (0.0 - 1.0)
- **Low (0.1-0.3):** More emotional, varies more
- **Medium (0.4-0.6):** Balanced
- **High (0.7-1.0):** Very consistent, robotic

**Recommended:** 0.4 for videos, 0.7 for consistent narration

### Similarity Boost (0.0 - 1.0)
- **Low:** More unique interpretation
- **High:** Sticks closer to original voice

**Recommended:** 0.8 for most videos

### Style (0.0 - 1.0)
- **Low:** Neutral, plain reading
- **High:** Very expressive, emotional

**Recommended:** 0.2 for narrator, 0.5 for dramatic

### Speed (0.5 - 2.0)
- **0.5:** Half speed (slow)
- **1.0:** Normal speed
- **2.0:** Double speed (fast)

**Recommended:** 1.0 for most content, 0.95 for formal

## Preset Combinations

We made some ready-to-use settings in `config.py`:

```python
VOICE_SETTINGS = {
    "default": {"stability": 0.5, "similarity_boost": 0.75},
    "narrator": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.2},
    "energetic": {"stability": 0.3, "similarity_boost": 0.9, "style": 0.5},
    "calm": {"stability": 0.7, "similarity_boost": 0.6}
}
```

## Using Different Voices in Code

### Python:
```python
from config import get_voice

# Get ID by name
voice_id = get_voice("brittney")  # Returns "kPzsL2i3teMYv0FxEYQ6"

# Or use directly
voice_id = "kPzsL2i3teMYv0FxEYQ6"
```

### Command Line:
```bash
python generate_audio.py --text "Hello!" --voice brittney
python generate_audio.py --text "Hello!" --voice george
python generate_audio.py --text "Hello!" --voice sarah
```

---

**Now you're a voice expert!** 

Check out [Troubleshooting](troubleshooting.md) if you run into any problems! 🔧