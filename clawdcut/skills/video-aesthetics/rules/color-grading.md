---
name: color-grading
description: Color grading presets and implementations - warm, vintage, vibrant, cinematic, and custom looks
metadata:
  tags: color-grading, filters, css, svg, color, tone
---

# Color Grading in Remotion

Implement professional color grading effects using CSS filters and SVG filters.

## CSS Filter Presets

### Quick Apply

```tsx
// Apply as style to any shot
<Shot 
  asset={video} 
  style={{ 
    filter: 'sepia(0.15) saturate(1.3) brightness(1.05)' 
  }} 
/>
```

### Preset Definitions

```tsx
export const COLOR_GRADING = {
  // Warm, nostalgic feel
  cinematicWarm: 'sepia(0.15) saturate(1.3) brightness(1.05)',
  
  // Old photograph look
  vintageSepia: 'sepia(0.4) contrast(0.9) brightness(1.1)',
  
  // High saturation, bold colors
  vibrantPop: 'saturate(1.4) contrast(1.1) brightness(1.05)',
  
  // Professional, understated
  mutedDocumentary: 'saturate(0.8) contrast(1.05) brightness(0.95)',
  
  // Cool, tech feel
  coolBlue: 'hue-rotate(15deg) saturate(0.9) brightness(1.0)',
  
  // Dramatic black and white
  filmNoir: 'grayscale(1) contrast(1.3) brightness(0.9)',
  
  // Golden hour warmth
  goldenHour: 'sepia(0.25) saturate(1.5) brightness(1.1) contrast(1.05)',
  
  // Cool winter tones
  winterCool: 'hue-rotate(20deg) saturate(0.85) brightness(1.05)',
  
  // Retro 70s
  retro70s: 'sepia(0.3) saturate(1.2) contrast(1.1) hue-rotate(-10deg)',
  
  // Cyan/teal orange (cinematic)
  tealOrange: 'saturate(1.1) contrast(1.05) hue-rotate(-15deg)',
} as const;
```

## ColorGrade Component

```tsx
import { AbsoluteFill } from 'remotion';

type ColorGradePreset = keyof typeof COLOR_GRADING;

interface ColorGradeProps {
  preset?: ColorGradePreset;
  customFilter?: string;
  intensity?: number; // 0-1, blends with original
}

export const ColorGrade: React.FC<ColorGradeProps> = ({
  preset = 'cinematicWarm',
  customFilter,
  intensity = 1,
}) => {
  const filter = customFilter || COLOR_GRADING[preset];
  
  // For partial intensity, we need CSS custom properties
  const style: React.CSSProperties = intensity < 1
    ? {
        filter: `url(#color-grade-${preset})`,
      }
    : {
        filter,
      };

  return (
    <AbsoluteFill style={style} pointerEvents="none" />
  );
};
```

## SVG Filter for Advanced Control

For more precise control, use SVG filters:

```tsx
// Define in your component
const SVGColorFilters = () => (
  <svg style={{ display: 'none' }}>
    <defs>
      <filter id="cinematic-warm">
        <feColorMatrix
          type="matrix"
          values="1 0 0 0 0
                  0 1 0 0 0
                  0 0 1 0 0
                  0 0 0 1 0"
        />
        <feComponentTransfer>
          <feFuncR type="linear" slope="1.1" intercept="-0.05"/>
          <feFuncG type="linear" slope="1.05" intercept="-0.02"/>
          <feFuncB type="linear" slope="0.9" intercept="0.05"/>
        </feComponentTransfer>
        <feColorMatrix
          type="saturate"
          values="1.3"
        />
      </filter>
    </defs>
  </svg>
);

// Apply with style
<div style={{ filter: 'url(#cinematic-warm)' }}>
  <Shot asset={video} />
