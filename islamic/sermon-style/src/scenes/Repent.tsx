import React from 'react';
import {C} from '../theme';
import {draw, lerp, life, pulse, ramp, rnd} from '../anim';
import {Figure, Ground, Label, Orb, Pool} from './Primitives';
import type {SceneProps} from './Scenes';

// Long video 01: the man who killed ninety-nine (Bukhari 3470, Muslim 2766) and the mother among the captives
// (Bukhari 5999, Muslim 2754). Same 1080 x 1920 stage: centre x 540, ground y 860. No prophet, companion or angel
// is drawn: the angels are only soft ambient light, never a figure.
const G = 860;
const WARM = '#f3e2b8';
const cueAt = (cue: Record<string, number>, k: string, f: number, len = 14) => (cue[k] !== undefined ? ramp(f, cue[k], cue[k] + len) : 0);

// ninety-nine dim red marks in an arc behind a figure
const NinetyNine: React.FC<{f: number; o: number; cx?: number; cy?: number; fade?: number; count?: number}> = ({f, o, cx = 540, cy = G - 60, fade = 0, count = 99}) => {
  const pts = [];
  for (let i = 0; i < count; i++) {
    const ring = i % 3, k = Math.floor(i / 3);
    const ang = Math.PI * (0.06 + 0.88 * (k / 32));
    const r = 210 + ring * 48 + rnd(i, 3) * 10;
    const x = cx - Math.cos(ang) * r * 1.25, y = cy - Math.sin(ang) * r;
    pts.push(<circle key={i} cx={x} cy={y} r={3.2 + rnd(i, 5) * 1.6} fill={C.red}
      opacity={o * (1 - fade) * (0.35 + 0.35 * pulse(f, 70, i * 9))} />);
  }
  return <g>{pts}</g>;
};

// 1. hook: ninety-nine marks; "is there repentance for me?"; the first answer is "no"; the second changes everything
export const Hook99: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, a <= 3 ? 0 : 8, 12);
  const marks = a <= 3 ? 0.6 + 0.4 * ramp(f, 0, 40) : ramp(f, a, a + 30);
  const q = cueAt(cue, 'q', f, 12);
  const no = cueAt(cue, 'no', f, 10);
  const two = cueAt(cue, 'two', f, 30);
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 120} r={420} o={0.35 * marks * (1 - two)} kind="red" />
      <Pool x={780} y={G - 120} r={260} o={0.6 * two} kind="gold" />
      <NinetyNine f={f} o={marks} fade={0.6 * two} />
      <Ground y={G} x0={260} x1={820} />
      <Figure x={540} y={G} s={1.15} pose="bow" color={C.line} />
      <g opacity={q * (1 - no)}><Label x={540} y={G - 160} t="؟" size={64} color={C.gold} weight={800} /></g>
      {/* the first door: closed, red */}
      <g opacity={no * (1 - 0.7 * two)}>
        <rect x={250} y={G - 180} width={84} height={180} fill="rgba(229,87,78,0.10)" stroke={C.red} strokeWidth={3} filter="url(#glowRed)" />
      </g>
      {/* the second door: open, gold light spilling */}
      <g opacity={two}>
        <path d={`M 746 ${G} L 746 ${G - 180} L 830 ${G - 180} L 830 ${G}`} stroke={C.gold} strokeWidth={3} fill="rgba(242,190,80,0.16)" filter="url(#glowGold)" />
        <path d={`M 746 ${G} L 690 ${G + 40} L 886 ${G + 40} L 830 ${G}`} fill="rgba(242,190,80,0.10)" />
      </g>
    </g>
  );
};

