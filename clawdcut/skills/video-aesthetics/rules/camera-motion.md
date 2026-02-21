---
name: camera-motion
description: Camera motion effects - Ken Burns, pan, tilt, zoom, and dynamic camera movements
metadata:
  tags: camera, motion, ken-burns, pan, tilt, zoom, tracking
---

# Camera Motion Effects

Implement professional camera movements in Remotion.

## Ken Burns Effect

The classic slow zoom and pan on still images.

### Basic Ken Burns

```tsx
import { interpolate, useCurrentFrame } from 'remotion';

interface KenBurnsProps {
  startFrame: number;
  duration: number;
  zoomIn?: boolean;
  panDirection?: 'left' | 'right' | 'up' | 'down' | 'none';
}

export const KenBurns: React.FC<KenBurnsProps> = ({
  startFrame,
  duration,
  zoomIn = true,
  panDirection = 'none',
}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) return null;

  const progress = localFrame / duration;
  
  // Zoom: 1 -> 1.15 (zoom in) or 1.15 -> 1 (zoom out)
  const scale = zoomIn
    ? interpolate(progress, [0, 1], [1, 1.15])
    : interpolate(progress, [0, 1], [1.15, 1]);

  // Pan movement
  const getPan = () => {
    const panAmount = 30; // pixels
    switch (panDirection) {
      case 'left':
        return { x: interpolate(progress, [0, 1], [0, -panAmount]) };
      case 'right':
        return { x: interpolate(progress, [0, 1], [0, panAmount]) };
      case 'up':
        return { y: interpolate(progress, [0, 1], [0, -panAmount]) };
      case 'down':
        return { y: interpolate(progress, [0, 1], [0, panAmount]) };
      default:
        return { x: 0, y: 0 };
    }
  };

  const pan = getPan();

  return {
    transform: `scale(${scale}) translate(${pan.x}px, ${pan.y}px)`,
  };
};
```

### Usage with Shot Component

```tsx
<Shot 
  asset={staticImage}
  style={KenBurns({ startFrame: 0, duration: 180, zoomIn: true, panDirection: 'right' })}
/>
```

## Preset Camera Motions

### Slow Zoom In

Creates intimacy and focus:

```tsx
const slowZoomIn = (progress: number) => interpolate(progress, [0, 1], [1, 1.2]);
```

### Slow Zoom Out

Creates reveal and scope:

```tsx
const slowZoomOut = (progress: number) => interpolate(progress, [0, 1], [1.2, 1]);
```

### Pan Left

Reveal from right to left:

```tsx
const panLeft = (progress: number) => ({
  x: interpolate(progress, [0, 1], [50, -30]),
  y: 0,
});
```

### Pan Right

Reveal from left to right:

```tsx
const panRight = (progress: number) => ({
  x: interpolate(progress, [0, 1], [-50, 30]),
  y: 0,
});
```

### Vertical Tilt Up

Reveal from top:

```tsx
const tiltUp = (progress: number) => ({
  x: 0,
  y: interpolate(progress, [0, 1], [40, -20]),
});
```

### Vertical Tilt Down

Reveal from bottom:

```tsx
const tiltDown = (progress: number) => ({
  x: 0,
  y: interpolate(progress, [0, 1], [-40, 20]),
});
```

### Diagonal Movement

Dynamic diagonal reveal:

```tsx
const diagonalMove = (progress: number) => ({
  x: interpolate(progress, [0, 1], [-30, 20]),
  y: interpolate(progress, [0, 1], [20, -30]),
});
```

### Orbit/Circle

Circular camera movement:

```tsx
const orbit = (progress: number, radius: number = 50) => ({
  x: Math.sin(progress * Math.PI * 2) * radius,
  y: (Math.cos(progress * Math.PI * 2) * radius) - radius,
});
```

## CameraMotion Component

Complete component with presets:

