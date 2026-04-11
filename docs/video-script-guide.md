# Video Script Guide 📝

## What's a Video Script?

A video script is like a blueprint for your video. It tells you:
- What to say
- When to say it
- What pictures to show

## Our Script Structure

We have 5 scenes that tell a story:

### Scene 1: The Problem
**Goal:** Make the viewer think "That's me!"

**Script:**
> "Every developer knows this feeling. You're building an AI system, and it starts spiraling out of control. Code everywhere. No direction. Tests failing. Sound familiar?"

**Purpose:** Start with a problem everyone relates to!

---

### Scene 2: The Discovery
**Goal:** Show there's a better way!

**Script:**
> "What if there was a better way? What if instead of writing every line of code, you could design the specifications that guide your AI? Enter... harness engineering. It's not about programming the AI directly. It's about creating environments, specifications, and feedback loops that let agents do reliable work."

**Purpose:** Introduce the solution!

---

### Scene 3: The Solution
**Goal:** Explain how it works!

**Script:**
> "Three companies cracked the code. OpenAI generated ONE MILLION lines of code with just 3 engineers. LangChain improved their agent by 14 percentage points - from 52.8% to 66.5% - just by changing the harness, not the model. Anthropic solved the long-running agent problem with feature lists and progress tracking. The secret? Self-verification before exit. Incremental progress over scope. Context that the agent can actually see."

**Purpose:** Give proof and details!

---

### Scene 4: The Impact
**Goal:** Show real results!

**Script:**
> "The results speak for themselves. OpenAI reached level 4 autonomy - agents that can go from prompt to PR with minimal human input. LangChain's sandwich approach - xhigh reasoning for planning, high for implementation, xhigh for verification - boosted performance by nearly 14 points. The shift? Humans don't write code anymore. They design systems. They steer. Agents execute."

**Purpose:** Make it real with numbers!

---

### Scene 5: The Future
**Goal:** Call to action!

**Script:**
> "The future of development isn't about writing more code. It's about creating better specifications. Better feedback loops. Better harnesses. Start with your environment. Add observability. Enforce verification. The agents are waiting. Are you ready to guide them?"

**Purpose:** Get the viewer to act!

---

## Story Structure (The Hero's Journey)

This follows a classic storytelling pattern:

```
PROBLEM → DISCOVERY → SOLUTION → IMPACT → FUTURE
    ↓          ↓           ↓         ↓        ↓
  Hook      Idea        Proof     Results   Action
```

### Why This Works:

1. **Start with pain** - Everyone understands frustration
2. **Offer hope** - There's a better way!
3. **Show evidence** - Real companies, real results
4. **Make it real** - Numbers and facts
5. **Call to action** - What should they do next?

## Making Your Own Script

### Step 1: Pick Your Topic
What's your video about? (Ours: "Harness Engineering")

### Step 2: Find the Problem
What problem does your audience have?

### Step 3: Find the Solution
What's the answer to that problem?

### Step 4: Add Proof
Who used this solution and got results?

### Step 5: Call to Action
What should the viewer do next?

## Script Format

We use a simple format:

```markdown
## Scene 1: [Title]

**Text:** "[What to say]"

**Image idea:** [What picture to show]
```

## Creating Video from Script

Our `create_video.py` script connects scenes to files:

```python
SCENES = {
    "scene1": {
        "audio": "brittney_scene1.mp3",
        "image": "scene1_chaos.png",
        "title": "The Problem"
    },
    # ... more scenes
}
```

## Tips for Good Scripts

✅ Keep sentences short
✅ Use active words (don't write "is being done", write "does")
✅ Ask questions to engage the viewer
✅ Use numbers for credibility
✅ End with a question or call to action

❌ Don't use too much jargon
❌ Don't make it too long
❌ Don't forget the hook

---

**Now write your own script!** 

Need help? Check out [How It Works](how-it-works.md) for more context! 🎬