import React from 'react';
import { Sequence } from 'remotion';
import { fps } from '../config/shots';
import { scene1Shots } from '../config/shots';
import { ShotComponent } from './ShotComponent';

// 场景1：脆弱的网络世界（0:00 - 0:25）
export const Scene1: React.FC = () => {
  return (
    <>
      {scene1Shots.map((shot, index) => {
        const from = shot.startTime * fps;
        const durationInFrames = shot.duration * fps;
        
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
