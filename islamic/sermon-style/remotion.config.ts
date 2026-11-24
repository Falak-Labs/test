import {Config} from '@remotion/cli/config';

Config.setEntryPoint('src/index.ts');
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setCrf(18);
Config.setPixelFormat('yuv420p');
Config.setChromiumOpenGlRenderer('swangle');
// Uses the system Chrome when REMOTION_CHROME is set (e.g. /usr/bin/google-chrome); otherwise Remotion downloads its own
if (process.env.REMOTION_CHROME) {
  Config.setBrowserExecutable(process.env.REMOTION_CHROME);
}
