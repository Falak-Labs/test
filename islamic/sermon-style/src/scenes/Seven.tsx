import React from 'react';
import {C} from '../theme';
import {draw, life, pulse, ramp, rnd} from '../anim';
import {Figure, Ground, Label, Pool} from './Primitives';
import type {SceneProps} from './Scenes';

// Episode 2: "seven whom Allah shades on the day there is no shade but His" (Bukhari 660).
// Same 1080 x 1920 stage as Scenes.tsx: centre x 540, ground at y 860.
const G = 860;
const cueAt = (cue: Record<string, number>, k: string, f: number, len = 14) => (cue[k] !== undefined ? ramp(f, cue[k], cue[k] + len) : 0);

// 1. a scorching crowd; seven of them stand in a cool shade; then an empty place: "maybe you are one of them"
export const ShadeCrowd: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, a <= 3 ? 0 : 8, 12);
  const seven = cue.seven !== undefined ? ramp(f, cue.seven, cue.seven + 24) : (a <= 3 ? 0.35 + 0.65 * ramp(f, a, a + 40) : 0);
  const you = cueAt(cue, 'you', f, 16);
  const heat = 0.8 + 0.2 * pulse(f, 46);
  const crowd = [];
  for (let i = 0; i < 26; i++) {
    const x = 250 + i * 22.5 + (rnd(i, 3) - 0.5) * 10;
    const inShade = i >= 9 && i <= 15;
    const s = 0.55 + 0.12 * rnd(i, 7);
    crowd.push(<Figure key={i} x={x} y={G - 2 * rnd(i, 5)} s={s} pose={inShade ? 'stand' : 'bow'} dir={i % 2 ? 1 : -1}
      color={inShade && seven > 0.5 ? '#f3e2b8' : C.line}
      o={inShade ? 0.55 + 0.45 * seven : (0.5 + 0.2 * rnd(i, 2)) * (1 - 0.45 * seven)} />);
  }
  const sx = 540;
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 330} r={520} o={0.55 * heat} kind="red" />
      <circle cx={540} cy={G - 360} r={46} fill="none" stroke={C.red} strokeWidth={3} opacity={0.75 * heat} filter="url(#glowRed)" />
      <Ground y={G} x0={220} x1={860} />
      {/* the shade: a cool, gently lit dome over the seven */}
      <path d={`M ${sx - 95} ${G} Q ${sx - 95} ${G - 170} ${sx} ${G - 175} Q ${sx + 95} ${G - 170} ${sx + 95} ${G}`}
        fill="rgba(120,170,220,0.10)" stroke={C.gold} strokeWidth={2.4} opacity={seven} filter="url(#glowGold)" />
      <Pool x={sx} y={G - 70} r={200} o={0.55 * seven} kind="gold" />
      {crowd}
      {/* an empty place, dashed, with a question mark */}
      <g opacity={you}>
        <circle cx={sx + 155} cy={G - 120} r={34} fill="none" stroke={C.gold} strokeWidth={2} strokeDasharray="6 7" opacity={0.6 + 0.4 * pulse(f, 40)} />
        <Label x={sx + 155} y={G - 106} t="؟" size={40} color={C.gold} weight={800} />
      </g>
    </g>
  );
};

