---
name: composition
description: Video composition layouts - split-screen, picture-in-picture, letterbox, and advanced grid layouts
metadata:
  tags: composition, layout, split-screen, pip, letterbox, grid
---

# Video Composition Layouts

Guide to implementing various composition layouts in Remotion.

## Basic Full Frame

Standard 16:9 aspect ratio filling the entire canvas:

```tsx
<Shot 
  asset={myVideo} 
  style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
/>
```

## Letterbox (Cinematic Widescreen)

21:9 aspect ratio with black bars:

```tsx
const Letterbox: React.FC<{
  children: React.ReactNode;
  aspectRatio?: number; // default 21/9 = 2.33
}> = ({ children, aspectRatio = 21 / 9 }) => {
  const { width, height } = useVideoConfig();
  const paddingTop = `${(1 / aspectRatio) * 100}%`;

  return (
    <div style={{
      width: '100%',
      height: '100%',
      backgroundColor: 'black',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      paddingTop,
    }}>
      <div style={{ marginTop: `-${paddingTop}`, width: '100%', height: '100%' }}>
        {children}
      </div>
    </div>
  );
};
```

## Split Screen (50/50)

Two shots side by side:

```tsx
const SplitScreen: React.FC<{
  left: React.ReactNode;
  right: React.ReactNode;
  dividerColor?: string;
  dividerWidth?: number;
}> = ({ 
  left, 
  right, 
  dividerColor = 'white', 
  dividerWidth = 4 
}) => {
  return (
    <div style={{
      display: 'flex',
      width: '100%',
      height: '100%',
    }}>
      <div style={{ width: '50%', height: '100%' }}>{left}</div>
      <div style={{ 
        width: dividerWidth, 
        backgroundColor: dividerColor 
      }} />
      <div style={{ width: '50%', height: '100%' }}>{right}</div>
    </div>
  );
};

// Usage
<SplitScreen
  left={<Shot asset={elderlyCouplets} />}
  right={<Shot asset={youngDigital} />}
/>
```

## Picture-in-Picture (PiP)

Small overlay on main content:

```tsx
const PictureInPicture: React.FC<{
  main: React.ReactNode;
  pip: React.ReactNode;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
  pipWidth?: number;
  pipHeight?: number;
  gap?: number;
}> = ({ 
  main, 
  pip, 
  position = 'bottom-right',
  pipWidth = 320,
  pipHeight = 180,
  gap = 20
}) => {
  const getPosition = () => {
    const style: React.CSSProperties = {
      position: 'absolute',
      width: pipWidth,
      height: pipHeight,
    };
    
    switch (position) {
      case 'top-right':
        return { ...style, top: gap, right: gap };
      case 'top-left':
        return { ...style, top: gap, left: gap };
      case 'bottom-right':
        return { ...style, bottom: gap, right: gap };
      case 'bottom-left':
        return { ...style, bottom: gap, left: gap };
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <div style={{ width: '100%', height: '100%' }}>{main}</div>
      <div style={getPosition()}>{pip}</div>
    </div>
  );
};
```

## Triple Split

Three equal sections:

```tsx
const TripleSplit: React.FC<{
  left: React.ReactNode;
  center: React.ReactNode;
  right: React.ReactNode;
  dividerWidth?: number;
}> = ({ left, center, right, dividerWidth = 2 }) => {
  return (
    <div style={{ display: 'flex', width: '100%', height: '100%' }}>
      <div style={{ flex: 1 }}>{left}</div>
      <div style={{ width: dividerWidth, backgroundColor: 'black' }} />
      <div style={{ flex: 1 }}>{center}</div>
      <div style={{ width: dividerWidth, backgroundColor: 'black' }} />
      <div style={{ flex: 1 }}>{right}</div>
    </div>
  );
};
```

## Grid Layout (2x2)

Four equal quadrants:

```tsx
const Grid2x2: React.FC<{
  topLeft: React.ReactNode;
  topRight: React.ReactNode;
  bottomLeft: React.ReactNode;
  bottomRight: React.ReactNode;
  gap?: number;
}> = ({ topLeft, topRight, bottomLeft, bottomRight, gap = 4 }) => {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gridTemplateRows: '1fr 1fr',
      gap: `${gap}px`,
      width: '100%',
      height: '100%',
    }}>
      {topLeft}
      {topRight}
      {bottomLeft}
      {bottomRight}
    </div>
  );
};
```

