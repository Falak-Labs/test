/* main.js (v2): the Yallah Say lesson engine, one file for every dialect (window.SCRIPT.theme picks the look).
   hook -> part 1 (five phrases, with time to think before each answer) -> quiz -> part 2 -> quiz ->
   hard word (parts, whole word, a sentence, its meaning, your turn) -> end card.  Draws any moment t (seconds). */
(function () {
  const TL = window.TL, SC = window.SCRIPT, A = window.A, C = window.C, P = A.P, FPS = 30, WD = SC.word, PH = SC.phrases, L = SC.L, NP = PH.length, PA = SC.theme === 'pa', SN = WD.sent;
  const NS = 'http://www.w3.org/2000/svg';
  const E = id => document.getElementById(id);
  const S = E('stage');
  const clamp = (x, a, b) => Math.min(b == null ? 1 : b, Math.max(a == null ? 0 : a, x));
  const lerp = (a, b, u) => a + (b - a) * u;
  const eo = u => 1 - Math.pow(1 - clamp(u), 3);
  const back = u => { u = clamp(u); const c = 2.2; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
  const pop = (t, t0, d) => t < t0 ? 0 : back((t - t0) / (d || 0.28));
  const hash = x => { const s = Math.sin(x * 127.1) * 43758.5453; return s - Math.floor(s); };
  const r2 = n => Math.round(n * 100) / 100;
  const zoom = (z, cx, cy) => `translate(${r2(cx * (1 - z))},${r2(cy * (1 - z))}) scale(${z.toFixed(4)})`;
  const ps = (x, y, s, r) => `translate(${r2(x)},${r2(y)})${r ? ` rotate(${r2(r)})` : ''} scale(${(s + 0.001).toFixed(3)})`;
  const G = e => typeof e === 'string' ? E(e) : e;
  const show = (e, on) => { e = G(e); if (on) e.removeAttribute('display'); else e.setAttribute('display', 'none'); };
  const tf = (e, s) => G(e).setAttribute('transform', s);
  const op = (e, v) => G(e).setAttribute('opacity', r2(clamp(v)));
  function el(tag, at, par) { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); if (par) par.appendChild(e); return e; }
  function blink(t, seed) {
    const T = 2.9, k = Math.floor((t + seed) / T), t0 = (k + 0.25 + 0.5 * hash(k * 7.13 + seed)) * T - seed, d = t - t0;
    return d < 0 || d > 0.2 ? 1 : d < 0.08 ? 1 - d / 0.08 : (d - 0.08) / 0.12;
  }

  // ---------- timeline: every beat = one spoken clip (or a silent pause), with its script line and word times
  const B = SC.beats.map((b, i) => Object.assign({ i }, b, TL.beats[i])), BI = {}, SH = TL.shots;
  B.forEach(b => {
    BI[b.id] = b; b.len = b.b - b.a; b.w = b.w || []; b.ws = b.w.map(x => b.a + x);
    b.we = b.w.map((x, k) => b.a + (b.e && b.e.length === b.w.length ? b.e[k] : k + 1 < b.w.length ? b.w[k + 1] : b.len));
    b.N = b.shot === 'T' || b.shot === 'K' ? b.p + 1 : b.shot === 'R' ? (b.round + 1) * 5 + .5 : b.shot === 'X' ? -1 : b.shot === 'H' ? NP + 1 : NP + 2;
  });
  SH.forEach((s, k) => { s.j = k + 1 < SH.length ? SH[k + 1].i : B.length; });
  const DING = PH.map((p, k) => B.find(b => b.shot === 'K' && b.p === k).b + 0.08), WIN = BI.w5.b + 0.05, CHEER = BI.v4.a + 0.05;
  const mouthOf = (b, t) => { const x = (t - b.a) * FPS, e = b.env || ''; if (x < 0) return 0; const i = Math.floor(x), p = +(e[i] || 0), q = +(e[i + 1] || 0); return (p + (q - p) * (x - i)) / 9; };
  const beatAt = (sh, t) => { let k = sh.i; for (let i = sh.i + 1; i < sh.j; i++) if (t >= B[i].a - 0.12) k = i; return B[k]; };

  // ---------- the look of each dialect
  const TH = PA
    ? { blue: ['#2E8B57', '#14502F'], gold: ['#E0353F', '#A5111B'], rose: ['#FFFFFF', '#E3DED2'], rose2: ['#F4F1EA', '#D5CFC0'], tint: '#0C2E1A', bgT: '#DDF2E4',
      lant: [[40, 70, .9], [900, 100, .9], [112, 60, .8], [968, 90, .8]], hud: { px: 150, pw: 780, fx: 204, lx: 252, la: 'start', ax: 530, ex: 586, bx: 860 } }
    : { blue: ['#3D63E3', '#1F3A9F'], gold: ['#F9E08A', '#D9A441'], rose: ['#F4BCC3', '#DE8A97'], rose2: ['#E9A0AB', '#CF7788'], tint: '#14306E', bgT: '#DCE6FF',
      lant: [[172, 250, .95], [918, 292, .95], [112, 196, .8], [968, 236, .8]], hud: { px: 270, pw: 540, fx: 318, lx: 496, la: 'end', ax: 512, ex: 566, bx: 762 } };
  const KC = { boy: ['#FFE9B8', P.saffron], girl: ['#CFF3EF', P.teal], boy2: ['#FFE0D6', '#E4572E'], girl2: ['#E8E0FB', '#8B6BD9'], boy3: ['#DCE8FB', '#4F86E0'], girl3: ['#FFE3EA', '#F28BA0'] };
  const KIDS = SC.kids, QK = KIDS.slice(2), WHO = ['T', 'A', 'L'].concat(QK.map((k, i) => 'Q' + i));

  // ---------- stage
  const grad = (id, a, b, x2, y2) => `<linearGradient id="${id}" x1="0" y1="0" x2="${x2 || 0}" y2="${y2 == null ? 1 : y2}"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient>`;
  const rad = (id, a, b) => `<radialGradient id="${id}" cx=".45" cy=".4" r=".65"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></radialGradient>`;
  const defs = `<defs>${grad('gBlue', TH.blue[0], TH.blue[1])}${grad('gGold', TH.gold[0], TH.gold[1])}${grad('gRose', TH.rose[0], TH.rose[1])}${grad('gRose2', TH.rose2[0], TH.rose2[1])}
${grad('gMust', '#F5C25C', '#DB9324')}${grad('gTealK', '#38C6BC', '#17958E')}${grad('gDesk', '#DDA66C', '#B0733C')}${grad('gWoodL', '#C58A4A', '#8A5226', 1, 1)}${grad('gBoardL', '#2A7460', '#184D3E', 1, 1)}
${rad('gSkinT', '#FAD8BA', '#ECB692')}${rad('gSkinK', '#F9D2AC', '#E8AC82')}
<radialGradient id="gGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE9A6" stop-opacity=".8"/><stop offset="1" stop-color="#FFE9A6" stop-opacity="0"/></radialGradient>
<radialGradient id="gLamp" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#FFFBE0"/><stop offset="1" stop-color="#F7AE3B"/></radialGradient>
<clipPath id="cpS"><circle r="95"/></clipPath><clipPath id="cpK"><circle cy="10" r="232"/></clipPath><clipPath id="cpT"><circle cy="34" r="194"/></clipPath>
<clipPath id="cpLg"><circle cx="${TH.hud.px + 50}" cy="194" r="36"/></clipPath>
<filter id="fSh" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#2A1400" flood-opacity=".34"/></filter>
<filter id="fSh2" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#2A1400" flood-opacity=".3"/></filter></defs>`;

  const img = id => `<image id="${id}" width="1080" height="1920" preserveAspectRatio="none"/>`;
  const kb = C.kid('kb', 'boy'), kg = C.kid('kg', 'girl'), hb = C.kid('hb', 'boy'), hg = C.kid('hg', 'girl');
  const s4 = 'M0 -20Q3 -3 20 0Q3 3 0 20Q-3 3 -20 0Q-3 -3 0 -20Z', tick = 'M-11 1L-3 9L12 -8';
  const SPK = [[70, 420, 1.1], [1012, 470, .9], [50, 1160, .8], [1030, 1140, 1.2], [972, 1560, 1], [520, 268, .7], [300, 1580, .8]];
  const pent = (cx, cy, r) => 'M' + [0, 2, 4, 1, 3].map(k => { const a = (k * 72 - 90) * Math.PI / 180; return r2(cx + r * Math.cos(a)) + ' ' + r2(cy + r * Math.sin(a)); }).join('L') + 'Z';
  const star5 = (R, r) => { let p = ''; for (let k = 0; k < 10; k++) { const a = (k * 36 - 90) * Math.PI / 180, q = k % 2 ? r : R; p += (k ? 'L' : 'M') + r2(q * Math.cos(a)) + ' ' + r2(q * Math.sin(a)); } return p + 'Z'; };
  // the round flag used in the top pill and on the dialect tab
  const flagDot = (cx, cy, r, id, lite) => PA
    ? `<clipPath id="${id}"><circle cx="${cx}" cy="${cy}" r="${r}"/></clipPath><g clip-path="url(#${id})">${A.flag(cx - r, cy - r, 2 * r + 4, 2 * r)}</g><circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${lite ? '#fff' : '#ddd'}" stroke-width="${lite ? 3 : 2}"/>`
    : (lite ? '' : `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${P.red}"/>`) + `<path d="${pent(cx, cy + 1, r * (lite ? .8 : .6))}" fill="none" stroke="${lite ? '#7BE0A0' : '#0B7A3E'}" stroke-width="3.6" stroke-linejoin="round"/>`;
  const badge = (id, c, d) => `<g id="${id}"><circle r="30" fill="${c}" stroke="#fff" stroke-width="5"/><path d="${d}" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>`;
  const av = (k, cy, r, bg, col, inner, cp, sw) => `<g id="av${k}"><circle id="ao${k}" cy="${cy}" r="${r + sw / 2 + 7}" fill="#fff"/><circle id="ab${k}" cy="${cy}" r="${r}" fill="${bg}"/><g id="ag${k}" clip-path="url(#${cp})">${inner}</g><circle id="ar${k}" cy="${cy}" r="${r}" fill="none" stroke="${col}" stroke-width="${sw}"/></g>`;
  const kidAv = (key, id, look) => { const k = id === 'hb' ? hb : id === 'hg' ? hg : C.kid(id, look); return av(key, 10, 232, KC[look][0], KC[look][1], k.body + k.head, 'cpK', 16); };
  const AV = { T: 'tB', A: 'hb', L: 'hg' }; QK.forEach((k, i) => { AV['Q' + i] = 'q' + i; });
  const N8 = [0, 1, 2, 3, 4, 5, 6, 7];
  const DW = (NP - 1) * 34 + (NP / 5 - 1) * 20, DX0 = 540 - (DW + 46) / 2, DOTX = k => k < NP ? DX0 + k * 34 + Math.floor(k / 5) * 20 : DX0 + DW + 46;
  // name badge on the pupil's shirt (close-up)
  const nameBadge = (id, name, col) => `<g id="${id}" transform="translate(-92,252) rotate(-5)"><rect x="-62" y="-24" width="124" height="48" rx="12" fill="#FFFDF6" stroke="${col}" stroke-width="5"/><text y="12" font-size="32" text-anchor="middle" fill="#2A1B14">${name}</text></g>`;
  const lan = (n, id) => `<g transform="translate(${TH.lant[n][0]},-8)">${A.lantern(id, TH.lant[n][1], TH.lant[n][2])}</g>`;
  const hd = TH.hud;

  S.innerHTML = defs + `
<g id="sT">${img('pT')}
${lan(0, 'ln1')}${lan(1, 'ln2')}
<g id="bd"><text x="150" y="556" font-size="44" fill="#FFD45C" opacity=".85">ABC</text>
<text id="bdn" x="612" y="556" font-size="40" text-anchor="end" fill="#FDFBF3" opacity=".8"></text>
<path id="bdu" d="M214 790Q262 766 310 790T406 790T502 790T550 784" pathLength="100" stroke-dasharray="100" fill="none" stroke="#FFD45C" stroke-width="7" stroke-linecap="round" opacity=".9"/></g>
<g id="tW" transform="translate(770,628)">${C.teacher('tT')}</g></g>
<g id="sK">${img('pKb')}${img('pKg')}
<g id="kW" transform="translate(540,650) scale(1.12)">${kb.body}${nameBadge('nbA', KIDS[0].name, '#B97A14')}${kg.body}${nameBadge('nbL', KIDS[1].name, '#12807A')}
<g id="desk"><path d="M-640 388H640V1400H-640Z" fill="url(#gDesk)"/><rect x="-640" y="388" width="1280" height="12" fill="#fff" opacity=".3"/>
<path d="M-640 540Q-220 520 180 544T640 530M-640 700Q-120 716 280 694T640 708" fill="none" stroke="#8E5A2B" stroke-width="3" opacity=".22"/>
<path d="M-640 900H640V1400H-640Z" fill="#8F5A2A"/><rect x="-640" y="892" width="1280" height="10" fill="#EBC592" opacity=".55"/>
<g transform="rotate(-10 -330 800)"><rect x="-372" y="780" width="84" height="42" rx="9" fill="#F28BA0"/><rect x="-372" y="780" width="30" height="42" rx="9" fill="#5E8BE0"/></g>
<g transform="translate(330,800)"><rect x="-70" y="-16" width="150" height="15" rx="7" fill="#E4572E" transform="rotate(-14)"/><rect x="-70" y="6" width="150" height="15" rx="7" fill="#1FA79E" transform="rotate(-4)"/><rect x="-70" y="28" width="150" height="15" rx="7" fill="#7B5CD6" transform="rotate(7)"/></g>
<ellipse cx="0" cy="476" rx="330" ry="30" fill="#5A3210" opacity=".16"/>
<path d="M-196 400H164L206 478H-238Z" fill="#FFFDF6"/><path d="M-16 400V478" stroke="#D8CFC0" stroke-width="4"/>
<path d="M-170 418H-42M-178 436H-42M-186 454H-42M10 418H150M10 436H162M10 454H174" stroke="#B9C4D6" stroke-width="3.5" stroke-linecap="round"/></g>
${kb.arms}${kg.arms}${kb.head}${kg.head}</g>
<g id="stk"><circle cx="-116" cy="96" r="16" fill="#fff"/><circle cx="-152" cy="132" r="9" fill="#fff"/>
<g filter="url(#fSh2)">${PH.map((p, i) => `<g id="ic${i}">${A.stk3(p.icon)}</g>`).join('')}</g></g>
<g id="brs">${N8.map(i => `<path id="br${i}" d="${s4}" fill="${i % 2 ? '#fff' : '#FFD23F'}"/>`).join('')}</g></g>
<g id="sH">${img('pH')}<rect y="1060" width="1080" height="860" fill="${TH.tint}" opacity=".3"/>${A.bigBoard(80, 446, 920, 392)}<g id="wbd"></g></g>
<g id="sB">${img('pC')}
${lan(2, 'ln3')}${lan(3, 'ln4')}
<g id="spk">${SPK.map((s, i) => `<path id="sp${i}" d="${s4}" fill="${i % 3 ? '#FFE08A' : '#fff'}"/>`).join('')}</g>
<g id="gX"></g><g id="gR"></g><g id="gC"></g></g>
<g id="cast">${QK.map((k, i) => kidAv('Q' + i, 'q' + i, k.look)).join('')}${av('T', 34, 194, TH.bgT, P.red, C.teacher('tB'), 'cpT', 14)}${kidAv('A', 'hb', 'boy')}${kidAv('L', 'hg', 'girl')}</g>
<g id="hud" transform="translate(0,96)"><g filter="url(#fSh2)"><rect x="${hd.px}" y="150" width="${hd.pw}" height="88" rx="44" fill="#FFFDF6"/></g>
<g id="hudM">${flagDot(hd.fx, 194, PA ? 26 : 25, 'cpFl', 0)}
<text x="${hd.lx}" y="208" font-size="40" text-anchor="${hd.la}" fill="${P.red}">${L.lang}</text>
<path d="M${hd.ax} 194H${hd.ax + 36}M${hd.ax + 24} 181L${hd.ax + 38} 194L${hd.ax + 24} 207" fill="none" stroke="${P.ink}" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="${hd.ex}" y="208" font-size="40" fill="${P.cobalt}">English</text>
<circle cx="${hd.bx}" cy="194" r="25" fill="${P.cobalt}"/><text x="${hd.bx}" y="206" font-size="32" text-anchor="middle" fill="#fff">A</text></g>
<g id="hudE"><image id="lg" x="${hd.px + 14}" y="158" width="72" height="72" clip-path="url(#cpLg)" preserveAspectRatio="xMidYMid slice"/>
<circle cx="${hd.px + 50}" cy="194" r="36" fill="none" stroke="#E9DCC3" stroke-width="3"/>
<text x="${hd.px + hd.pw / 2 + 36}" y="208" font-size="40" text-anchor="middle" fill="${P.ink}">${L.handle}</text></g>
<g id="dots">${PH.map((p, i) => `<g id="dt${i}"><circle id="dc${i}" r="11" stroke="#fff" stroke-width="3.5"/><path id="dk${i}" d="${tick}" transform="scale(.52)" fill="none" stroke="#fff" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/></g>`).join('')}
<g id="dt${NP}"><path id="dc${NP}" d="${star5(19, 8.5)}" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></g></g></g>
<g id="card"><g filter="url(#fSh)"><rect x="60" y="1172" width="960" height="330" rx="46" fill="#FFFBF1"/></g>
<g id="tabD"><rect id="tabDr" x="104" y="1136" width="246" height="70" rx="35" fill="${P.red}"/>${flagDot(146, 1172, PA ? 19 : 19, 'cpFt', 1)}
<text id="tabDt" x="176" y="1185" font-size="36" fill="#fff" letter-spacing="2">${L.TAB}</text></g>
<g id="tabE"><rect x="104" y="1136" width="276" height="70" rx="35" fill="${P.cobalt}"/>
<path d="M130 1158H164Q170 1158 170 1164V1180Q170 1186 164 1186H146L136 1196V1186H130Q124 1186 124 1180V1164Q124 1158 130 1158Z" fill="#fff"/>
<text x="272" y="1185" font-size="36" text-anchor="middle" fill="#fff" letter-spacing="2">ENGLISH</text></g>
<g id="tmr"><rect x="290" y="1226" width="500" height="16" rx="8" fill="#EADBC0"/><rect id="tmf" x="290" y="1226" width="500" height="16" rx="8" fill="#F2B134"/></g>
<g id="thk"></g></g>
<g id="names"></g>
<g id="cft"></g>
<rect id="fl" width="1080" height="1920" fill="#fff" opacity="0"/>`;

  // ---------- text helpers
  function fit(t, maxW) { const w = t.getComputedTextLength(); if (w > maxW) t.setAttribute('font-size', r2(parseFloat(t.getAttribute('font-size')) * maxW / w)); return t; }
  function arText(par, at, parts) {
    const t = el('text', Object.assign({ 'text-anchor': 'middle', class: 'ar' }, at), par);
    return parts.map((w, k) => { const s = el('tspan', {}, t); s.textContent = w; if (k < parts.length - 1) t.appendChild(document.createTextNode(' ')); return s; });
  }
  const arLine = (par, at, str, maxW) => fit(arText(par, at, str.split(' '))[0].parentNode, maxW);
  // lay out Latin words on one or two centred lines; every word is its own element so it can pop
  const SPC = 0.38;
  function words(par, list, o) {
    const probe = el('text', { 'font-size': o.size }, par);
    const meas = s => list.map(w => { probe.setAttribute('font-size', s); probe.textContent = w; return probe.getComputedTextLength(); });
    const sum = (ws, a, b, sp) => ws.slice(a, b).reduce((x, y) => x + y, 0) + sp * (b - a - 1);
    let size = o.size, ws = meas(size), n = list.length, lines = [[0, n]];
    const one = sum(ws, 0, n, size * SPC);
    if (one > o.maxW) {
      if (size * o.maxW / one >= o.min) size = size * o.maxW / one;
      else {
        let best = null;
        for (let k = 1; k < n; k++) { const m = Math.max(sum(ws, 0, k, size * SPC), sum(ws, k, n, size * SPC)); if (!best || m < best.m) best = { k, m }; }
        if (best.m > o.maxW) size = size * o.maxW / best.m;
        lines = [[0, best.k], [best.k, n]];
      }
      ws = meas(size);
    }
    probe.remove();
    const sp = size * SPC, lh = size * 1.18, items = [];
    items.L = []; items.gh = o.gh == null ? 0.2 : o.gh;
    lines.forEach((ln, li) => {
      const w = sum(ws, ln[0], ln[1], sp), y = o.cy + (li - (lines.length - 1) / 2) * lh + size * 0.36; let x = o.cx - w / 2;
      items.L.push({ x0: x, x1: x + w, y, size });
      for (let i = ln[0]; i < ln[1]; i++) {
        const g = el('g', {}, par);
        const mk = el('rect', { x: r2(-ws[i] / 2 - size * 0.14), y: r2(-size * 0.86), width: r2(ws[i] + size * 0.28), height: r2(size * 1.12), rx: r2(size * 0.24), fill: o.mark, opacity: 0 }, g);
        const tx = el('text', { 'font-size': r2(size), 'text-anchor': 'middle', fill: o.fill, stroke: o.fill, 'stroke-width': r2(size * 0.028), class: 'fat' }, g);
        tx.textContent = list[i];
        items[i] = { g, mk, tx, x: x + ws[i] / 2, y, f: o.fill, k: Math.min(0.17, 22 / ws[i]) };
        x += ws[i] + sp;
      }
    });
    return items;
  }
  // st / en = when each word starts and ends
  function drawWords(items, st, en, t) {
    items.forEach((it, i) => {
      const d = t - st[i] + 0.05, on = clamp(d / 0.07), s = 1 + (d >= 0 ? it.k * Math.exp(-d / 0.11) : 0);
      it.g.setAttribute('transform', `translate(${r2(it.x)},${r2(it.y)}) scale(${s.toFixed(3)})`);
      it.tx.setAttribute('opacity', r2(lerp(items.gh, 1, on)));
      it.mk.setAttribute('opacity', r2(clamp(d / 0.06) * (1 - clamp((t - en[i] - 0.06) / 0.16))));
    });
  }
  const paint = (it, c) => { it.tx.setAttribute('fill', c); it.tx.setAttribute('stroke', c); };

  const TABS = { T: ['TEACHER', P.cobalt], A: [KIDS[0].name.toUpperCase(), '#D98E0F'], L: [KIDS[1].name.toUpperCase(), '#12958D'], AL: ['CLASS', '#7B5CD6'], Y: ['YOUR TURN', '#E4572E'] }, TABK = ['D', 'E', 'T', 'A', 'L', 'AL', 'Y'];
  const TABW = { D: 246, E: 276 }, RPW = [], CAPS = [], TBD = [], SY = [], ROW = [], CF = [], CC = {}, H = {}, XB = [], NM = {}, TQ = [];
  function build() {
    const card = E('card'), INK = { cx: 540, maxW: 800, fill: P.ink, mark: '#FFDA6B' };
    const dt = E('tabDt'); if (dt.getComputedTextLength() > 190) dt.setAttribute('font-size', 31);
    TABW.D = 176 - 104 + dt.getComputedTextLength() + 34; E('tabDr').setAttribute('width', r2(TABW.D));
    for (const k in TABS) {
      const g = el('g', { id: 'tab' + k }, card), r = el('rect', { x: 104, y: 1136, height: 70, rx: 35, fill: TABS[k][1] }, g);
      const tx = el('text', { y: 1185, 'font-size': 36, 'text-anchor': 'middle', fill: '#fff', 'letter-spacing': 2 }, g); tx.textContent = TABS[k][0];
      TABW[k] = tx.getComputedTextLength() + 76; r.setAttribute('width', r2(TABW[k])); tx.setAttribute('x', r2(104 + TABW[k] / 2));
    }
    // the phrase in the dialect stays in sight (top right of the card) while the pupil thinks and answers
    const tr = el('g', { id: 'tabR' }, card); el('rect', { id: 'rpR', y: 1136, height: 70, rx: 35, fill: '#FFF1D6', stroke: P.red, 'stroke-width': 3.5 }, tr);
    PH.forEach((p, k) => { const t = el('text', { id: 'rp' + k, x: 912, y: 1184, 'font-size': 34, 'text-anchor': 'end', fill: P.red }, tr); t.textContent = p.dz.replace(/[.!]$/, ''); RPW[k] = t.getComputedTextLength(); });
    el('g', {}, card).innerHTML = badge('vo', '#2BB673', tick);
    // "think first": a question in the dialect and three question marks, while the timer runs out
    const th = E('thk'); arLine(th, { x: 540, y: 1296, 'font-size': 50, fill: P.red }, L.think, 780);
    [0, 1, 2].forEach(k => { const q = el('text', { 'font-size': 120, 'text-anchor': 'middle', fill: k === 1 ? '#F2B134' : P.cobalt }, th); q.textContent = '?'; TQ.push(q); });

    B.forEach(b => {
      if (b.shot === 'T') { // chalk text on the teacher's board
        const g = el('g', { id: 'bd' + b.i }, E('bd'));
        if (b.board) { // the hook: the word in the dialect, and a question
          b.bd = arText(g, { x: 380, y: 676, 'font-size': 124, fill: '#FFD45C' }, [b.board[0]]); fit(b.bd[0].parentNode, 440);
          b.bq = el('text', { x: 380, y: 808, 'font-size': 92, 'text-anchor': 'middle', fill: '#FDFBF3' }, g); b.bq.textContent = b.board[1]; fit(b.bq, 430);
        } else {
          const ws = b.ar.split(' '), at = (y, x) => ({ x: x || 380, y, 'font-size': 88, fill: '#FDFBF3' });
          if (ws.length > 2) { const h = Math.ceil(ws.length / 2); b.bd = arText(g, at(654, 372), ws.slice(0, h)).concat(arText(g, at(762, 292), ws.slice(h))); b.bd.two = 1; }
          else b.bd = arText(g, at(716), ws);
          g.querySelectorAll('text').forEach((t, n) => fit(t, n ? 300 : 450));     // the second line stays clear of the pointer
        }
        TBD.push(b);
      }
      if ('TKH'.indexOf(b.shot) < 0 || b.fast || (b.sil && b.id !== 'v3')) return;
      const g = el('g', { id: 'cp' + b.i }, card), c = b.cap = {};
      if (b.syl != null) {
        c.big = el('text', { x: 540, y: 1392, 'font-size': 190, 'text-anchor': 'middle', fill: b.sp === 'T' ? P.navy : P.cobalt }, g); c.big.textContent = WD.parts[b.syl];
        el('text', { x: 540, y: 1470, 'font-size': 40, 'text-anchor': 'middle', fill: P.red }, g).textContent = '“' + WD.say[b.syl] + '”';
      } else if (b.dz) {
        const hs = b.shot === 'H' && !b.gl;      // on the hard-word card the pupils' name pills sit along the top edge
        c.W = words(g, b.dz.split(' '), Object.assign({}, INK, b.gl ? { cy: 1258, size: 78, min: 58 } : hs ? { cy: 1300, size: 84, min: 62 } : { cy: 1296, size: 94, min: 60 }));
        if (hs && c.W.L.length > 1) { c.W.forEach(it => it.g.remove()); c.W = words(g, b.dz.split(' '), Object.assign({}, INK, { cy: 1306, size: 68, min: 68 })); }
        if (b.gl && c.W.L.length > 1) { c.W.forEach(it => it.g.remove()); c.W = words(g, b.dz.split(' '), Object.assign({}, INK, { cy: 1266, size: 60, min: 60 })); }
        c.A = arText(g, { x: 540, y: b.gl ? 1410 : 1450, 'font-size': b.gl ? 50 : 60, fill: P.red }, b.ar.split(' ')); fit(c.A[0].parentNode, 780);
        if (b.gl) { const q = el('text', { x: 540, y: 1474, 'font-size': 37, 'text-anchor': 'middle', fill: P.cobalt }, g); q.textContent = '“' + b.gl + '”'; fit(q, 800); }
      } else {
        const turn = b.id === 'v3';
        c.W = words(g, b.en.split(' '), { cx: 540, cy: turn ? 1330 : 1352, maxW: 800, size: 100, min: 84, fill: P.navy, mark: '#FFD23F', gh: b.shot === 'H' ? 0.07 : 0.2 });
        (b.hot || []).forEach(k => paint(c.W[k], '#E4572E'));
        if (turn) arLine(g, { x: 540, y: 1476, 'font-size': 40, fill: P.red }, L.turnAr, 780);
      }
      CAPS.push(b);
    });
    ['T', 'K'].forEach(k => { // the fast round: all five parts in one line
      const g = el('g', { id: 'cpF' + k }, card);
      H['f' + k] = words(g, WD.parts, { cx: 540, cy: 1322, maxW: 800, size: 112, min: 70, fill: k === 'T' ? P.navy : P.cobalt, mark: k === 'T' ? '#FFD23F' : '#8DE3B4' });
      el('text', { x: 540, y: 1464, 'font-size': 40, 'text-anchor': 'middle', fill: P.red }, g).textContent = WD.say.join(' · ');
    });

    // name pills (drawn over the card, so pupils can peek from behind it)
    KIDS.forEach((k, i) => {
      const key = i < 2 ? 'AL'[i] : 'Q' + (i - 2), g = el('g', { id: 'nm' + key, filter: 'url(#fSh2)' }, E('names')), r = el('rect', { y: -19, height: 38, rx: 19, fill: KC[k.look][1], stroke: '#fff', 'stroke-width': 3 }, g);
      const tx = el('text', { y: 9, 'font-size': 25, 'text-anchor': 'middle', fill: '#fff' }, g); tx.textContent = k.name;
      const w = tx.getComputedTextLength() + 30; r.setAttribute('x', r2(-w / 2)); r.setAttribute('width', r2(w)); NM[key] = g;
    });

    // the hard word on the big board
    const wb = E('wbd');
    H.hd = el('g', {}, wb);
    el('text', { x: 116, y: 508, 'font-size': 36, fill: '#FFD45C', 'letter-spacing': 1 }, H.hd).textContent = "TODAY'S HARD WORD";
    arLine(H.hd, { x: 856, y: 510, 'font-size': 40, fill: '#FDFBF3' }, L.hardAr, 250);
    H.qq = el('text', { x: 540, y: 700, 'font-size': 150, 'text-anchor': 'middle', fill: '#FDFBF3' }, wb); H.qq.textContent = '? ? ?';
    H.wo = el('g', {}, wb); H.wd = el('g', {}, H.wo);
    let FS = 83; const probe = el('text', { 'font-size': FS }, wb), pad = 13, gap = 22;
    let ws = WD.parts.map(p => { probe.textContent = p; return probe.getComputedTextLength(); }), W = ws.reduce((a, b) => a + b, 0);
    const room = 860 - 10 * pad - 4 * gap;
    if (W > room) { FS = r2(FS * room / W); probe.setAttribute('font-size', FS); ws = WD.parts.map(p => { probe.textContent = p; return probe.getComputedTextLength(); }); W = ws.reduce((a, b) => a + b, 0); }
    probe.remove();
    let xm = 540 - W / 2, xs = 540 - (W + 10 * pad + 4 * gap) / 2 + pad;
    WD.parts.forEach((p, i) => {
      const g = el('g', {}, H.wd), z = el('g', {}, g), tile = el('rect', { x: -pad, y: r2(-FS * 1.02), width: r2(ws[i] + 2 * pad), height: r2(FS * 1.42), rx: 16, fill: '#fff', stroke: '#FDFBF3', 'stroke-width': 3.5 }, z);
      const tx = el('text', { 'font-size': FS, fill: '#FDFBF3' }, z); tx.textContent = p;
      const h = el('g', {}, g); arLine(h, { x: r2(ws[i] / 2), y: 96, 'font-size': 44, fill: '#FFD45C' }, WD.ah[i], 150);
      el('text', { x: r2(ws[i] / 2), y: 146, 'font-size': 30, 'text-anchor': 'middle', fill: '#FDFBF3', opacity: .8 }, h).textContent = WD.say[i];
      const ck = el('g', {}, g); ck.innerHTML = `<circle r="19" fill="#2BB673" stroke="#fff" stroke-width="4"/><path d="${tick}" transform="scale(.72)" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
      SY[i] = { g, z, tile, tx, h, ck, w: ws[i], xm, xs }; xm += ws[i]; xs += ws[i] + 2 * pad + gap;
    });
    H.mean = arLine(wb, { x: 540, y: 730, 'font-size': 50, fill: '#FFD45C' }, L.meanAr, 600);
    H.rl = el('g', {}, wb); const rx0 = r2(540 - W * 0.61 - 6), rx1 = r2(540 + W * 0.61 + 6);
    H.rp = el('path', { d: `M${rx0} 706H${rx1}`, stroke: '#FFD45C', 'stroke-width': 6, 'stroke-linecap': 'round', pathLength: 100, 'stroke-dasharray': 100 }, H.rl);
    el('path', { d: `M${rx0} 690v32M${rx1} 690v32`, stroke: '#FFD45C', 'stroke-width': 6, 'stroke-linecap': 'round' }, H.rl);
    el('text', { x: 540, y: 772, 'font-size': 44, 'text-anchor': 'middle', fill: '#FFD45C' }, H.rl).textContent = WD.full.length + ' letters!';
    // the word in a sentence, then what the sentence means
    H.sn = el('g', {}, wb);
    H.sW = words(H.sn, SN.en.split(' '), { cx: 540, cy: 632, maxW: 820, size: 70, min: 54, fill: '#FDFBF3', mark: '#FFD45C', gh: 0 });
    (SN.hot || []).forEach(k => paint(H.sW[k], '#FFD45C'));
    H.st = arLine(wb, { x: 540, y: H.sW.L.length > 1 ? 792 : 760, 'font-size': 54, fill: '#FFD45C' }, SN.ar, 820);
    const chip = (c, txt, bolt, w) => { w = w || 224; const g = el('g', { filter: 'url(#fSh2)' }, wb); g.innerHTML = `<rect x="${-w / 2}" y="-30" width="${w}" height="60" rx="30" fill="${c}" stroke="#fff" stroke-width="4"/>${bolt ? '<path d="M-78 -18L-92 4H-80L-86 20L-66 -4H-78Z" fill="#FFD23F"/>' : ''}<text x="${bolt ? 12 : 0}" y="13" font-size="36" text-anchor="middle" fill="#fff" letter-spacing="2">${txt}</text>`; return g; };
    H.cs = chip(P.teal, 'SLOW'); H.cf = chip('#E4572E', 'FAST ×2', 1); H.ci = chip('#7B5CD6', 'IN A SENTENCE', 0, 340); H.cy = chip('#E4572E', 'YOUR TURN!', 0, 290);
    H.rb = el('g', { filter: 'url(#fSh2)' }, wb);
    H.rb.innerHTML = `<path d="M-236 -22L-196 -34V34L-236 22L-218 0ZM236 -22L196 -34V34L236 22L218 0Z" fill="#B5301F"/><rect x="-200" y="-38" width="400" height="76" rx="12" fill="#E4572E"/>
<path d="${star5(15, 6.5)}" transform="translate(-164,0)" fill="#FFD23F"/><path d="${star5(15, 6.5)}" transform="translate(164,0)" fill="#FFD23F"/><text y="17" font-size="48" text-anchor="middle" fill="#fff" letter-spacing="2">GOOD JOB!</text>`;
    const cols = ['#FFD23F', '#E4572E', '#2BB673', '#5E8BE0', '#F28BA0', '#fff'];
    for (let i = 0; i < 46; i++) { const Lf = i % 2 === 0; CF.push({ e: el('rect', { x: -8, y: -12, width: 16, height: 24, rx: 4, fill: cols[i % 6] }, E('cft')), x0: Lf ? 120 : 960, vx: (Lf ? 1 : -1) * (60 + 400 * hash(i + 1)), vy: -(760 + 520 * hash(i + 31)), r0: 360 * hash(i + 5), w: 300 + 500 * hash(i + 17), f: 5 + 6 * hash(i + 23) }); }

    // section cards ("Part 1", "Part 2"): a clear break between the parts of the lesson
    B.filter(b => b.shot === 'X').forEach(b => {
      const g = el('g', { id: 'gx' + b.i }, E('gX')), o = { g };
      o.b = el('g', { filter: 'url(#fSh)' }, g); o.b.innerHTML = `<circle r="150" fill="#FFFBF1"/><circle r="126" fill="#F2B134"/><text y="62" font-size="176" text-anchor="middle" fill="#fff" stroke="#fff" stroke-width="5" class="fat">${b.n}</text>`;
      o.t = el('g', {}, g); arLine(o.t, { x: 540, y: 1006, 'font-size': 112, fill: '#fff' }, b.ar, 860);
      o.e = el('text', { x: 540, y: 1092, 'font-size': 56, 'text-anchor': 'middle', fill: '#FFE08A', 'letter-spacing': 2 }, g); o.e.textContent = b.en;
      XB[b.i] = o;
    });

    // quiz card: the five phrases of the round; each English answer stays hidden until it is heard again
    const gR = E('gR'), rt = el('g', { id: 'rT' }, gR);
    arLine(rt, { x: 540, y: 494, 'font-size': 84, fill: '#fff' }, L.quizAr, 700);
    el('text', { x: 540, y: 552, 'font-size': 40, 'text-anchor': 'middle', fill: '#FFE08A' }, rt).textContent = L.quizSub;
    const rc = el('g', { id: 'rc' }, gR); let rgs = ''; for (let g = 0; g < NP / 5; g++) rgs += `<g id="rg${g}"></g>`;
    rc.innerHTML = `<g filter="url(#fSh)"><rect x="70" y="586" width="940" height="656" rx="42" fill="#FFFBF1"/></g>` + rgs;
    PH.forEach((p, j) => {
      const k = j % 5, Y = 600 + k * 126, g = el('g', {}, E('rg' + Math.floor(j / 5))), o = ROW[j] = { g };
      if (k) el('path', { d: `M112 ${Y - 1}H968`, stroke: '#EADBC0', 'stroke-width': 3, 'stroke-linecap': 'round' }, g);
      o.mk = el('rect', { x: 184, y: Y + 62, width: 0, height: 56, rx: 14, fill: '#FFE08A' }, g);
      o.c = el('circle', { cx: 140, cy: Y + 64, r: 34, fill: k % 2 ? P.teal : P.saffron }, g);
      el('text', { x: 140, y: Y + (j < 9 ? 80 : 78), 'font-size': j < 9 ? 44 : 38, 'text-anchor': 'middle', fill: '#fff' }, g).textContent = j + 1;
      el('text', { x: 196, y: Y + 46, 'font-size': 36, fill: P.ink }, g).textContent = p.dz;
      o.e = el('text', { x: 196, y: Y + 104, 'font-size': 50, fill: P.cobalt }, g); o.e.textContent = p.en; o.w = o.e.getComputedTextLength();
      o.q = el('g', {}, g); o.q.innerHTML = `<rect x="190" y="${Y + 64}" width="${r2(Math.max(220, o.w * .8))}" height="52" rx="14" fill="#EFE6D2"/><text x="214" y="${Y + 103}" font-size="44" fill="#B9A98A" letter-spacing="10">???</text>`;
      o.k = el('g', {}, g); o.k.innerHTML = `<circle r="25" fill="#2BB673"/><path d="${tick}" fill="none" stroke="#fff" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>`;
    });

    // end card
    const gC = E('gC');
    CC.t = el('g', {}, gC); arLine(CC.t, { x: 540, y: 486, 'font-size': 84, fill: '#fff' }, L.endQ, 760);
    CC.wc = el('g', {}, gC); CC.wc.innerHTML = `<g filter="url(#fSh)"><rect x="80" y="536" width="920" height="278" rx="42" fill="#FFFBF1"/></g>`;
    arLine(CC.wc, { x: 540, y: 600, 'font-size': 40, fill: P.red }, L.endWord, 700);
    const cw = el('text', { x: 540, y: 706, 'font-size': 96, 'text-anchor': 'middle', fill: P.navy }, CC.wc); cw.textContent = WD.parts.join('·'); fit(cw, 840);
    arLine(CC.wc, { x: 540, y: 780, 'font-size': 44, fill: P.cobalt }, L.endEq, 760);
    CC.cta = el('g', {}, gC); const ct = arLine(CC.cta, { x: 500, y: 916, 'font-size': 88, fill: '#FFD23F' }, L.cta, 640);
    CC.ic = el('g', {}, CC.cta); CC.ix = 500 + ct.getComputedTextLength() / 2 + 84;
    CC.ic.innerHTML = `<path d="M-40 -36H40Q52 -36 52 -24V14Q52 26 40 26H-6L-30 48V26H-40Q-52 26 -52 14V-24Q-52 -36 -40 -36Z" fill="#fff"/><circle cx="-24" cy="-5" r="7" fill="${P.cobalt}"/><circle cx="0" cy="-5" r="7" fill="${P.cobalt}"/><circle cx="24" cy="-5" r="7" fill="${P.cobalt}"/>`;
    CC.en = el('text', { x: 540, y: 968, 'font-size': 36, 'text-anchor': 'middle', fill: '#fff' }, gC); CC.en.textContent = L.ctaEn;
    CC.fol = el('g', {}, gC); CC.fol.innerHTML = `<g filter="url(#fSh2)"><rect x="-200" y="-41" width="400" height="82" rx="41" fill="#F2B134"/></g><circle cx="132" cy="0" r="27" fill="${P.ink}"/><path d="M119 0H145M132 -13V13" stroke="#fff" stroke-width="7" stroke-linecap="round"/>`;
    arLine(CC.fol, { x: -34, y: 19, 'font-size': 52, fill: P.ink }, L.follow, 240);
    CC.sub = arLine(gC, { x: 540, y: 1128, 'font-size': 36, fill: '#fff' }, L.sub, 520);
    const bub = (txt, size, tail) => { const g = el('g', { filter: 'url(#fSh2)' }, gC), r = el('path', { fill: '#FFFBF1' }, g), tx = el('text', { y: r2(size * 0.36), 'font-size': size, 'text-anchor': 'middle', fill: P.navy }, g); tx.textContent = txt;
      const w = tx.getComputedTextLength() / 2 + 34; r.setAttribute('d', `M${r2(-w + 30)} -36H${r2(w - 30)}A30 30 0 0 1 ${r2(w)} -6V6A30 30 0 0 1 ${r2(w - 30)} 36H${tail + 22}L${tail + 6} 62L${tail - 14} 36H${r2(-w + 30)}A30 30 0 0 1 ${r2(-w)} 6V-6A30 30 0 0 1 ${r2(-w + 30)} -36Z`); return g; };
    CC.bL = bub(BI.o2.en, 42, 96); CC.bA = bub(BI.o3.en, 48, 20);
    show('tBaL', false); show('tBaR', false);
  }

  // ---------- acting for the round portraits (board, quiz and end card): one pose while line b is being said
  function poseOf(who, b, t, md) {
    const kid = who !== 'T', spk = b.sp === who || (b.sp === 'AL' && kid), d = t - b.b, x = t - b.a, m = spk ? mouthOf(b, t) : 0, n = WHO.indexOf(who);
    const sd = n % 2 ? 1 : -1, seed = who === 'T' ? 1.3 : who === 'A' ? 2.4 : who === 'L' ? 0.6 : 3.1 + n * 1.7;
    const o = { m, round: .5 + .5 * Math.sin(t * 8.6 + seed), smile: who === 'T' ? .8 : .6, open: blink(t, seed), happy: 0, gx: spk || who === 'T' ? .8 * Math.sin(t * .9 + seed) : 5 * sd, gy: 0,
      brow: .3 * m, tilt: 0, rot: 1.5 * Math.sin(t * 1.05 + seed * 2), dy: -(who === 'T' ? 4 : 7) * m, dx: 0, lean: 0, spk: spk ? 1 : 0 };
    switch (md) {
      case 'repeat': o.brow = .5; o.smile = 1; o.dy += 4 * Math.sin(t * 9 + seed); if (d > .08) o.happy = 1; break;
      case 'nod': o.smile = .9; o.dy += 4 * Math.sin(t * 7 + seed); if (d > .1 && b.len > .01) o.happy = 1; break;
      case 'amused': o.smile = 1; o.rot = 2.5 * Math.sin(t * 6); if (d > -.3) o.happy = 1; break;
      case 'bravo': o.happy = 1; o.smile = 1; o.dy -= 9 * Math.abs(Math.sin(t * 10 + seed)); break;
      case 'wow': o.open *= 1.2; o.brow = 1; o.gy = -4; o.gx = lerp(-6, 6, clamp(x / Math.max(b.len, .1))); break;
      case 'board': o.gy = -4; o.gx = who === 'A' ? -1 : -4; break;
      case 'grin': o.smile = 1; o.brow = .5; if (d > .05) o.happy = 1; break;
      case 'wait': o.smile = 1; o.brow = .7; o.gx = 0; o.gy = 1; o.rot = 3 * Math.sin(t * 2.2 + seed); break;
      case 'win': o.brow = .8; o.smile = 1; if (d > .03) { o.happy = 1; o.dy -= 10 * Math.abs(Math.sin(d * 9)) * Math.exp(-d / .8); } break;
    }
    return o;
  }
  const NUM = ['m', 'round', 'smile', 'open', 'happy', 'gx', 'gy', 'brow', 'tilt', 'rot', 'dy', 'dx', 'lean', 'spk'];
  // the pose at time t, eased across the change from one line to the next
  function actor(who, sh, t, mdOf) {
    const b = beatAt(sh, t), p = poseOf(who, b, t, mdOf(b, who)), u = (t - b.a + 0.12) / 0.16;
    if (b.i === sh.i || u >= 1) return p;
    const q = poseOf(who, B[b.i - 1], t, mdOf(B[b.i - 1], who)), k = eo(u), o = {};
    NUM.forEach(n => { o[n] = lerp(q[n], p[n], k); });
    return o;
  }
  function lanterns(t, ids) {
    ids.forEach((id, k) => { tf(id, `rotate(${r2(2.1 * Math.sin(t * 1.25 + k * 2.1))})`); E(id + 'g').setAttribute('opacity', r2(0.8 + 0.14 * Math.sin(t * 3.3 + k))); });
  }
  // pos[who] = [x, y, scale, y of the name pill or 0, peek]: a peeking pupil is drawn whole, and the caption card hides the body
  function castDraw(t, sh, pos, mdOf, tq) {
    WHO.forEach((w, n) => {
      const p = pos[w], nm = NM[w]; show('av' + w, !!p); if (nm) show(nm, !!p && !!p[3]); if (!p) return;
      const pk = !!p[4], o = actor(w, sh, t, mdOf), t0 = (pk && tq != null ? tq : sh.a) + .05 * n, inn = eo((t - t0) / .4);
      tf('av' + w, ps(p[0] + o.dx, p[1] + (pk ? 110 : 60) * (1 - inn), p[2] * (1 + (pk ? 0 : .09) * o.spk), o.lean)); op('av' + w, (t - t0) / .2);
      if (w !== 'T') { show('ao' + w, !pk); show('ab' + w, !pk); show('ar' + w, !pk); if (pk) E('ag' + w).removeAttribute('clip-path'); else E('ag' + w).setAttribute('clip-path', 'url(#cpK)'); }
      E('ar' + w).setAttribute('stroke-width', r2((w === 'T' ? 14 : 16) * (1 + .6 * o.spk)));
      o.dy *= pk ? 1.6 : .6; C.pose(AV[w], w === 'T' ? 'teacher' : 'kid', o);
      if (nm && p[3]) { tf(nm, ps(p[0], p[3], pop(t, t0 + .25, .3))); }
    });
  }

  // ---------- the teacher at the board says the phrase in the dialect
  function drawT(t, sh, b) {
    const u = (t - sh.a) / (sh.b - sh.a), m = mouthOf(b, t), q = b.p >= 0 && PH[b.p].q, pre = t < b.a - .12;
    tf('sT', zoom(1 + .035 * u + .03 * (1 - eo((t - sh.a) / .24)), 640, 820));
    lanterns(t, ['ln1', 'ln2']);
    TBD.forEach(x => show('bd' + x.i, x === b));
    if (b.board) {
      b.bd[0].setAttribute('fill-opacity', r2(clamp((t - sh.a - .05) / .25)));
      b.bq.setAttribute('opacity', r2(clamp((t - sh.a - .3) / .25))); tf(b.bq, zoom(1 + .07 * Math.sin(t * 6.5), 380, 780));
    } else b.bd.forEach((s, k) => s.setAttribute('fill-opacity', r2(clamp((t - b.ws[k] + .06) / .2))));
    show('bdu', !b.board);
    E('bdn').textContent = b.p >= 0 ? (b.p + 1) + '/' + NP : '';
    tf('bdu', `translate(${b.bd.two ? -40 : 0},${b.bd.two ? 34 : 0})`); E('bdu').setAttribute('stroke-dashoffset', r2(100 * (1 - eo((t - b.b + .25) / .35))));
    let tap = 0; b.ws.forEach(w => { const d = t - w; if (d >= 0) tap = Math.max(tap, Math.exp(-d / .14)); });
    tf('tTaL', `rotate(${r2(-2 - 6 * tap + 1.2 * Math.sin(t * 1.7))} -124 180)`);
    tf('tTaR', `rotate(${r2(3 * Math.sin(t * 2.1) - 9 * m)} 124 180)`);
    tf('tTb', `rotate(${r2(.5 * Math.sin(t * 1.1))} 0 760)`);
    C.pose('tT', 'teacher', { m, round: .5 + .5 * Math.sin(t * 9), smile: .8, open: blink(t, 1.3), gx: pre ? -4 : .6 * Math.sin(t * .9), gy: 0, brow: (q || b.board ? .9 : .4) * m,
      rot: 1.3 * Math.sin(t * 1.15) - (pre ? 2.5 : 0), dy: -4 * m });
  }

  // ---------- one pupil in close-up: first a moment to think, then the answer in English, with the meaning sticker
  function drawK(t, sh, b) {
    const i = b.p, ph = PH[i], boy = b.sp === 'A', id = boy ? 'kb' : 'kg', ot = boy ? 'kg' : 'kb';
    const u = (t - sh.a) / (sh.b - sh.a), m = mouthOf(b, t), dd = t - DING[i], hp = clamp(dd / .14), th = clamp((b.a - .08 - t) / .16);
    show('pKb', boy); show('pKg', !boy); show('nbA', boy); show('nbL', !boy);
    ['b', 'a', 'h'].forEach(s => { show(id + s, true); show(ot + s, false); });
    tf('sK', zoom(1 + .04 * u + .03 * (1 - eo((t - sh.a) / .24)), 540, 790));
    const talk = clamp((t - b.a) / .3) * (1 - hp);
    C.pose(id, 'kid', {
      m: dd > 0 || th > .5 ? 0 : m, round: .5 + .5 * Math.sin(t * 8.3 + i), smile: lerp(.6 + .7 * hp, .35, th), open: blink(t, 2.4 + i * .7),
      happy: dd > .1 && dd < .8 ? 1 : 0, gx: lerp(2.5 * Math.sin(t * .8 + i), boy ? 7 : -7, th), gy: lerp(ph.worry ? 2 * talk : 0, -7, th),
      brow: (ph.q ? .7 : .25) * m + .4 * talk * (ph.q ? 1 : 0) + .5 * hp + .8 * th, tilt: (ph.worry ? 13 * talk : 0) + 5 * th,
      rot: 2 * Math.sin(t * .95 + i * 1.7) + (ph.q ? 3.5 * talk : 0) + (boy ? 4 : -4) * th, dy: -7 * m - (dd > 0 ? 12 * Math.exp(-dd / .16) * Math.sin(dd * 16) : 0)
    });
    tf('stk', `translate(902,470) rotate(${r2(-7 + 4 * Math.sin(t * 1.9))}) scale(${(.92 * pop(t, sh.a + .12, .34) + .001).toFixed(3)})`);
    PH.forEach((x, k) => show('ic' + k, k === i));
    for (let k = 0; k < 8; k++) {
      const a = k * Math.PI / 4 + .3, r = 122 + 96 * eo(dd / .5);
      show('br' + k, dd > 0 && dd < .6);
      tf('br' + k, `translate(${r2(902 + r * Math.cos(a))},${r2(470 + r * Math.sin(a))}) scale(${r2(1.5 * (1 - clamp(dd / .6)) + .2)})`);
    }
  }

  // ---------- the hard word
  const HP = { T: [205, 968, .58, 0], A: [556, 968, .47, 0], L: [812, 968, .47, 0] };
  QK.forEach((k, i) => { HP['Q' + i] = [500 + i * 148, 1124, .3, 1192, 1]; });
  const HACT = { hb: ['grin', 'board', 'board'], w0: ['talk', 'board', 'board'], tw: ['talk', 'board', 'board'], w1: ['listen', 'wow', 'board'], w5: ['grin', 'win', 'nod'], w6: ['bravo', 'grin', 'nod'],
    v0: ['talk', 'board', 'board'], v2: ['talk', 'board', 'board'], v3: ['wait', 'wait', 'wait'], v4: ['bravo', 'bravo', 'bravo'] };   // v4: the whole class says the word
  const mdH = (b, w) => { const a = HACT[b.id], n = Math.min(2, WHO.indexOf(w)); if (a) return a[n]; const s = b.sp === w || (b.sp === 'AL' && w !== 'T'); return s ? (w === 'T' ? 'talk' : 'repeat') : w === 'T' || b.syl == null ? 'listen' : 'board'; };
  function drawH(t, sh, b) {
    const u = (t - sh.a) / (sh.b - sh.a), tw = BI.tw, w1 = BI.w1, w2 = BI.w2, w3 = BI.w3, w4 = BI.w4, w6 = BI.w6, v0 = BI.v0, v1 = BI.v1, v2 = BI.v2, v3 = BI.v3;
    tf('sH', zoom(1 + .02 * u + .03 * (1 - eo((t - sh.a) / .3)), 540, 640));
    const sp = eo((t - w2.a - .15) / .7) * (1 - eo((t - w4.a - .1) / .55)), wr = clamp((t - tw.a + .05) / (tw.len * .8)) * SY.length, slow = t < w3.a - .1, sn = eo((t - v0.a - .1) / .55);
    op(H.hd, (t - sh.a - .15) / .3);
    op(H.qq, clamp((t - sh.a - .3) / .3) * (1 - clamp((t - tw.a + .15) / .15))); tf(H.qq, zoom(1 + .05 * Math.sin(t * 6), 540, 650));
    tf(H.wd, zoom(lerp(1.22, 1, sp) + (t >= WIN ? .12 * Math.exp(-(t - WIN) / .25) : 0), 540, 618));
    op(H.wo, 1 - sn * 1.6);      // the sentence takes the board
    SY.forEach((s, i) => {
      let hT = 0, hK = 0;
      [['s' + i + 't', 0], ['s' + i + 'a', 1], ['f' + i + 't', 0], ['f' + i + 'k', 1]].forEach(q => { const x = BI[q[0]]; if (!x) return; const h = t < x.a - .04 ? 0 : t <= x.b ? 1 : Math.exp(-(t - x.b) / .16); if (q[1]) hK = Math.max(hK, h); else hT = Math.max(hT, h); });
      const dn = BI['s' + i + 'a'], df = BI['f' + i + 'k'], hot = Math.max(hT, hK);
      const ck = slow ? pop(t, dn.b, .25) : t < df.b ? 1 - clamp((t - w3.a + .1) / .15) : pop(t, df.b, .2);
      tf(s.g, `translate(${r2(lerp(s.xm, s.xs, sp))},646)`); tf(s.z, zoom(1 + .14 * hot, s.w / 2, -30)); op(s.g, wr - i);
      s.tile.setAttribute('fill', hot > .02 ? (hK > hT ? '#7BE0A0' : '#FFD45C') : '#fff'); s.tile.setAttribute('fill-opacity', r2(sp * lerp(.08, 1, hot))); s.tile.setAttribute('stroke-opacity', r2(.55 * sp));
      s.tx.setAttribute('fill', hot > .5 && sp > .5 ? P.ink : t >= WIN ? '#FFE08A' : '#FDFBF3');
      op(s.h, sp); tf(s.ck, ps(s.w + 8, -82, ck * sp));
    });
    const rl = w1 ? clamp((t - w1.a - .5) / .25) * (1 - clamp((t - w2.a + .2) / .2)) : 0;   // the "so long!" ruler, when the script has that line
    op(H.rl, rl); if (w1) H.rp.setAttribute('stroke-dashoffset', r2(100 * (1 - eo((t - w1.a - .5) / .6))));
    op(H.mean, clamp((t - tw.b) / .3) * (1 - sp) * (1 - rl) * (1 - sn));
    // the sentence is written on the board word by word as it is said; then its meaning
    op(H.sn, sn);
    H.sW.forEach((it, k) => { const d = t - (v1.ws[k] != null ? v1.ws[k] : v1.a) + .05; it.g.setAttribute('transform', `translate(${r2(it.x)},${r2(it.y)}) scale(${(1 + (d >= 0 ? it.k * Math.exp(-d / .11) : 0)).toFixed(3)})`); it.tx.setAttribute('opacity', r2(clamp(d / .08))); });
    op(H.st, (t - v2.a + .05) / .3);
    tf(H.cs, ps(540, 432, pop(t, BI.s0t.a - .35, .3) * (1 - clamp((t - w3.a + .15) / .15)), -3));
    tf(H.cf, ps(540, 432, pop(t, w3.a + .05, .3) * (1 - clamp((t - w4.a + .1) / .15)) * (1 + .05 * Math.sin(t * 14)), 3));
    tf(H.ci, ps(540, 432, pop(t, v0.a + .05, .3) * (1 - clamp((t - v3.a + .12) / .12)), -3));
    tf(H.cy, ps(540, 432, pop(t, v3.a, .3) * (1 - clamp((t - v3.b + .1) / .12)) * (1 + .06 * Math.sin(t * 9)), 3));
    tf(H.rb, ps(540, t >= v0.a - .2 ? 494 : 806, Math.max(pop(t, w6.a + .1, .35) * (1 - clamp((t - v0.a + .2) / .15)), pop(t, CHEER, .35)), -3 + 1.5 * Math.sin(t * 3)));
    const d = t - CHEER, fly = d >= 0 && d < 3.2; show('cft', fly);
    if (fly) CF.forEach(c => { tf(c.e, `translate(${r2(c.x0 + c.vx * d)},${r2(890 + c.vy * d + 560 * d * d)}) rotate(${r2(c.r0 + c.w * d)}) scale(1,${r2(Math.cos(d * c.f))})`); op(c.e, 1 - (d - 2.3) / .8); });
    castDraw(t, sh, HP, mdH, BI.w0.a - .15);
  }

  // ---------- section card, quiz card and end card (patterned background)
  function blueBg(t, sh) {
    lanterns(t, ['ln3', 'ln4']);
    SPK.forEach((s, k) => { const tw = .5 + .5 * Math.sin(t * 3.1 + k * 1.9); tf('sp' + k, `translate(${s[0]},${s[1]}) scale(${r2(s[2] * (.5 + .9 * tw))}) rotate(${r2(20 * Math.sin(t + k))})`); op('sp' + k, clamp((t - sh.a - .1 * k) / .3) * (.35 + .65 * tw)); });
  }
  function drawX(t, sh, b) {
    const a = sh.a, out = 1 - clamp((t - sh.b + .16) / .16);
    B.forEach(x => { if (x.shot === 'X') show('gx' + x.i, x === b); });
    const o = XB[b.i];
    tf(o.b, ps(540, 720, pop(t, a + .05, .4) * out, -6 + 6 * eo((t - a) / .5))); op(o.g, out);
    op(o.t, (t - a - .22) / .2); tf(o.t, `translate(0,${r2(40 * (1 - eo((t - a - .22) / .35)))})`);
    op(o.e, (t - a - .38) / .2);
    WHO.forEach(w => { show('av' + w, false); if (NM[w]) show(NM[w], false); });
  }
  const RP = { T: [200, 1378, .6, 0], A: [556, 1378, .48, 1512], L: [826, 1378, .48, 1512] };
  QK.forEach((k, i) => { RP['Q' + i] = [222 + i * 212, 1672, .31, 1762]; });
  const mdR = (b, w) => b.sp === w ? (w === 'T' ? 'talk' : 'repeat') : b.sil ? (w === 'T' ? 'grin' : 'wait') : w === 'T' ? 'grin' : 'nod';
  function drawR(t, sh, b) {
    const a = sh.a, g = B[sh.i].round, rc = BI['rc' + g], tin = rc.b - .12, up = eo((t - tin) / .45);
    op('rT', (t - a - .05) / .2); tf('rT', `translate(0,${r2(lerp(300, 0, up))}) ` + zoom(lerp(1.3, 1, up) * (pop(t, a + .05, .4) * .15 + .85), 540, 510));
    tf('rc', `translate(0,${r2(70 * (1 - eo((t - tin - .05) / .42)))})`); op('rc', (t - tin - .05) / .2);
    for (let r = 0; r < NP / 5; r++) show('rg' + r, r === g);
    let prev = rc.b;
    for (let k = 0; k < 5; k++) {
      const r = ROW[g * 5 + k], x = BI['rc' + g + '_' + k], t0 = tin + .2 + .1 * k, rev = clamp((t - x.a + .14) / .14), act = t >= prev - .05 && t < x.a - .1;
      op(r.g, clamp((t - t0) / .18) * (act || rev > 0 ? 1 : .45)); tf(r.g, `translate(${r2(-36 * (1 - eo((t - t0) / .3)))},0)`);
      op(r.e, rev); op(r.q, 1 - rev);
      tf(r.c, zoom(act ? 1 + .12 * Math.abs(Math.sin(t * 7)) : 1, 140, 600 + k * 126 + 64));
      r.mk.setAttribute('width', r2((r.w + 24) * eo((t - x.a + .1) / .3))); r.mk.setAttribute('opacity', r2(rev * (.35 + .65 * (1 - clamp((t - x.b - .2) / .3)))));
      tf(r.k, ps(944, 600 + k * 126 + 90, pop(t, x.b, .3)));
      prev = x.b;
    }
    castDraw(t, sh, RP, mdR);
  }
  const CP = { T: [205, 1350, .6, 0], A: [556, 1350, .48, 1484], L: [820, 1350, .48, 1484] };
  QK.forEach((k, i) => { CP['Q' + i] = [222 + i * 212, 1646, .31, 1736]; });
  const mdC = (b, w) => b.sp === w ? (w === 'T' ? 'talk' : 'grin') : b.id === 'o1' ? (w === 'T' ? 'listen' : 'nod') : w === 'T' ? 'amused' : w[0] === 'Q' ? 'bravo' : 'nod';
  function drawC(t, sh, b) {
    const a = sh.a, o1 = BI.o1, o2 = BI.o2, o3 = BI.o3, t2 = o1.ws.length > 7 ? o1.ws[2] : o1.a + o1.len * .22, t3 = o1.ws.length > 7 ? o1.ws[7] : o1.a + o1.len * .6;
    op(CC.t, (t - a) / .2); tf(CC.t, `translate(0,${r2(-24 * (1 - eo((t - a) / .3)))})`);
    tf(CC.wc, `translate(0,${r2(60 * (1 - eo((t - a - .15) / .45)))})`); op(CC.wc, (t - a - .15) / .2);
    tf(CC.cta, zoom(pop(t, t2 - .05, .34) + .001, 540, 890)); tf(CC.ic, ps(CC.ix, 884, .95, 8 * Math.sin(t * 4))); op(CC.en, (t - t2 - .25) / .3);
    tf(CC.fol, ps(540, 1044, pop(t, t3 - .05, .34) * (1 + .035 * Math.sin((t - t3) * 7) * clamp((t - t3 - .4) / .3)))); op(CC.sub, (t - t3 - .25) / .3);
    tf(CC.bL, ps(715, 1178, pop(t, o2.a - .1, .3) * (1 - clamp((t - o3.a + .15) / .12)))); tf(CC.bA, ps(560, 1178, pop(t, o3.a - .1, .3)));
    castDraw(t, sh, CP, mdC);
  }

  // ---------- progress marks (the phrases in rounds of five, then the star for the hard word) and the caption card
  function hud(t, b, k) {
    show('hudM', k !== 'C'); show('hudE', k === 'C');
    for (let n = 0; n <= NP; n++) {
      const t1 = n < NP ? DING[n] : WIN, done = t >= t1, act = !done && b.N === n + 1;
      const s = done ? 1 + .7 * Math.exp(-(t - t1) / .12) : act ? 1 + .14 * Math.sin(t * 7) : 1;
      E('dc' + n).setAttribute('fill', done ? (n < NP ? '#2BB673' : '#FFC83D') : act ? '#F2B134' : '#E9DCC3');
      if (n < NP) show('dk' + n, done);
      tf('dt' + n, `translate(${r2(DOTX(n))},278) scale(${s.toFixed(3)})`);
    }
  }
  function timer(frac) { show('tmr', frac != null); if (frac != null) E('tmf').setAttribute('width', r2(Math.max(18, 500 * clamp(frac)))); }
  function card(t, sh, b) {
    tf('card', `translate(0,${r2(14 * (1 - eo((t - (b.i === sh.i ? sh.a : b.a - .12)) / .2)))})`);
    const think = b.shot === 'K' && t < b.a - .08, turn = b.id === 'v3';
    const tab = b.shot === 'K' ? 'E' : turn ? 'Y' : b.sp === 'T' ? (b.dz ? 'D' : 'T') : b.sp, c = b.cap, rn = b.shot === 'K';
    TABK.forEach(k => show('tab' + k, k === tab));
    CAPS.forEach(x => show('cp' + x.i, x === b && !think));
    show('cpFT', !!b.fast && b.sp === 'T'); show('cpFK', !!b.fast && b.sp !== 'T');
    show('tabR', rn);
    if (rn) { PH.forEach((p, k) => show('rp' + k, k === b.p)); E('rpR').setAttribute('x', r2(912 - RPW[b.p] - 30)); E('rpR').setAttribute('width', r2(RPW[b.p] + 60)); }
    const vo = b.st === 'ok' && t >= b.b + .08;
    show('vo', vo); if (vo) tf('vo', ps(104 + TABW[tab] + 44, 1171, pop(t, b.b + .08, .3)));
    show('thk', think);
    timer(turn ? (b.b - t) / b.len : think ? (b.a - .08 - t) / Math.max(.2, b.a - .08 - sh.a) : null);
    if (think) {
      TQ.forEach((q, k) => { const ph = t * 5.2 - k * .9; q.setAttribute('transform', `translate(${430 + k * 110},${r2(1436 - 16 * Math.max(0, Math.sin(ph)))}) rotate(${r2((k - 1) * 8 + 5 * Math.sin(ph))})`); });
    } else if (b.fast) { const T = b.sp === 'T', bs = [0, 1, 2, 3, 4].map(i => BI['f' + i + (T ? 't' : 'k')]); drawWords(H[T ? 'fT' : 'fK'], bs.map(x => x.a), bs.map(x => x.b), t); }
    else if (turn) { const lit = c.W.map(() => b.a - 1); drawWords(c.W, lit, lit, t); }
    else if (c.W) {
      drawWords(c.W, b.ws, b.we, t);
      if (c.A) c.A.forEach((s, k) => s.setAttribute('fill-opacity', r2(lerp(.25, 1, clamp((t - b.ws[k] + .05) / .1)))));
    } else tf(c.big, zoom(1 + .1 * mouthOf(b, t) + .25 * (1 - eo((t - b.a + .1) / .18)), 540, 1330));
  }

  window.renderFrame = function (t) {
    t = clamp(t, 0, TL.dur - 0.0001);
    let sh = SH[SH.length - 1];
    for (const s of SH) if (t < s.b - 1e-6) { sh = s; break; }
    const k = sh.k, b = beatAt(sh, t), blue = k === 'R' || k === 'C' || k === 'X', carded = !blue && (!!b.cap || !!b.fast);
    show('sT', k === 'T'); show('sK', k === 'K'); show('sH', k === 'H'); show('sB', blue); show('gX', k === 'X'); show('gR', k === 'R'); show('gC', k === 'C');
    show('card', carded); show('cast', blue || k === 'H'); show('names', blue || k === 'H'); show('cft', false);
    if (k === 'T') drawT(t, sh, b); else if (k === 'K') drawK(t, sh, b); else if (k === 'H') drawH(t, sh, b);
    else { blueBg(t, sh); (k === 'R' ? drawR : k === 'X' ? drawX : drawC)(t, sh, b); }
    if (carded) card(t, sh, b);
    hud(t, b, k);
    op('fl', k === 'T' || k === 'K' ? 0 : .5 * (1 - (t - sh.a) / .22));
  };
  window.RENDER_DURATION = TL.dur;

  function raster(svg, w, h, blur) {
    return new Promise((res, rej) => {
      const im = new Image();
      im.onload = () => {
        const c = document.createElement('canvas'); c.width = w; c.height = h;
        const x = c.getContext('2d'), mg = blur ? blur * 4 : 0;
        if (blur) x.filter = `blur(${blur}px)`;
        x.drawImage(im, -mg, -mg, w + 2 * mg, h + 2 * mg);
        res(c.toDataURL('image/png'));
      };
      im.onerror = () => rej(new Error('plate failed'));
      im.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    });
  }
  const setImg = (id, url) => new Promise(res => { const e = E(id); e.addEventListener('load', res, { once: true }); e.addEventListener('error', res, { once: true }); e.setAttribute('href', url); });
  window.RENDER_READY = (async () => {
    await document.fonts.ready;
    const W = 1188, HH = 2112;
    const pl = await Promise.all([raster(A.bgTeacher(W, HH), W, HH, 0), raster(A.bgKid(W, HH, false), W, HH, 8), raster(A.bgKid(W, HH, true), W, HH, 8),
      raster(A.bgKid(W, HH, true), W, HH, 14), raster(A.bgEnd(W, HH), W, HH, 0)]);
    await Promise.all([setImg('pT', pl[0]), setImg('pKb', pl[1]), setImg('pKg', pl[2]), setImg('pH', pl[3]), setImg('pC', pl[4]), setImg('lg', 'logo.png')]);
    build();
    window.renderFrame(0);
    window.READY_OK = true;
  })();
})();
