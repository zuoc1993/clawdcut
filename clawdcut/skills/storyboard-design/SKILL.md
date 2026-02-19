---
name: storyboard-design
description: Use when converting scripts into visual shot plans, planning camera movements, or creating visual references for video production that require specific shot composition and timing
---

# Storyboard Design

## Overview

Transforms written scripts into visual production plans. Defines specific shots with camera angles, movements, durations, and compositional references that guide the actual video production or editing process.

## When to Use

**Use this skill when:**

- Script needs translation into specific visual shots
- Camera movements and angles need precise planning
- Shot durations and pacing require calculation
- Visual references and mood boards are needed
- Production team needs clear visual guidance
- Complex sequences require breakdown into individual shots

**Don't use when:**

- User has provided existing footage to edit (proceed directly to editing)
- Simple single-shot video with no camera movement
- Content is audio-only (podcast, music)

## Core Pattern

```
Parse → Decompose → Design → Sequence → Reference
```

1. **Parse**: Analyze script for visual content, emotion, and timing
2. **Decompose**: Break narrative into discrete visual moments
3. **Design**: Specify each shot's technical parameters (type, angle, movement, duration)
4. **Sequence**: Arrange shots with appropriate transitions and rhythm
5. **Reference**: Gather visual references for style, composition, and mood

## Quick Reference

| Shot Type | Use For | Typical Duration | Emotional Effect |
|-----------|---------|------------------|------------------|
| Extreme Wide | Establishing location | 3-5s | Scale, isolation |
| Wide | Full subject + context | 3-5s | Grounding, setting |
| Medium | Waist up, action/dialogue | 4-7s | Standard, balanced |
| Close-up | Face, emotion, detail | 3-5s | Intimacy, emphasis |
| Extreme Close-up | Specific detail, texture | 2-3s | Intensity, abstraction |

| Camera Movement | Use For | Emotional Effect |
|-----------------|---------|------------------|
| Static | Stability, observation | Objective, calm |
| Push in | Reveal, focus, intimacy | Growing importance |
| Pull out | Context, perspective shift | Expansion, revelation |
| Pan | Environment scan, following | Spatial awareness |
| Tilt | Vertical reveal, emphasis | Height, dominance |
| Track/Dolly | Movement through space | Immersion, dynamism |
| Handheld | Realism, urgency | Documentary, tension |

## Implementation

### Script Parsing

```python
def parse_script_for_visuals(script_segment):
    """
    Extract visual requirements from script text.
    """
    visual_analysis = {
        "time_code": "0:15-0:30",
        "action": "walking through Kyoto streets",
        "emotion": "peaceful, contemplative",
        "key_elements": ["stone pavement", "traditional buildings", "cherry blossoms"],
        "movement": "continuous forward motion",
        "lighting": "afternoon, dappled sunlight"
    }
    return visual_analysis
```

### Shot Decomposition

```python
def decompose_into_shots(visual_analysis, total_duration):
    """
    Break narrative moment into individual shots.
    """
    shots = [
        {
            "shot_number": 1,
            "type": "wide",
            "duration": 5,
            "description": "Street perspective, establishing depth",
            "camera": "static, eye level",
            "lighting": "natural afternoon side light"
        },
        {
            "shot_number": 2,
            "type": "medium",
            "duration": 5,
            "description": "Subject from behind, walking",
            "camera": "tracking, following",
            "lighting": "backlit silhouette"
        },
        {
            "shot_number": 3,
            "type": "close-up",
            "duration": 5,
            "description": "Cherry blossom petals falling",
            "camera": "static, slow motion",
            "lighting": "backlit, translucent petals"
        }
    ]
    return shots
```

### Shot Specification

```python
def specify_shot(shot_concept):
    """
    Create complete shot specification.
    """
    shot_spec = {
        "shot_id": "S01_03",
        "time_code": "0:25-0:30",
        "duration_seconds": 5,
        
        "shot_type": "close-up",
        "shot_size": "extreme_close-up",  # wide, medium, close-up, etc.
        
        "camera": {
            "angle": "eye level",  # eye level, low, high, dutch
            "movement": "static",  # static, push, pull, pan, tilt, track
            "speed": "normal",  # normal, slow, fast
            "lens": "85mm"  # focal length/effect
        },
        
        "composition": {
            "rule": "rule_of_thirds",  # rule_of_thirds, center, symmetry
            "subject_position": "center",
            "depth": "shallow"  # deep, shallow
        },
        
        "lighting": {
            "quality": "soft",  # hard, soft
            "direction": "backlight",  # front, side, back, top
            "color_temp": "warm"  # warm, cool, neutral
        },
        
        "content": {
            "subject": "cherry blossom petals",
            "action": "falling slowly",
            "foreground": "out of focus branch",
            "background": "blurred street scene"
        },
        
        "sound": {
            "music": "continues from previous",
            "sfx": "soft wind, petal rustle",
            "voice": "none"
        },
        
        "notes": "Shoot at 60fps for slow motion playback",
        "reference_images": ["ref_sakura_01.jpg"]
    }
    return shot_spec
```

