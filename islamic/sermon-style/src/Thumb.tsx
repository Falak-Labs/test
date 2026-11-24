import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Background, PALETTES} from './Background';
import {Defs} from './scenes/Primitives';
import {SCENES, ThreeLights} from './scenes/Scenes';
import {C, FONT, Layout} from './theme';
import {Seg} from './Text';

// YouTube thumbnail (1280x720): one picture (two lights turning back, one gold light going in) + one short line
const L: Layout = {w: 1280, h: 720, headY: 0, headSize: 0, subY: 0, subSize: 0, stageX: 640, stageY: 478, groundY: 0, scale: 1.55};

export const Thumb: React.FC<{segs: Seg[]; scene?: string; palette?: string; f?: number; cue?: Record<string, number>}> = ({segs, scene, palette, f = 60, cue}) => {
  const S = scene ? SCENES[scene] : null;
  return (
  <AbsoluteFill style={{backgroundColor: C.bgEdge}}>
    <Background layout={L} palette={PALETTES[palette ?? 'slate']} glowY={420} dust={45} />
    <svg width={1280} height={720} style={{position: 'absolute'}}>
      <Defs />
      <g transform={`translate(${L.stageX} ${L.stageY}) scale(${L.scale}) translate(-540 -780)`}>
        {S ? <S f={f} a={-100} b={100000} cue={cue ?? {}} /> : <ThreeLights f={60} a={0} b={100000} cue={{ret: 34, enter: 30, gold: 0}} />}
      </g>
    </svg>
    <div style={{position: 'absolute', top: 26, left: 0, width: 1280, display: 'flex', justifyContent: 'center', direction: 'rtl'}}>
      <div style={{whiteSpace: 'nowrap', lineHeight: 1.5}}>
        {segs.map((s, i) => (
          <span key={i} style={s.s === 'g' || s.s === 'r'
            ? {fontFamily: FONT.ruqaa, fontWeight: 700, fontSize: 132, color: s.s === 'r' ? C.red : C.gold, marginInline: '0.3em', // Ruqaa strokes reach into the gap
              textShadow: `0 0 26px ${s.s === 'r' ? C.redGlow : C.goldGlow}, 0 4px 0 rgba(0,0,0,0.5)`}
            : {fontFamily: FONT.sans, fontWeight: 900, fontSize: 112, color: '#ffffff', marginInline: '0.12em',
              textShadow: '0 4px 0 rgba(0,0,0,0.55), 0 0 22px rgba(0,0,0,0.6)'}}>{s.t}</span>
        ))}
      </div>
    </div>
  </AbsoluteFill>
);
};
