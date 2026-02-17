import React from 'react';
import { Sequence } from 'remotion';
import { fps } from '../config/shots';
import { scene5Shots } from '../config/shots';
import { ShotComponent } from './ShotComponent';
import { Shot24Multi } from './Shot24Multi';

// 场景5：未来已来（2:15 - 2:40）
export const Scene5: React.FC = () => {
  return (
    <>
      {scene5Shots.map((shot, index) => {
        const from = shot.startTime * fps;
        const durationInFrames = shot.duration * fps;
        
        // Shot 24 使用多画面切换组件
        if (shot.id === 24) {
          return (
            <Sequence
              key={shot.id}
              from={from}
              durationInFrames={durationInFrames}
              premountFor={fps}
            >
              <Shot24Multi />
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
