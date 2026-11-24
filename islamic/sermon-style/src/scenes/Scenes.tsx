import React from 'react';
import {C} from '../theme';
import {draw, lerp, life, pulse, ramp, rnd} from '../anim';
import {Figure, Ground, Label, Orb, Pool} from './Primitives';

// Every scene is drawn on a 1080 x 1920 stage: centre x 540, illustration around y 640, ground at y 860.
export type SceneProps = {f: number; a: number; b: number; cue: Record<string, number>};
const G = 860;
const gate = (x: number, o = 1) => (
  <g opacity={o}>
    <path d={`M ${x - 52} ${G} L ${x - 52} ${G - 96} Q ${x - 52} ${G - 150} ${x} ${G - 150} Q ${x + 52} ${G - 150} ${x + 52} ${G - 96} L ${x + 52} ${G}`}
      stroke={C.line} strokeWidth={3} fill="rgba(5,9,13,0.55)" strokeLinejoin="round" />
    <path d={`M ${x - 30} ${G} L ${x - 30} ${G - 84} Q ${x - 30} ${G - 118} ${x} ${G - 118} Q ${x + 30} ${G - 118} ${x + 30} ${G - 84} L ${x + 30} ${G}`}
      stroke={C.lineDim} strokeWidth={2} fill="none" />
  </g>
);

// 1. "imagine your last day": the sun sets behind the ground line while you stand watching
export const Sunset: React.FC<SceneProps> = ({f, a, b}) => {
  const p = ramp(f, a + 6, b + 10);
  const sy = lerp(610, 930, p);
  const glow = 1 - ramp(f, a + (b - a) * 0.45, b + 10);
  return (
    <g opacity={life(f, a, b, 10, 12)}>
      <defs><clipPath id="aboveGround"><rect x={0} y={0} width={1080} height={G} /></clipPath></defs>
      <g clipPath="url(#aboveGround)">
        <Pool x={630} y={sy} r={320} o={0.9 * glow + 0.1} />
        <circle cx={630} cy={sy} r={62} stroke={C.gold} strokeWidth={3} fill="rgba(240,199,94,0.06)" filter="url(#glowGold)" />
      </g>
      <Ground y={G} x0={250} x1={830} p={ramp(f, a, a + 22)} />
      <Figure x={455} y={G} s={1} o={ramp(f, a + 8, a + 20)} />
    </g>
  );
};

// 2. "everyone walks behind you, up to the grave's door": a quiet procession towards an arched gate
export const Procession: React.FC<SceneProps> = ({f, a, b}) => {
  const o = life(f, a, b, 10, 12);
  const t = f - a;
  const n = 6;
  const lead = Math.max(455, 840 - t * 1.25);
  const figs = [];
  for (let i = 0; i < n; i++) {
    const x = lead + i * 58 + (i % 2) * 8;
    figs.push(<Figure key={i} x={x} y={G} s={0.85} pose="walk" phase={t / 7 + i * 1.7} dir={-1}
      o={(0.55 + 0.35 * rnd(i, 9)) * ramp(f, a + i * 3, a + 12 + i * 3)} />);
  }
  // the bier, carried at the front
  const bx = lead + 29;
  return (
    <g opacity={o}>
      <Ground y={G} x0={230} x1={880} />
      {gate(300, ramp(f, a, a + 14))}
      <Pool x={300} y={G - 70} r={150} o={0.35} kind="cool" />
      <rect x={bx - 62} y={G - 98} width={124} height={14} rx={7} stroke={C.line} strokeWidth={2.6} fill="rgba(220,225,231,0.08)" filter="url(#glowSoft)" />
      {figs}
    </g>
  );
};