```tsx
import { interpolate, useCurrentFrame, spring } from 'remotion';

type MotionPreset = 
  | 'static'
  | 'slow-zoom-in'
  | 'slow-zoom-out'
  | 'pan-left'
  | 'pan-right'
  | 'tilt-up'
  | 'tilt-down'
  | 'diagonal'
  | 'orbit'
  | 'figure-eight';

interface CameraMotionProps {
  preset?: MotionPreset;
  startFrame: number;
  duration: number;
  speed?: number; // motion speed multiplier
  intensity?: number; // motion range multiplier
}

export const useCameraMotion = ({
  preset = 'static',
  startFrame,
  duration,
  speed = 1,
  intensity = 1,
}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) {
    return { transform: 'scale(1) translate(0, 0)' };
  }

  const progress = (localFrame / duration) * speed;
  const clampedProgress = Math.min(progress, 1);

  const baseIntensity = 30 * intensity;

  switch (preset) {
    case 'slow-zoom-in': {
      const scale = interpolate(clampedProgress, [0, 1], [1, 1 + 0.15 * intensity]);
      return { transform: `scale(${scale})` };
    }
    
    case 'slow-zoom-out': {
      const scale = interpolate(clampedProgress, [0, 1], [1 + 0.15 * intensity, 1]);
      return { transform: `scale(${scale})` };
    }
    
    case 'pan-left': {
      const x = interpolate(clampedProgress, [0, 1], [baseIntensity, -baseIntensity]);
      return { transform: `translateX(${x}px)` };
    }
    
    case 'pan-right': {
      const x = interpolate(clampedProgress, [0, 1], [-baseIntensity, baseIntensity]);
      return { transform: `translateX(${x}px)` };
    }
    
    case 'tilt-up': {
      const y = interpolate(clampedProgress, [0, 1], [baseIntensity, -baseIntensity]);
      return { transform: `translateY(${y}px)` };
    }
    
    case 'tilt-down': {
      const y = interpolate(clampedProgress, [0, 1], [-baseIntensity, baseIntensity]);
      return { transform: `translateY(${y}px)` };
    }
    
    case 'diagonal': {
      const x = interpolate(clampedProgress, [0, 1], [-baseIntensity, baseIntensity]);
      const y = interpolate(clampedProgress, [0, 1], [baseIntensity, -baseIntensity]);
      return { transform: `translate(${x}px, ${y}px)` };
    }
    
    case 'orbit': {
      const x = Math.sin(clampedProgress * Math.PI * 2) * baseIntensity;
      const y = (Math.cos(clampedProgress * Math.PI * 2) - 1) * baseIntensity;
      return { transform: `translate(${x}px, ${y}px)` };
    }
    
    case 'figure-eight': {
      const x = Math.sin(clampedProgress * Math.PI * 4) * baseIntensity * 0.5;
      const y = Math.sin(clampedProgress * Math.PI * 2) * baseIntensity;
      return { transform: `translate(${x}px, ${y}px)` };
    }
    
    default:
      return { transform: 'scale(1) translate(0, 0)' };
  }
};

// Usage
export const ShotWithMotion: React.FC<{
  asset: string;
  type: 'image' | 'video';
  preset?: MotionPreset;
  startFrame: number;
  duration: number;
}> = ({ asset, type, preset = 'static', startFrame, duration }) => {
  const motionStyle = useCameraMotion({ preset, startFrame, duration });

  return (
    <AbsoluteFill>
      {type === 'image' ? (
        <Img src={asset} style={{ ...motionStyle, width: '100%', height: '100%', objectFit: 'cover' }} />
      ) : (
        <Video src={asset} style={{ ...motionStyle, width: '100%', height: '100%', objectFit: 'cover' }} />
      )}
    </AbsoluteFill>
  );
};
```

## Dynamic Camera (Spring-based)

Natural, organic motion using spring physics:

```tsx
const DynamicCamera: React.FC<{
  startFrame: number;
  duration: number;
  motionType?: 'pulse' | 'sway' | 'breathe';
}> = ({ startFrame, duration, motionType = 'pulse' }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) return null;

  const springValue = spring({
    frame: localFrame,
    fps: 30,
    config: { damping: 15, stiffness: 50 },
  });

  switch (motionType) {
    case 'pulse': {
      const scale = interpolate(springValue, [0, 1], [1, 1.03]);
      return { transform: `scale(${scale})` };
    }
    case 'sway': {
      const x = interpolate(springValue, [0, 1], [-10, 10]);
      return { transform: `translateX(${x}px)` };
    }
    case 'breathe': {
      const scale = interpolate(Math.sin(localFrame * 0.05), [-1, 1], [1, 1.02]);
      return { transform: `scale(${scale})` };
    }
  }
};
```

## Tracking Shot

Following movement in video:

```tsx
const TrackingShot: React.FC<{
  direction: 'left' | 'right' | 'up' | 'down';
  speed?: number;
}> = ({ direction, speed = 1 }) => {
  const frame = useCurrentFrame();
  
  const offset = frame * speed;
  
  const getTransform = () => {
    switch (direction) {
      case 'left':
        return { x: offset, y: 0 };
      case 'right':
        return { x: -offset, y: 0 };
      case 'up':
        return { x: 0, y: offset };
      case 'down':
        return { x: 0, y: -offset };
    }
  };

  const { x, y } = getTransform();
  
  return {
    transform: `translate(${x}px, ${y}px) scale(1.1)`,
  };
};
```

## Motion Preset Selection Guide

| Preset | Feel | Best For |
|--------|------|----------|
| Static | Stable, grounded | Establishing shots, interviews |
| Slow zoom in | Intimate, focused | Portraits, emotional moments |
| Slow zoom out | Revealing, epic | Location reveals, conclusions |
| Pan left | Story progression | Following action left-to-right |
| Pan right | Story progression | Following action right-to-left |
| Diagonal | Dynamic, energetic | Action, transitions |
| Orbit | Cinematic, fluid | Product shots, hero moments |
| Figure-eight | Playful, whimsical | Creative, artistic content |
| Pulse | Heartbeat, alive | Emotional peaks |
| Breathe | Calm, meditative | Transitions, breathing room |
