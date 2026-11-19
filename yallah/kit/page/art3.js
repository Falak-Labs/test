/* art3.js: meaning stickers for episode 1 (one per phrase), centred on 0,0, about 210 px wide */
(function () {
  const A = window.A, P = A.P;
  const ring = c => `<circle r="108" fill="#fff"/><circle r="95" fill="${c}"/>`;
  const SK = '#EDB98F', SKL = '#B9794F';
  const finger = (x, h) => `<rect x="${x}" y="${-10 - h}" width="15" height="${h + 12}" rx="7.5" fill="${SK}" stroke="${SKL}" stroke-width="3.5"/>`;
  // an open hand, waving
  const hand = (c, col) => ring(c) + `<path d="M56 -50q17 17 9 40M72 -66q28 28 15 64M-62 -34q-12 14 -6 30" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round"/>
<g transform="rotate(-14 0 10)">${finger(-33, 44)}${finger(-16, 56)}${finger(1, 54)}${finger(18, 42)}
<path d="M-30 14L-56 -6" stroke="${SKL}" stroke-width="22" stroke-linecap="round"/><path d="M-30 14L-56 -6" stroke="${SK}" stroke-width="15" stroke-linecap="round"/>
<rect x="-35" y="-18" width="70" height="76" rx="26" fill="${SK}" stroke="${SKL}" stroke-width="3.5"/><rect x="-31" y="-24" width="62" height="22" fill="${SK}"/>
<path d="M-18 26q18 12 36 0" fill="none" stroke="${SKL}" stroke-width="3.5" stroke-linecap="round" opacity=".7"/></g>`;
  const face = (c, brows, mouth, extra) => ring(c) + `<circle r="62" fill="#FFC83D" stroke="#E0A93E" stroke-width="5"/>
<ellipse cx="-23" cy="-10" rx="7.5" ry="10.5" fill="#4A2D1D"/><ellipse cx="23" cy="-10" rx="7.5" ry="10.5" fill="#4A2D1D"/>
<ellipse cx="-40" cy="14" rx="12" ry="8" fill="#F38E88" opacity=".6"/><ellipse cx="40" cy="14" rx="12" ry="8" fill="#F38E88" opacity=".6"/>${brows}
<path d="${mouth}" fill="none" stroke="#4A2D1D" stroke-width="8" stroke-linecap="round"/>${extra}`;
  const badge = (txt, size, y) => ring('#E6EDFF') + `<g transform="rotate(-6)"><rect x="-82" y="-58" width="164" height="116" rx="17" fill="#fff" stroke="${P.red}" stroke-width="5"/>
<path d="M-82 -20V-41Q-82 -58 -65 -58H65Q82 -58 82 -41V-20Z" fill="${P.red}"/>
<text y="-31" font-size="19" text-anchor="middle" fill="#fff" letter-spacing="1.5">MY NAME IS</text>
<text y="${y}" font-size="${size}" text-anchor="middle" fill="${P.navy}">${txt}</text></g>`;
  const K = {};
  K.wave = hand('#FFF3D6', P.teal);
  K.bye = hand('#DDF1FF', P.saffron);
  K.smile = face('#E3F6E8', '', 'M-34 12Q0 50 34 12', `<path d="M58 -74q3 17 20 20q-17 3 -20 20q-3 -17 -20 -20q17 -3 20 -20Z" fill="#FFD23F"/>`);
  K.sorry = face('#E6EDFF', `<path d="M-42 -28L-14 -38M42 -28L14 -38" stroke="#4A2D1D" stroke-width="7" stroke-linecap="round"/>`, 'M-22 36Q0 20 22 36',
    `<path d="M58 -56q11 17 0 26q-11 -9 0 -26Z" fill="#6EC3F4"/>`);
  K.name_q = badge('?', 66, 40);
  K.name_lina = badge('Lina', 46, 32);
  K.globe = ring('#DDF1FF') + `<circle cy="10" r="58" fill="#4FA3E3" stroke="#2E78B8" stroke-width="5"/>
<path d="M-42 -8q8 -24 30 -22q10 10 -2 20q0 14 -16 18q-12 -4 -12 -16ZM6 4q20 -10 32 6q4 18 -10 28q-18 4 -22 -16ZM-22 42q10 -8 20 2q-4 14 -16 12Z" fill="#6CC06A"/>
<path d="M-58 10H58M0 -48V68M-41 -31Q0 -15 41 -31M-41 51Q0 35 41 51" fill="none" stroke="#fff" stroke-width="3" opacity=".45"/>
<path d="M46 -86c-15 0 -26 11 -26 25c0 18 26 42 26 42s26 -24 26 -42c0 -14 -11 -25 -26 -25Z" fill="${P.red}" stroke="#fff" stroke-width="4"/><circle cx="46" cy="-61" r="10" fill="#fff"/>`;
  K.water = ring('#DDF4F1') + `<path d="M-44 -60H44L33 64H-33Z" fill="#fff" opacity=".8"/>
<path d="M-39 -8q10 -9 19.500 0t19.500 0t19.500 0t19.500 0L33 64H-33Z" fill="#59B7F0"/>
<path d="M-44 -60H44L33 64H-33Z" fill="none" stroke="#6FA9CC" stroke-width="6" stroke-linejoin="round"/>
<path d="M-27 -42L-21 46" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".75"/>
<path d="M66 -58q12 18 0 28q-12 -10 0 -28Z" fill="#59B7F0"/><path d="M-70 -30q9 13 0 21q-9 -8 0 -21Z" fill="#59B7F0"/>`;
  K.wc = ring('#EFE9DC') + `<rect x="-64" y="-64" width="128" height="128" rx="24" fill="${P.cobalt}"/>
<rect x="-53" y="-53" width="106" height="106" rx="16" fill="none" stroke="#fff" stroke-width="4" opacity=".55"/>
<text y="21" font-size="60" text-anchor="middle" fill="#fff">WC</text>`;
  K.again = ring('#ECE5FF') + `<g fill="none" stroke="#7B5CD6" stroke-width="15" stroke-linecap="round"><path d="M-52 -4A52 52 0 0 1 30 -43"/><path d="M52 4A52 52 0 0 1 -30 43"/></g>
<path d="M18 -68L58 -42L20 -18Z" fill="#7B5CD6"/><path d="M-18 68L-58 42L-20 18Z" fill="#7B5CD6"/>`;
  K.heart = ring('#FFE9F0') + `<path d="M0 62C-58 22 -72 -8 -72 -30C-72 -54 -54 -68 -36 -68C-19 -68 -6 -58 0 -45C6 -58 19 -68 36 -68C54 -68 72 -54 72 -30C72 -8 58 22 0 62Z" fill="#E4405F" stroke="#B5223F" stroke-width="5" stroke-linejoin="round"/>
<path d="M-46 -34q4 -17 21 -19" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".8"/>`;
  K.flower = ring('#FFF3D6') + `<path d="M0 44q-28 4 -38 30q28 4 38 -30ZM0 44q28 4 38 30q-28 4 -38 -30Z" fill="#6CC06A"/>` +
    [0, 1, 2, 3, 4, 5].map(k => { const a = (k * 60 - 90) * Math.PI / 180; return `<circle cx="${(36 * Math.cos(a)).toFixed(1)}" cy="${(36 * Math.sin(a) - 10).toFixed(1)}" r="25" fill="#F28BA0" stroke="#D96A84" stroke-width="3.5"/>`; }).join('') +
    `<circle cy="-10" r="22" fill="#FFC83D" stroke="#E0A93E" stroke-width="4"/>`;
  K.tomorrow = ring('#FFEFD9') + `<rect x="-64" y="-50" width="128" height="114" rx="15" fill="#fff" stroke="#C9CCD6" stroke-width="4"/>
<path d="M-64 -20V-35Q-64 -50 -49 -50H49Q64 -50 64 -35V-20Z" fill="${P.red}"/>
<path d="M-32 -64v22M32 -64v22" stroke="#5B4636" stroke-width="9" stroke-linecap="round"/>
<circle cx="-6" cy="24" r="19" fill="#FFC83D"/><g stroke="#F2B134" stroke-width="6" stroke-linecap="round"><path d="M-6 -6v-7M-6 54v7M-36 24h-7M24 24h7M-27 3l-5 -5M15 3l5 -5M-27 45l-5 5M15 45l5 5"/></g>
<circle cx="54" cy="52" r="24" fill="#2BB673" stroke="#fff" stroke-width="5"/><text x="54" y="62" font-size="27" text-anchor="middle" fill="#fff">+1</text>`;

  // ---- episode 2: restaurant and market
  const gold = '#F2B134', goldD = '#C98A1E';
  const coin = (x, y, r, t) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${gold}" stroke="${goldD}" stroke-width="5"/><circle cx="${x}" cy="${y}" r="${r - 9}" fill="none" stroke="#FFE08A" stroke-width="3"/><text x="${x}" y="${y + r * .36}" font-size="${r * 1.05}" text-anchor="middle" fill="#fff" stroke="${goldD}" stroke-width="1.5">${t}</text>`;
  K.table2 = ring('#FFEFD9') + `<path d="M-8 4H8L14 58H-14Z" fill="#8A5226"/><ellipse cy="64" rx="38" ry="9" fill="#8A5226"/>
<ellipse cy="2" rx="68" ry="24" fill="#8A5226"/><ellipse cy="-4" rx="68" ry="24" fill="#C98A4E"/>
<ellipse cx="-26" cy="-6" rx="19" ry="7" fill="#fff"/><ellipse cx="26" cy="-6" rx="19" ry="7" fill="#fff"/><ellipse cx="-26" cy="-7" rx="10" ry="3.5" fill="#E9E1D3"/><ellipse cx="26" cy="-7" rx="10" ry="3.5" fill="#E9E1D3"/>
<path d="M0 -14V-44" stroke="#fff" stroke-width="7" stroke-linecap="round"/><path d="M0 -44Q-9 -60 0 -70Q9 -60 0 -44Z" fill="#FFC83D"/>
<circle cx="56" cy="-52" r="25" fill="#2BB673" stroke="#fff" stroke-width="5"/><text x="56" y="-42" font-size="31" text-anchor="middle" fill="#fff">2</text>`;
  K.menu = ring('#FFF3D6') + `<g transform="rotate(-5)"><rect x="-48" y="-68" width="96" height="136" rx="12" fill="#fff" stroke="#C9CCD6" stroke-width="4"/>
<path d="M-48 -32V-56Q-48 -68 -36 -68H36Q48 -68 48 -56V-32Z" fill="${P.red}"/><text y="-41" font-size="25" text-anchor="middle" fill="#fff" letter-spacing="2">MENU</text>
<g stroke="#B9C4D6" stroke-width="5" stroke-linecap="round"><path d="M-30 -10H8M-30 12H12M-30 34H4"/></g><g fill="${P.red}"><circle cx="30" cy="-10" r="4.5"/><circle cx="30" cy="12" r="4.5"/><circle cx="30" cy="34" r="4.5"/></g></g>`;
  K.chicken = ring('#FFEFD9') + `<path d="M12 14L50 52" stroke="#F4EAD8" stroke-width="15" stroke-linecap="round"/><circle cx="48" cy="62" r="10" fill="#F4EAD8"/><circle cx="62" cy="48" r="10" fill="#F4EAD8"/>
<ellipse cx="-12" cy="-12" rx="50" ry="40" transform="rotate(-40 -12 -12)" fill="#D98A3D" stroke="#A8641F" stroke-width="5"/>
<path d="M-40 -22Q-30 -52 -4 -54" fill="none" stroke="#F3C98F" stroke-width="9" stroke-linecap="round"/><circle cx="6" cy="-4" r="5" fill="#A8641F" opacity=".5"/><circle cx="-22" cy="12" r="4" fill="#A8641F" opacity=".5"/>`;
  K.onion = ring('#F1E6FF') + `<path d="M0 -62Q6 -40 4 -26" fill="none" stroke="#6CC06A" stroke-width="9" stroke-linecap="round"/>
<path d="M0 -34Q-66 -10 -50 34Q-36 68 0 68Q36 68 50 34Q66 -10 0 -34Z" fill="#C77DD6" stroke="#9A55AD" stroke-width="5" stroke-linejoin="round"/>
<path d="M0 -30Q-32 6 -14 64M0 -30Q32 6 14 64" fill="none" stroke="#E9C6F0" stroke-width="5" stroke-linecap="round"/>
<circle r="70" fill="none" stroke="#E4405F" stroke-width="13"/><path d="M-50 -50L50 50" stroke="#E4405F" stroke-width="13" stroke-linecap="round"/>`;
  K.cold = ring('#E3F2FF') + `<g stroke="#3F93DB" stroke-width="10" stroke-linecap="round" fill="none">` +
    [0, 60, 120].map(a => `<g transform="rotate(${a})"><path d="M0 -70V70"/><path d="M-16 -52L0 -38L16 -52M-16 52L0 38L16 52"/></g>`).join('') + `</g><circle r="10" fill="#fff" stroke="#3F93DB" stroke-width="5"/>`;
  K.yum = ring('#E3F6E8') + `<rect x="-66" y="2" width="30" height="64" rx="8" fill="#5E8BE0"/>
<path d="M-30 -2L-8 -50Q-2 -66 14 -62Q30 -56 24 -36L18 -8H52Q68 -8 66 8L62 22Q70 32 64 42Q70 52 62 62Q64 72 50 70H-30Z" fill="${SK}" stroke="${SKL}" stroke-width="4" stroke-linejoin="round"/>
<path d="M20 20H58M16 42H56" stroke="${SKL}" stroke-width="3.5" stroke-linecap="round" opacity=".6"/>
<path d="M58 -66q3 17 20 20q-17 3 -20 20q-3 -17 -20 -20q17 -3 20 -20Z" fill="#FFD23F"/>`;
  K.bill = ring('#EFE9DC') + `<path d="M-46 -66H46V60L35 51L23 60L12 51L0 60L-12 51L-23 60L-35 51L-46 60Z" fill="#fff" stroke="#C9CCD6" stroke-width="4" stroke-linejoin="round"/>
<g stroke="#B9C4D6" stroke-width="5" stroke-linecap="round"><path d="M-28 -44H8M-28 -26H14M-28 -8H2"/></g><path d="M-28 14H28" stroke="${P.ink}" stroke-width="4" stroke-linecap="round"/>
<text x="-4" y="42" font-size="21" text-anchor="middle" fill="${P.ink}">TOTAL</text>` + coin(44, -44, 24, '$');
  const arc = r => { const q = (r * .7071).toFixed(1), y = (46 - r * .7071).toFixed(1); return `<path d="M${-q} ${y}A${r} ${r} 0 0 1 ${q} ${y}"/>`; };
  K.wifi = ring('#E6EDFF') + `<g fill="none" stroke="${P.cobalt}" stroke-width="12" stroke-linecap="round">${arc(30)}${arc(54)}${arc(78)}</g><circle cy="46" r="10" fill="${P.cobalt}"/>`;
  K.coins = ring('#FFF3D6') + [2, 1, 0].map(k => { const y = 36 - k * 24; return `<path d="M-50 ${y}v14Q-50 66 0 ${y + 32}Q50 66 50 ${y + 14}v-14Z" fill="${goldD}"/><ellipse cy="${y}" rx="50" ry="17" fill="${gold}" stroke="${goldD}" stroke-width="4"/><ellipse cy="${y}" rx="34" ry="10" fill="none" stroke="#FFE08A" stroke-width="3"/>`; }).join('') +
    `<path d="M58 -58q3 17 20 20q-17 3 -20 20q-3 -17 -20 -20q17 -3 20 -20Z" fill="#fff"/>`;
  const arrow = (c, up) => `<path d="${up ? 'M56 -56L84 -14H66V46H46V-14H28Z' : 'M56 56L84 14H66V-46H46V14H28Z'}" fill="${c}" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>`;
  K.pricey = ring('#FFE3DC') + `<g transform="translate(-8,4) scale(.92)">` + coin(-18, 6, 50, '$') + arrow('#E4405F', true) + '</g>';
  K.down = ring('#DFF5E8') + `<g transform="translate(-8,-2) scale(.92)">` + coin(-18, 6, 50, '$') + arrow('#2BB673', false) + '</g>';
  K.bag = ring('#FFE9F0') + `<path d="M-28 -24V-44Q-28 -64 0 -64Q28 -64 28 -44V-24" fill="none" stroke="#8A5A44" stroke-width="9" stroke-linecap="round"/>
<path d="M-54 -26H54L60 60Q60 70 50 70H-50Q-60 70 -60 60Z" fill="#F28BA0" stroke="#D96A84" stroke-width="5" stroke-linejoin="round"/>
<path d="M0 8l9 20l22 2l-17 15l5 22l-19 -12l-19 12l5 -22l-17 -15l22 -2Z" fill="#fff"/>`;
  K.morocco = ring('#FFE9E6') + `<rect x="-72" y="-56" width="9" height="118" rx="4" fill="#8A5A44"/><path d="M-67 -62Q-34 -76 0 -62T66 -62V28Q33 42 0 28T-67 28Z" fill="#C1272D" stroke="#9E1B20" stroke-width="3"/>
<path d="M0 -42L-15 4L24 -24H-24L15 4Z" transform="translate(0,-1) scale(1.1)" fill="none" stroke="#0A7A3E" stroke-width="5.5" stroke-linejoin="round"/>`;
  // "nice to meet you": two hands shaking
  K.handshake = ring('#E8F7EE') + `<path d="M-20 -62l-9 -19M0 -68v-22M20 -62l9 -19" stroke="#FFC83D" stroke-width="8" stroke-linecap="round"/>
<path d="M-98 34L-36 2" stroke="#2E5FB5" stroke-width="52"/><path d="M-98 34L-36 2" stroke="#4F86E0" stroke-width="44"/>
<path d="M98 34L36 2" stroke="#B5391A" stroke-width="52"/><path d="M98 34L36 2" stroke="#E4572E" stroke-width="44"/>
<path d="M-44 6L14 22" stroke="${SKL}" stroke-width="46" stroke-linecap="round"/><path d="M-44 6L14 22" stroke="${SK}" stroke-width="39" stroke-linecap="round"/>
<path d="M44 6L-10 20" stroke="#A9683F" stroke-width="46" stroke-linecap="round"/><path d="M44 6L-10 20" stroke="#DBA273" stroke-width="39" stroke-linecap="round"/>
<path d="M-26 4q9 -10 18 0M-8 8q9 -10 18 0M10 12q9 -10 18 0" fill="none" stroke="#A9683F" stroke-width="5" stroke-linecap="round"/>
<rect x="-60" y="-12" width="13" height="40" rx="5" transform="rotate(-27 -53 8)" fill="#FFFDF6"/><rect x="47" y="-12" width="13" height="40" rx="5" transform="rotate(27 53 8)" fill="#FFFDF6"/>`;
  // "how old are you?": a cake with a question mark
  K.age_q = ring('#FFE9F0') + `<rect x="-78" y="60" width="156" height="14" rx="7" fill="#C98A12"/>
<rect x="-62" y="6" width="124" height="56" rx="12" fill="#F28BA0"/>
<path d="M-62 28Q-46 46 -31 28T0 28T31 28T62 28V16Q62 6 50 6H-50Q-62 6 -62 16Z" fill="#FFFDF6"/>
<circle cx="-36" cy="48" r="5" fill="#FFD45C"/><circle cx="0" cy="50" r="5" fill="#7BD0C8"/><circle cx="36" cy="48" r="5" fill="#FFD45C"/>
<text y="4" font-size="84" text-anchor="middle" fill="${P.cobalt}" stroke="#fff" stroke-width="8" class="fat">?</text>`;
  // "I'm from Palestine": the flag on a pole
  K.palestine = ring('#E9F6EC') + `<rect x="-72" y="-56" width="9" height="118" rx="4" fill="#8A5A44"/>
<clipPath id="cpPsF"><path d="M-67 -62Q-34 -76 0 -62T66 -62V28Q33 42 0 28T-67 28Z"/></clipPath>
<g clip-path="url(#cpPsF)"><rect x="-70" y="-80" width="140" height="50" fill="#111"/><rect x="-70" y="-30" width="140" height="30" fill="#fff"/><rect x="-70" y="0" width="140" height="50" fill="#0B8A3C"/>
<path d="M-67 -80L-14 -16L-67 46Z" fill="#CE1126"/></g>
<path d="M-67 -62Q-34 -76 0 -62T66 -62V28Q33 42 0 28T-67 28Z" fill="none" stroke="#2A2A2A" stroke-opacity=".55" stroke-width="3"/>`;
  A.stk3 = n => K[n] || (A.STK && A.STK.indexOf(n) >= 0 ? A.stk(n) : A.icon(n));
})();