// 3. "the Messenger of Allah ﷺ said": an open book in a gold glow, specks of light rising
export const Book: React.FC<SceneProps> = ({f, a, b}) => {
  const o = life(f, a, b, 10, 12);
  const d = ramp(f, a, a + 24);
  const specks = [];
  for (let i = 0; i < 16; i++) {
    const life_ = ((f - a) * (0.6 + rnd(i, 3) * 0.6) + rnd(i, 5) * 120) % 120;
    specks.push(<circle key={i} cx={470 + rnd(i, 7) * 140} cy={560 - life_ * 1.4} r={1.6 + rnd(i, 2) * 1.6} fill={C.gold}
      opacity={(1 - life_ / 120) * 0.8 * d} />);
  }
  return (
    <g opacity={o}>
      <Pool x={540} y={590} r={300} o={0.8 * d} />
      <g stroke={C.line} strokeWidth={3} fill="none" strokeLinejoin="round" strokeLinecap="round">
        <path d="M 540 612 Q 470 590 372 598 L 372 718 Q 470 708 540 732 Z" {...draw(d)} />
        <path d="M 540 612 Q 610 590 708 598 L 708 718 Q 610 708 540 732 Z" {...draw(d)} />
        <path d="M 540 612 L 540 732" {...draw(d)} />
        {[0, 1, 2, 3, 4].map((k) => (
          <path key={k} d={`M ${690} ${625 + k * 18} L ${565 + (k % 2) * 18} ${627 + k * 18}`} stroke={C.lineDim} strokeWidth={2.2}
            {...draw(ramp(f, a + 14 + k * 3, a + 26 + k * 3))} />
        ))}
      </g>
      {specks}
    </g>
  );
};


// 0. hook: three lights follow you; two turn back, one goes in with you (who they are comes later)
export const ThreeLights: React.FC<SceneProps> = ({f, a, b, cue}) => {
  // first scene of the video: on screen from frame 0 (the first frame is what people see before they decide)
  const o = a <= 3 ? 1 - ramp(f, b - 12, b) : life(f, a, b, 6, 12);
  const enter = a <= 3 ? 0.75 + 0.25 * ramp(f, a, a + 20) : ramp(f, a, a + 30);
  const ret = cue.ret !== undefined ? ramp(f, cue.ret, cue.ret + 40) : 0;
  const goin = cue.enter !== undefined ? ramp(f, cue.enter, cue.enter + 34) : 0;
  const gold = cue.gold !== undefined ? ramp(f, cue.gold, cue.gold + 14) : 0;
  const base = [500, 630, 760];
  return (
    <g opacity={o}>
      <Ground y={G} x0={220} x1={880} />
      <Pool x={300} y={G - 70} r={180} o={0.9 * goin} />
      {gate(300)}
      <path d={`M 880 ${G - 96} L 380 ${G - 96}`} stroke={C.lineDim} strokeWidth={2} strokeDasharray="4 12" opacity={0.5 * enter * (1 - goin)} />
      {base.map((bx, i) => {
        const isOne = i === 2;
        let x = bx + (1 - enter) * (380 + i * 40);
        let oi = Math.min(1, enter * 1.15);
        if (!isOne) {
          x += ret * (170 + i * 60);
          oi *= 1 - 0.8 * ret;
        } else {
          x = lerp(x, 300, goin);
          oi *= 1 - 0.55 * ramp(goin, 0.85, 1, (t) => t);
        }
        const y = G - 96 + Math.sin((f - a) / 13 + i * 1.3) * 4;
        const golden = isOne ? gold : 0;
        return (
          <g key={i} opacity={oi}>
            <Pool x={x} y={y} r={110} o={0.5} kind={golden > 0.5 ? 'gold' : 'cool'} />
            <circle cx={x} cy={y} r={18} fill={golden > 0.5 ? C.gold : '#e8edf3'} filter={golden > 0.5 ? 'url(#glowGold)' : 'url(#glowSoft)'} />
            <circle cx={x} cy={y} r={34} stroke={golden > 0.5 ? C.gold : C.lineDim} strokeWidth={2} fill="none" opacity={0.6} />
          </g>
        );
      })}
    </g>
  );
};

