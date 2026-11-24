import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
import {Background, PALETTES} from './Background';
import {Headline, Seg, Subtitle} from './Text';
import {SCENES} from './scenes/Scenes';
import {Defs} from './scenes/Primitives';
import {C, FONT, Layout} from './theme';
import {life, ramp} from './anim';

loadFont({family: FONT.sans, url: staticFile('fonts/Cairo-Variable.ttf'), weight: '200 1000'});
loadFont({family: FONT.ruqaa, url: staticFile('fonts/ArefRuqaa-Regular.ttf'), weight: '400'});
loadFont({family: FONT.ruqaa, url: staticFile('fonts/ArefRuqaa-Bold.ttf'), weight: '700'});
loadFont({family: FONT.naskh, url: staticFile('fonts/Amiri-Regular.ttf'), weight: '400'});
loadFont({family: FONT.naskh, url: staticFile('fonts/Amiri-Bold.ttf'), weight: '700'});

export type Beat = {from: number; to: number; head?: Seg[]; sub?: string; subFrom?: number; subColor?: 'w' | 'r' | 'g'; echo?: number};
export type SceneSpan = {id: string; from: number; to: number; cue: Record<string, number>};
export type Episode = {
  fps: number; durationInFrames: number; palette?: string;
  beats: Beat[]; scenes: SceneSpan[];
  card?: {from: number; to: number; lines: string[]; ref: string};
};

const EndCard: React.FC<{card: NonNullable<Episode['card']>; layout: Layout}> = ({card, layout}) => {
  const f = useCurrentFrame();
  const o = life(f, card.from, card.to, 14, 16);
  if (o <= 0) return null;
  const size = layout.w > layout.h ? 36 : 46;
  return (
    <div style={{position: 'absolute', left: 0, width: layout.w, top: layout.headY - size * 1.9, direction: 'rtl', opacity: o,
      display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6,
      filter: `blur(${((1 - ramp(f, card.from, card.from + 14)) * 8).toFixed(2)}px)`}}>
      {card.lines.map((ln, i) => (
        <div key={i} style={{fontFamily: FONT.naskh, fontWeight: 700, fontSize: size, color: i === card.lines.length - 1 ? C.gold : '#eef1f5',
          lineHeight: 1.75, textShadow: i === card.lines.length - 1 ? `0 0 18px ${C.goldGlow}` : '0 0 12px rgba(220,225,231,0.2)',
          whiteSpace: 'nowrap', opacity: ramp(f, card.from + i * 8, card.from + i * 8 + 14)}}>{ln}</div>
      ))}
      <div style={{fontFamily: FONT.sans, fontWeight: 600, fontSize: size * 0.56, color: C.muted, marginTop: 10,
        opacity: ramp(f, card.from + 30, card.from + 44)}}>{card.ref}</div>
    </div>
  );
};

export const Sermon: React.FC<{episode: Episode; layout: Layout}> = ({episode, layout}) => {
  const f = useCurrentFrame();
  const vertical = layout.h > layout.w;
  // stage: scenes are drawn for the 1080 x 1920 frame; the 16:9 frame scales and recentres them
  const stage = `translate(${layout.stageX} ${layout.stageY}) scale(${layout.scale}) translate(-540 -780)`;
  return (
    <AbsoluteFill style={{backgroundColor: C.bgEdge}}>
      <Background layout={layout} palette={PALETTES[episode.palette ?? 'slate']} glowY={vertical ? 760 : layout.stageY} />
      <svg width={layout.w} height={layout.h} style={{position: 'absolute'}}>
        <Defs />
        <g transform={stage}>
          {episode.scenes.map((s, i) => {
            if (f < s.from - 2 || f > s.to + 2) return null;
            const S = SCENES[s.id];
            return S ? <S key={i} f={f} a={s.from} b={s.to} cue={s.cue} /> : null;
          })}
        </g>
      </svg>
      {episode.beats.map((bt, i) => (
        <React.Fragment key={i}>
          {bt.head && <Headline segs={bt.head} from={bt.from} to={bt.to} layout={layout} echo={bt.echo} />}
          {bt.sub && <Subtitle text={bt.sub} from={bt.subFrom ?? bt.from} to={bt.to} layout={layout} color={bt.subColor} />}
        </React.Fragment>
      ))}
      {episode.card && <EndCard card={episode.card} layout={layout} />}
    </AbsoluteFill>
  );
};