### Transition Planning

```python
def plan_transition(from_shot, to_shot, style="natural"):
    """
    Determine transition type between shots.
    """
    transitions = {
        "natural": {
            "cut": "standard, direct",
            "fade": "time passage, mood shift",
            "dissolve": "memory, connection",
            "wipe": "energetic, modern"
        },
        "match_cut": {
            "graphic": "shape/color continuity",
            "movement": "action continues across cut",
            "sound": "audio bridges visual change"
        }
    }
    
    # Choose based on content relationship and pacing needs
    return select_transition(from_shot, to_shot, style)
```

### Mood Board Creation

```python
def create_mood_board(project_style):
    """
    Compile visual references for production.
    """
    mood_board = {
        "project": "Summer Travel",
        "style": "healing/natural",
        
        "color_palette": {
            "primary": ["#FFD700", "#98FB98", "#87CEEB"],
            "secondary": ["#FFFFFF", "#FFB6C1"],
            "mood": "warm, fresh, bright"
        },
        
        "lighting_references": [
            {"type": "golden_hour", "description": "Warm, soft, directional"},
            {"type": "backlight_silhouette", "description": "Contours, rim light"}
        ],
        
        "composition_references": [
            {"technique": "rule_of_thirds", "use": "Landscape horizons"},
            {"technique": "leading_lines", "use": "Paths, roads, rivers"},
            {"technique": "frame_within_frame", "use": "Doorways, arches"}
        ],
        
        "film_references": [
            {"title": "Little Forest", "elements": "Natural light, food, seasons"},
            {"title": "Our Little Sister", "elements": "Warm family moments, tradition"}
        ]
    }
    return mood_board
```

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Shot type monotony | Boring visual rhythm | Vary shot sizes; follow wide→medium→close-up pattern |
| 180-degree rule violation | Spatial confusion, disorientation | Establish axis and maintain camera position relative to it |
| Over-complex movement | Distracting from content | Movement serves story; static often better |
| Jump cuts without purpose | Amateur appearance | Use cutaways or matching action to bridge time |
| Ignoring lighting continuity | Disconnected scenes | Plan lighting scheme across sequence |
| Shots too long | Pacing drags | Most shots 3-7 seconds; vary for rhythm |
| Missing coverage | No options in editing | Get wide, medium, and close of key moments |
| Unclear subject | Viewer doesn't know where to look | Use composition to direct attention |

## Shot List Template

```json
{
  "project": "Travel Video",
  "scene": "Kyoto Streets",
  "total_duration": 15,
  "shots": [
    {
      "id": "S01_01",
      "time": "0:00-0:05",
      "type": "wide",
      "duration": 5,
      "description": "Street establishing shot",
      "camera": "static, eye level",
      "notes": "Get depth, both sides of street"
    },
    {
      "id": "S01_02", 
      "time": "0:05-0:10",
      "type": "medium",
      "duration": 5,
      "description": "Subject walking away",
      "camera": "tracking, following",
      "notes": "Maintain consistent distance"
    },
    {
      "id": "S01_03",
      "time": "0:10-0:15", 
      "type": "close-up",
      "duration": 5,
      "description": "Cherry blossom petals",
      "camera": "static, slow motion",
      "notes": "Shoot 60fps for slow mo"
    }
  ]
}
```

## Red Flags - Design Issues

- **Same shot size repeated**: More than 2 consecutive shots of same type
- **Unclear camera direction**: Vague descriptions like "move camera around"
- **Missing time calculations**: Shot durations don't add up to scene duration
- **Impossible transitions**: Suggesting continuous movement across incompatible shots
- **No lighting plan**: Assuming lighting will "work out" on set
- **Over-reliance on effects**: Using transitions/effects to fix poor shot planning
- **Ignoring audio**: Visual plan without sound design consideration
