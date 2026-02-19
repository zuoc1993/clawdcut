---
name: creative-scripting
description: Use when creating video narration, voiceover scripts, or dialogue that requires emotional storytelling, style-appropriate language, and precise timing alignment with visual content
---

# Creative Scripting

## Overview

Transforms creative intent into production-ready narration and dialogue. Focuses on matching language style to video tone, pacing content to fit time constraints, and creating authentic emotional resonance.

## When to Use

**Use this skill when:**

- Writing narration or voiceover for video content
- Dialogue needs to match a specific emotional tone (healing, energetic, suspenseful, documentary)
- Script duration must align with visual timing constraints
- Audience-specific language adaptation is required
- Emotional arc needs careful calibration (avoid over-dramatization or under-delivery)

**Don't use when:**

- Content is purely informational with no narrative component
- User has already provided finalized script text
- Technical specifications document (not creative writing)

## Core Pattern

```
Analyze → Structure → Draft → Calibrate → Finalize
```

1. **Analyze**: Extract intent, target audience, emotional goals, duration constraints
2. **Structure**: Choose narrative framework (three-act, emotional arc, problem-solution)
3. **Draft**: Write with style-specific vocabulary, pacing, and sentence structures
4. **Calibrate**: Adjust for timing (120-150 words/minute), emotional authenticity, audience fit
5. **Finalize**: Polish for flow, eliminate redundancy, ensure visual-textual alignment

## Quick Reference

| Video Style | Language | Sentence Structure | Key Vocabulary | Pacing |
|-------------|----------|-------------------|----------------|--------|
| Healing (治愈系) | Warm, poetic | Short with pauses | Light, shadows, time, memory | Slow, contemplative |
| Energetic (热血系) | Forceful, short | Parallel, repetitive | Dreams, breakthrough, change | Fast, punchy |
| Suspenseful (悬疑系) | Mysterious, suggestive | Questions, inversions | Truth, secrets, clues | Measured, withholding |
| Documentary (记录系) | Objective, factual | Clear statements | Time, place, events, data | Steady, informative |

## Implementation

### Intent Analysis

```python
def analyze_intent(user_request):
    """
    Extract all relevant parameters from user input.
    """
    analysis = {
        "intent": "travel documentation",
        "tone": "healing/peaceful",
        "duration_seconds": 150,
        "target_audience": "general, social media",
        "key_themes": ["journey", "beauty", "reflection"],
        "style_reference": "Japanese travel vlogs",
        "constraints": {
            "max_words": 150 * 2.2,  # ~330 words for 150s
            "language": "chinese",
            "avoid": ["clichés", "over-dramatization"]
        }
    }
    return analysis
```

### Structure Design

```python
def design_structure(analysis):
    """
    Map content to narrative structure with timing.
    """
    structure = {
        "opening": {
            "duration": 15,
            "emotion": "anticipation",
            "function": "hook the viewer",
            "word_count": 20
        },
        "development": {
            "duration": 90,
            "emotion": "immersion",
            "function": "deliver experience",
            "word_count": 150
        },
        "climax": {
            "duration": 30,
            "emotion": "revelation",
            "function": "emotional peak",
            "word_count": 50
        },
        "ending": {
            "duration": 15,
            "emotion": "closure",
            "function": "memorable takeaway",
            "word_count": 25
        }
    }
    return structure
```

### Style-Specific Writing

**Healing Style Example:**

```
Opening (15s, ~20 words):
"Some journeys aren't about arriving. They're about beginning."

Characteristics:
- Short sentences with natural pauses
- Metaphorical language
- Nature and time imagery
- Contemplative tone
```

**Energetic Style Example:**

```
Opening (10s, ~15 words):
"Three years. One thousand days. This moment."

Characteristics:
- Single words as sentences
- Numerical impact
- Urgency and momentum
- Direct address
```

### Timing Calibration

```python
def calibrate_timing(script_segment, target_duration):
    """
    Adjust word count and pacing to fit duration.
    """
    words = len(script_segment.split())
    target_words = target_duration * 2.2  # ~130 wpm for Chinese
    
    if words > target_words * 1.1:
        return "condense", target_words
    elif words < target_words * 0.9:
        return "expand", target_words
    else:
        return "ok", words
```

### Emotional Authenticity Check

```python
def check_authenticity(script, target_emotion):
    """
    Detect over-dramatization or emotional manipulation.
    """
    red_flags = [
        "excessive superlatives (most beautiful, greatest ever)",
        "forced sentimentality",
        "unearned emotional payoff",
        "cliché phrases without fresh perspective"
    ]
    
    # Score emotional authenticity 1-10
    # Return recommendations for improvement
```

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Word count mismatch | Narration doesn't fit visual timing | Calculate 120-150 words/minute before drafting |
| Style inconsistency | Mixing poetic with technical language | Commit to one style vocabulary per project |
| Over-explaining | Telling what visuals already show | Trust visual storytelling; narration adds layers |
| Forced emotion | Manipulative language turns off audience | Earn emotional moments through narrative buildup |
| Ignoring audience | Wrong register for target viewers | Define audience demographics and language level |
| Wall of text | Dense narration overwhelms | Use line breaks, pauses; 10-15 words max per line |
| Cliché dependence | Generic, forgettable content | Replace common phrases with specific, fresh observations |

## Script Structure Templates

### Travel/Experience Video

```
Opening (0:00-0:15): Invitation
- Hook: Single impactful sentence
- Mood: Anticipatory, opening possibility

Development (0:15-1:30): Immersion  
- Sensory details: What viewer sees/feels
- Emotional journey: Building connection
- Rhythm: Varied pacing, highs and lows

Climax (1:30-2:00): Revelation
- Emotional peak: Moment of realization
- Visual-text synergy: Words enhance the image

Ending (2:00-2:30): Resonance
- Memory anchor: What stays with viewer
- Gentle closure: Open but satisfying
```

### Product Launch Video

```
Opening (0:00-0:10): Intrigue
- Pattern interrupt: Unexpected start
- Build: Countdown or accumulation

Problem (0:10-0:30): Recognition
- Empathy: "We hear you"
- Stakes: Why this matters

Solution (0:30-1:00): Revelation
- Product as answer: Not features, transformation
- Proof: Social validation or demonstration

Climax (1:00-1:30): Declaration
- Bold statement: Positioning
- Call: Immediate action

Close (1:30-1:45): Landing
- Information: Price/availability
- Final impact: Memorable phrase
```

## Red Flags - Quality Issues

- **Cliché density**: Multiple phrases like "once in a lifetime", "journey of a lifetime", "heart and soul"
- **Mismatched tone**: Technical jargon in emotional moment, flowery language in factual section
- **Timing overflow**: Word count exceeds duration capacity (read faster ≠ better)
- **Visual competition**: Describing exactly what's on screen instead of adding meaning
- **Audience disconnect**: Using slang that misses the demographic or formal language for casual content
- **Information dumps**: Too many facts too quickly without emotional context
