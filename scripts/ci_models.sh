#!/usr/bin/env bash
# Fetch the voice and speech-check models a production job needs into $TTS_HOME (cached between runs).
#   bash scripts/ci_models.sh "en,ar"
set -euo pipefail
langs="$1"
: "${TTS_HOME:?}"
mkdir -p "$TTS_HOME/asr"
get() {  # url dest
  if [ ! -s "$2" ]; then
    curl -fL --retry 6 --retry-delay 5 --retry-all-errors -o "$2.part" "$1"
    mv "$2.part" "$2"
  fi
}
asr() {  # sherpa-onnx whisper model name
  if [ ! -d "$TTS_HOME/asr/sherpa-onnx-whisper-$1" ]; then
    curl -fL --retry 6 --retry-delay 5 --retry-all-errors \
      "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-$1.tar.bz2" | tar xj -C "$TTS_HOME/asr"
  fi
}
if [[ ",$langs," == *",ar,"* ]]; then
  d="$TTS_HOME/namaa-saudi"; mkdir -p "$d"
  for f in t3_mtl23ls_v2.safetensors s3gen.safetensors ve.safetensors conds.pt mtl_tokenizer.json tokenizer.json README.md; do
    get "https://huggingface.co/NAMAA-Space/NAMAA-Saudi-TTS/resolve/main/$f" "$d/$f"
  done
  get "https://huggingface.co/ResembleAI/chatterbox/resolve/main/grapheme_mtl_merged_expanded_v1.json" "$d/grapheme_mtl_merged_expanded_v1.json"
  asr small
fi
if [[ ",$langs," == *",en,"* ]]; then
  asr base.en
fi
du -sh "$TTS_HOME"/* 2>/dev/null || true
