/* art.js: backgrounds, props and icons, all drawn as SVG markup */
(function () {
  const P = {
    cream: '#F9EDD6', cream2: '#F0DBB6', plaster: '#E6CC9F', plaster2: '#D2B07C',
    cobalt: '#0B6B3A', navy: '#1B1B1B', teal: '#1FA79E', saffron: '#F2B134', gold: '#E9B949',
    terra: '#C8623B', terra2: '#9E4425', wood: '#B0733A', wood2: '#7A4520', brass: '#E0A93E',
    brass2: '#9C6B1B', red: '#CE1126', white: '#FFFDF6', ink: '#2A1B14'
  };
  const f = n => Math.round(n * 10) / 10;
  const A = { P };

  function star(cx, cy, R, rot, ratio) {
    const p = [];
    for (let k = 0; k < 16; k++) {
      const a = (k * 22.5 + (rot || 0) - 90) * Math.PI / 180, r = k % 2 ? R * (ratio || 0.7654) : R;
      p.push(f(cx + r * Math.cos(a)) + ',' + f(cy + r * Math.sin(a)));
    }
    return p.join(' ');
  }
  A.star = star;

  // Palestinian encaustic floor tile (cement tile: black corner circles, red lozenge, green heart)
  function zellige(id, s) {
    const h = s / 2, k = s * 0.26;
    return `<pattern id="${id}" width="${s}" height="${s}" patternUnits="userSpaceOnUse">
<rect width="${s}" height="${s}" fill="#F3E9D2"/>
<rect x="${s * 0.03}" y="${s * 0.03}" width="${s * 0.94}" height="${s * 0.94}" fill="none" stroke="#C9B48A" stroke-width="${f(s * 0.012)}"/>
${[[0, 0], [s, 0], [0, s], [s, s]].map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="${f(k)}" fill="#1B1B1B"/><circle cx="${p[0]}" cy="${p[1]}" r="${f(k * 0.55)}" fill="#F3E9D2"/>`).join('')}
<polygon points="${h},${f(s * 0.12)} ${f(s * 0.88)},${h} ${h},${f(s * 0.88)} ${f(s * 0.12)},${h}" fill="${P.red}"/>
<polygon points="${h},${f(s * 0.24)} ${f(s * 0.76)},${h} ${h},${f(s * 0.76)} ${f(s * 0.24)},${h}" fill="#F3E9D2"/>
<polygon points="${h},${f(s * 0.36)} ${f(s * 0.64)},${h} ${h},${f(s * 0.64)} ${f(s * 0.36)},${h}" fill="#0B6B3A"/>
</pattern>`;
  }

  // tatreez (Palestinian cross-stitch embroidery) band: stitched diamond-and-cross motif in red and green on black
  const STITCH = ['....#....', '...#.#...', '..#...#..', '.#..G..#.', '#..GGG..#', '.#..G..#.', '..#...#..', '...#.#...', '....#....'];
  function band(id, s) {
    const c = s / 9;
    let r = '';
    STITCH.forEach((row, y) => row.split('').forEach((ch, x) => {
      if (ch === '.') return;
      const col = ch === 'G' ? '#2FA45B' : P.red, X = f(x * c), Y = f(y * c), d = f(c * 0.12);
      r += `<rect x="${X + d}" y="${Y + d}" width="${f(c - 2 * d)}" height="${f(c - 2 * d)}" fill="${col}"/><path d="M${X + d} ${Y + d}L${f(X + c - d)} ${f(Y + c - d)}M${f(X + c - d)} ${Y + d}L${X + d} ${f(Y + c - d)}" stroke="#fff" stroke-opacity=".55" stroke-width="${f(c * 0.1)}"/>`;
    }));
    return `<pattern id="${id}" width="${s}" height="${s}" patternUnits="userSpaceOnUse"><rect width="${s}" height="${s}" fill="#161616"/>${r}</pattern>`;
  }

  // Palestinian flag (black, white, green, red triangle), x,y = top left
  A.flag = function (x, y, w, h) {
    const t = h / 3;
    return `<g><rect x="${x}" y="${y}" width="${w}" height="${t}" fill="#111"/><rect x="${x}" y="${f(y + t)}" width="${w}" height="${t}" fill="#fff"/><rect x="${x}" y="${f(y + 2 * t)}" width="${w}" height="${t}" fill="#0B8A3C"/><path d="M${x} ${y}L${f(x + w * 0.4)} ${f(y + h / 2)}L${x} ${f(y + h)}Z" fill="${P.red}"/></g>`;
  };

  const commonDefs = `
<linearGradient id="gWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBF1DD"/><stop offset="1" stop-color="#EFD9B2"/></linearGradient>
<linearGradient id="gWallU" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1000"><stop offset="0" stop-color="#FCF3E0"/><stop offset="1" stop-color="#F1DDB8"/></linearGradient>
<linearGradient id="gWood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C58A4A"/><stop offset="1" stop-color="#8A5226"/></linearGradient>
<linearGradient id="gBoard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A7460"/><stop offset="1" stop-color="#184D3E"/></linearGradient>
<linearGradient id="gFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9683F"/><stop offset="1" stop-color="#7E3F22"/></linearGradient>
<linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD0FF"/><stop offset="1" stop-color="#E9F7FF"/></linearGradient>
<radialGradient id="gPool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF6D6" stop-opacity=".85"/><stop offset="1" stop-color="#FFF6D6" stop-opacity="0"/></radialGradient>
<radialGradient id="gVig" cx=".5" cy=".46" r=".75"><stop offset=".55" stop-color="#3A1E00" stop-opacity="0"/><stop offset="1" stop-color="#3A1E00" stop-opacity=".34"/></radialGradient>
<filter id="fSoft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>`;

  const wrap = (w, h, defs, body) =>
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 1080 1920"><defs>${commonDefs}${defs}</defs>${body}</svg>`;

  function board(x, y, w, h) {
    return `<g>
<rect x="${x - 34}" y="${y + h + 18}" width="${w + 68}" height="26" rx="9" fill="${P.wood2}"/>
<rect x="${x - 24}" y="${y - 24}" width="${w + 48}" height="${h + 48}" rx="24" fill="url(#gWood)"/>
<rect x="${x - 24}" y="${y - 24}" width="${w + 48}" height="${h + 48}" rx="24" fill="none" stroke="#5E3413" stroke-opacity=".45" stroke-width="4"/>
<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="url(#gBoard)"/>
<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="none" stroke="#0C2A20" stroke-opacity=".55" stroke-width="7"/>
<ellipse cx="${x + w * 0.3}" cy="${y + h * 0.8}" rx="${w * 0.26}" ry="${h * 0.09}" fill="#fff" opacity=".05"/>
<ellipse cx="${x + w * 0.72}" cy="${y + h * 0.22}" rx="${w * 0.2}" ry="${h * 0.08}" fill="#fff" opacity=".045"/>
<rect x="${x + 46}" y="${y + h + 8}" width="52" height="13" rx="6" fill="#FFFDF6"/>
<rect x="${x + 110}" y="${y + h + 8}" width="40" height="13" rx="6" fill="#FFD45C"/>
<rect x="${x + 162}" y="${y + h + 8}" width="46" height="13" rx="6" fill="#F59AA6"/>
<rect x="${x + w - 150}" y="${y + h - 8}" width="96" height="16" rx="5" fill="#D9C7A8"/>
<rect x="${x + w - 150}" y="${y + h + 4}" width="96" height="18" rx="5" fill="#5B4636"/>
</g>`;
  }

  // sample a cubic bezier
  function cubic(p0, p1, p2, p3, n) {
    const out = [];
    for (let i = 0; i <= n; i++) {
      const t = i / n, u = 1 - t;
      out.push([u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
        u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]]);
    }
    return out;
  }

  // ---- classroom behind the teacher (wide shot)
  A.bgTeacher = function (w, h) {
    const L = cubic([60, 500], [60, 250], [250, 118], [540, 118], 9), R = cubic([540, 118], [830, 118], [1020, 250], [1020, 500], 9);
    const lobes = L.concat(R.slice(1)).map(p => `<circle cx="${f(p[0])}" cy="${f(p[1])}" r="33" fill="url(#gWallU)"/>`).join('');
    const lobeRing = L.concat(R.slice(1)).map(p => `<circle cx="${f(p[0])}" cy="${f(p[1])}" r="39" fill="${P.gold}"/>`).join('');
    const defs = zellige('zA', 120) + band('bA', 46);
    const body = `
<rect width="1080" height="1920" fill="url(#gWallU)"/>
<path d="M0 0H1080V960H1020V500C1020 250 830 118 540 118C250 118 60 250 60 500V960H0Z" fill="${P.plaster}"/>
<path d="M0 0H1080V330C1000 170 800 60 540 60C280 60 80 170 0 330Z" fill="${P.plaster2}" opacity=".5"/>
<path d="M60 960V500C60 250 250 118 540 118C830 118 1020 250 1020 500V960Z" fill="url(#gWallU)"/>
<ellipse cx="170" cy="560" rx="330" ry="380" fill="url(#gPool)"/><ellipse cx="910" cy="560" rx="330" ry="380" fill="url(#gPool)"/>
<rect x="0" y="486" width="60" height="26" fill="${P.gold}"/><rect x="1020" y="486" width="60" height="26" fill="${P.gold}"/>
${A.flag(486, 36, 108, 72)}<rect x="484" y="34" width="4" height="90" fill="#6B4A2A"/>
${board(110, 480, 540, 410)}
<ellipse cx="716" cy="820" rx="200" ry="330" fill="#5A3A1A" opacity=".16" filter="url(#fSoft)"/>
<rect x="0" y="950" width="1080" height="8" fill="${P.gold}"/>
<rect x="0" y="958" width="1080" height="46" fill="url(#bA)"/>
<rect x="0" y="1004" width="1080" height="8" fill="${P.gold}"/>
<rect x="0" y="1012" width="1080" height="600" fill="url(#zA)"/>
<rect x="0" y="1012" width="1080" height="600" fill="#3A1E00" opacity=".1"/>
<rect x="0" y="1012" width="1080" height="40" fill="#000" opacity=".1"/>
<rect x="0" y="1596" width="1080" height="34" fill="${P.wood2}"/>
<rect x="0" y="1630" width="1080" height="290" fill="url(#gFloor)"/>
<g filter="url(#fSoft)">
<ellipse cx="392" cy="2010" rx="210" ry="150" fill="#C9482A"/><circle cx="392" cy="1868" r="112" fill="#1F1410"/>
<ellipse cx="664" cy="2014" rx="210" ry="150" fill="#7559C4"/><circle cx="664" cy="1872" r="108" fill="#2A1712"/><ellipse cx="566" cy="1950" rx="27" ry="64" fill="#2A1712"/><ellipse cx="762" cy="1950" rx="27" ry="64" fill="#2A1712"/>
<ellipse cx="150" cy="2000" rx="290" ry="190" fill="#D99A2B"/><circle cx="150" cy="1800" r="150" fill="#2B1A12"/>
<ellipse cx="930" cy="2010" rx="280" ry="190" fill="#1E9B94"/><circle cx="930" cy="1810" r="140" fill="#3A2218"/>
<circle cx="830" cy="1700" r="62" fill="#3A2218"/><circle cx="1030" cy="1700" r="62" fill="#3A2218"/>
</g>
<rect width="1080" height="1920" fill="url(#gVig)"/>`;
    return wrap(w, h, defs, body);
  };

  // ---- softly blurred classroom behind the pupils (close-up)
  A.bgKid = function (w, h, flip) {
    const defs = zellige('zB', 170) + band('bB', 60);
    const books = [['#C1272D', 34, 150], ['#1F4BA8', 28, 170], ['#F2B134', 40, 140], ['#1FA79E', 30, 160], ['#7B5CD6', 26, 150], ['#E4572E', 36, 172]];
    let bx = 58, shelf = '';
    books.forEach(b => { shelf += `<rect x="${bx}" y="${610 - b[2]}" width="${b[1]}" height="${b[2]}" rx="5" fill="${b[0]}"/>`; bx += b[1] + 6; });
    bx = 66;
    books.slice().reverse().forEach(b => { shelf += `<rect x="${bx}" y="${820 - b[2] + 18}" width="${b[1]}" height="${b[2] - 18}" rx="5" fill="${b[0]}"/>`; bx += b[1] + 6; });
    const body = `<g ${flip ? 'transform="translate(1080,0) scale(-1,1)"' : ''}>
<rect x="-60" y="-60" width="1200" height="2040" fill="url(#gWall)"/>
<ellipse cx="230" cy="330" rx="420" ry="420" fill="url(#gPool)"/>
<rect x="30" y="400" width="290" height="440" rx="12" fill="${P.wood2}"/>
<rect x="46" y="416" width="258" height="196" fill="#5A3216"/><rect x="46" y="628" width="258" height="196" fill="#5A3216"/>
${shelf}
<path d="M690 830V430C690 280 990 280 990 430V830Z" fill="${P.wood}"/>
<path d="M716 806V436C716 316 964 316 964 436V806Z" fill="url(#gSky)"/>
<circle cx="900" cy="430" r="46" fill="#FFF3B0"/>
<path d="M790 806V600" stroke="#6B4A2A" stroke-width="16" stroke-linecap="round"/>
<path d="M790 600C750 560 720 566 706 590M790 600C760 540 740 520 716 520M790 600C800 540 830 520 866 524M790 600C830 566 860 570 880 596M790 600C790 540 800 520 806 500" fill="none" stroke="#2E8B57" stroke-width="15" stroke-linecap="round"/>
<path d="M840 316V806M716 560H964" stroke="${P.wood}" stroke-width="14"/>
<line x1="210" y1="-60" x2="210" y2="140" stroke="${P.brass2}" stroke-width="6"/>
<circle cx="210" cy="250" r="190" fill="url(#gPool)"/>
<path d="M176 140H244L266 230L236 330H184L154 230Z" fill="#FFD76E" stroke="${P.brass2}" stroke-width="9" stroke-linejoin="round"/>
<path d="M716 316H964L470 1000H120Z" fill="#fff" opacity=".13"/>
<rect x="-60" y="866" width="1200" height="10" fill="${P.gold}"/>
<rect x="-60" y="876" width="1200" height="60" fill="url(#bB)"/>
<rect x="-60" y="936" width="1200" height="10" fill="${P.gold}"/>
<rect x="-60" y="946" width="1200" height="1040" fill="url(#zB)"/>
<rect x="-60" y="946" width="1200" height="1040" fill="#3A1E00" opacity=".12"/>
</g>`;
    return wrap(w, h, defs, body);
  };

  // ---- end card background: deep olive green with tatreez eight-pointed stars
  A.bgEnd = function (w, h) {
    const sz = 180, c = sz / 9;
    const ST = ['....#....', '...###...', '..#.#.#..', '.#.###.#.', '#.#####.#', '.#.###.#.', '..#.#.#..', '...###...', '....#....'];
    let st = '';
    ST.forEach((row, y) => row.split('').forEach((ch, x) => { if (ch === '#') st += `<rect x="${f(x * c + 1)}" y="${f(y * c + 1)}" width="${f(c - 2)}" height="${f(c - 2)}" fill="#fff" fill-opacity="${(x + y) % 2 ? .13 : .2}"/>`; }));
    const defs = `<linearGradient id="gEnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B8A4C"/><stop offset=".6" stop-color="#0E6A38"/><stop offset="1" stop-color="#083F22"/></linearGradient>
<radialGradient id="gTop" cx=".5" cy="0" r=".8"><stop offset="0" stop-color="#B5F0C8" stop-opacity=".5"/><stop offset="1" stop-color="#B5F0C8" stop-opacity="0"/></radialGradient>
<pattern id="zO" width="${sz}" height="${sz}" patternUnits="userSpaceOnUse">${st}</pattern>
${band('bO', 46)}`;
    const body = `<rect width="1080" height="1920" fill="url(#gEnd)"/><rect width="1080" height="1920" fill="url(#zO)"/>
<rect width="1080" height="1920" fill="url(#gTop)"/><rect y="0" width="1080" height="46" fill="url(#bO)"/><rect y="1874" width="1080" height="46" fill="url(#bO)"/>
<rect width="1080" height="1920" fill="url(#gVig)" opacity=".7"/>`;
    return wrap(w, h, defs, body);
  };

  // ---- hanging flag pennant on a string, origin at the ceiling hook (same swing hooks as the old lantern)
  A.lantern = function (id, len, k) {
    return `<g id="${id}"><line x1="0" y1="-60" x2="0" y2="${len}" stroke="#6B4A2A" stroke-width="5"/>
<g transform="translate(0,${len}) scale(${k})">
<circle id="${id}g" cx="0" cy="0" r="1" fill="none" opacity="0"/>
<circle cx="0" cy="0" r="10" fill="#6B4A2A"/>
<rect x="-6" y="0" width="12" height="150" rx="4" fill="#8A5A2B"/>
<g transform="translate(6,6)">${A.flag(0, 0, 150, 100)}<rect x="0" y="0" width="150" height="100" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="3"/></g>
<g transform="translate(-6,126)"><path d="M0 0C-26 -8 -46 6 -50 26C-30 24 -12 22 0 0Z M0 0C-4 -26 12 -48 34 -50C32 -30 20 -12 0 0Z" fill="#6E8B3D"/><circle cx="-34" cy="22" r="7" fill="#3E4A1E"/><circle cx="20" cy="-34" r="7" fill="#3E4A1E"/></g>
</g></g>`;
  };

  // ---- meaning stickers (one per phrase), centred on 0,0, about 210 px wide
  A.icon = function (n) {
    const ring = c => `<circle r="108" fill="#fff"/><circle r="95" fill="${c}"/>`;
    const T = 'font-family="Noto Sans,DejaVu Sans,sans-serif" font-weight="700" text-anchor="middle"';
    if (n === 'tag') return ring('#DDF4F1') + `<g transform="rotate(-16)">
<path d="M-66 -40H26L70 0L26 40H-66Q-78 40 -78 28V-28Q-78 -40 -66 -40Z" fill="${P.saffron}"/>
<path d="M-66 -40H26L70 0L26 40H-66Q-78 40 -78 28V-28Q-78 -40 -66 -40Z" fill="none" stroke="#C98A12" stroke-width="5" stroke-linejoin="round"/>
<circle cx="40" cy="0" r="10" fill="#fff" stroke="#C98A12" stroke-width="4"/>
<text x="-24" y="22" font-size="64" fill="${P.ink}" ${T}>?</text></g>
<path d="M36 -12Q64 -52 44 -84" fill="none" stroke="${P.ink}" stroke-width="5" stroke-linecap="round"/>`;
    if (n === 'clock') return ring('#FFEFD9') + `<circle cx="-40" cy="-56" r="21" fill="${P.red}"/><circle cx="40" cy="-56" r="21" fill="${P.red}"/>
<path d="M-44 50L-58 70M44 50L58 70" stroke="${P.ink}" stroke-width="9" stroke-linecap="round"/>
<circle cx="0" cy="2" r="62" fill="#E4572E"/><circle cx="0" cy="2" r="48" fill="#FFFDF6"/>
<path d="M0 -36V-28M0 32V40M-38 2H-30M30 2H38" stroke="#B9AFA0" stroke-width="5" stroke-linecap="round"/>
<path d="M0 2V-28M0 2L22 14" stroke="${P.ink}" stroke-width="8" stroke-linecap="round"/><circle cx="0" cy="2" r="6" fill="${P.ink}"/>
<path d="M-10 -74H10" stroke="${P.ink}" stroke-width="9" stroke-linecap="round"/>`;
    if (n === 'tajine') return ring('#FFEFD9') + `<g transform="translate(0,12)">
<path d="M-30 -66Q-40 -78 -30 -90M0 -72Q-10 -84 0 -96M30 -66Q20 -78 30 -90" fill="none" stroke="#BBAA94" stroke-width="6" stroke-linecap="round"/>
<ellipse cx="0" cy="48" rx="88" ry="22" fill="#8E3F1E"/><ellipse cx="0" cy="42" rx="88" ry="20" fill="#B5532E"/><ellipse cx="0" cy="40" rx="70" ry="13" fill="#7A3418"/>
<path d="M-62 40L-12 -44Q0 -58 12 -44L62 40Q0 56 -62 40Z" fill="${P.terra}"/>
<path d="M-62 40L-12 -44Q0 -58 12 -44L20 -30Q-14 -12 -34 46Q-50 44 -62 40Z" fill="#E28E60" opacity=".85"/>
<path d="M-46 24L-34 12L-22 24L-10 12L2 24L14 12L26 24L38 12L48 24" fill="none" stroke="#FFFDF6" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M-24 -12H24" stroke="#FFFDF6" stroke-width="5" stroke-linecap="round"/>
<circle cx="0" cy="-54" r="12" fill="#8E3F1E"/></g>`;
    if (n === 'what') return ring('#ECE5FF') + `<path d="M-70 -64H70Q88 -64 88 -46V26Q88 44 70 44H2L-34 78V44H-70Q-88 44 -88 26V-46Q-88 -64 -70 -64Z" fill="#7B5CD6"/>
<text x="-34" y="20" font-size="80" fill="#fff" ${T}>?</text><text x="30" y="20" font-size="80" fill="#FFD45C" ${T}>?</text>`;
    return ring('#DDF1FF') + `<g stroke="${P.saffron}" stroke-width="10" stroke-linecap="round"><path d="M-14 -78V-62M-14 46V62M-84 -8H-68M-64 -58L-52 -46M-64 42L-52 30M36 -58L24 -46"/></g>
<circle cx="-14" cy="-8" r="42" fill="#FFC83D"/><circle cx="-26" cy="-20" r="14" fill="#FFE08A"/>
<g fill="#fff" stroke="#B9D3EA" stroke-width="4"><ellipse cx="34" cy="38" rx="50" ry="26"/></g>
<circle cx="10" cy="26" r="24" fill="#fff"/><circle cx="42" cy="16" r="30" fill="#fff"/><ellipse cx="34" cy="40" rx="48" ry="23" fill="#fff"/>`;
  };

  window.A = A;
})();
