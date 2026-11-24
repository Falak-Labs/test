import React from 'react';
import {Composition} from 'remotion';
import {Sermon, Episode} from './Sermon';
import {HORIZONTAL, VERTICAL} from './theme';
import episodeJson from './data/episode.json';

const episode = episodeJson as unknown as Episode;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Short" component={Sermon} width={1080} height={1920} fps={episode.fps}
      durationInFrames={episode.durationInFrames} defaultProps={{episode, layout: VERTICAL}} />
    <Composition id="Long" component={Sermon} width={1920} height={1080} fps={episode.fps}
      durationInFrames={episode.durationInFrames} defaultProps={{episode, layout: HORIZONTAL}} />
  </>
);
