import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Img,
  staticFile,
} from 'remotion';
import { Video } from '@remotion/media';
import type { Shot } from '../config/shots';

type ShotComponentProps = {
  shot: Shot;
};

export const ShotComponent: React.FC<ShotComponentProps> = ({ shot }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const durationInFrames = shot.duration * fps;

  // Ken Burns 效果（推拉镜头）
  const getKenBurnsTransform = () => {
    if (shot.cameraMove === 'pushIn') {
      const scale = interpolate(frame, [0, durationInFrames], [1, 1.15], {
        extrapolateRight: 'clamp',
      });
      return `scale(${scale})`;
    }
    if (shot.cameraMove === 'pullOut') {
      const scale = interpolate(frame, [0, durationInFrames], [1.15, 1], {
        extrapolateRight: 'clamp',
      });
      return `scale(${scale})`;
    }
    if (shot.cameraMove === 'pan') {
      const translateX = interpolate(frame, [0, durationInFrames], [0, -50], {
        extrapolateRight: 'clamp',
      });
      return `translateX(${translateX}px)`;
    }
    if (shot.cameraMove === 'tilt') {
      const translateY = interpolate(frame, [0, durationInFrames], [0, -30], {
        extrapolateRight: 'clamp',
      });
      return `translateY(${translateY}px)`;
    }
    return 'scale(1)';
  };

  // 抖动效果
  const getGlitchTransform = () => {
    if (shot.effect === 'glitch') {
      const offsetX = Math.sin(frame * 0.5) * 3;
      const offsetY = Math.cos(frame * 0.7) * 2;
      return `translate(${offsetX}px, ${offsetY}px)`;
    }
    return '';
  };

  // 淡入效果
  const opacity = interpolate(
    frame,
    [0, fps * 0.3, durationInFrames - fps * 0.3, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateRight: 'clamp' }
  );

  // 色调调整（冷色到暖色）
  const getColorFilter = () => {
    if (shot.effect === 'colorShift') {
      // 场景1使用冷色调
      const hueRotate = interpolate(frame, [0, durationInFrames], [0, -10], {
        extrapolateRight: 'clamp',
      });
      const saturate = 0.8;
      return `hue-rotate(${hueRotate}deg) saturate(${saturate})`;
    }
    return 'none';
  };

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* 主图片 */}
      {shot.image && (
        <AbsoluteFill style={{ overflow: 'hidden' }}>
          <Img
            src={staticFile(shot.image)}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `${getKenBurnsTransform()} ${getGlitchTransform()}`,
              filter: getColorFilter(),
            }}
          />
        </AbsoluteFill>
      )}

      {/* 黑屏特殊处理 */}
      {!shot.image && (
        <AbsoluteFill style={{ backgroundColor: 'black' }} />
      )}

      {/* 视频叠加层 */}
      {shot.overlayVideo && (
        <AbsoluteFill
          style={{
            mixBlendMode: shot.blendMode || 'overlay',
            opacity: shot.overlayOpacity || 0.4,
          }}
        >
          <Video
            src={staticFile(shot.overlayVideo)}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
            }}
            volume={0}
          />
        </AbsoluteFill>
      )}

      {/* 文字叠加 */}
      {shot.text && (
        <AbsoluteFill
          style={{
            justifyContent: 'center',
            alignItems: 'center',
            display: 'flex',
          }}
        >
          <div
            style={{
              fontSize: shot.text.includes('\n') ? 60 : 80,
              fontWeight: 'bold',
              color: 'white',
              textShadow: '0 0 20px rgba(0,0,0,0.8)',
              textAlign: 'center',
              fontFamily: 'Arial, sans-serif',
              padding: '20px',
              backgroundColor: 'rgba(0,0,0,0.3)',
              borderRadius: '10px',
              whiteSpace: 'pre-line',
            }}
          >
            {shot.text}
          </div>
        </AbsoluteFill>
      )}

      {/* 旁白字幕（底部） */}
      {shot.narration && (
        <AbsoluteFill
          style={{
            justifyContent: 'flex-end',
            alignItems: 'center',
            paddingBottom: 80,
            display: 'flex',
          }}
        >
          <div
            style={{
              fontSize: 48,
              fontWeight: '500',
              color: 'white',
              textShadow: '0 0 10px rgba(0,0,0,0.9)',
              textAlign: 'center',
              fontFamily: 'Arial, sans-serif',
              maxWidth: '80%',
              lineHeight: 1.6,
              backgroundColor: 'rgba(0,0,0,0.5)',
              padding: '20px 40px',
              borderRadius: '8px',
            }}
          >
            {shot.narration}
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
