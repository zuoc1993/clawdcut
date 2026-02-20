---
name: remotion-developer
description: Use when transforming storyboards into Remotion video code, generating TypeScript/React components for video production, or setting up Remotion Studio for video preview
---

# Remotion Developer

## Overview

Transforms storyboards and scripts into production-ready Remotion (React + TypeScript) video code. Generates complete Remotion projects with proper component architecture, handles TypeScript compilation, and manages Remotion Studio for preview.

## When to Use

**Use this skill when:**

- Converting visual storyboards into declarative React components
- Building complete Remotion TypeScript projects from scratch
- Generating video timeline components with Sequences
- Implementing camera movements and transitions in code
- Setting up Remotion Studio for video preview
- Handling TypeScript compilation and error fixing

**Don't use when:**

- Working with existing Remotion code (modification only)
- Creating simple static images without video elements
- Building non-React video solutions

## Core Pattern

```
Parse → Plan → Generate → Validate → Launch
```

1. **Parse**: Read script.md and storyboard.md to understand video structure
2. **Plan**: Map shots to Remotion Sequences, design component architecture
3. **Generate**: Create TypeScript files (types → components → Video → Root)
4. **Validate**: Compile TypeScript, auto-fix errors (max 3 attempts)
5. **Launch**: Start Remotion Studio on available port

## Project Structure

```
.clawdcut/remotion/
├── remotion.config.ts          # Project configuration
├── package.json                # Dependencies
├── tsconfig.json              # TypeScript config (strict mode)
└── src/
    ├── Root.tsx               # Composition registration
    ├── Video.tsx              # Main timeline with Sequences
    ├── components/
    │   ├── types.ts           # TypeScript interfaces
    │   ├── Shot.tsx           # Reusable shot component
    │   ├── Transitions.tsx    # Transition effects
    │   └── TextOverlay.tsx    # Animated text overlays
```

## Quick Reference

| Shot Duration | Frames @ 30fps |
|--------------|----------------|
| 1 second     | 30 frames      |
| 3 seconds    | 90 frames      |
| 5 seconds    | 150 frames     |
| 10 seconds   | 300 frames     |

| Camera Movement | Implementation Approach |
|----------------|------------------------|
| Static         | No animation, fixed position |
| Push in        | interpolate scale 1.0 → 1.15 |
| Pull out       | interpolate scale 1.15 → 1.0 |
| Pan left       | interpolate translateX 0 → -50px |
| Pan right      | interpolate translateX 0 → 50px |

## Implementation

### TypeScript Interfaces

```typescript
// src/components/types.ts
export interface ShotProps {
  src: string;
  type: 'image' | 'video';
  durationInFrames: number;
  cameraMovement?: 'static' | 'push' | 'pull' | 'pan-left' | 'pan-right';
  filters?: {
    brightness?: number;
    contrast?: number;
    saturate?: number;
  };
}

export interface TextOverlayProps {
  text: string;
  startFrame: number;
  durationInFrames: number;
  position: 'top' | 'center' | 'bottom';
  animation?: 'fade' | 'slide' | 'scale';
  style?: React.CSSProperties;
}

export interface TransitionProps {
  children: React.ReactNode;
  durationInFrames: number;
}
```

### Shot Component

```typescript
// src/components/Shot.tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { ShotProps } from './types';

export const Shot: React.FC<ShotProps> = ({
  src,
  type,
  durationInFrames,
  cameraMovement = 'static',
  filters
}) => {
  const frame = useCurrentFrame();
  
  const getCameraTransform = () => {
    switch (cameraMovement) {
      case 'push':
        const scale = interpolate(frame, [0, durationInFrames], [1, 1.15]);
        return `scale(${scale})`;
      case 'pull':
        const pullScale = interpolate(frame, [0, durationInFrames], [1.15, 1]);
        return `scale(${pullScale})`;
      case 'pan-left':
        const x = interpolate(frame, [0, durationInFrames], [0, -50]);
        return `translateX(${x}px)`;
      case 'pan-right':
        const rx = interpolate(frame, [0, durationInFrames], [0, 50]);
        return `translateX(${rx}px)`;
      default:
        return undefined;
    }
  };
  
  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <div style={{
        width: '100%',
        height: '100%',
        transform: getCameraTransform(),
        transition: 'transform linear'
      }}>
        {type === 'image' ? (
          <img
            src={src}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              filter: filters ? `
                brightness(${filters.brightness || 1})
                contrast(${filters.contrast || 1})
                saturate(${filters.saturate || 1})
              ` : undefined
            }}
          />
        ) : (
          <Video src={src} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        )}
      </div>
    </AbsoluteFill>
  );
};
```

### Transition Components

```typescript
// src/components/Transitions.tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { TransitionProps } from './types';

// Fade Transition
export const FadeTransition: React.FC<TransitionProps> = ({
  children,
  durationInFrames
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, durationInFrames], [0, 1]);
  
  return (
    <AbsoluteFill style={{ opacity }}>
      {children}
    </AbsoluteFill>
  );
};

// Slide Transition  
export const SlideTransition: React.FC<TransitionProps & {
  direction: 'left' | 'right' | 'up' | 'down';
}> = ({ children, direction, durationInFrames }) => {
  const frame = useCurrentFrame();
  
  const getTransform = () => {
    const value = interpolate(frame, [0, durationInFrames], [100, 0]);
    switch (direction) {
      case 'left': return `translateX(${value}%)`;
      case 'right': return `translateX(-${value}%)`;
      case 'up': return `translateY(${value}%)`;
      case 'down': return `translateY(-${value}%)`;
    }
  };
  
  return (
    <AbsoluteFill style={{ transform: getTransform() }}>
      {children}
    </AbsoluteFill>
  );
};
```

