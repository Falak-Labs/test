import React from 'react';
import {Composition} from 'remotion';
import {Sermon, Episode} from './Sermon';
import {HORIZONTAL, VERTICAL} from './theme';
import {Thumb} from './Thumb';
import episodeJson from './data/episode.json';

const episode = episodeJson as unknown as Episode;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Short" component={Sermon} width={1080} height={1920} fps={episode.fps}
      durationInFrames={episode.durationInFrames} defaultProps={{episode, layout: VERTICAL}} />
    <Composition id="Long" component={Sermon} width={1920} height={1080} fps={episode.fps}
      durationInFrames={episode.durationInFrames} defaultProps={{episode, layout: HORIZONTAL}} />
    <Composition id="ThumbA" component={Thumb} width={1280} height={720} fps={30} durationInFrames={1}
      defaultProps={{segs: [{t: 'مين اللي', s: 'w'}, {t: 'يدخل معك؟', s: 'g'}]}} />
    <Composition id="ThumbB" component={Thumb} width={1280} height={720} fps={30} durationInFrames={1}
      defaultProps={{segs: [{t: 'واحد بس', s: 'g'}, {t: 'يدخل معك', s: 'w'}]}} />
    <Composition id="ThumbC" component={Thumb} width={1280} height={720} fps={30} durationInFrames={1}
      defaultProps={{segs: [{t: 'ثلاثة', s: 'g'}, {t: 'يمشون وراك', s: 'w'}]}} />
  </>
);
