import React from 'react';
import { Sequence } from 'remotion';
import { fps } from '../config/shots';
import { scene4Shots } from '../config/shots';
import { ShotComponent } from './ShotComponent';
import { Shot20SplitScreen } from './Shot20SplitScreen';

// 场景4：更公平的互联网（1:45 - 2:15）
export const Scene4: React.FC = () => {
  return (
    <>
      {scene4Shots.map((shot, index) => {
        const from = shot.startTime * fps;
        const durationInFrames = shot.duration * fps;
        
        // Shot 20 使用分屏组件
        if (shot.id === 20) {
          return (
            <Sequence
              key={shot.id}
              from={from}
              durationInFrames={durationInFrames}
              premountFor={fps}
            >
              <Shot20SplitScreen />
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