### Text Overlay with Animation

```typescript
// src/components/TextOverlay.tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { TextOverlayProps } from './types';

export const TextOverlay: React.FC<TextOverlayProps> = ({
  text,
  startFrame,
  durationInFrames,
  position = 'center',
  animation = 'fade',
  style
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 10, stiffness: 100 }
  });
  
  const getPosition = () => {
    switch (position) {
      case 'top': return { top: '10%', left: '50%', transform: 'translateX(-50%)' };
      case 'center': return { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' };
      case 'bottom': return { bottom: '10%', left: '50%', transform: 'translateX(-50%)' };
    }
  };
  
  const getAnimation = () => {
    switch (animation) {
      case 'fade': return { opacity: progress };
      case 'scale': return { transform: `scale(${progress})`, opacity: progress };
      case 'slide': return { transform: `translateY(${(1-progress) * 20}px)`, opacity: progress };
    }
  };
  
  return (
    <AbsoluteFill style={{ ...getPosition(), ...getAnimation(), ...style }}>
      {text}
    </AbsoluteFill>
  );
};
```

### Video Timeline Structure

```typescript
// src/Root.tsx
import { Composition } from 'remotion';
import { Video } from './Video';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MainVideo"
      component={Video}
      durationInFrames={900}  // 30s @30fps
      fps={30}
      width={1920}
      height={1080}
    />
  );
};

// src/Video.tsx
import { Sequence } from 'remotion';
import { Shot } from './components/Shot';
import { TextOverlay } from './components/TextOverlay';
import { FadeTransition } from './components/Transitions';

export const Video: React.FC = () => {
  return (
    <>
      {/* Shot 1: 0:00-0:05 (150 frames) */}
      <Sequence from={0} durationInFrames={150}>
        <Shot
          src="../assets/images/opening_scene.jpg"
          type="image"
          durationInFrames={150}
          cameraMovement="push"
        />
        <TextOverlay
          text="故事开始..."
          startFrame={0}
          durationInFrames={60}
          position="center"
          animation="fade"
        />
      </Sequence>
      
      {/* Shot 2: 0:05-0:12 with fade transition */}
      <Sequence from={150} durationInFrames={210}>
        <FadeTransition durationInFrames={30}>
          <Shot
            src="../assets/videos/walking_scene.mp4"
            type="video"
            durationInFrames={210}
            cameraMovement="track"
          />
        </FadeTransition>
      </Sequence>
    </>
  );
};
```

## Best Practices

### Performance
- Use `lazy` property to defer loading large assets
- Avoid complex calculations on every frame, use `useMemo`
- Optimize image sizes, avoid 4K images in 1080p projects

### Animation Timing
- Transitions: 15-30 frames (0.5-1s @30fps)
- Text animation entry: 15-20 frames
- Camera movement: adjust speed based on shot duration
- Use spring animation over linear interpolation for natural motion

### Type Safety
- Define interfaces for all props
- Use strict TypeScript configuration
- Avoid `any` type

### Error Handling
- Check if asset files exist before referencing
- Handle video loading failures gracefully
- Ensure time calculations don't exceed bounds

## Common Patterns

### Looping Video
```tsx
<Video src={src} loop style={{ width: '100%', height: '100%' }} />
```

### Ken Burns Effect
```tsx
const scale = interpolate(frame, [0, duration], [1, 1.15]);
const x = interpolate(frame, [0, duration], [0, -50]);
```

### Background Music
```tsx
import { Audio } from 'remotion';
<Audio src="../assets/audio/background.mp3" volume={0.5} />
```

## Package Dependencies

```json
{
  "dependencies": {
    "@remotion/cli": "^4.0.0",
    "@remotion/player": "^4.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "remotion": "^4.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/web": "^0.0.0",
    "typescript": "^5.0.0"
  }
}
```

## Commands

### TypeScript Compilation Check
```bash
cd .clawdcut/remotion && npx tsc --noEmit
```

### Start Remotion Studio
```bash
cd .clawdcut/remotion && npx remotion studio --port 3000 --no-open
```

### Build Video (for reference)
```bash
cd .clawdcut/remotion && npx remotion render src/index.ts MainVideo out/video.mp4
```

## Error Recovery

### TypeScript Compilation Errors
1. Read error message carefully
2. Fix type errors before logic errors
3. Recompile and verify
4. Max 3 auto-fix attempts before reporting failure

### Port Conflicts
1. Check if port is occupied: `lsof -i :3000`
2. Try next port: `npx remotion studio --port 3001 --no-open`
3. Auto-increment until finding available port

### Missing Assets
1. Verify asset exists in `.clawdcut/assets/`
2. If missing: use placeholder or skip shot
3. Report missing assets to Director Agent
4. Never crash on missing files
