---
name: transitions
description: Advanced transition effects for Remotion - wipe, zoom, blur, slide, and custom transitions
metadata:
  tags: transitions, animation, wipe, zoom, blur, motion
---

# Transition Effects in Remotion

This document provides implementation details for various transition effects.

## Basic Opacity Transition

The simplest transition using opacity interpolation:

```tsx
import { interpolate, useCurrentFrame } from 'remotion';

const OpacityTransition: React.FC<{
  children: React.ReactNode;
  startFrame: number;
  duration?: number;
}> = ({ children, startFrame, duration = 30 }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) return null;

  const opacity = interpolate(localFrame, [0, duration], [0, 1]);

  return (
    <div style={{ opacity }}>
      {children}
    </div>
  );
};
```

## Wipe Transition

Using clipPath for directional wipes:

```tsx
const WipeTransition: React.FC<{
  direction: 'left' | 'right' | 'up' | 'down';
  startFrame: number;
  duration?: number;
}> = ({ direction, startFrame, duration = 30 }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;
  
  if (localFrame < 0 || localFrame > duration) return null;

  const progress = localFrame / duration;
  
  const getClipPath = () => {
    switch (direction) {
      case 'left':
        return `inset(0 ${100 - progress * 100}% 0 0)`;
      case 'right':
        return `inset(0 0 0 ${100 - progress * 100}%)`;
      case 'up':
        return `inset(${100 - progress * 100}% 0 0 0)`;
      case 'down':
        return `inset(0 0 ${100 - progress * 100}% 0)`;
    }
  };

  return (
    <div style={{ clipPath: getClipPath() }}>
      {/* Next shot content */}
    </div>
  );
};
```

## Zoom Through Transition

Zoom into center, then expand to reveal next shot:

```tsx
import { interpolate, spring, useCurrentFrame } from 'remotion';

const ZoomThroughTransition: React.FC<{
  startFrame: number;
  duration?: number;
}> = ({ startFrame, duration = 45 }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) return null;

  // Phase 1: Zoom in to center (0-50%)
  // Phase 2: Zoom out to reveal (50-100%)
  const phase = localFrame / duration;
  
  const scale = phase < 0.5 
    ? interpolate(phase, [0, 0.5], [1, 2])
    : interpolate(phase, [0.5, 1], [2, 1]);
    
  const opacity = phase < 0.5
    ? interpolate(phase, [0, 0.5], [1, 0])
    : interpolate(phase, [0.5, 1], [0, 1]);

  return (
    <div style={{
      transform: `scale(${scale})`,
      opacity,
    }}>
      {/* Next shot content */}
    </div>
  );
};
```

## Blur Transition

Smooth blur transition:

```tsx
const BlurTransition: React.FC<{
  startFrame: number;
  duration?: number;
  maxBlur?: number;
}> = ({ startFrame, duration = 30, maxBlur = 10 }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) return null;

  const progress = localFrame / duration;
  
  // First half: increase blur on current
  // Second half: decrease blur on next
  const blur = progress < 0.5
    ? interpolate(progress, [0, 0.5], [0, maxBlur])
    : interpolate(progress, [0.5, 1], [maxBlur, 0]);

  return (
    <div style={{ filter: `blur(${blur}px)` }}>
      {/* Content */}
    </div>
  );
};
```

## Slide Transition

Sliding transition with optional bounce:

```tsx
const SlideTransition: React.FC<{
  direction: 'left' | 'right' | 'up' | 'down';
  startFrame: number;
  duration?: number;
  bounce?: boolean;
}> = ({ direction, startFrame, duration = 30, bounce = false }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) return null;

  const progress = bounce
    ? spring({ frame: localFrame, fps: 30, from: 0, to: 1 })
    : localFrame / duration;

  const getTransform = () => {
    const distance = '100%';
    switch (direction) {
      case 'left':
        return `translateX(${interpolate(progress, [0, 1], [-distance as number, 0])}%)`;
      case 'right':
        return `translateX(${interpolate(progress, [0, 1], [distance as number, 0])}%)`;
      case 'up':
        return `translateY(${interpolate(progress, [0, 1], [-distance as number, 0])}%)`;
      case 'down':
        return `translateY(${interpolate(progress, [0, 1], [distance as number, 0])}%)`;
    }
  };

  return (
    <div style={{ transform: getTransform() }}>
      {/* Content */}
    </div>
  );
};
```

## Flash/Whiteout Transition

Quick white flash for energetic cuts:

```tsx
const FlashTransition: React.FC<{
  startFrame: number;
  duration?: number;
}> = ({ startFrame, duration = 15 }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) return null;

  const opacity = interpolate(
    localFrame, 
    [0, duration * 0.3, duration], 
    [0, 1, 0]
  );

  return (
    <div style={{
      position: 'absolute',
      inset: 0,
      backgroundColor: 'white',
      opacity,
    }} />
  );
};
```

## Usage in Video Component

```tsx
import { Sequence } from 'remotion';

// Between shots
<Sequence from={0} durationInFrames={120}>
  <Shot asset={shot1} />
</Sequence>

// Add transition after first shot
<Sequence from={90} durationInFrames={30}>
  <ZoomThroughTransition startFrame={0}>
    <Shot asset={shot2} />
  </ZoomThroughTransition>
</Sequence>
```
