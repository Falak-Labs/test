// Render several frames as JPEG stills with one bundle (fast checks before a full render).
// usage: node tools/stills.mjs <Composition> <outDir> <frame> [frame...]
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition, openBrowser} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

const [comp, outDir, ...frames] = process.argv.slice(2);
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const browser = await openBrowser('chrome', {browserExecutable: process.env.REMOTION_CHROME || null,
  chromiumOptions: {gl: 'swangle'}});
const composition = await selectComposition({serveUrl, id: comp, puppeteerInstance: browser});
for (const fr of frames) {
  const output = path.join(outDir, `${comp}_${String(fr).padStart(5, '0')}.jpg`);
  await renderStill({composition, serveUrl, output, frame: Number(fr), imageFormat: 'jpeg', jpegQuality: 92, puppeteerInstance: browser});
  console.log(output);
}
await browser.close({silent: true});
