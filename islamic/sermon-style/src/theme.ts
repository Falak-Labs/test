// Palette and layout measured from the reference video (see analysis): dark slate radial background, cool-white
// line art, gold for mercy/light/key words, red for sin/loss. Everything else is derived from these.
export const C = {
  bgCenter: '#18212d',
  bgMid: '#111a24',
  bgEdge: '#05090d',
  line: '#dce1e7',
  lineDim: 'rgba(220,225,231,0.35)',
  ground: 'rgba(220,225,231,0.28)',
  gold: '#f0c75e',
  goldDeep: '#e2ad3f',
  goldGlow: 'rgba(242,190,80,0.75)',
  red: '#e5574e',
  redGlow: 'rgba(229,87,78,0.7)',
  sub: '#c3cad4',
  muted: '#8c96a3',
  dust: '#c8d3e0',
};

export const FONT = {
  sans: 'Cairo',
  ruqaa: 'Aref Ruqaa',
  naskh: 'Amiri',
};

export type Layout = {
  w: number;
  h: number;
  headY: number; // centre of the headline
  headSize: number;
  subY: number;
  subSize: number;
  stageX: number; // centre of the illustration
  stageY: number;
  groundY: number;
  scale: number; // illustration scale (1 = drawn for the 1080x1920 stage)
};

// 9:16 short: content kept above the bottom 40% (TikTok / Reels / Shorts UI), like the reference
export const VERTICAL: Layout = {
  w: 1080, h: 1920, headY: 245, headSize: 66, subY: 1075, subSize: 40,
  stageX: 540, stageY: 780, groundY: 884, scale: 1.3,
};

// 16:9 long-form YouTube: same drawing, scaled, headline on top, subtitle near the bottom
export const HORIZONTAL: Layout = {
  w: 1920, h: 1080, headY: 128, headSize: 58, subY: 955, subSize: 38,
  stageX: 960, stageY: 585, groundY: 677, scale: 1.15,
};