// 2. "he can't sleep": a man lying under the moon, faint circles (faces) gather; he gets up; one light of regret
export const Sleepless: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 12);
  const faces = cueAt(cue, 'faces', f, 60);
  const people = cueAt(cue, 'people', f, 18);
  const broken = cueAt(cue, 'broken', f, 14);
  const stand = cueAt(cue, 'stand', f, 18);
  const regret = cueAt(cue, 'regret', f, 24);
  const ring = [];
  for (let i = 0; i < 40; i++) {
    const x = 300 + rnd(i, 2) * 480, y = 470 + rnd(i, 9) * 300;
    const on = Math.max(0, Math.min(1, faces * 40 - i));
    ring.push(<circle key={i} cx={x + Math.sin((f + i * 20) / 50) * 6} cy={y} r={14 + rnd(i, 4) * 8} fill="none" stroke={C.lineDim}
      strokeWidth={1.6} opacity={on * (0.25 + 0.3 * pulse(f, 80, i * 13)) * (1 - 0.6 * regret)} />);
  }
  return (
    <g opacity={o}>
      <circle cx={820} cy={430} r={34} fill="none" stroke={C.line} strokeWidth={2.4} opacity={0.6} />
      <circle cx={834} cy={420} r={30} fill="#0c1d20" opacity={0.9} />
      {ring}
      <Ground y={G} x0={240} x1={840} />
      {/* people stepping away from him */}
      {[0, 1, 2, 3].map((i) => (
        <Figure key={i} x={(i < 2 ? 330 - i * 55 : 750 + (i - 2) * 55) + (i < 2 ? -1 : 1) * 40 * people} y={G} s={0.75}
          color={C.lineDim} o={people * (1 - stand * 0.6)} dir={i < 2 ? -1 : 1} pose="walk" phase={f / 9 + i} />
      ))}
      <Figure x={540} y={G} s={1.1} pose="lie" color={C.line} o={1 - stand} />
      <Figure x={540} y={G} s={1.1} pose={stand > 0.99 ? 'stand' : 'bow'} color={regret > 0.5 ? WARM : C.line} o={stand} />
      {broken > 0 && stand < 0.5 && <path d={`M 520 ${G - 32} l 10 -8 l -6 -6 l 12 -8`} stroke={C.red} strokeWidth={2.4} fill="none" opacity={broken} />}
      <Orb x={540} y={G - 56} r={6 + 3 * regret} o={regret} />
    </g>
  );
};

// 3. the monk: a small cell with a lit window; the man walks to the door; "no" — the window dies, the door turns red;
// the count becomes a hundred; the door shuts
export const MonkCell: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 12);
  const walk = ramp(f, a, (cue.knock ?? b) - 6);
  const no = cueAt(cue, 'no', f, 10);
  const hundred = cueAt(cue, 'hundred', f, 20);
  const shut = cueAt(cue, 'shut', f, 10);
  const cx = 700;
  const manX = lerp(300, cx - 70, walk);
  return (
    <g opacity={o}>
      <Pool x={cx} y={G - 120} r={260} o={0.45 * (1 - no)} kind="gold" />
      <Pool x={cx} y={G - 120} r={260} o={0.4 * no} kind="red" />
      <Ground y={G} x0={220} x1={880} />
      <g stroke={C.line} strokeWidth={3} fill="rgba(5,9,13,0.55)" strokeLinejoin="round">
        <path d={`M ${cx - 90} ${G} L ${cx - 90} ${G - 170} L ${cx} ${G - 240} L ${cx + 90} ${G - 170} L ${cx + 90} ${G} Z`} />
      </g>
      <rect x={cx + 28} y={G - 160} width={36} height={40} fill={C.gold} opacity={0.75 * (1 - no)} filter="url(#glowGold)" />
      <rect x={cx + 28} y={G - 160} width={36} height={40} fill="none" stroke={C.line} strokeWidth={2} />
      <rect x={cx - 52} y={G - 120} width={56} height={120} fill={no > 0 ? 'rgba(229,87,78,0.14)' : 'rgba(242,190,80,0.08)'}
        stroke={no > 0 ? C.red : C.line} strokeWidth={2.6} filter={no > 0 ? 'url(#glowRed)' : undefined} />
      {shut > 0 && <path d={`M ${cx - 60} ${G - 60} L ${cx + 10} ${G - 60}`} stroke={C.red} strokeWidth={5} opacity={shut} />}
      <Figure x={manX} y={G} s={1.0} pose={walk < 1 ? 'walk' : 'stand'} phase={f / 7} color={C.line} />
      <g opacity={hundred}>
        <NinetyNine f={f} o={0.8} cx={480} cy={G - 40} count={100} />
      </g>
    </g>
  );
};

