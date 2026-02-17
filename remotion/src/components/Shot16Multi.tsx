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

// Shot 16: 三画面快速切换
export const Shot16Multi: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const images = [
    'assets/images/mother_online_shopping.jpg',
    'assets/images/student_online_learning.jpg',
    'assets/images/small_business_owner.jpg',
  ];
  
  const durationPerImage = 3 * fps; // 每个画面约3秒
  const currentIndex = Math.floor(frame / durationPerImage);
  const imageIndex = Math.min(currentIndex, images.length - 1);
  
  const opacity = interpolate(
    frame,
    [0, fps * 0.2, durationPerImage * images.length - fps * 0.2, durationPerImage * images.length],
    [0, 1, 1, 0],
    { extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* 当前图片 */}
      <AbsoluteFill style={{ overflow: 'hidden' }}>
        <Img
          src={staticFile(images[imageIndex])}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      </AbsoluteFill>

      {/* 叠加视频 */}
      <AbsoluteFill
        style={{
          mixBlendMode: 'overlay',
          opacity: 0.15,
        }}
      >
        <Video
          src={staticFile('assets/videos/geometric_network_lines_4k.mp4')}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
          volume={0}
        />
      </AbsoluteFill>

      {/* 旁白字幕 */}
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
          当你在深夜网购时，当孩子在课堂上看视频时，当创业者实现梦想时——Cloudflare 都在背后，为你护航。
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
