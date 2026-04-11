# Video Image Generation Prompts

## Master Prompt (Consistency Guidelines)

Apply this to ALL image generations:

```
Create a professional tech presentation visual with the following style:
- Modern, sleek dark theme with deep navy (#0a0a1a) to purple (#1a0a2e) gradient background
- Abstract geometric shapes and patterns representing code, AI, and technology
- Soft glowing accents in cyan (#00d4ff) and purple (#7c3aed)
- Clean, minimalist design suitable for a video about software development/AI
- No text in the image - leave space for text overlay
- Professional quality suitable for a corporate/educational video
- Slight 3D depth effect with subtle shadows
- Aspect ratio: 16:9 (1280x720)
```

## Scene-Specific Prompts

### Scene 1: The Problem
**Script:** "Every developer knows this feeling. You're building an AI system, and it starts spiraling out of control. Code everywhere. No direction. Tests failing. Sound familiar?"

**Image Prompt:**
```
Chaos and disorder visualization: scattered code snippets floating in disarray, 
broken connections, warning symbols, red accent colors mixed with dark background, 
frustrating messy situation, abstract representation of code gone wrong, 
dark navy to deep red gradient, professional presentation style, no text
```

### Scene 2: The Discovery  
**Script:** "What if there was a better way? What if instead of writing every line of code, you could design the specifications that guide your AI?"

**Image Prompt:**
```
Eureka moment visualization: a bright light illuminating a clear path through complexity, 
blueprint or map emerging from darkness, GPS navigation style, guiding path forward, 
hope and clarity, cyan glow leading the way, dark background with spotlight effect, 
professional presentation style, no text
```

### Scene 3: The Solution
**Script:** "Three companies cracked the code. OpenAI generated ONE MILLION lines of code with just 3 engineers. LangChain improved their agent by 14 percentage points. The secret? Self-verification before exit."

**Image Prompt:**
```
Structure and architecture visualization: three pillars or foundation blocks standing strong,
connected nodes forming a network, organized system with clear boundaries, 
blueprints and specifications, building something great, cyan and purple pillars,
dark gradient background, professional presentation style, no text
```

### Scene 4: The Impact
**Script:** "The results speak for themselves. OpenAI reached level 4 autonomy - agents that can go from prompt to PR with minimal human input."

**Image Prompt:**
```
Success and achievement visualization: rocketship or upward trajectory, 
trophy or medal concept, level progression steps climbing upward, 
achievement unlocked, green and cyan success colors, dark background,
professional presentation style, no text
```

### Scene 5: The Future
**Script:** "The future of development isn't about writing more code. It's about creating better specifications. Better feedback loops. Better harnesses. The agents are waiting. Are you ready to guide them?"

**Image Prompt:**
```
Future and possibility visualization: open road or path stretching to horizon,
light at the end of tunnel, sunrise or new dawn, connected network expanding,
possibility and potential, warm cyan to purple gradient, horizon with hope,
professional presentation style, no text
```

## Usage Notes

1. **All images should be:** 1280x720 (16:9), dark theme, no text
2. **Consistency:** Use the master prompt style across all images
3. **Text overlay:** Add scene title and key text in video editing
4. **Color palette:** Cyan (#00d4ff), Purple (#7c3aed), Dark Navy (#0a0a1a)

## Generate Images Using

```bash
# Example with OpenAI (requires API key)
python generate_images.py --scene 1 --api-key YOUR_OPENAI_KEY

# Or manually via ChatGPT/DALL-E interface
# Copy the scene prompt and generate in ChatGPT
```