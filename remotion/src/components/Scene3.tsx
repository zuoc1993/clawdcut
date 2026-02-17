import React from 'react';
import { Sequence } from 'remotion';
import { fps } from '../config/shots';
import { scene3Shots } from '../config/shots';
import { ShotComponent } from './ShotComponent';
import { Shot16Multi } from './Shot16Multi';

// 场景3：无形的守护者（0:55 - 1:45）
export const Scene3: React.FC = () => {
  return (
    <>
      {scene3Shots.map((shot, index) => {
        const from = shot.startTime * fps;
        const durationInFrames = shot.duration * fps;
        
        // Shot 16 使用特殊的多画面切换组件
        if (shot.id === 16) {
          return (
            <Sequence
              key={shot.id}
              from={from}
              durationInFrames={durationInFrames}
              premountFor={fps}
            >
              <Shot16Multi />
            </Sequence>
          );
        }
        
        return (
          <Sequence
            key={shot.id}
            from={from}
            durationInFrames={durationInFrames}
            premountFor={fps}
          >
            <ShotComponent shot={shot} />
          </Sequence>
        );
      })}
    </>
  );
};