// 4. despair: a man sits under a locked door; he refuses to give up and stands
export const Despair: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 12);
  const refuse = cueAt(cue, 'refuse', f, 20);
  const ask = cueAt(cue, 'ask', f, 20);
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 120} r={300} o={0.25 + 0.3 * refuse} kind={refuse > 0.5 ? 'gold' : 'cool'} />
      <Ground y={G} x0={260} x1={820} />
      <rect x={600} y={G - 190} width={90} height={190} fill="rgba(5,9,13,0.6)" stroke={C.lineDim} strokeWidth={3} />
      <g stroke={C.lineDim} strokeWidth={3} fill="none" opacity={1 - refuse}>
        <rect x={630} y={G - 100} width={30} height={24} rx={3} />
        <path d={`M 636 ${G - 100} q 9 -22 18 0`} />
      </g>
      <Figure x={520} y={G} s={1.05} pose={refuse > 0.6 ? 'stand' : 'bow'} color={refuse > 0.6 ? WARM : C.line} />
      <Orb x={520} y={G - 140} r={7} o={refuse} />
      <g opacity={ask}><Label x={420} y={G - 200} t="؟" size={54} color={C.gold} weight={800} /></g>
    </g>
  );
};

// 5. the scholar: an open door, warm light floods out on "yes"; a path to another land; three lights (regret, leave, change)
export const ScholarDoor: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 12);
  const yes = cueAt(cue, 'yes', f, 30);
  const go = cueAt(cue, 'go', f, 40);
  const r = ['r1', 'r2', 'r3'].map((k) => cueAt(cue, k, f, 12));
  const dx = 640;
  const openW = 70 * yes;
  return (
    <g opacity={o}>
      <Pool x={dx} y={G - 100} r={220 + 260 * yes} o={0.3 + 0.5 * yes} kind="gold" />
      <Ground y={G} x0={220} x1={900} />
      <path d={`M ${dx - 50} ${G} L ${dx - 50} ${G - 190} L ${dx + 50} ${G - 190} L ${dx + 50} ${G}`} stroke={C.line} strokeWidth={3}
        fill="rgba(242,190,80,0.10)" />
      <rect x={dx - 46} y={G - 186} width={92 - openW} height={186} fill="rgba(5,9,13,0.85)" stroke={C.lineDim} strokeWidth={2} />
      <path d={`M ${dx - 50} ${G} L ${dx - 160} ${G + 60} L ${dx + 160} ${G + 60} L ${dx + 50} ${G}`} fill="rgba(242,190,80,0.12)" opacity={yes} />
      <Figure x={460} y={G} s={1.05} color={yes > 0.5 ? WARM : C.line} />
      {/* the other land, far away, people bowing in worship */}
      <g opacity={go}>
        <path d={`M 120 ${G - 340} L 960 ${G - 340}`} stroke={C.lineDim} strokeWidth={1.6} strokeDasharray="6 10" {...draw(go)} />
        {[0, 1, 2, 3, 4].map((i) => <Figure key={i} x={830 + i * 34} y={G - 345} s={0.42} pose="bow" color={WARM} />)}
        <Pool x={900} y={G - 380} r={130} o={0.6} kind="gold" />
      </g>
      {r.map((v, i) => <Orb key={i} x={400 + i * 140} y={G - 470} r={8} o={v} />)}
    </g>
  );
};

// 6. "what is your land today?": a group, a phone, a night habit; heavy (red) when you go to them, lighter when you leave;
// "get up and go"; rights returned
export const YourLand: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 12);
  const g1 = cueAt(cue, 'group', f), g2 = cueAt(cue, 'phone', f), g3 = cueAt(cue, 'habit', f);
  const heavy = cueAt(cue, 'heavy', f, 18);
  const rise = cueAt(cue, 'rise', f, 30);
  const rights = cueAt(cue, 'rights', f, 20);
  const col = heavy > 0.5 && rise < 0.5 ? C.red : C.line;
  const away = 120 * rise;
  return (
    <g opacity={o * (1 - 0.85 * rights)}>
      <Ground y={G} x0={220} x1={860} />
      <g opacity={g1} transform={`translate(${-away} 0)`}>
        {[0, 1, 2].map((i) => <Figure key={i} x={300 + i * 38} y={G} s={0.8} color={col} dir={-1} />)}
      </g>
      <g opacity={g2} transform={`translate(0 ${-away * 0.3})`} stroke={col} strokeWidth={3} fill="none">
        <rect x={510} y={G - 300} width={64} height={116} rx={10} />
        <circle cx={542} cy={G - 200} r={4} fill={col} />
        <rect x={520} y={G - 288} width={44} height={76} fill={col} fillOpacity={0.12} stroke="none" />
      </g>
      <g opacity={g3} transform={`translate(${away} 0)`} stroke={col} strokeWidth={3} fill="none">
        <circle cx={770} cy={G - 240} r={30} />
        <circle cx={782} cy={G - 250} r={26} fill="#0c1d20" stroke="none" />
      </g>
      <Figure x={540 + 40 * rise} y={G} s={1.05} pose={rise > 0 && rise < 1 ? 'walk' : 'stand'} phase={f / 7}
        color={rise > 0.5 ? WARM : C.line} o={1} />
      <Pool x={540} y={G - 100} r={240} o={0.15 + 0.35 * rise} kind={heavy > 0.5 && rise < 0.5 ? 'red' : 'gold'} />
    </g>
  );
};

