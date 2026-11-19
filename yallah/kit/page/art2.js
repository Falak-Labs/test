/* art2.js: lesson 2 extras. Meaning stickers, the big word board and the long desk */
(function () {
  const A = window.A, P = A.P;
  const ring = c => `<circle r="108" fill="#fff"/><circle r="95" fill="${c}"/>`;
  const clip = s => `<g clip-path="url(#cpS)">${s}</g>`;
  const cal = (x, y, r) => `<g transform="rotate(${r} 0 24)"><rect x="${x}" y="${y}" width="46" height="62" rx="7" fill="#fff" stroke="#C9CCD6" stroke-width="3"/><rect x="${x}" y="${y}" width="46" height="17" rx="7" fill="${P.red}"/></g>`;
  const K = {};

  // "I'm angry!": a steaming red face
  K.angry = ring('#FFE3DD') + `<path d="M-52 -60q-13 -9 -2 -21q-12 -10 2 -19M52 -60q13 -9 2 -21q12 -10 -2 -19" fill="none" stroke="#B9AFA0" stroke-width="8" stroke-linecap="round"/>
<circle cy="8" r="62" fill="#EE5340"/><circle cy="8" r="62" fill="none" stroke="#B5301F" stroke-width="5"/>
<path d="M-42 -20L-12 -6M42 -20L12 -6" stroke="#4A0F0A" stroke-width="10" stroke-linecap="round"/>
<circle cx="-24" cy="8" r="9" fill="#fff"/><circle cx="24" cy="8" r="9" fill="#fff"/><circle cx="-22" cy="9" r="4.5" fill="#4A0F0A"/><circle cx="22" cy="9" r="4.5" fill="#4A0F0A"/>
<path d="M-24 46Q0 26 24 46" fill="none" stroke="#4A0F0A" stroke-width="9" stroke-linecap="round"/>`;

  // "I have ten years": ten years kept in a pocket
  K.years = ring('#E6EDFF') + cal(-52, -76, -18) + cal(-23, -86, 3) + cal(8, -76, 22) + `
<path d="M-62 -26H62V24Q62 68 0 80Q-62 68 -62 24Z" fill="#3D63E3"/><path d="M-62 -26H62V-12H-62Z" fill="#2A49B5"/>
<path d="M-50 -4V22Q-50 56 0 66Q50 56 50 22V-4" fill="none" stroke="#F9E08A" stroke-width="4" stroke-dasharray="9 7" stroke-linecap="round"/>
<text y="34" font-size="50" text-anchor="middle" fill="#FFD45C">10</text><text y="56" font-size="17" text-anchor="middle" fill="#fff" letter-spacing="2">YEARS</text>`;

  // "I am ten years old": a birthday cake
  K.cake = ring('#FFE9F0') + `<rect x="-78" y="60" width="156" height="14" rx="7" fill="#C98A12"/>
<rect x="-62" y="6" width="124" height="56" rx="12" fill="#F28BA0"/>
<path d="M-62 28Q-46 46 -31 28T0 28T31 28T62 28V16Q62 6 50 6H-50Q-62 6 -62 16Z" fill="#FFFDF6"/>
<circle cx="-36" cy="48" r="5" fill="#FFD45C"/><circle cx="0" cy="50" r="5" fill="#7BD0C8"/><circle cx="36" cy="48" r="5" fill="#FFD45C"/>
<text y="2" font-size="62" text-anchor="middle" fill="${P.cobalt}" stroke="#fff" stroke-width="7" class="fat">10</text>
<path d="M-18 -76q10 12 0 22q-10 -10 0 -22ZM18 -76q10 12 0 22q-10 -10 0 -22Z" fill="#F2B134"/>`;

  // "The cold hit me": an ice cube with a boxing glove
  K.cold = ring('#DDF1FF') + `<path d="M-62 -66l8 11M-30 -74l2 13M2 -66l-6 11" stroke="#3E97DB" stroke-width="5" stroke-linecap="round"/>
<rect x="-74" y="-40" width="88" height="88" rx="18" fill="#9AD8FF" stroke="#3E97DB" stroke-width="5"/>
<path d="M-60 -24h22M-60 -12h10" stroke="#fff" stroke-width="6" stroke-linecap="round"/>
<path d="M-56 -2l18 9M-6 -2l-18 9" stroke="${P.navy}" stroke-width="7" stroke-linecap="round"/>
<circle cx="-45" cy="14" r="5" fill="${P.navy}"/><circle cx="-17" cy="14" r="5" fill="${P.navy}"/>
<path d="M-44 30q13 10 26 0" fill="none" stroke="${P.navy}" stroke-width="5" stroke-linecap="round"/>
<path d="M14 6h22" stroke="#9AD8FF" stroke-width="18" stroke-linecap="round"/>
<circle cx="58" cy="4" r="27" fill="${P.red}"/><circle cx="45" cy="-18" r="11" fill="${P.red}"/><rect x="26" y="-10" width="13" height="28" rx="5" fill="#FFFDF6"/>
<polygon points="${A.star(78, -54, 23, 0, 0.45)}" fill="#FFD23F"/>`;

  // "I caught a cold": red nose, thermometer, scarf
  K.sick = ring('#FFF3D6') + `<circle cy="-6" r="60" fill="#F6CFA6"/>
<path d="M-42 -18q11 -11 22 0M20 -18q11 -11 22 0" fill="none" stroke="#4A2D1D" stroke-width="7" stroke-linecap="round"/>
<ellipse cx="-38" cy="14" rx="13" ry="8" fill="#F38E88" opacity=".6"/><ellipse cx="38" cy="14" rx="13" ry="8" fill="#F38E88" opacity=".6"/>
<circle cy="6" r="13" fill="#E4572E"/><path d="M-20 32h20" stroke="#9A3B34" stroke-width="6" stroke-linecap="round"/>
<g transform="rotate(-22 4 32)"><rect x="2" y="26" width="64" height="12" rx="6" fill="#fff" stroke="#B9AFA0" stroke-width="3"/><circle cx="68" cy="32" r="9" fill="${P.red}"/></g>
<path d="M-56 36Q0 74 56 36L64 62Q0 104 -64 62Z" fill="${P.teal}"/><path d="M22 74l16 34h-30Z" fill="#17958E"/>
<path d="M58 -58q11 17 0 26q-11 -9 0 -26Z" fill="#6EC3F4"/>`;

  // "Hit me a phone": a bandaged phone
  K.phone = ring('#FFE3DD') + `<g transform="rotate(16)"><rect x="-38" y="-68" width="76" height="134" rx="15" fill="${P.ink}"/><rect x="-29" y="-56" width="58" height="100" rx="6" fill="#BFE6FF"/>
<path d="M-8 -56l-9 30l17 13l-11 30l15 27" fill="none" stroke="${P.ink}" stroke-width="4" stroke-linejoin="round"/><circle cy="55" r="5" fill="#BFE6FF"/>
<g transform="rotate(-38 0 -4)"><rect x="-46" y="-17" width="92" height="26" rx="11" fill="#F1C99B" stroke="#C98A12" stroke-width="3"/><rect x="-14" y="-17" width="28" height="26" fill="#FBE3C2"/></g></g>
<polygon points="${A.star(66, -56, 25, 0, 0.45)}" fill="#FFD23F"/><polygon points="${A.star(-68, -44, 16, 0, 0.45)}" fill="#FFD23F"/>
<path d="M-74 26l-16 8M-70 46l-14 14" stroke="${P.red}" stroke-width="6" stroke-linecap="round"/>`;

  // "Call me!": a ringing phone
  K.ring = ring('#DDF4F1') + `<path d="M-56 -30q-15 30 0 60M-76 -44q-24 44 0 88M56 -30q15 30 0 60M76 -44q24 44 0 88" fill="none" stroke="${P.teal}" stroke-width="7" stroke-linecap="round"/>
<rect x="-38" y="-68" width="76" height="136" rx="15" fill="${P.ink}"/><rect x="-29" y="-56" width="58" height="104" rx="6" fill="#EFFFF6"/><circle cy="58" r="5" fill="#EFFFF6"/>
<circle cy="-6" r="23" fill="#2BB673"/>
<path d="M-11 -11q-3 9 5 17q8 8 17 5l2 -7l-7 -4l-4 3q-5 -3 -7 -7l3 -4l-4 -7Z" fill="#fff"/>`;

  // "I cut the road": scissors through the asphalt
  K.cut = ring('#EFE9DC') + clip(`<g transform="rotate(-12)"><rect x="-110" y="-14" width="220" height="64" fill="#4A4A55"/>
<path d="M-96 18h28M-52 18h28M30 18h28M74 18h28" stroke="#fff" stroke-width="7"/>
<path d="M6 -22l-11 15l13 12l-13 14l13 13l-9 18" fill="none" stroke="#EFE9DC" stroke-width="13" stroke-linejoin="round"/></g>`) + `
<path d="M-12 -58L12 -2M14 -58L-10 -2" stroke="#8D99AE" stroke-width="10" stroke-linecap="round"/><circle cx="1" cy="-31" r="5" fill="${P.ink}"/>
<circle cx="-20" cy="-72" r="15" fill="none" stroke="${P.red}" stroke-width="9"/><circle cx="22" cy="-72" r="15" fill="none" stroke="${P.red}" stroke-width="9"/>`;

  // "I crossed the road": a zebra crossing
  K.cross = ring('#E3F6E8') + clip(`<rect x="-110" y="-4" width="220" height="74" fill="#4A4A55"/>
<path d="M-70 2v62M-42 2v62M-14 2v62M14 2v62M42 2v62M70 2v62" stroke="#fff" stroke-width="16"/>`) + `
<circle cx="2" cy="-68" r="13" fill="#2BB673"/>
<path d="M0 -52v32M0 -42l-19 15M0 -42l19 10M0 -20l-15 28M0 -20l17 25" fill="none" stroke="#2BB673" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`;

  // "No hitting!"
  K.nohit = `<circle r="108" fill="#fff"/><circle r="86" fill="#FFF6F0" stroke="${P.red}" stroke-width="16"/>
<rect x="-52" y="-2" width="32" height="36" rx="13" fill="#EDB98F" stroke="#B9794F" stroke-width="4"/>
<rect x="-38" y="-30" width="76" height="62" rx="19" fill="#EDB98F" stroke="#B9794F" stroke-width="4"/>
<path d="M-19 -28v22M0 -28v22M19 -28v22" stroke="#B9794F" stroke-width="4" stroke-linecap="round"/>
<path d="M-60 -60L60 60" stroke="${P.red}" stroke-width="16" stroke-linecap="round"/>`;

  // "Let's hit the road!": off we go
  K.road = ring('#BFE6FF') + clip(`<rect x="-110" y="8" width="220" height="110" fill="#7CC36A"/>
<path d="M-14 8H14L78 110H-78Z" fill="#4A4A55"/><path d="M0 16v12M0 40v18M0 72v26" stroke="#fff" stroke-width="6"/>`) + `
<circle cx="54" cy="-46" r="20" fill="#FFC83D"/><path d="M-80 -42h34a14 14 0 0 0 -24 -12a16 16 0 0 0 -10 12Z" fill="#fff"/>
<g transform="translate(-4,36)"><path d="M-42 6Q-42 -8 -28 -10L-18 -29Q-14 -35 -6 -35H18Q26 -35 30 -29L40 -10Q48 -8 48 6V15H-42Z" fill="#E4572E"/>
<path d="M-14 -12L-7 -27H9V-12ZM15 -12V-27H20L29 -12Z" fill="#DDF1FF"/><circle cx="-21" cy="17" r="11" fill="${P.ink}"/><circle cx="27" cy="17" r="11" fill="${P.ink}"/>
<circle cx="-21" cy="17" r="4" fill="#B9AFA0"/><circle cx="27" cy="17" r="4" fill="#B9AFA0"/></g>
<path d="M-90 30h26M-86 48h18" stroke="#fff" stroke-width="6" stroke-linecap="round"/>`;

  A.STK = ['angry', 'tajine', 'years', 'cake', 'cold', 'sick', 'phone', 'ring', 'cut', 'cross', 'nohit', 'road'];
  A.stk = n => n === 'tajine' ? A.icon('tajine') : K[n];

  // big chalkboard for the hard word (live SVG, so the word can be animated on it)
  A.bigBoard = function (x, y, w, h) {
    return `<g><rect x="${x - 34}" y="${y + h + 20}" width="${w + 68}" height="26" rx="9" fill="${P.wood2}"/>
<rect x="${x - 26}" y="${y - 26}" width="${w + 52}" height="${h + 52}" rx="26" fill="url(#gWoodL)"/>
<rect x="${x - 26}" y="${y - 26}" width="${w + 52}" height="${h + 52}" rx="26" fill="none" stroke="#5E3413" stroke-opacity=".45" stroke-width="4"/>
<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="url(#gBoardL)"/>
<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="none" stroke="#0C2A20" stroke-opacity=".55" stroke-width="7"/>
<ellipse cx="${x + w * 0.3}" cy="${y + h * 0.84}" rx="${w * 0.26}" ry="${h * 0.07}" fill="#fff" opacity=".05"/>
<ellipse cx="${x + w * 0.74}" cy="${y + h * 0.2}" rx="${w * 0.2}" ry="${h * 0.07}" fill="#fff" opacity=".045"/>
<rect x="${x + 50}" y="${y + h + 10}" width="52" height="13" rx="6" fill="#FFFDF6"/><rect x="${x + 114}" y="${y + h + 10}" width="40" height="13" rx="6" fill="#FFD45C"/>
<rect x="${x + w - 150}" y="${y + h + 6}" width="96" height="18" rx="5" fill="#5B4636"/></g>`;
  };

  // one long desk for the two pupils. Y = top edge, xs = where each pupil sits
  A.desk = function (Y, xs) {
    const nb = x => `<ellipse cx="${x}" cy="${Y + 60}" rx="236" ry="26" fill="#5A3210" opacity=".14"/>
<path d="M${x - 116} ${Y + 16}H${x + 96}L${x + 126} ${Y + 86}H${x - 150}Z" fill="#FFFDF6"/><path d="M${x - 8} ${Y + 16}L${x - 10} ${Y + 86}" stroke="#D8CFC0" stroke-width="4"/>
<path d="M${x - 100} ${Y + 34}H${x - 24}M${x - 108} ${Y + 50}H${x - 24}M${x - 116} ${Y + 66}H${x - 26}M${x + 10} ${Y + 34}H${x + 88}M${x + 10} ${Y + 50}H${x + 96}M${x + 10} ${Y + 66}H${x + 104}" stroke="#B9C4D6" stroke-width="3.5" stroke-linecap="round"/>`;
    return `<g><path d="M-80 ${Y}H1160V2000H-80Z" fill="url(#gDesk)"/><rect x="-80" y="${Y}" width="1240" height="11" fill="#fff" opacity=".3"/>
<path d="M-80 ${Y + 124}Q300 ${Y + 108} 640 ${Y + 128}T1160 ${Y + 116}" fill="none" stroke="#8E5A2B" stroke-width="3" opacity=".22"/>
${nb(xs[0])}${nb(xs[1])}
<g transform="rotate(-10 540 ${Y + 112})"><rect x="505" y="${Y + 96}" width="70" height="34" rx="8" fill="#F28BA0"/><rect x="505" y="${Y + 96}" width="25" height="34" rx="8" fill="#5E8BE0"/></g>
<path d="M-80 ${Y + 540}H1160V2000H-80Z" fill="#8F5A2A"/><rect x="-80" y="${Y + 532}" width="1240" height="10" fill="#EBC592" opacity=".55"/>
${[0, 1, 2, 3, 4, 5, 6].map(i => `<polygon points="${A.star(i * 180, Y + 690, 46, 0)}" fill="#C58A4A" opacity=".55"/><polygon points="${A.star(i * 180, Y + 690, 24, 22.5)}" fill="#7A4520" opacity=".6"/>`).join('')}</g>`;
  };
})();
