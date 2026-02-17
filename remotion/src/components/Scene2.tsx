import React from 'react';
import { Sequence } from 'remotion';
import { fps } from '../config/shots';
import { scene2Shots } from '../config/shots';
import { ShotComponent } from './ShotComponent';

// 场景2：改变，从质疑开始（0:25 - 0:55）
export const Scene2: React.FC = () => {
  return (
    <>
      {scene2Shots.map((shot, index) => {
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