// 6b. rights of people: a balance with two sides that come level
export const Rights: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 12);
  const level = cueAt(cue, 'level', f, 40);
  const tilt = 14 * (1 - level);
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 200} r={280} o={0.35} kind="gold" />
      <g stroke={WARM} strokeWidth={4} fill="none" strokeLinecap="round" transform={`translate(540 ${G - 200}) scale(1.6)`}>
        <path d="M 0 -70 L 0 80 M -50 80 L 50 80" />
        <g transform={`rotate(${tilt} 0 -50)`}>
          <path d="M -80 -50 L 80 -50" />
          <path d="M -80 -50 L -104 0 L -56 0 Z M 80 -50 L 56 0 L 104 0 Z" />
        </g>
        <circle cx={0} cy={-76} r={6} fill={WARM} />
      </g>
    </g>
  );
};

// 7. the road: a long road under the sun and dust; a voice says "go back"; death in the middle of the road;
// he leans his chest toward the good land
export const Road: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 14);
  const death = cue.death ?? b;
  const walk = ramp(f, a, death, (t: number) => t);
  const back = cueAt(cue, 'back', f, 16) * (1 - cueAt(cue, 'nogo', f, 16));
  const fall = cueAt(cue, 'death', f, 24);
  const lean = cueAt(cue, 'lean', f, 30);
  const x = lerp(170, 560, walk);
  const dust = [];
  for (let i = 0; i < 22; i++) {
    const t = ((f - a) * (0.5 + rnd(i, 2) * 0.6) + rnd(i, 4) * 200) % 200;
    dust.push(<circle key={i} cx={980 - t * 4.4} cy={G - 20 - rnd(i, 6) * 90 - Math.sin((f + i * 30) / 30) * 6} r={1.4 + rnd(i, 3) * 1.4}
      fill={C.dust} opacity={0.35 * (1 - fall * 0.7)} />);
  }
  return (
    <g opacity={o}>
      <circle cx={540} cy={G - 420} r={48} fill="none" stroke={C.gold} strokeWidth={2.6} opacity={0.55 * (1 - fall)} filter="url(#glowGold)" />
      <Pool x={540} y={G - 400} r={380} o={0.3 * (1 - fall)} kind="gold" />
      <path d={`M 80 ${G} L 1000 ${G}`} stroke={C.ground} strokeWidth={2.4} />
      {/* the good land, far right */}
      <g opacity={0.5 + 0.5 * lean}>
        {[0, 1, 2].map((i) => <Figure key={i} x={900 + i * 30} y={G} s={0.45} pose="bow" color={WARM} />)}
        <Pool x={930} y={G - 30} r={120} o={0.4 + 0.5 * lean} kind="gold" />
      </g>
      {dust}
      {/* a red shadow behind him: "go back" */}
      <Figure x={x - 70} y={G} s={0.95} color={C.red} o={0.5 * back} dir={-1} />
      <Figure x={x} y={G} s={1.0} pose={fall > 0.5 ? 'lie' : 'walk'} phase={f / 8} color={lean > 0.5 ? WARM : C.line} o={1} />
      <Orb x={x + 30} y={G - 14} r={5 + 3 * lean} o={lean} />
      {lean > 0 && <path d={`M ${x + 40} ${G - 14} L ${x + 40 + 280 * lean} ${G - 14}`} stroke={C.gold} strokeWidth={1.6} strokeDasharray="4 8" opacity={0.6 * lean} />}
    </g>
  );
};