</div>
```

## Teal & Orange (Hollywood Look)

The classic cinematic color grade:

```tsx
const TealOrangeGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      filter: `
        contrast(1.05)
        saturate(1.15)
        hue-rotate(-10deg)
        brightness(0.98)
      `,
    }}
  >
    {/* Add color overlay for teal shadows, orange highlights */}
    <div
      style={{
        position: 'absolute',
        inset: 0,
        background: `
          linear-gradient(
            to right,
            rgba(0, 128, 128, 0.15),
            transparent 40%,
            transparent 60%,
            rgba(255, 140, 0, 0.1)
          )
        `,
        mixBlendMode: 'soft-light',
      }}
    />
    {children}
  </div>
);
```

## Vignette Effect

Darken edges to focus attention:

```tsx
const Vignette: React.FC<{
  intensity?: number; // 0-1
  smoothness?: number; // gradient softness
}> = ({ intensity = 0.5, smoothness = 0.5 }) => {
  const gradient = `radial-gradient(
    circle,
    transparent ${100 - 30 * smoothness}%,
    rgba(0, 0, 0, ${intensity}) ${100 - 15 * smoothness}%,
    rgba(0, 0, 0, ${intensity * 0.8}) 100%
  )`;

  return (
    <AbsoluteFill
      style={{
        background: gradient,
        pointerEvents: 'none',
      }}
    />
  );
};
```

## Film Grain Overlay

Add texture and retro feel:

```tsx
const Grain: React.FC<{
  opacity?: number;
  animated?: boolean;
}> = ({ opacity = 0.06, animated = true }) => {
  const frame = useCurrentFrame();
  
  // Animated grain for more natural feel
  const offset = animated 
    ? `${(frame * 0.5) % 100}% ${(frame * 0.7) % 100}%`
    : '0 0';

  return (
    <AbsoluteFill
      style={{
        backgroundImage: `url("data:image/svg+xml,...")`,
        backgroundSize: '200px 200px',
        backgroundPosition: offset,
        opacity,
        mixBlendMode: 'overlay',
        pointerEvents: 'none',
      }}
    />
  );
};

// Simpler version using CSS noise
const GrainCSS: React.FC<{ opacity?: number }> = ({ opacity = 0.05 }) => (
  <AbsoluteFill
    style={{
      background: 'url("data:image/svg+xml,")',
      opacity,
      filter: 'url(#noise)',
      pointerEvents: 'none',
    }}
  />
);
```

## Light Leaks

Dreamy light overlay effects:

```tsx
const LightLeak: React.FC<{
  color?: string;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  intensity?: number;
}> = ({ 
  color = 'rgba(255, 150, 50, 0.3)',
  position = 'top-left',
  intensity = 0.3,
}) => {
  const getPosition = () => {
    switch (position) {
      case 'top-left': return { top: '-20%', left: '-20%', transform: 'rotate(-45deg)' };
      case 'top-right': return { top: '-20%', right: '-20%', transform: 'rotate(45deg)' };
      case 'bottom-left': return { bottom: '-20%', left: '-20%', transform: 'rotate(45deg)' };
      case 'bottom-right': return { bottom: '-20%', right: '-20%', transform: 'rotate(-45deg)' };
    }
  };

  return (
    <AbsoluteFill pointerEvents="none">
      <div
        style={{
          position: 'absolute',
          width: '80%',
          height: '80%',
          background: color,
          filter: 'blur(80px)',
          opacity: intensity,
          ...getPosition(),
        }}
      />
    </AbsoluteFill>
  );
};
```

## Complete Example

```tsx
export const VideoWithGrading: React.FC = () => {
  return (
    <AbsoluteFill>
      {/* Main content */}
      <Shot asset={mainVideo} />
      
      {/* Color grading layer */}
      <ColorGrade preset="cinematicWarm" />
      
      {/* Vignette */}
      <Vignette intensity={0.4} />
      
      {/* Film grain */}
      <Grain opacity={0.05} animated={true} />
      
      {/* Light leak accent */}
      <LightLeak position="top-right" color="rgba(255, 180, 100, 0.2)" />
    </AbsoluteFill>
  );
};
```

## Preset Selection Guide

| Preset | Emotions | Best For |
|--------|---------|----------|
| Cinematic Warm | Nostalgic, loving, inviting | Family, holidays, memories |
| Vintage Sepia | Historical, timeless, classic | History, vintage content |
| Vibrant Pop | Energetic, youthful, bold | Product, social media |
| Muted Documentary | Professional, serious | Corporate, documentary |
| Cool Blue | Calm, trustworthy, tech | Tech, medical, corporate |
| Film Noir | Dramatic, mysterious | Films, artistic content |
| Teal Orange | Cinematic, Hollywood | Movies, trailers |
| Golden Hour | Warm, romantic, dreamy | Weddings, portraits |