// small icons drawn inside the three companions
const IconFamily: React.FC<{x: number; y: number; c: string}> = ({x, y, c}) => (
  <g stroke={c} strokeWidth={2.4} fill="none" strokeLinecap="round">
    {[-16, 0, 16].map((dx, i) => (
      <g key={i} transform={`translate(${x + dx} ${y + (i === 2 ? 4 : 0)}) scale(${i === 2 ? 0.75 : 1})`}>
        <circle cx={0} cy={-12} r={5} />
        <path d="M 0 -7 L 0 8 M 0 8 L -5 18 M 0 8 L 5 18 M 0 -2 L -6 6 M 0 -2 L 6 6" />
      </g>
    ))}
  </g>
);
const IconCoins: React.FC<{x: number; y: number; c: string}> = ({x, y, c}) => (
  <g stroke={c} strokeWidth={2.4} fill="none">
    {[0, 1, 2].map((k) => <ellipse key={k} cx={x} cy={y + 10 - k * 9} rx={17} ry={6} />)}
    <path d={`M ${x - 17} ${y + 10} L ${x - 17} ${y - 8} M ${x + 17} ${y + 10} L ${x + 17} ${y - 8}`} />
  </g>
);
const IconDeed: React.FC<{x: number; y: number; c: string}> = ({x, y, c}) => (
  <g stroke={c} strokeWidth={2.6} fill="none" strokeLinejoin="round">
    <path d={`M ${x} ${y - 20} C ${x + 14} ${y - 4} ${x + 12} ${y + 12} ${x} ${y + 14} C ${x - 12} ${y + 12} ${x - 14} ${y - 4} ${x} ${y - 20} Z`} />
    <path d={`M ${x} ${y + 2} C ${x + 5} ${y + 6} ${x + 4} ${y + 11} ${x} ${y + 12}`} />
  </g>
);

// 4. the hadith: three follow the dead, two go back, one stays
export const ThreeFollow: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 12);
  const enter = ramp(f, a + 4, a + 40);
  const ret = cue.ret !== undefined ? ramp(f, cue.ret, cue.ret + 50) : 0;
  const stay = cue.stay !== undefined ? ramp(f, cue.stay, cue.stay + 30) : 0;
  const base = [480, 630, 780];
  const items = [
    {k: 'family', label: 'أهله', Icon: IconFamily},
    {k: 'wealth', label: 'ماله', Icon: IconCoins},
    {k: 'deed', label: 'عمله', Icon: IconDeed},
  ];
  return (
    <g opacity={o}>
      <Ground y={G} x0={220} x1={880} />
      {gate(300)}
      <path d={`M 880 ${G - 96} L 380 ${G - 96}`} stroke={C.lineDim} strokeWidth={2} strokeDasharray="4 12" opacity={0.6 * enter} />
      {items.map((it, i) => {
        const isDeed = i === 2;
        let x = base[i] + (1 - enter) * (320 + i * 60);
        let oi = enter;
        if (!isDeed) {
          x += ret * (150 + i * 45);
          oi *= 1 - 0.75 * ret;
        } else {
          x = lerp(x, 400, stay);
        }
        const y = G - 96 + Math.sin((f - a) / 14 + i) * 3;
        const col = isDeed ? C.gold : C.line;
        const lab = cue[it.k] !== undefined ? ramp(f, cue[it.k], cue[it.k] + 10) : 0;
        return (
          <g key={it.k} opacity={oi}>
            {isDeed && <Pool x={x} y={y} r={130 + 120 * stay} o={0.45 + 0.55 * stay + 0.15 * pulse(f, 60)} />}
            <circle cx={x} cy={y} r={56} stroke={col} strokeWidth={3.2} fill="rgba(5,9,13,0.6)" filter={isDeed ? 'url(#glowGold)' : undefined} />
            <g transform={`translate(${x} ${y}) scale(1.35) translate(${-x} ${-y})`}><it.Icon x={x} y={y} c={col} /></g>
            <Label x={x} y={G + 58} t={it.label} size={38} color={isDeed ? C.gold : C.sub} o={lab * (isDeed ? 1 : 1 - ret)} weight={700} />
          </g>
        );
      })}
    </g>
  );
};

const house = (x: number, lit: number) => (
  <g>
    <Pool x={x} y={G - 40} r={170} o={0.55 * lit} />
    <path d={`M ${x - 55} ${G} L ${x - 55} ${G - 70} L ${x} ${G - 118} L ${x + 55} ${G - 70} L ${x + 55} ${G}`} stroke={C.line} strokeWidth={3} fill="rgba(5,9,13,0.5)" strokeLinejoin="round" />
    <rect x={x - 16} y={G - 62} width={32} height={28} stroke={lit > 0.1 ? C.gold : C.lineDim} strokeWidth={2.4} fill={`rgba(240,199,94,${0.75 * lit})`} filter={lit > 0.1 ? 'url(#glowGold)' : undefined} />
  </g>
);

