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

// Shot 24: 三画面快速切换（未来科技）
export const Shot24Multi: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const images = [
    'assets/images/smart_home_iot.jpg',
    'assets/images/5g_network_tower.jpg',
    'assets/images/smart_city_robots.jpg',
  ];
  
  const texts = ['边缘计算', '人工智能', '无服务器'];
  const durationPerImage = 3 * fps;
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
            filter: 'saturate(1.2) contrast(1.1)',
          }}
        />
      </AbsoluteFill>

      {/* 叠加视频 */}
      <AbsoluteFill
        style={{
          mixBlendMode: 'overlay',
          opacity: 0.25,
        }}
      >
        <Video
          src={staticFile('assets/videos/network_nodes_particles_4k.mp4')}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
          volume={0}
        />
      </AbsoluteFill>

      {/* 技术标签 */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          display: 'flex',
        }}
      >
        <div
          style={{
            fontSize: 100,
            fontWeight: 'bold',
            color: 'white',
            textShadow: '0 0 30px rgba(243, 128, 32, 0.8)',
            textAlign: 'center',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          {texts[imageIndex]}
        </div>
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
          边缘计算、人工智能、无服务器架构——Cloudflare 站在最前沿。
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
