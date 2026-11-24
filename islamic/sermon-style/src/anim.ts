import {Easing, interpolate} from 'remotion';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// 0 -> 1 between frames a and b (eased)
export const ramp = (f: number, a: number, b: number, ease = Easing.bezier(0.33, 0, 0.2, 1)) =>
  b <= a ? (f >= a ? 1 : 0) : interpolate(f, [a, b], [0, 1], {...clamp, easing: ease});

// fade in at a (over inF), fade out at b (over outF)
export const life = (f: number, a: number, b: number, inF = 10, outF = 10) =>
  Math.min(ramp(f, a, a + inF), 1 - ramp(f, b - outF, b));

// smooth pulse 0..1 with period p frames
export const pulse = (f: number, p = 90, phase = 0) => 0.5 - 0.5 * Math.cos(((f + phase) / p) * Math.PI * 2);

// deterministic pseudo-random in [0,1)
export const rnd = (i: number, salt = 1) => {
  const x = Math.sin(i * 127.1 * salt + 311.7 * salt) * 43758.5453;
  return x - Math.floor(x);
};

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

// stroke-dash "drawing" props for a path with pathLength=1
export const draw = (p: number) => ({pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - Math.max(0, Math.min(1, p))});