// 5. your family cries a little, then goes back home
export const FamilyHome: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 12);
  const turn = cue.turn ?? Math.round((a + b) / 2);
  const walk = ramp(f, turn, b, (t) => t);
  const lit = cue.home !== undefined ? ramp(f, cue.home, cue.home + 14) : 0;
  const fam = [
    {x: 465, s: 0.95}, {x: 522, s: 0.95}, {x: 566, s: 0.66},
  ];
  return (
    <g opacity={o}>
      <Ground y={G} x0={230} x1={880} />
      <path d={`M 278 ${G} Q 340 ${G - 46} 402 ${G}`} stroke={C.line} strokeWidth={3} fill="rgba(5,9,13,0.5)" />
      <rect x={333} y={G - 74} width={14} height={36} rx={5} stroke={C.lineDim} strokeWidth={2.4} fill="none" />
      {house(790, lit)}
      {fam.map((m, i) => {
        const moving = f >= turn;
        const x = m.x + walk * (205 - i * 10);
        return (
          <Figure key={i} x={x} y={G} s={m.s} pose={moving ? 'walk' : 'bow'} phase={(f - turn) / 6 + i}
            dir={moving ? 1 : -1} o={(1 - ramp(f, b - 16, b)) * 0.95} />
        );
      })}
    </g>
  );
};

// 6. your wealth is divided while you are gone
export const WealthSplit: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 12);
  const split = cue.split !== undefined ? ramp(f, cue.split, cue.split + 26) : 0;
  const gone = cue.gone !== undefined ? ramp(f, cue.gone, cue.gone + 24) : 0;
  const bars = [
    {x: 360, h: 170, l: 'شقة'}, {x: 455, h: 250, l: 'عربية'}, {x: 550, h: 205, l: 'أرض'}, {x: 645, h: 290, l: 'رصيد'},
  ];
  const w = 66;
  return (
    <g opacity={o}>
      <Ground y={G} x0={250} x1={860} />
      {bars.map((br, i) => {
        const grow = ramp(f, a + 4 + i * 5, a + 30 + i * 5);
        const h = br.h * grow;
        const col = split > 0.5 ? C.muted : C.gold;
        const parts = [0, 1, 2];
        return (
          <g key={i}>
            {parts.map((k) => {
              const ph = h / 3;
              const pw = w / 3 - 5;
              const x = lerp(br.x - w / 2, br.x - w / 2 + k * (w / 3) + 2.5, split);
              const y = lerp(G - ph * (k + 1), G - ph, split);
              const ww = lerp(w, pw, split);
              return (
                <rect key={k} x={x} y={y + (split > 0 ? 0 : 0)} width={ww} height={Math.max(0, ph - 3)} rx={lerp(8, 4, split)}
                  stroke={col} strokeWidth={2.8} fill={split > 0.5 ? 'rgba(140,150,163,0.05)' : 'rgba(240,199,94,0.08)'}
                  opacity={1 - 0.45 * split} filter={split < 0.5 && grow > 0.95 ? 'url(#glowSoft)' : undefined} />
              );
            })}
            <circle cx={br.x} cy={G - h - 20 + split * (h * 2 / 3)} r={6} stroke={col} strokeWidth={2.4} fill="none" opacity={grow * (1 - 0.8 * split)} />
            <Label x={br.x} y={G + 44} t={br.l} size={28} color={C.gold} o={grow * (1 - 0.6 * split)} />
          </g>
        );
      })}
      <Figure x={800} y={G} s={0.95} dir={-1} o={ramp(f, a + 10, a + 22) * (1 - gone)} />
      {gone > 0 && <Pool x={800} y={G - 50} r={90} kind="cool" o={0.5 * (1 - gone)} />}
    </g>
  );
};

