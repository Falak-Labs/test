import React from 'react';
import {C} from '../theme';
import {draw} from '../anim';

// Shared SVG filters and gradients (put once inside the stage <svg>)
export const Defs: React.FC = () => (
  <defs>
    <filter id="glowGold" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7" result="b" />
      <feMerge><feMergeNode in="b" /><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <filter id="glowSoft" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.5" result="b" />
      <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <filter id="glowRed" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="6" result="b" />
      <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <radialGradient id="poolGold">
      <stop offset="0%" stopColor="#f6c65a" stopOpacity="0.55" />
      <stop offset="35%" stopColor="#e9b04a" stopOpacity="0.22" />
      <stop offset="100%" stopColor="#e9b04a" stopOpacity="0" />
    </radialGradient>
    <radialGradient id="poolRed">
      <stop offset="0%" stopColor="#e5574e" stopOpacity="0.5" />
      <stop offset="40%" stopColor="#c8433b" stopOpacity="0.18" />
      <stop offset="100%" stopColor="#c8433b" stopOpacity="0" />
    </radialGradient>
    <radialGradient id="poolCool">
      <stop offset="0%" stopColor="#c9d6e6" stopOpacity="0.22" />
      <stop offset="100%" stopColor="#c9d6e6" stopOpacity="0" />
    </radialGradient>
  </defs>
);

export const Pool: React.FC<{x: number; y: number; r: number; o?: number; kind?: 'gold' | 'red' | 'cool'}> = ({
  x, y, r, o = 1, kind = 'gold',
}) => (o > 0 ? <circle cx={x} cy={y} r={r} fill={`url(#pool${kind === 'gold' ? 'Gold' : kind === 'red' ? 'Red' : 'Cool'})`} opacity={o} /> : null);

export const Ground: React.FC<{y: number; x0?: number; x1?: number; p?: number; o?: number}> = ({y, x0 = 300, x1 = 780, p = 1, o = 1}) => (
  <path d={`M ${x1} ${y} L ${x0} ${y}`} stroke={C.ground} strokeWidth={2.2} fill="none" opacity={o} {...draw(p)} strokeLinecap="round" />
);

// Stick figure standing on (x, ground). pose: stand | walk | bow | lie. dir: 1 faces right, -1 faces left
export const Figure: React.FC<{
  x: number; y: number; s?: number; color?: string; o?: number; pose?: 'stand' | 'walk' | 'bow' | 'lie';
  phase?: number; dir?: number; glow?: boolean; draw?: number;
}> = ({x, y, s = 1, color = C.line, o = 1, pose = 'stand', phase = 0, dir = 1, glow = false, draw: dp = 1}) => {
  if (o <= 0) return null;
  const sw = 3.2;
  const common = {stroke: color, strokeWidth: sw / s, fill: 'none', strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  let body: React.ReactNode;
  if (pose === 'lie') {
    body = (
      <g>
        <circle cx={-44} cy={-10} r={10.5} {...common} />
        <path d="M -32 -10 L 14 -10 M 14 -10 L 46 -6 M 14 -10 L 46 -14 M -20 -10 L 4 -4" {...common} />
      </g>
    );
  } else {
    const sw2 = pose === 'walk' ? Math.sin(phase) * 13 : 0;
    const arm = pose === 'walk' ? Math.sin(phase + Math.PI) * 10 : 0;
    const bow = pose === 'bow' ? 1 : 0;
    const headX = bow * 7 * dir;
    const headY = -84 + bow * 6;
    body = (
      <g>
        <circle cx={headX} cy={headY} r={10.5} {...common} {...(dp < 1 ? draw(dp) : {})} />
        <path d={`M ${headX * 0.6} ${headY + 11} L 0 -38`} {...common} {...(dp < 1 ? draw(dp) : {})} />
        <path d={`M 0 -38 L ${-10 + sw2} 0 M 0 -38 L ${10 - sw2} 0`} {...common} {...(dp < 1 ? draw(dp) : {})} />
        <path d={`M ${headX * 0.5} -64 L ${-13 + arm} ${-40 + bow * 4} M ${headX * 0.5} -64 L ${13 - arm} ${-40 + bow * 4}`} {...common} {...(dp < 1 ? draw(dp) : {})} />
      </g>
    );
  }
  return (
    <g transform={`translate(${x} ${y}) scale(${s * dir} ${s})`} opacity={o} filter={glow ? 'url(#glowSoft)' : undefined}>
      {body}
    </g>
  );
};

export const Orb: React.FC<{x: number; y: number; r: number; color?: string; o?: number; ring?: number; glow?: 'gold' | 'red' | 'cool'}> = ({
  x, y, r, color = C.gold, o = 1, ring = 0, glow = 'gold',
}) => (o > 0 ? (
  <g opacity={o}>
    <Pool x={x} y={y} r={r * 5.5} kind={glow} />
    <circle cx={x} cy={y} r={r} fill={color} filter={glow === 'gold' ? 'url(#glowGold)' : glow === 'red' ? 'url(#glowRed)' : 'url(#glowSoft)'} />
    {ring > 0 && <circle cx={x} cy={y} r={r * 2.1} stroke={color} strokeWidth={2} fill="none" opacity={0.55 * ring} />}
  </g>
) : null);

// Arabic label drawn in SVG (Cairo), right-to-left
export const Label: React.FC<{x: number; y: number; t: string; size?: number; color?: string; o?: number; font?: string; weight?: number}> = ({
  x, y, t, size = 30, color = C.sub, o = 1, font = 'Cairo', weight = 600,
}) => (o > 0 ? (
  <text x={x} y={y} textAnchor="middle" direction="rtl" fontFamily={font} fontWeight={weight} fontSize={size} fill={color} opacity={o}>
    {t}
  </text>
) : null);
