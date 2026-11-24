import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {rnd} from './anim';
import {C, Layout} from './theme';

export type BgPalette = {center: string; mid: string; edge: string; dust: string};
export const PALETTES: Record<string, BgPalette> = {
  slate: {center: C.bgCenter, mid: C.bgMid, edge: C.bgEdge, dust: C.dust}, // the reference look
  teal: {center: '#122a2c', mid: '#0c1d20', edge: '#040b0c', dust: '#bfe0dc'},
  maroon: {center: '#2a1618', mid: '#1c0f11', edge: '#080405', dust: '#e8cfc8'},
  indigo: {center: '#1a1a36', mid: '#111127', edge: '#05050d', dust: '#cfd0f0'},
  sand: {center: '#2a2216', mid: '#1c170f', edge: '#090705', dust: '#efdcb8'},
};

// Dark radial gradient + vignette + slow drifting dust + film grain (grain also stops gradient banding in H.264)
export const Background: React.FC<{layout: Layout; palette?: BgPalette; dust?: number; glowY?: number}> = ({
  layout,
  palette = PALETTES.slate,
  dust = 70,
  glowY,
}) => {
  const f = useCurrentFrame();
  const {w, h} = layout;
  const cy = glowY ?? layout.stageY + 80;
  const dots = [];
  for (let i = 0; i < dust; i++) {
    const x0 = rnd(i, 1.3) * w;
    const y0 = rnd(i, 2.7) * h;
    const speed = 0.08 + rnd(i, 3.1) * 0.25; // px per frame, upward
    const y = (((y0 - f * speed) % h) + h) % h;
    const x = x0 + Math.sin(f / (90 + rnd(i, 4.2) * 120) + i) * 6;
    const r = 0.8 + rnd(i, 5.5) * 1.6;
    const tw = 0.12 + 0.38 * (0.5 + 0.5 * Math.sin(f / (25 + rnd(i, 6.1) * 40) + i * 1.7));
    dots.push(<circle key={i} cx={x} cy={y} r={r} fill={palette.dust} opacity={tw * (0.4 + 0.6 * rnd(i, 7.7))} />);
  }
  const g = Math.floor(f / 2) % 4;
  return (
    <AbsoluteFill>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse ${w * 0.95}px ${h * 0.62}px at ${w / 2}px ${cy}px, ${palette.center} 0%, ${palette.mid} 45%, ${palette.edge} 100%)`,
        }}
      />
      <svg width={w} height={h} style={{position: 'absolute'}}>
        {dots}
      </svg>
      <Img
        src={staticFile(`tex/grain_${g}.png`)}
        style={{position: 'absolute', width: w, height: h, opacity: 0.07, mixBlendMode: 'overlay'}}
      />
    </AbsoluteFill>
  );
};