// 8. the measure: he lies between two lands; soft light gathers above (never a figure); dashed measuring lines;
// the good land comes closer, the other moves away; one span; forgiven
export const Measure: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 12, 14);
  const lights = cueAt(cue, 'lights', f, 40);
  const measure = cueAt(cue, 'measure', f, 30);
  const move = cueAt(cue, 'move', f, 70);
  const span = cueAt(cue, 'span', f, 16);
  const forgive = cueAt(cue, 'forgive', f, 50);
  const goodX = lerp(900, 760, move), badX = lerp(180, 90, move);
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 380} r={420} o={0.35 * lights + 0.5 * forgive} kind="gold" />
      <Pool x={540} y={G - 380} r={300} o={0.25 * lights * (1 - forgive)} kind="cool" />
      {Array.from({length: 14}).map((_, i) => (
        <circle key={i} cx={360 + rnd(i, 3) * 360} cy={G - 420 + rnd(i, 7) * 160 + Math.sin((f + i * 25) / 40) * 8}
          r={2 + rnd(i, 5) * 2} fill={i % 2 ? '#dfe9ff' : C.gold} opacity={lights * (0.3 + 0.4 * pulse(f, 70, i * 11))} />
      ))}
      <path d={`M 40 ${G} L 1040 ${G}`} stroke={C.ground} strokeWidth={2.2} />
      {/* the evil land (left) and the good land (right) */}
      <g transform={`translate(${badX - 180} 0)`} opacity={0.8 - 0.4 * move}>
        <rect x={130} y={G - 90} width={110} height={90} fill="rgba(229,87,78,0.08)" stroke={C.red} strokeWidth={2} opacity={0.7} />
      </g>
      <g transform={`translate(${goodX - 900} 0)`}>
        <rect x={840} y={G - 90} width={110} height={90} fill="rgba(242,190,80,0.12)" stroke={C.gold} strokeWidth={2.4} filter="url(#glowGold)" />
        <Pool x={895} y={G - 50} r={140} o={0.5} kind="gold" />
      </g>
      <Figure x={540} y={G} s={0.95} pose="lie" color={forgive > 0.3 ? WARM : C.line} />
      {/* measuring lines */}
      <g opacity={measure}>
        <path d={`M 500 ${G + 36} L ${badX + 60} ${G + 36}`} stroke={C.lineDim} strokeWidth={2} strokeDasharray="6 8" {...draw(measure)} />
        <path d={`M 580 ${G + 36} L ${goodX - 60} ${G + 36}`} stroke={C.gold} strokeWidth={2} strokeDasharray="6 8" {...draw(measure)} />
      </g>
      {span > 0 && (
        <g opacity={span}>
          <path d={`M 586 ${G + 58} L 586 ${G + 74} L 626 ${G + 74} L 626 ${G + 58}`} stroke={C.gold} strokeWidth={3} fill="none" filter="url(#glowGold)" />
        </g>
      )}
    </g>
  );
};

// 9. one span: a single slow light in the silence; the ground bends toward one sincere man
export const OneLight: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 30, 14);
  const bend = cueAt(cue, 'earth', f, 40);
  const hand = cueAt(cue, 'hand', f, 20);
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 220} r={260 + 30 * pulse(f, 120)} o={0.55} kind="gold" />
      <Orb x={540} y={G - 220} r={10 + 2 * pulse(f, 90)} o={1} ring={0.5 + 0.5 * pulse(f, 90)} />
      <path d={`M 200 ${G} Q 540 ${G - 70 * bend} 880 ${G}`} stroke={C.ground} strokeWidth={2.4} fill="none" />
      <g opacity={hand}>
        <path d={`M 500 ${G - 120} L 580 ${G - 120}`} stroke={C.gold} strokeWidth={3} />
        <path d={`M 500 ${G - 132} L 500 ${G - 108} M 580 ${G - 132} L 580 ${G - 108}`} stroke={C.gold} strokeWidth={3} />
      </g>
    </g>
  );
};

