import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Scene1 } from './components/Scene1';
import { Scene2 } from './components/Scene2';
import { Scene3 } from './components/Scene3';
import { Scene4 } from './components/Scene4';
import { Scene5 } from './components/Scene5';

export const CloudflareVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* 场景1：脆弱的网络世界（0:00 - 0:25） */}
      <Scene1 />
      
      {/* 场景2：改变，从质疑开始（0:25 - 0:55） */}
      <Scene2 />
      
      {/* 场景3：无形的守护者（0:55 - 1:45） */}
      <Scene3 />
      
      {/* 场景4：更公平的互联网（1:45 - 2:15） */}
      <Scene4 />
      
      {/* 场景5：未来已来（2:15 - 2:40） */}
      <Scene5 />
    </AbsoluteFill>
  );
};