// the seven icons, drawn around (0,0) at about 200 px
const Icon: React.FC<{k: number; f: number; c: string}> = ({k, f, c}) => {
  const st = {stroke: c, strokeWidth: 4, fill: 'none', strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  switch (k) {
    case 0: { // the just ruler: a balance, level
      const sway = Math.sin(f / 22) * 2;
      return (<g {...st}>
        <path d="M 0 -70 L 0 60 M -40 60 L 40 60 M -70 -50 L 70 -50" transform={`rotate(${sway} 0 -50)`} />
        <path d="M -70 -50 L -92 0 L -48 0 Z M 70 -50 L 48 0 L 92 0 Z" />
        <circle cx={0} cy={-76} r={6} fill={c} />
      </g>);
    }
    case 1: // a young man who grew up worshipping: a figure bowing in prayer
      return <g transform="translate(0 70)"><Figure x={0} y={0} s={1.5} pose="bow" color={c} /></g>;
    case 2: // a heart attached to the mosques: an arch with a heart hanging inside
      return (<g {...st}>
        <path d="M -70 70 L -70 -20 Q -70 -90 0 -95 Q 70 -90 70 -20 L 70 70" />
        <path d="M 0 -95 L 0 -40" strokeWidth={2.5} />
        <path d="M 0 0 C -10 -14 -32 -12 -32 -28 C -32 -42 -14 -48 0 -34 C 14 -48 32 -42 32 -28 C 32 -12 10 -14 0 0 Z" fill={c} fillOpacity={0.25}
          transform={`translate(0 ${2 * Math.sin(f / 15)})`} />
      </g>);
    case 3: // two who love each other for Allah: two figures, one light between them
      return (<g transform="translate(0 70)">
        <Figure x={-38} y={0} s={1.35} color={c} /><Figure x={38} y={0} s={1.35} color={c} dir={-1} />
        <circle cx={0} cy={-150} r={9} fill={C.gold} filter="url(#glowGold)" />
      </g>);
    case 4: // "I fear Allah": a man walking away from a red-lit door
      return (<g transform="translate(0 70)">
        <path d="M -95 0 L -95 -120 L -35 -120 L -35 0" stroke={C.red} strokeWidth={3} fill="rgba(229,87,78,0.10)" filter="url(#glowRed)" />
        <Figure x={40} y={0} s={1.35} pose="walk" phase={f / 7} color={c} />
      </g>);
    case 5: { // charity given in secret: a coin dropping through a slot, the left side dark
      const t = (f % 60) / 60;
      return (<g {...st}>
        <rect x={-60} y={10} width={120} height={60} rx={8} />
        <path d="M -18 10 L 18 10" strokeWidth={6} />
        <circle cx={0} cy={-80 + 85 * t} r={14} fill={c} fillOpacity={0.3} opacity={t < 0.95 ? 1 : 0} />
        <path d="M -95 -90 L -95 75" stroke={C.lineDim} strokeWidth={2} strokeDasharray="5 7" />
      </g>);
    }
    default: // remembered Allah alone and his eyes overflowed: a lone figure, a tear of light
      return (<g transform="translate(0 70)">
        <Figure x={0} y={0} s={1.5} pose="bow" color={c} />
        <path d={`M 22 ${-118 + (f % 50) * 0.6} q 5 9 0 13 q -5 -4 0 -13 Z`} fill={C.gold} filter="url(#glowGold)" opacity={0.9} />
      </g>);
  }
};

export const SEVEN_LABELS = ['الإمام العادل', 'شاب نشأ في عبادة ربه', 'قلبه معلق بالمساجد', 'تحابا في الله', 'إني أخاف الله', 'صدقة في السر', 'ذكر الله خاليًا'];

// 2. the hadith: each of the seven appears big in the centre on its cue, a row of seven lights fills below
export const SevenIcons: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 12);
  const at = Array.from({length: 7}, (_, i) => cue['k' + (i + 1)]);
    const rowY = G + 40, x0 = 540 - 3 * 64;
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 160} r={300} o={0.35} kind="gold" />
      {at.map((t, i) => {
        if (t === undefined) return null;
        const next = at[i + 1] ?? b;
        const v = Math.min(ramp(f, t, t + 10), 1 - ramp(f, next - 4, next + 6));
        if (v <= 0) return null;
        return (<g key={i} opacity={v} transform={`translate(540 ${G - 150}) scale(${1.45 + 0.1 * v})`}>
          <Icon k={i} f={f - t} c={'#f3e2b8'} />
        </g>);
      })}
      {at.map((t, i) => {
        const on = t !== undefined ? ramp(f, t, t + 12) : 0;
        return (<g key={'d' + i}>
          <circle cx={x0 + i * 64} cy={rowY} r={11} fill="none" stroke={C.lineDim} strokeWidth={2} />
          <circle cx={x0 + i * 64} cy={rowY} r={11} fill={C.gold} opacity={on} filter="url(#glowGold)" />
        </g>);
      })}
    </g>
  );
};

// 3. "not for his looks, not for how many know him... mostly things no one sees but Allah"
export const Unseen: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 12);
  const crowdGone = cueAt(cue, 'gone', f, 24);
  const lights = ['tear', 'coin', 'heart'].map((k) => cueAt(cue, k, f, 12));
  const fans = [];
  for (let i = 0; i < 18; i++) {
    const x = 270 + i * 31 + (rnd(i, 4) - 0.5) * 12;
    if (Math.abs(x - 540) < 40) continue;
    fans.push(<Figure key={i} x={x} y={G} s={0.62 + 0.1 * rnd(i, 8)} color={C.line} dir={x < 540 ? 1 : -1}
      o={(0.45 + 0.25 * rnd(i, 1)) * (1 - crowdGone)} />);
  }
  const pts = [[440, G - 190], [540, G - 230], [640, G - 190]];
  return (
    <g opacity={o}>
      <Ground y={G} x0={250} x1={830} o={0.7} />
      {fans}
      <Pool x={540} y={G - 80} r={170 + 120 * crowdGone} o={0.15 + 0.4 * crowdGone} kind="gold" />
      <Figure x={540} y={G} s={1.1} color={crowdGone > 0.5 ? '#f3e2b8' : C.line} />
      {pts.map(([x, y], i) => (lights[i] > 0 ? (
        <g key={i} opacity={lights[i]}>
          <line x1={540} y1={G - 60} x2={x} y2={y} stroke={C.gold} strokeWidth={1.4} opacity={0.35} {...draw(lights[i])} />
          <circle cx={x} cy={y} r={7 + 3 * lights[i]} fill={C.gold} filter="url(#glowGold)" />
        </g>) : null))}
    </g>
  );
};

// 4. "and you? which of the seven can you start tonight?": seven lit places and an eighth, empty, that fills on "choose"
export const EighthPlace: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 10, 0);
  const fill = cueAt(cue, 'choose', f, 30);
  const xs = Array.from({length: 8}, (_, i) => 540 - 3.5 * 74 + i * 74);
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 60} r={360} o={0.3 + 0.3 * fill} kind="gold" />
      <Ground y={G} x0={230} x1={850} o={0.6} />
      {xs.map((x, i) => {
        const last = i === 7;
        const show = ramp(f, a + i * 4, a + 14 + i * 4);
        return (<g key={i} opacity={show}>
          <Figure x={x} y={G} s={0.82} color={last ? (fill > 0.5 ? '#f3e2b8' : C.lineDim) : '#f3e2b8'} o={last ? 0.5 + 0.5 * fill : 0.9} />
          {last && fill < 0.98 && <Label x={x} y={G - 110} t="؟" size={38} color={C.gold} weight={800} o={(1 - fill) * (0.6 + 0.4 * pulse(f, 36))} />}
          {(!last || fill > 0) && <circle cx={x} cy={G - 118} r={6} fill={C.gold} opacity={last ? fill : 0.9} filter="url(#glowGold)" />}
        </g>);
      })}
    </g>
  );
};