## Grid Layout (3x3)

Nine equal sections:

```tsx
const Grid3x3: React.FC<{
  children: React.ReactNode[];
  gap?: number;
}> = ({ children, gap = 2 }) => {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gridTemplateRows: 'repeat(3, 1fr)',
      gap: `${gap}px`,
      width: '100%',
      height: '100%',
    }}>
      {children}
    </div>
  );
};
```

## Offset/Asymmetric Layout

Creative asymmetric positioning:

```tsx
const OffsetLayout: React.FC<{
  main: React.ReactNode;
  overlay: React.ReactNode;
  mainSize?: number; // 60-80%
  offsetX?: number;
  offsetY?: number;
}> = ({ 
  main, 
  overlay, 
  mainSize = 70, 
  offsetX = 10, 
  offsetY = -10 
}) => {
  return (
    <div style={{ 
      position: 'relative', 
      width: '100%', 
      height: '100%',
      overflow: 'hidden',
    }}>
      {/* Main content - slightly offset */}
      <div style={{
        position: 'absolute',
        width: `${mainSize}%`,
        height: '100%',
        left: 0,
        top: 0,
      }}>
        {main}
      </div>
      
      {/* Overlay - offset to create depth */}
      <div style={{
        position: 'absolute',
        width: `${100 - mainSize}%`,
        height: '80%',
        right: 0,
        bottom: offsetY,
      }}>
        {overlay}
      </div>
    </div>
  );
};
```

## Diagonal Split

Diagonal line split for dynamic composition:

```tsx
const DiagonalSplit: React.FC<{
  left: React.ReactNode;
  right: React.ReactNode;
  angle?: number; // degrees
}> = ({ left, right, angle = 15 }) => {
  return (
    <div style={{ 
      width: '100%', 
      height: '100%', 
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Left side */}
      <div style={{
        position: 'absolute',
        width: '100%',
        height: '100%',
        clipPath: `polygon(0 0, 100% 0, ${100 - angle}% 100%, 0 100%)`,
      }}>
        {left}
      </div>
      
      {/* Right side */}
      <div style={{
        position: 'absolute',
        width: '100%',
        height: '100%',
        clipPath: `polygon(${100 - angle}% 0, 100% 0, 100% 100%, ${100 - angle}% 100%)`,
      }}>
        {right}
      </div>
    </div>
  );
};
```

## Circle Frame

Circular frame for artistic effect:

```tsx
const CircleFrame: React.FC<{
  children: React.ReactNode;
  size?: number; // percentage of width
}> = ({ children, size = 80 }) => {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'black',
    }}>
      <div style={{
        width: `${size}%`,
        aspectRatio: '1',
        borderRadius: '50%',
        overflow: 'hidden',
      }}>
        {children}
      </div>
    </div>
  );
};
```

## Animated Composition Transitions

Smooth transitions between compositions:

```tsx
const AnimatedSplitScreen: React.FC<{
  left: React.ReactNode;
  right: React.ReactNode;
  startFrame: number;
  duration?: number;
}> = ({ left, right, startFrame, duration = 60 }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > duration) {
    return (
      <div style={{ display: 'flex', width: '100%', height: '100%' }}>
        <div style={{ width: '50%' }}>{left}</div>
        <div style={{ width: '50%' }}>{right}</div>
      </div>
    );
  }

  const progress = localFrame / duration;
  const dividerX = interpolate(progress, [0, 1], [0, 50]);

  return (
    <div style={{ display: 'flex', width: '100%', height: '100%' }}>
      <div style={{ width: `${dividerX}%`, overflow: 'hidden' }}>
        {left}
      </div>
      <div style={{ width: `${100 - dividerX * 2}%`, flexShrink: 0 }} />
      <div style={{ width: `${dividerX}%`, overflow: 'hidden' }}>
        {right}
      </div>
    </div>
  );
};
```