// 10. the mother (abstract, faceless): small lights scattered among the captives; she goes from one to another;
// she finds her own child; then mercy fills the whole sky
export const Mother: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 14, 14);
  const found = cueAt(cue, 'found', f, 24);
  const mercy = cueAt(cue, 'mercy', f, 70);
  const kids = [[300, G], [420, G], [690, G], [820, G], [560, G]];
  const seek = ((f - a) / 110) % 4;
  const k0 = kids[Math.floor(seek)], k1 = kids[Math.floor(seek) + 1];
  const tt = seek - Math.floor(seek);
  const mx = found > 0 ? lerp(lerp(k0[0], k1[0], tt), 560, found) : lerp(k0[0], k1[0], tt);
  const sky = [];
  for (let i = 0; i < 60; i++) {
    sky.push(<circle key={i} cx={60 + rnd(i, 2) * 960} cy={280 + rnd(i, 8) * 520} r={1.6 + rnd(i, 4) * 2.4} fill={C.gold}
      opacity={mercy * (0.3 + 0.6 * pulse(f, 90, i * 17))} />);
  }
  return (
    <g opacity={o}>
      <Pool x={540} y={G - 300} r={300 + 500 * mercy} o={0.25 + 0.5 * mercy} kind="gold" />
      {sky}
      <Ground y={G} x0={200} x1={880} />
      {kids.map(([x], i) => (
        <g key={i} opacity={i === 4 ? 1 : 1 - 0.6 * found}>
          <Figure x={x} y={G} s={0.42} color={i === 4 && found > 0.5 ? WARM : C.lineDim} />
          <circle cx={x} cy={G - 50} r={4} fill={C.gold} opacity={0.5} filter="url(#glowGold)" />
        </g>
      ))}
      <Figure x={mx} y={G} s={1.0} pose={found > 0.5 ? 'bow' : 'walk'} phase={f / 7} color={found > 0.5 ? WARM : C.line} />
      <Pool x={560} y={G - 50} r={120} o={0.7 * found} kind="gold" />
    </g>
  );
};

// 11. close: footsteps of light on a path; "O Lord, and return"; death without warning (the light dims);
// the door of repentance is open — now
export const StepsClose: React.FC<SceneProps> = ({f, a, b, cue}) => {
  const o = life(f, a, b, 14, 20);
  const step = cueAt(cue, 'step', f, 20);
  const words = cueAt(cue, 'words', f, 20);
  const pray = cueAt(cue, 'pray', f, 24);
  const dim = cueAt(cue, 'death', f, 20) * (1 - cueAt(cue, 'open', f, 30));
  const open = cueAt(cue, 'open', f, 40);
  const now = cueAt(cue, 'now', f, 30);
  const dx = 840;
  return (
    <g opacity={o}>
      <Pool x={dx} y={G - 110} r={200 + 300 * open + 120 * now} o={(0.3 + 0.5 * open) * (1 - 0.6 * dim)} kind="gold" />
      <Ground y={G} x0={160} x1={940} />
      <path d={`M ${dx - 48} ${G} L ${dx - 48} ${G - 190} L ${dx + 48} ${G - 190} L ${dx + 48} ${G}`} stroke={C.gold} strokeWidth={3}
        fill="rgba(242,190,80,0.14)" filter="url(#glowGold)" />
      <rect x={dx - 44} y={G - 186} width={88 * (1 - open)} height={186} fill="rgba(5,9,13,0.8)" />
      {Array.from({length: 6}).map((_, i) => (
        <ellipse key={i} cx={260 + i * 85} cy={G + 22} rx={22} ry={6} fill={C.gold}
          opacity={(i === 0 ? step : ramp(f, (cue.step ?? a) + 30 + i * 30, (cue.step ?? a) + 50 + i * 30)) * 0.8} filter="url(#glowGold)" />
      ))}
      <g opacity={words}>
        <path d={`M 360 ${G - 230} L 520 ${G - 230}`} stroke={C.red} strokeWidth={3} strokeDasharray="10 8" opacity={0.6} />
      </g>
      <Figure x={240} y={G} s={1.0} pose={pray > 0.5 && open < 0.5 ? 'bow' : 'stand'} color={pray > 0.5 ? WARM : C.line} o={1 - 0.4 * dim} />
      <Orb x={240} y={G - 140} r={6} o={pray * (1 - 0.7 * dim)} />
    </g>
  );
};
