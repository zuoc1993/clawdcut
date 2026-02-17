import { Composition } from 'remotion';
import { CloudflareVideo } from './CloudflareVideo';
import { durationInFrames, fps } from './config/shots';

export const RemotionRoot = () => {
  return (
    <Composition
      id="CloudflareVideo"
      component={CloudflareVideo}
      durationInFrames={durationInFrames}
      fps={fps}
      width={1920}
      height={1080}
    />
  );
};
