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

// Shot 20: 分屏对比（左侧企业，右侧小工作室）
export const Shot20SplitScreen: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const duration = 10 * fps;

  const opacity = interpolate(
    frame,
    [0, fps * 0.3, duration - fps * 0.3, duration],
    [0, 1, 1, 0],
    { extrapolateRight: 'clamp' }
  );

  // 中间连接线的动画
  const connectionOpacity = interpolate(
    frame,
    [fps * 2, fps * 4],
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* 左侧：大型企业服务器 */}
      <AbsoluteFill
        style={{
          left: 0,
          width: '50%',
          overflow: 'hidden',
        }}
      >
        <Img
          src={staticFile('assets/images/enterprise_server_room.jpg')}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      </AbsoluteFill>

      {/* 右侧：小工作室 */}
      <AbsoluteFill
        style={{
          right: 0,
          width: '50%',
          overflow: 'hidden',
        }}
      >
        <Img
          src={staticFile('assets/images/small_workspace_desk.jpg')}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      </AbsoluteFill>

      {/* 中间连接线动画 */}
      <AbsoluteFill
        style={{
          left: '45%',
          width: '10%',
          justifyContent: 'center',
          alignItems: 'center',
          opacity: connectionOpacity,
        }}
      >
        <div
          style={{
            width: 4,
            height: '100%',
            background: 'linear-gradient(to bottom, transparent, #F38020, transparent)',
          }}
        />
      </AbsoluteFill>

      {/* 数据流动叠加 */}
      <AbsoluteFill
        style={{
          mixBlendMode: 'overlay',
          opacity: 0.3,
        }}
      >
        <Video
          src={staticFile('assets/videos/data_flow_network_4k.mp4')}
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
          有人问，Cloudflare 是什么？我们说——它是让互联网变得更公平的力量。
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
