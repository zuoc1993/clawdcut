---
name: video-aesthetics
description: Video aesthetic design principles - color grading, transitions, camera motion, composition, and atmosphere effects
metadata:
  tags: aesthetics, color-grading, transitions, composition, cinematography, visual-design
---

# Video Aesthetics Design

This skill provides comprehensive guidance for making aesthetic decisions in video production.

## When to Use

- When designing visual style for a new video project
- When choosing color grading presets
- When planning transition effects between shots
- When designing camera motion (Ken Burns, pan, tilt)
- When creating composition layouts (split-screen, letterbox)
- When adding atmosphere effects (vignette, grain, particles)

---

## Color Grading Presets

Choose a color grading preset that matches the video's emotional tone:

### 1. Cinematic Warm
- **Feel**: Nostalgic, warm, inviting
- **CSS Filter**: `sepia(0.15) saturate(1.3) brightness(1.05)`
- **Use Case**: Family videos, holidays, memories

### 2. Vintage Sepia
- **Feel**: Old photograph, historical, timeless
- **CSS Filter**: `sepia(0.4) contrast(0.9) brightness(1.1)`
- **Use Case**: Historical content, vintage aesthetic

### 3. Vibrant Pop
- **Feel**: Energetic, youthful, bold
- **CSS Filter**: `saturate(1.4) contrast(1.1) brightness(1.05)`
- **Use Case**: Product videos, social media, commercials

### 4. Muted Documentary
- **Feel**: Professional, understated, cinematic
- **CSS Filter**: `saturate(0.8) contrast(1.05) brightness(0.95)`
- **Use Case**: Documentary, interviews, corporate

### 5. Cool Blue
- **Feel**: Calm, professional, tech
- **CSS Filter**: `hue-rotate(15deg) saturate(0.9) brightness(1.0)`
- **Use Case**: Tech videos, corporate, medical

### 6. Film Noir
- **Feel**: Dramatic, mysterious, high contrast
- **CSS Filter**: `grayscale(1) contrast(1.3) brightness(0.9)`
- **Use Case**: Dramatic content, noir aesthetic

---

## Transition Effects

Choose transitions that enhance the narrative flow:

### Basic Transitions

| Type | Description | Implementation |
|------|-------------|----------------|
| **dissolve** | Cross-fade between shots | opacity interpolation |
| **fade-to-black** | Fade out to black, then in | black overlay opacity |
| **hard-cut** | Instant change | no transition |

### Advanced Transitions

| Type | Description | Implementation |
|------|-------------|----------------|
| **wipe-left/right** | Shutter wipe effect | clipPath animation |
| **zoom-through** | Zoom into center then expand | scale 1→2→1 with opacity |
| **blur-transition** | Blur out then sharpen | filter: blur() |
| **slide** | Slide from direction | translateX/Y |
| **elastic** | Bouncy transition | spring physics |
| **glitch** | Digital distortion | CSS glitch effect |

### Transition Timing

- **Fast transitions**: 15-20 frames (0.5-0.7s) - energetic
- **Medium transitions**: 30 frames (1s) - balanced
- **Slow transitions**: 45-60 frames (1.5-2s) - dramatic

---

## Camera Motion

Add dynamic movement to static shots:

### Ken Burns Effect
Slow, gentle zoom and pan on still images.

```tsx
const scale = interpolate(frame, [0, duration], [1, 1.15]);
const translateX = interpolate(frame, [0, duration], [0, -30]);
const translateY = interpolate(frame, [0, duration], [0, -20]);

style={{
  transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
}}
```

### Motion Types

| Type | Feel | Parameters |
|------|------|------------|
| **static** | Stable, grounded | none |
| **slow-zoom-in** | Intimate, focused | scale 1→1.2 over 3-5s |
| **slow-zoom-out** | Revealing, epic | scale 1.2→1 over 3-5s |
| **pan-left** | Revealing left-to-right | translateX |
| **pan-right** | Revealing right-to-left | translateX |
| **tracking** | Following action | combine translate + scale |
| **orbit** | Cinematic rotation | rotate around center |

---

## Composition Layouts

### Standard Layouts

1. **Full Frame** - Standard 16:9, fills screen
2. **Letterbox** - 21:9 cinematic widescreen with black bars
3. **Pillarbox** - 4:3 with vertical black bars

### Advanced Layouts

| Layout | Description | Use Case |
|--------|-------------|----------|
| **Split-screen** | Two shots side by side | Comparison, dialogue |
| **Picture-in-Picture** | Small overlay on main content | Commentary, reaction |
| **Triple-split** | Three equal sections | Timeline, process |
| **Grid** | 2x2 or 3x3 grid layout | Gallery, montage |
| **Offset** | Asymmetric positioning | Artistic, modern |

### Implementation

```tsx
// Split-screen (50/50)
<div style={{ display: 'flex', width: '100%', height: '100%' }}>
  <div style={{ width: '50%' }}><Shot ... /></div>
  <div style={{ width: '50%' }}><Shot ... /></div>
</div>

// Letterbox (21:9)
<div style={{ 
  paddingTop: '9/21 * 100%', // 42.86%
  height: '100%',
  backgroundColor: 'black'
}}>
  <div style={{ marginTop: '-42.86%' }}>
    <Shot ... />
  </div>
</div>
```

---

## Atmosphere Effects

### Vignette
Darkens edges to focus attention on center.

```tsx
<AbsoluteFill style={{
  background: 'radial-gradient(circle, transparent 40%, rgba(0,0,0,0.6) 100%)',
  pointerEvents: 'none',
}} />
```

### Film Grain
Adds texture and retro feel.

```tsx
<div style={{
  backgroundImage: `url(${grainTexture})`,
  opacity: 0.08,
  mixBlendMode: 'overlay',
}} />
```

### Light Leaks
Bright overlapping colors for dreamy effect.

```tsx
<AbsoluteFill style={{
  background: 'linear-gradient(135deg, rgba(255,150,0,0.2), transparent 50%)',
  mixBlendMode: 'screen',
}} />
```

### Particles
Floating particles for atmosphere (snow, dust, sparkles).

```tsx
// Use @remotion/particles or CSS animation
<div style={{
  backgroundImage: 'url(/particles.png)',
  animation: 'float 10s infinite linear',
}} />
```

---

## Text Animation Styles

| Animation | Description | Best For |
|-----------|-------------|----------|
| **fade** | Simple opacity fade | Subtitles |
| **slide-up** | Slide from bottom | Titles |
| **scale-in** | Scale from small to normal | Big reveals |
| **typewriter** | Character by character | Narration |
| **calligraphy** | Brush stroke effect | Chinese/Artistic |
| **elastic** | Bouncy entrance | Energetic |
| **blur-reveal** | Blur to sharp | Dramatic |

---

## Quick Reference

### Aesthetic Decision Checklist

- [ ] Color grading preset selected
- [ ] Transition style defined per scene
- [ ] Camera motion (Ken Burns) for still images
- [ ] Composition layout (full/split/PIP/letterbox)
- [ ] Atmosphere effects (vignette, grain)
- [ ] Text animation style chosen

### Implementation Order

1. Define color grading in root Video component
2. Apply transitions between Sequences
3. Add Ken Burns to Shot component
4. Build composition layouts
5. Layer atmosphere effects
6. Add text animations

---

## Related Rules

- [transitions.md](./rules/transitions.md) - Detailed transition implementations
- [text-animations.md](./rules/text-animations.md) - Text animation patterns
- [videos.md](./rules/videos.md) - Video component usage
- [animations.md](./rules/animations.md) - General animation techniques
