# Video Script with Audio Tags - Enhanced Version

## Using ElevenLabs v3 Audio Tags for Human-like Expression

All scenes use `eleven_v3` model with audio tags for:
- Natural pauses
- Emotional tone changes
- Emphasis and dramatic effect

---

## Scene 1: The Problem

**With Audio Tags:**
> "Every developer knows this feeling [short pause] 
> You're building an AI system, and it starts spiraling out of control [long pause] 
> Code everywhere [pause] 
> No direction [pause] 
> Tests failing [emphatic] 
> Sound familiar? [short pause]"

---

## Scene 2: The Discovery

**With Audio Tags:**
> "What if there was a better way? [pause] 
> What if instead of writing every line of code [pause] 
> you could design the specifications [short pause] 
> that guide your AI? [emphatic] 
> 
> Enter... [long pause] harness engineering [emphatic]. 
> 
> It's not about programming the AI directly [softly] 
> [pause] 
> It's about creating environments, specifications, and feedback loops [emphatic] 
> that let agents do reliable work."

---

## Scene 3: The Solution

**With Audio Tags:**
> "Three companies cracked the code [emphatic]. 
> 
> OpenAI generated ONE MILLION lines of code [excited] 
> with just three engineers [pause] 
> 
> LangChain improved their agent by fourteen percentage points [emphatic] 
> [pause] 
> from fifty-two point eight percent [short pause] 
> to sixty-six point five percent [dramatic] 
> [pause] 
> just by changing the harness [short pause] 
> not the model [pause]. 
> 
> Anthropic solved the long-running agent problem [emphatic] 
> with feature lists [pause] 
> and progress tracking [pause]. 
> 
> The secret? [long pause] 
> Self-verification before exit [emphatic]. 
> Incremental progress over scope [pause]. 
> Context that the agent can actually see [softly]."

---

## Scene 4: The Impact

**With Audio Tags:**
> "The results speak for themselves [emphatic] [pause]. 
> 
> OpenAI reached level four autonomy [emphatic] 
> [pause] 
> agents that can go from prompt to PR [short pause] 
> with minimal human input [pause]. 
> 
> LangChain's sandwich approach [pause] 
> [xhigh reasoning] for planning [pause] 
> [high] for implementation [pause] 
> [xhigh] for verification [short pause] 
> boosted performance by nearly fourteen points [emphatic] [pause]. 
> 
> The shift? [long pause] 
> Humans don't write code anymore [emphatic]. 
> They design systems [pause]. 
> They steer [pause]. 
> Agents execute [emphatic]."

---

## Scene 5: The Future

**With Audio Tags:**
> "The future of development isn't about writing more code [emphatic] [pause]. 
> 
> It's about creating better specifications [pause]. 
> Better feedback loops [pause]. 
> Better harnesses [emphatic]. 
> 
> Start with your environment [short pause]. 
> Add observability [pause]. 
> Enforce verification [emphatic]. 
> 
> The agents are waiting [long pause]. 
> Are you ready to guide them? [emphatic] [short pause]"

---

## Technical Notes

### How to Use with API

For `eleven_v3` model, pass the text directly with audio tags:

```json
{
  "text": "Every developer knows this feeling [short pause] You're building an AI system...",
  "model_id": "eleven_v3",
  "voice_settings": {
    "stability": 0.4,
    "similarity_boost": 0.8,
    "style": 0.2
  }
}
```

### Voice Settings for Expressive Audio

For best results with audio tags, use:
- **stability**: 0.3-0.5 (lower = more expressive)
- **similarity_boost**: 0.8-0.9
- **style**: 0.2-0.4

### Tag Duration Notes

- Audio tags typically affect ~4-5 words before returning to normal
- Use `[long pause]` for scene transitions
- Use `[emphatic]` for key stats/numbers
- Use `[softly]` for confidential or thoughtful moments