// 7. "one thing stays with you... your deeds": a single light that grows into rings around you
export const OneThing: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 14);
  const one = cue.one !== undefined ? ramp(f, cue.one, cue.one + 12) : ramp(f, a + 20, a + 32);
  const deed = cue.deed !== undefined ? ramp(f, cue.deed, cue.deed + 30) : 0;
  const cx = 540, cy = G - 60;
  return (
    <g opacity={o}>
      <Ground y={G} x0={330} x1={750} o={0.7} />
      <Pool x={cx} y={cy} r={140 + 260 * deed} o={0.25 * one + 0.75 * deed} />
      {[0, 1, 2].map((k) => {
        const rr = (70 + k * 48) * deed;
        return rr > 2 ? <circle key={k} cx={cx} cy={cy} r={rr} stroke={C.gold} strokeWidth={2.4 - k * 0.5} fill="none"
          opacity={(0.9 - k * 0.25) * deed * (0.8 + 0.2 * pulse(f, 70, k * 20))} filter={k === 0 ? 'url(#glowGold)' : undefined} /> : null;
      })}
      <circle cx={cx} cy={cy - 50 * (1 - deed)} r={4 + 4 * one + 6 * deed} fill={C.gold} opacity={one} filter="url(#glowGold)" />
      <Figure x={cx} y={G} s={1} o={0.35 + 0.65 * deed} color={deed > 0.5 ? '#f3e2b8' : C.line} />
    </g>
  );
};

// 8. "if your grave were closed today: light, or darkness?"
export const Grave: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 12);
  const close = cue.close !== undefined ? ramp(f, cue.close, cue.close + 20) : 0;
  const light = cue.light !== undefined ? ramp(f, cue.light, cue.light + 14) : 0;
  const dark = cue.dark !== undefined ? ramp(f, cue.dark, cue.dark + 16) : 0;
  const glow = light * (1 - dark);
  const top = G - 66;
  const flick = 0.75 + 0.25 * Math.sin((f - a) / 2.3) * Math.sin((f - a) / 5.1);
  return (
    <g opacity={o}>
      <Ground y={top - 0} x0={250} x1={830} />
      <defs><clipPath id="graveClip"><rect x={392} y={top + 6} width={296} height={128} rx={6} /></clipPath></defs>
      <g clipPath="url(#graveClip)">
        <rect x={392} y={top + 6} width={296} height={128} fill="rgba(3,6,9,0.85)" />
        <Pool x={540} y={top + 80} r={260} o={glow} />
        <Pool x={540} y={top + 80} r={200} o={0.5 * dark * (1 - ramp(f, cue.dark ?? b, (cue.dark ?? b) + 40))} kind="red" />
      </g>
      <rect x={392} y={top + 6} width={296} height={128} rx={6} stroke={glow > 0.3 ? C.gold : C.line} strokeWidth={3} fill="none"
        opacity={0.95 - 0.5 * dark} filter={glow > 0.3 ? 'url(#glowGold)' : undefined} />
      <Figure x={548} y={top + 108} s={0.95} pose="lie" color={glow > 0.3 ? '#f3e2b8' : C.line} o={1 - 0.5 * dark} />
      <circle cx={470} cy={top + 90} r={5} fill={C.gold} opacity={(0.35 + 0.65 * glow) * flick * (1 - 0.85 * dark)} filter="url(#glowGold)" />
      <rect x={lerp(720, 392, close)} y={top - 4} width={296} height={14} rx={5} stroke={C.line} strokeWidth={2.6} fill="rgba(8,12,17,0.95)" opacity={close} />
    </g>
  );
};

