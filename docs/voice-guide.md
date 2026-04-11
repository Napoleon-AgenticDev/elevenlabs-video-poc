# Voice Guide 🎤

## Meet the Voices!

Think of these like different characters in a movie. Each one has their own personality!

## The Voices in Our Project

### Brittney (kPzsL2i3teMYv0FxEYQ6) ⭐ PRIMARY - RECOMMENDED
- **Personality:** Fun, youthful, informative
- **Sounds like:** That friend who always tells you about cool new stuff
- **Best for:** YouTube videos, social media, educational content
- **Vibe:** Energetic and friendly!

**Why Brittney?** She's optimized for our video scripts with perfect expression of Audio Tags!

---

## ✨ NEW: ElevenLabs v3 Audio Tags

This is the SECRET SAUCE for spectacular videos! Audio Tags make AI voice sound like a REAL person with emotions!

### What Are Audio Tags?

Put tags in square brackets `[]` anywhere in your script to control:
- 🎭 Emotions
- ⏸️ Pauses
- 🔊 Volume
- ⚡ Speed

### Complete Audio Tags Reference

#### 🎭 Emotion Tags
| Tag | When to Use | Example |
|-----|-------------|---------|
| `[sad]` | Sad, somber moments | "It failed again [sad]" |
| `[angry]` | Frustrated, upset | "Tests failing [angry]!" |
| `[happily]` | Happy, excited | "We did it [happily]!" |
| `[sorrowful]` | Deep sadness | "The code was lost [sorrowful]" |
| `[excited]` | Very enthusiastic | "ONE MILLION lines [excited]!" |
| `[emphatic]` | Strong emphasis | "The SECRET [emphatic] is..." |

#### 🔊 Volume/Delivery Tags
| Tag | When to Use | Example |
|-----|-------------|---------|
| `[shouts]` | Louder, shouted | "CODE EVERYWHERE [shouts]!" |
| `[whispers]` | Quiet, secretive | "Not about coding directly [whispers]" |
| `[softly]` | Gentle delivery | "peaceful solution [softly]" |
| `[loud]` | Very loud | "[loud] BREAKTHROUGH!" |
| `[quiet]` | Very quiet | "[quiet] top secret" |

#### ⏸️ Pause Tags (v3 Only!)
| Tag | Effect | Example |
|-----|--------|---------|
| `[pause]` | Natural pause | "Hello [pause] world" |
| `[short pause]` | Brief pause | "Wait [short pause] what?" |
| `[long pause]` | Extended pause | "The answer is... [long pause] YES" |
| `[dramatic]` | Theatrical pause | "[dramatic] and then..." |

#### ⚡ Speed Tags
| Tag | Effect | Example |
|-----|--------|---------|
| `[slow]` | Slower pace | "Carefully [slow] analyze" |
| `[fast]` | Faster pace | "Quickly [fast] fix this" |
| `[rushed]` | Very fast | "[rushed] finish now" |
| `[drawn out]` | Extended vowels | "Sooo [drawn out] cooool" |

#### 🎬 Special Tags
| Tag | Effect | Example |
|-----|--------|---------|
| `[sighs]` | Sighing sound | "[sighs] finally done" |
| `[laughs]` | Laughter | "[laughs] so funny!" |
| `[clears throat]` | Throat clear | "[clears throat] excuse me" |
| `[coughs]` | Cough | "[coughs] pardon me" |

### Example Script with All Tags

```python
SCENE_1 = """
Every developer knows [emphatic] this feeling [long pause] 

You're building an AI system... 
and it starts spiraling OUT OF CONTROL [shouts] [long pause] 

Code EVERYWHERE [excited] [short pause] 
No direction [slow] [pause] 
Tests failing [emphatic] [short pause] 

Sound familiar? [emphatic] [short pause]
"""
```

## Voice Settings Deep Dive 🎛️

### For Maximum Expression (SPECTACULAR Videos)

Use these settings for drama and emotion:

```python
VOICE_SETTINGS = {
    "stability": 0.25,      # Very low = more expression!
    "similarity_boost": 0.9,  # High = sounds like original voice
    "style": 0.5,            # High = emotional range
    "speed": 1.0
}
```

### Stability (0.0 - 1.0)
- **Low (0.1-0.3):** ⭐ More emotional, varies more - USE FOR DRAMA
- **Medium (0.4-0.6):** Balanced
- **High (0.7-1.0):** Very consistent, robotic

### Similarity Boost (0.0 - 1.0)
- **Low:** More unique interpretation
- **High:** ⭐ Sticks closer to original voice - USE 0.8-0.9

### Style (0.0 - 1.0) - v3 Only!
- **Low:** Neutral, plain reading
- **High:** ⭐ Very expressive, emotional - USE 0.3-0.5 FOR DRAMA

## How to Pick the Right Voice

| Scenario | Best Voice | Audio Tags |
|----------|------------|------------|
| Social media, fun | Brittney ⭐ | [excited], [shouts] |
| Story, narrative | George | [slow], [dramatic] |
| Professional, business | Sarah | [emphatic], [pause] |
| Casual, podcast | Roger | [softly], [laughs] |
| Educational | Matilda | [clear], [emphatic] |
| Action, dramatic | Adam | [shouts], [excited] |

## Using in Code

### Python:
```python
from config import get_voice

voice_id = get_voice("brittney")  # Returns "kPzsL2i3teMYv0FxEYQ6"
```

### Command Line:
```bash
python generate_spectacular_audio.py --scene 1
python generate_spectacular_audio.py --all
```

---

## Pro Tips for Spectacular Audio

1. **Use [emphatic]** on key stats and numbers
2. **Use [long pause]** before reveals
3. **Use [shouts]** for dramatic emphasis
4. **Use [whispers]** for confidential info
5. **Lower stability (0.25)** = more expression
6. **Higher style (0.5)** = more emotion

---

**Now you're ready to make SPECTACULAR videos!** 

Check out [video-script-guide.md](video-script-guide.md) for writing scripts with expression! 🚀