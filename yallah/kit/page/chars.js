/* chars.js: the teacher and the two pupils, drawn as SVG and posed every frame */
(function () {
  const C = {};
  const E = id => document.getElementById(id);
  const f = n => Math.round(n * 100) / 100;
  const LIP = '#9A3B34';

  // mouth centred on 0,0. w = half width, H = max opening, o = 0..1 open, r = 0..1 rounded, s = smile
  C.mouth = function (w, H, o, r, s) {
    if (o < 0.07) {
      const k = s == null ? 0.5 : s;
      return `<path d="M${f(-w)} ${f(-k * 5)}Q0 ${f(w * 0.62 * k + 3)} ${f(w)} ${f(-k * 5)}" fill="none" stroke="${LIP}" stroke-width="${f(w * 0.16 + 2)}" stroke-linecap="round"/>`;
    }
    const ww = w * (1 - 0.3 * (r || 0)), h = Math.max(H * 0.16, o * H), th = Math.min(H * 0.2, h * 0.4);
    return `<path d="M${f(-ww)} 0Q0 ${f(-ww * 0.2)} ${f(ww)} 0Q${f(ww * 0.92)} ${f(h)} 0 ${f(h)}Q${f(-ww * 0.92)} ${f(h)} ${f(-ww)} 0Z" fill="#5E161C" stroke="${LIP}" stroke-width="${f(w * 0.1 + 1.5)}" stroke-linejoin="round"/>` +
      `<path d="M${f(-ww * 0.74)} 1Q0 ${f(-ww * 0.13)} ${f(ww * 0.74)} 1L${f(ww * 0.6)} ${f(th)}Q0 ${f(th + 2)} ${f(-ww * 0.6)} ${f(th)}Z" fill="#fff"/>` +
      (h > H * 0.4 ? `<ellipse cx="0" cy="${f(h * 0.74)}" rx="${f(ww * 0.46)}" ry="${f(h * 0.2)}" fill="#E8747A"/>` : '');
  };

  function eye(id, cx, cy, rx, ry, ir, extra) {
    const ax = f(rx * 0.94), ay = f(-ry * 0.34);
    return `<g transform="translate(${cx},${cy})"><g id="${id}">
<ellipse rx="${rx}" ry="${ry}" fill="#fff"/>
<g id="${id}p"><circle r="${ir}" fill="#6A4022"/><circle r="${f(ir * 0.86)}" fill="#7C4E2A"/><circle r="${f(ir * 0.52)}" fill="#1E0F08"/>
<circle cx="${f(-ir * 0.36)}" cy="${f(-ir * 0.42)}" r="${f(ir * 0.3)}" fill="#fff"/><circle cx="${f(ir * 0.38)}" cy="${f(ir * 0.4)}" r="${f(ir * 0.14)}" fill="#fff" opacity=".85"/></g>
<path d="M${-ax} ${ay}A${rx} ${ry} 0 0 1 ${ax} ${ay}" fill="none" stroke="#2A1810" stroke-width="${f(rx * 0.2 + 2)}" stroke-linecap="round"/>${extra || ''}
</g><path id="${id}c" d="" fill="none" stroke="#2A1810" stroke-width="${f(rx * 0.2 + 2.5)}" stroke-linecap="round" display="none"/></g>`;
  }

  // ---------- teacher. origin = centre of the face
  C.teacher = function (id) {
    let knots = '';
    for (let y = 250; y < 760; y += 44) if (y < 380 || y > 460) knots += `<circle cx="0" cy="${y}" r="5.5" fill="#B8862A"/>`;
    const arm = (sx, wing) => `
<path d="M${sx * 122} 182L${sx * 190} 298" stroke="#1A2F86" stroke-width="72" stroke-linecap="round"/>
<path d="M${sx * 122} 182L${sx * 190} 298" stroke="url(#gBlue)" stroke-width="64" stroke-linecap="round"/>
<path d="M${sx * 190} 298L${sx * 236} 226" stroke="#1A2F86" stroke-width="64" stroke-linecap="round"/>
<path d="M${sx * 190} 298L${sx * 236} 226" stroke="#2F52CF" stroke-width="56" stroke-linecap="round"/>
<path d="M${sx * 228} 240L${sx * 240} 221" stroke="#F0CB5E" stroke-width="58" stroke-linecap="butt"/>${wing}`;
    return `<g id="${id}"><g id="${id}b">
<g id="${id}aL">${arm(-1, `<path d="M-246 206L-322 96" stroke="#8A5A2B" stroke-width="10" stroke-linecap="round"/><circle cx="-322" cy="96" r="8" fill="#C1272D"/>
<circle cx="-246" cy="208" r="24" fill="#EDB98F"/><path d="M-262 196Q-250 186 -236 194" fill="none" stroke="#D99B77" stroke-width="4" stroke-linecap="round"/>`)}</g>
<path d="M-72 120C-112 128 -140 150 -144 190L-162 420C-168 520 -180 600 -198 780H198C180 600 168 520 162 420L144 190C140 150 112 128 72 120Z" fill="url(#gBlue)"/>
<path d="M-72 120C-112 128 -140 150 -144 190L-162 420C-168 520 -180 600 -198 780H-120C-112 560 -104 330 -72 120Z" fill="#fff" opacity=".1"/>
<path d="M72 120C112 128 140 150 144 190L162 420C168 520 180 600 198 780H150C140 560 122 330 72 120Z" fill="#000" opacity=".12"/>
<rect x="-18" y="150" width="36" height="640" fill="url(#gGold)"/>${knots}
<path d="M-160 388Q0 410 160 388L165 446Q0 468 -165 446Z" fill="url(#gGold)"/>
<path d="M-160 388Q0 410 160 388M-165 446Q0 468 165 446" fill="none" stroke="#B8862A" stroke-width="4"/>
<ellipse cx="0" cy="428" rx="34" ry="27" fill="#F9E08A" stroke="#B8862A" stroke-width="4"/><polygon points="${window.A.star(0, 428, 15, 0)}" fill="#C1272D"/>
<g id="${id}aR">${arm(1, `<ellipse cx="246" cy="204" rx="24" ry="27" transform="rotate(24 246 204)" fill="#EDB98F"/>
<path d="M228 196Q222 180 232 172" fill="none" stroke="#EDB98F" stroke-width="13" stroke-linecap="round"/>`)}</g>
</g><g id="${id}h">
<ellipse cx="0" cy="-16" rx="126" ry="136" fill="url(#gRose)"/>
<path d="M-118 20C-134 110 -162 160 -136 198C-86 236 86 236 136 198C162 160 134 110 118 20Z" fill="url(#gRose2)"/>
<path d="M-98 152Q0 210 98 152M-72 190Q0 226 72 190" fill="none" stroke="#C4667A" stroke-width="5" stroke-linecap="round" opacity=".6"/>
<ellipse cx="0" cy="116" rx="64" ry="18" fill="#B85468" opacity=".28"/>
<ellipse cx="0" cy="4" rx="85" ry="97" fill="url(#gSkinT)"/>
<path d="M-80.6 -27A85 97 0 0 1 80.6 -27" fill="none" stroke="#F9D9DD" stroke-width="13"/>
<path d="M-112 -70Q-60 -150 30 -146" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".28"/>
${eye(id + 'eL', -35, -2, 20, 22, 15.2, '<path d="M-20 -9L-29 -16" stroke="#2A1810" stroke-width="5.5" stroke-linecap="round"/>')}
${eye(id + 'eR', 35, -2, 20, 22, 15.2, '<path d="M20 -9L29 -16" stroke="#2A1810" stroke-width="5.5" stroke-linecap="round"/>')}
<path id="${id}bL" d="M-58 -39Q-37 -54 -14 -44" fill="none" stroke="#4A2D1D" stroke-width="7" stroke-linecap="round"/>
<path id="${id}bR" d="M58 -39Q37 -54 14 -44" fill="none" stroke="#4A2D1D" stroke-width="7" stroke-linecap="round"/>
<path d="M-6 31Q0 38 7 31" fill="none" stroke="#D7936C" stroke-width="4.5" stroke-linecap="round"/>
<ellipse cx="-55" cy="38" rx="19" ry="12" fill="#F29C96" opacity=".5"/><ellipse cx="55" cy="38" rx="19" ry="12" fill="#F29C96" opacity=".5"/>
<g id="${id}m" transform="translate(0,60)"></g>
</g></g>`;
  };

  // ---------- pupils. origin = centre of the face. returns three layers so the desk can sit between them
  const LOOKS = {
    boy: { boy: 1, g1: 'url(#gMust)', g2: '#B97A14', g3: '#E9A93A', hair: '#2B1A12', hair2: '#523425', style: 'curly' },
    girl: { boy: 0, g1: 'url(#gTealK)', g2: '#12807A', g3: '#22ABA2', hair: '#3B2218', hair2: '#6A4230', style: 'buns', trim: 'url(#gGold)', dot: '#C1272D', line: '#F4CF63' },
    boy2: { boy: 1, g1: '#E4572E', g2: '#B5391A', g3: '#EE6E48', hair: '#1F1410', hair2: '#4A3226', style: 'short' },
    girl2: { boy: 0, g1: '#8B6BD9', g2: '#5E44A8', g3: '#9C80E3', hair: '#2A1712', hair2: '#5A3A2C', style: 'braids', trim: '#FFF6E0', dot: '#5E44A8', line: '#CDBDF5' },
    boy3: { boy: 1, g1: '#4F86E0', g2: '#2E5FB5', g3: '#6397EA', hair: '#3A2416', hair2: '#6A4630', style: 'spiky', glasses: 1 },
    girl3: { boy: 0, g1: '#F28BA0', g2: '#C9607A', g3: '#F7A3B4', hair: '#4A2A1A', hair2: '#7A4E36', style: 'pony', trim: '#FFF6E0', dot: '#C9607A', line: '#FBD0D9' }
  };
  C.LOOKS = LOOKS;
  // kind = one of LOOKS. returns three layers so the desk can sit between them
  C.kid = function (id, kind) {
    const L = LOOKS[kind] || LOOKS.boy, boy = !!L.boy, g1 = L.g1, g2 = L.g2, g3 = L.g3, hair = L.hair, hair2 = L.hair2, st = L.style;
    const arm = sx => `<path d="M${sx * 186} 306Q${sx * 214} 424 ${sx * 112} 444" fill="none" stroke="${g2}" stroke-width="93" stroke-linecap="round"/>
<path d="M${sx * 186} 306Q${sx * 214} 424 ${sx * 112} 444" fill="none" stroke="${g3}" stroke-width="86" stroke-linecap="round"/>`;
    const body = `<g id="${id}b">
${boy ? `<path d="M-180 226Q0 96 180 226Q152 272 98 272Q0 216 -98 272Q-152 272 -180 226Z" fill="${g2}"/>` : ''}
<path d="M-212 420C-216 310 -184 222 -96 190L-40 176H40L96 190C184 222 216 310 212 420L228 640H-228Z" fill="${g1}"/>
<path d="M-42 104H42V188Q0 216 -42 188Z" fill="#DFA078"/>
${boy
        ? `<path d="M-64 180Q0 236 64 180" fill="none" stroke="#FFF6E0" stroke-width="17" stroke-linecap="round"/><rect x="-17" y="206" width="34" height="150" rx="8" fill="#FFF6E0"/>
<circle cx="0" cy="236" r="5.5" fill="${g2}"/><circle cx="0" cy="268" r="5.5" fill="${g2}"/><circle cx="0" cy="300" r="5.5" fill="${g2}"/><circle cx="0" cy="332" r="5.5" fill="${g2}"/>`
        : `<path d="M-66 180Q0 240 66 180" fill="none" stroke="${L.trim}" stroke-width="18" stroke-linecap="round"/><rect x="-15" y="208" width="30" height="440" fill="${L.trim}"/>
<circle cx="0" cy="244" r="6" fill="${L.dot}"/><circle cx="0" cy="282" r="6" fill="${L.dot}"/><circle cx="0" cy="320" r="6" fill="${L.dot}"/>
<path d="M-150 250Q-120 236 -96 246M150 250Q120 236 96 246" fill="none" stroke="${L.line}" stroke-width="7" stroke-linecap="round"/>`}
</g>`;
    const arms = `<g id="${id}a">${arm(-1)}${arm(1)}
<g transform="translate(92,436) rotate(-56)"><rect x="-9" y="-160" width="18" height="136" fill="#FFC83D"/><rect x="-9" y="-160" width="6" height="136" fill="#E9A93A"/>
<polygon points="-9,-24 9,-24 0,6" fill="#F3D9B1"/><polygon points="-3.4,-5 3.4,-5 0,6" fill="#3A2A22"/><rect x="-9" y="-178" width="18" height="18" rx="4" fill="#F28BA0"/><rect x="-9" y="-164" width="18" height="7" fill="#B0B7C3"/></g>
<ellipse cx="-84" cy="446" rx="42" ry="31" fill="#EDB088"/><path d="M-108 430Q-90 416 -66 424" fill="none" stroke="#D98F68" stroke-width="5" stroke-linecap="round"/>
<ellipse cx="88" cy="446" rx="42" ry="31" fill="#EDB088"/><path d="M110 430Q92 416 68 424" fill="none" stroke="#D98F68" stroke-width="5" stroke-linecap="round"/>
</g>`;
    const curls = [[-130, -74, 40], [-106, -114, 42], [-64, -140, 42], [-16, -152, 44], [34, -152, 44], [80, -136, 42], [118, -106, 42], [138, -68, 38], [-144, -38, 30], [148, -34, 28]];
    const lash = sx => boy ? '' : `<path d="M${sx * 33} -12L${sx * 45} -22M${sx * 26} -22L${sx * 35} -35" stroke="#2A1810" stroke-width="6" stroke-linecap="round"/>`;
    const side = `<path d="M-153 -10Q-168 30 -156 62Q-148 74 -141 60Q-137 28 -139 -6Z" fill="${hair}"/><path d="M153 -10Q168 30 156 62Q148 74 141 60Q137 28 139 -6Z" fill="${hair}"/>`;
    const back = {
      curly: `<ellipse cx="0" cy="-44" rx="160" ry="146" fill="${hair}"/>`,
      buns: `<circle cx="-120" cy="-150" r="62" fill="${hair}"/><circle cx="120" cy="-150" r="62" fill="${hair}"/>
<path d="M-150 -176Q-120 -200 -90 -186M150 -176Q120 -200 90 -186" fill="none" stroke="${hair2}" stroke-width="8" stroke-linecap="round"/>
<path d="M-158 -112L-98 -92" stroke="#F2B134" stroke-width="16" stroke-linecap="round"/><path d="M158 -112L98 -92" stroke="#F2B134" stroke-width="16" stroke-linecap="round"/>
<ellipse cx="0" cy="-24" rx="170" ry="164" fill="${hair}"/>`,
      short: `<ellipse cx="0" cy="-40" rx="158" ry="140" fill="${hair}"/><path d="M-10 -170Q8 -206 38 -186Q16 -184 14 -164Z" fill="${hair}"/>`,
      spiky: `<ellipse cx="0" cy="-36" rx="156" ry="132" fill="${hair}"/><path d="M-150 -60L-140 -150L-104 -118L-78 -188L-40 -136L-4 -200L34 -138L70 -190L100 -122L138 -154L150 -60Z" fill="${hair}" stroke="${hair}" stroke-width="10" stroke-linejoin="round"/>`,
      braids: [-1, 1].map(sx => `<ellipse cx="${sx * 170}" cy="74" rx="31" ry="38" fill="${hair}"/><ellipse cx="${sx * 177}" cy="138" rx="29" ry="36" fill="${hair}"/><ellipse cx="${sx * 180}" cy="200" rx="27" ry="34" fill="${hair}"/>
<path d="M${sx * 154} 60L${sx * 188} 88M${sx * 160} 124L${sx * 194} 152M${sx * 164} 188L${sx * 196} 214" stroke="${hair2}" stroke-width="6" stroke-linecap="round"/>
<rect x="${sx * 180 - 24}" y="228" width="48" height="18" rx="9" fill="#FFD23F"/><path d="M${sx * 180 - 18} 246Q${sx * 180} 300 ${sx * 180 + 18} 246Z" fill="${hair}"/>`).join('') + `<ellipse cx="0" cy="-24" rx="168" ry="162" fill="${hair}"/>`,
      pony: `<path d="M92 -150C176 -218 266 -150 248 -50C240 -2 210 34 178 70C184 6 172 -68 92 -150Z" fill="${hair}"/><path d="M150 -150Q214 -150 226 -78" fill="none" stroke="${hair2}" stroke-width="8" stroke-linecap="round"/>
<ellipse cx="116" cy="-148" rx="30" ry="19" transform="rotate(38 116 -148)" fill="#FFD23F"/><ellipse cx="0" cy="-24" rx="168" ry="162" fill="${hair}"/>`
    }[st];
    const front = {
      curly: curls.map(c => `<circle cx="${c[0]}" cy="${c[1]}" r="${c[2]}" fill="${hair}"/>`).join('') +
        `<path d="M-120 -128Q-104 -146 -84 -140M-34 -172Q-14 -186 8 -178M60 -160Q80 -168 96 -154M-142 -86Q-134 -100 -120 -100" fill="none" stroke="${hair2}" stroke-width="7" stroke-linecap="round"/>`,
      buns: `<path d="M-156 8C-166 -112 -98 -172 0 -172C98 -172 166 -112 156 8C142 -50 110 -92 62 -108C12 -78 -70 -72 -110 -38C-128 -22 -146 -10 -156 8Z" fill="${hair}"/>${side}
<path d="M-96 -132Q-40 -160 30 -150M-126 -84Q-104 -110 -78 -118" fill="none" stroke="${hair2}" stroke-width="7" stroke-linecap="round"/>`,
      short: `<path d="M-154 -6C-164 -112 -96 -170 0 -170C96 -170 164 -112 154 -6C146 -52 126 -84 96 -98C60 -70 -20 -66 -74 -82C-112 -70 -140 -44 -154 -6Z" fill="${hair}"/>
<path d="M-94 -136Q-36 -160 34 -152M-128 -92Q-110 -112 -88 -118" fill="none" stroke="${hair2}" stroke-width="7" stroke-linecap="round"/>`,
      spiky: `<path d="M-152 -14C-158 -100 -100 -150 0 -150C100 -150 158 -100 152 -14C132 -70 80 -106 0 -106C-80 -106 -132 -70 -152 -14Z" fill="${hair}"/>
<path d="M-78 -150L-70 -172M-4 -160L0 -184M70 -152L76 -174" stroke="${hair2}" stroke-width="7" stroke-linecap="round"/>`,
      braids: `<path d="M0 -172C-98 -172 -166 -112 -156 8C-140 -48 -96 -98 0 -134C96 -98 140 -48 156 8C166 -112 98 -172 0 -172Z" fill="${hair}"/>${side}
<path d="M-112 -112Q-70 -146 -20 -152M112 -112Q70 -146 20 -152" fill="none" stroke="${hair2}" stroke-width="7" stroke-linecap="round"/>`,
      pony: `<path d="M-156 8C-166 -112 -98 -172 0 -172C98 -172 166 -112 156 8C152 -34 140 -58 124 -70C80 -60 40 -58 0 -58C-40 -58 -80 -60 -124 -70C-140 -58 -152 -34 -156 8Z" fill="${hair}"/>${side}
<path d="M-70 -70Q-66 -112 -50 -138M0 -62V-140M70 -70Q66 -112 50 -138" fill="none" stroke="${hair2}" stroke-width="6" stroke-linecap="round" opacity=".8"/>`
    }[st];
    const head = `<g id="${id}h">
${back}
<ellipse cx="-151" cy="16" rx="24" ry="32" fill="#EDB088"/><ellipse cx="-151" cy="16" rx="11" ry="17" fill="#D98F68"/>
<ellipse cx="151" cy="16" rx="24" ry="32" fill="#EDB088"/><ellipse cx="151" cy="16" rx="11" ry="17" fill="#D98F68"/>
<path d="M-150 -8C-150 -108 -92 -150 0 -150C92 -150 150 -108 150 -8C150 92 96 142 0 142C-96 142 -150 92 -150 -8Z" fill="url(#gSkinK)"/>
${front}
${eye(id + 'eL', -63, 6, 35, 40, 24, lash(-1))}${eye(id + 'eR', 63, 6, 35, 40, 24, lash(1))}
${L.glasses ? `<g fill="#fff" fill-opacity=".14" stroke="#2A1B14" stroke-width="7"><circle cx="-63" cy="6" r="48"/><circle cx="63" cy="6" r="48"/><path d="M-15 0Q0 -10 15 0M-111 -4L-148 -16M111 -4L148 -16" fill="none" stroke-linecap="round"/></g>` : ''}
<path id="${id}bL" d="M-98 -50Q-66 -72 -34 -57" fill="none" stroke="${hair}" stroke-width="12" stroke-linecap="round"/>
<path id="${id}bR" d="M98 -50Q66 -72 34 -57" fill="none" stroke="${hair}" stroke-width="12" stroke-linecap="round"/>
<path d="M-10 54Q0 64 10 54" fill="none" stroke="#D38E66" stroke-width="5.5" stroke-linecap="round"/>
<ellipse cx="-103" cy="66" rx="30" ry="19" fill="#F38E88" opacity=".45"/><ellipse cx="103" cy="66" rx="30" ry="19" fill="#F38E88" opacity=".45"/>
<g id="${id}m" transform="translate(0,92)"></g>
</g>`;
    return { body, arms, head };
  };

  const G = {
    teacher: { mw: 24, mH: 29, rx: 20, ry: 22, px: 0, py: 112, bl: [-36, -46], br: [36, -46] },
    kid: { mw: 31, mH: 44, rx: 35, ry: 40, px: 0, py: 150, bl: [-66, -60], br: [66, -60] }
  };

  function setEye(id, open, happy, g) {
    const e = E(id), c = E(id + 'c');
    if (happy > 0.5) {
      e.setAttribute('display', 'none'); c.removeAttribute('display');
      c.setAttribute('d', `M${-g.rx} ${f(g.ry * 0.28)}Q0 ${f(-g.ry * 0.8)} ${g.rx} ${f(g.ry * 0.28)}`);
    } else if (open < 0.4) {
      e.setAttribute('display', 'none'); c.removeAttribute('display');
      c.setAttribute('d', `M${-g.rx} ${f(g.ry * 0.02)}Q0 ${f(g.ry * 0.55)} ${g.rx} ${f(g.ry * 0.02)}`);
    } else {
      c.setAttribute('display', 'none'); e.removeAttribute('display');
      e.setAttribute('transform', `scale(1,${f(open)})`);
    }
  }

  // o: {m, round, smile, open, happy, gx, gy, brow, tilt, rot, dy}
  C.pose = function (id, type, o) {
    const g = G[type];
    E(id + 'm').innerHTML = C.mouth(g.mw, g.mH, o.m || 0, o.round || 0, o.smile);
    setEye(id + 'eL', o.open == null ? 1 : o.open, o.happy || 0, g);
    setEye(id + 'eR', o.open == null ? 1 : o.open, o.happy || 0, g);
    const p = `translate(${f(o.gx || 0)},${f(o.gy || 0)})`;
    E(id + 'eLp').setAttribute('transform', p); E(id + 'eRp').setAttribute('transform', p);
    const by = f(-(o.brow || 0) * (type === 'kid' ? 14 : 7)), tl = o.tilt || 0;
    E(id + 'bL').setAttribute('transform', `translate(0,${by}) rotate(${f(tl)} ${g.bl[0]} ${g.bl[1]})`);
    E(id + 'bR').setAttribute('transform', `translate(0,${by}) rotate(${f(-tl)} ${g.br[0]} ${g.br[1]})`);
    E(id + 'h').setAttribute('transform', `translate(0,${f(o.dy || 0)}) rotate(${f(o.rot || 0)} ${g.px} ${g.py})`);
  };

  window.C = C;
})();
