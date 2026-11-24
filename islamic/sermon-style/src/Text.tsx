import React from 'react';
import {useCurrentFrame} from 'remotion';
import {life, ramp} from './anim';
import {C, FONT, Layout} from './theme';

// A headline is a list of segments in reading order. s: w = white sans (colloquial), g = gold Ruqaa (key word),
// r = red Ruqaa (sin / loss), q = white Ruqaa (quoted text), m = muted sans, gs = gold sans
export type Seg = {t: string; s?: 'w' | 'g' | 'r' | 'q' | 'm' | 'gs'; at?: number};

const segStyle = (s: Seg['s'], size: number): React.CSSProperties => {
  switch (s) {
    case 'g':
      return {fontFamily: FONT.ruqaa, fontWeight: 700, color: C.gold, fontSize: size * 1.12,
        textShadow: `0 0 18px ${C.goldGlow}, 0 0 42px rgba(242,190,80,0.35)`};
    case 'r':
      return {fontFamily: FONT.ruqaa, fontWeight: 700, color: C.red, fontSize: size * 1.12,
        textShadow: `0 0 18px ${C.redGlow}, 0 0 40px rgba(229,87,78,0.3)`};
    case 'q':
      return {fontFamily: FONT.ruqaa, fontWeight: 700, color: '#eef1f5', fontSize: size * 1.12,
        textShadow: '0 0 14px rgba(220,225,231,0.25)'};
    case 'm':
      return {fontFamily: FONT.sans, fontWeight: 600, color: C.muted, fontSize: size};
    case 'gs':
      return {fontFamily: FONT.sans, fontWeight: 800, color: C.gold, fontSize: size,
        textShadow: `0 0 16px ${C.goldGlow}`};
    default:
      return {fontFamily: FONT.sans, fontWeight: 800, color: '#f2f4f7', fontSize: size,
        textShadow: '0 0 12px rgba(220,225,231,0.18)'};
  }
};

// Fades in with a blur (as in the reference), segments with `at` appear on their own spoken word
export const Headline: React.FC<{segs: Seg[]; from: number; to: number; layout: Layout; echo?: number}> = ({
  segs, from, to, layout, echo,
}) => {
  const f = useCurrentFrame();
  const instant = from <= 3; // the opening headline is already there on frame 0
  const o = instant ? 1 - ramp(f, to - 8, to) : life(f, from, to, 9, 8);
  if (o <= 0) return null;
  const inP = instant ? 1 : ramp(f, from, from + 12);
  const blur = (1 - inP) * 10 + ramp(f, to - 8, to) * 8;
  return (
    <div
      style={{
        position: 'absolute', left: 0, width: layout.w, top: layout.headY - layout.headSize * 1.1,
        height: layout.headSize * 2.2, display: 'flex', alignItems: 'center', justifyContent: 'center',
        direction: 'rtl', opacity: o, filter: `blur(${blur.toFixed(2)}px)`,
        transform: `translateY(${((1 - inP) * 14).toFixed(2)}px)`,
      }}
    >
      <div style={{whiteSpace: 'nowrap', lineHeight: 1.6}}>
        {segs.map((sg, i) => {
          const p = sg.at === undefined ? 1 : ramp(f, sg.at, sg.at + 8);
          const st = segStyle(sg.s, layout.headSize);
          const glitch = echo !== undefined && (sg.s === 'r' || sg.s === 'g') ? ramp(f, echo, echo + 4) - ramp(f, echo + 10, echo + 22) : 0;
          return (
            <span key={i} style={{...st, opacity: p, position: 'relative', display: 'inline-block', marginInline: '0.16em',
              filter: p < 1 ? `blur(${((1 - p) * 8).toFixed(2)}px)` : undefined}}>
              {glitch > 0 && [1, 2, 3].map((k) => (
                <span key={k} style={{position: 'absolute', right: 0, top: k * 9 * glitch, opacity: 0.35 / k,
                  filter: 'blur(1.5px)'}}>{sg.t}</span>
              ))}
              {sg.t.includes('ﷺ')
                ? sg.t.split('ﷺ').map((part, k, arr) => (
                    <React.Fragment key={k}>{part}{k < arr.length - 1 && (
                      <span style={{fontFamily: 'Amiri', fontWeight: 400, fontSize: '0.78em', textShadow: 'none', marginInline: '0.1em'}}>ﷺ</span>
                    )}</React.Fragment>
                  ))
                : sg.t}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export const Subtitle: React.FC<{text: string; from: number; to: number; layout: Layout; color?: 'w' | 'r' | 'g'}> = ({
  text, from, to, layout, color = 'w',
}) => {
  const f = useCurrentFrame();
  const o = life(f, from, to, 8, 8);
  if (o <= 0) return null;
  const col = color === 'r' ? C.red : color === 'g' ? C.gold : C.sub;
  return (
    <div
      style={{
        position: 'absolute', left: 0, width: layout.w, top: layout.subY - layout.subSize, height: layout.subSize * 2,
        display: 'flex', alignItems: 'center', justifyContent: 'center', direction: 'rtl', opacity: o * 0.92,
        fontFamily: FONT.sans, fontWeight: 600, fontSize: layout.subSize, color: col,
        textShadow: color === 'w' ? 'none' : `0 0 14px ${color === 'r' ? C.redGlow : C.goldGlow}`,
        filter: `blur(${((1 - ramp(f, from, from + 10)) * 6).toFixed(2)}px)`,
      }}
    >
      {text}
    </div>
  );
};