// 9. the deeds you keep postponing: a list that turns from red to gold
export const Checklist: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 12);
  const rows = ['الصلاة', 'الصدقة', 'القرآن', 'بر الوالدين', 'ذكر الله'];
  const x0 = 380, y0 = 470, w = 320, h = 400;
  const gold = cue.gold ?? b + 1000;
  const seal = ramp(f, gold + rows.length * 7, gold + rows.length * 7 + 22);
  return (
    <g opacity={o}>
      <rect x={x0} y={y0} width={w} height={h} rx={16} stroke={C.line} strokeWidth={3} fill="rgba(220,225,231,0.035)"
        {...draw(ramp(f, a, a + 22))} />
      {rows.map((r, i) => {
        const ap = ramp(f, a + 10 + i * 6, a + 22 + i * 6);
        const g = ramp(f, gold + i * 7, gold + i * 7 + 10);
        const y = y0 + 70 + i * 62;
        return (
          <g key={i} opacity={ap}>
            <text x={x0 + w - 26} y={y + 10} textAnchor="end" fontFamily="Cairo" fontWeight={700} fontSize={30}
              fill={g > 0.5 ? C.gold : C.sub}>{r}</text>
            <path d={`M ${x0 + 140} ${y} L ${x0 + 62} ${y}`} stroke={C.lineDim} strokeWidth={2.4} strokeLinecap="round" />
            <circle cx={x0 + 38} cy={y} r={7 * (1 - g) + 0.01} fill={C.red} filter="url(#glowRed)" opacity={1 - g} />
            <path d={`M ${x0 + 27} ${y} L ${x0 + 36} ${y + 9} L ${x0 + 52} ${y - 10}`} stroke={C.gold} strokeWidth={3.4} fill="none"
              strokeLinecap="round" strokeLinejoin="round" {...draw(g)} filter={g > 0 ? 'url(#glowGold)' : undefined} />
          </g>
        );
      })}
      <g opacity={seal}>
        <Pool x={x0 + 18} y={y0 + h - 18} r={120} o={0.6} />
        <circle cx={x0 + 18} cy={y0 + h - 18} r={40} stroke={C.gold} strokeWidth={3.2} fill="rgba(5,9,13,0.85)" filter="url(#glowGold)" {...draw(seal)} />
        <path d={`M ${x0 + 1} ${y0 + h - 18} L ${x0 + 13} ${y0 + h - 6} L ${x0 + 36} ${y0 + h - 32}`} stroke={C.gold} strokeWidth={4} fill="none"
          strokeLinecap="round" strokeLinejoin="round" {...draw(ramp(f, gold + rows.length * 7 + 12, gold + rows.length * 7 + 30))} />
      </g>
    </g>
  );
};

// 10. "start today": a tree grows and its fruits light up one by one
export const Tree: React.FC<SceneProps> = ({f, a, b}) => {
  const o = life(f, a, b, 12, 18);
  const t = ramp(f, a, a + 70, (x) => x);
  const segs: {x1: number; y1: number; x2: number; y2: number; d: number}[] = [];
  const tips: {x: number; y: number; d: number}[] = [];
  const grow = (x: number, y: number, ang: number, len: number, depth: number, d0: number) => {
    const x2 = x + Math.cos(ang) * len, y2 = y - Math.sin(ang) * len;
    segs.push({x1: x, y1: y, x2, y2, d: d0});
    if (depth === 0) { tips.push({x: x2, y: y2, d: d0 + 0.12}); return; }
    grow(x2, y2, ang + 0.42, len * 0.72, depth - 1, d0 + 0.16);
    grow(x2, y2, ang - 0.42, len * 0.72, depth - 1, d0 + 0.16);
  };
  grow(540, G, Math.PI / 2, 108, 4, 0);
  return (
    <g opacity={o}>
      <Ground y={G} x0={330} x1={750} />
      <Pool x={540} y={660} r={300} o={0.75 * ramp(f, a + 40, a + 90)} />
      {segs.map((s, i) => (
        <path key={i} d={`M ${s.x1} ${s.y1} L ${s.x2} ${s.y2}`} stroke={C.line} strokeWidth={Math.max(1.6, 4 - s.d * 4)} strokeLinecap="round"
          {...draw(ramp(t, s.d * 0.8, s.d * 0.8 + 0.18))} />
      ))}
      {tips.map((p, i) => {
        const on = ramp(f, a + 50 + i * 3, a + 62 + i * 3);
        return on > 0 ? <circle key={i} cx={p.x} cy={p.y} r={6} fill={C.gold} opacity={on * (0.75 + 0.25 * pulse(f, 50, i * 7))} filter="url(#glowGold)" /> : null;
      })}
    </g>
  );
};

export const SCENES: Record<string, React.FC<SceneProps>> = {
  ThreeLights, Sunset, Procession, Book, ThreeFollow, FamilyHome, WealthSplit, OneThing, Grave, Checklist, Tree,
};
