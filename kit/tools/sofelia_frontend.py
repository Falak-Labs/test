# Vendored from hamdallah/Sofelia-TTS-82M (Apache-2.0), unchanged except this header.
# Reviewed Nov 8 2026: pure text normalization + lexicon lookup, no I/O beyond reading ar_lexicon.json.
"""
Sofelia TTS — Palestinian Arabic text frontend.

espeak-ng's Arabic G2P underspecifies dialect pronunciation. This module fixes
the systematic issues before phonemization:
  - Arabic punctuation (،؛؟) -> Latin (,;?) so the model gets pause/question cues
  - word-final ة read as /t/ for out-of-lexicon words -> rewritten to a bare fatha
  - a small Palestinian pronunciation lexicon (ar_lexicon.json) for words espeak
    mis-reads or strips vowels from (هيك، وين، تنين، قلت، معلش، ...)
Then, after G2P, phonemes outside Kokoro's 178-token vocab are remapped:
  ħ->ʰ, ʕ->ʁ, ˤ->ᵊ, dental diacritic and []-> dropped.
"""

import json
import re
from pathlib import Path

PHONEME_FIXUPS = {
    "ħ": "ʰ",
    "ʕ": "ʁ",
    "ˤ": "ᵊ",
    "̪": "",
    "[": "",
    "]": "",
}

PUNCT_MAP = str.maketrans({"،": ",", "؛": ";", "؟": "?"})

_MARBUTA_WORD = re.compile(r"([ؠ-يـ]+ة)(?![ؠ-ي])")
_HERE = Path(__file__).resolve().parent
_LEXICON_PATH = _HERE / "ar_lexicon.json"

_marbuta_cache = {}
_lexicon = None
_lexicon_re = None


def _load_lexicon():
    global _lexicon, _lexicon_re
    if _lexicon is None:
        if _LEXICON_PATH.exists():
            entries = json.loads(_LEXICON_PATH.read_text(encoding="utf-8"))
            _lexicon = {k: v for k, v in entries.items() if not k.startswith("_")}
        else:
            _lexicon = {}
        if _lexicon:
            alts = "|".join(re.escape(w) for w in sorted(_lexicon, key=len, reverse=True))
            _lexicon_re = re.compile(rf"(?<![ؠ-يـ])({alts})(?![ؠ-يـ])")
    return _lexicon, _lexicon_re


def normalize_taa_marbuta(text, g2p):
    def repl(m):
        word = m.group(1)
        fixed = _marbuta_cache.get(word)
        if fixed is None:
            try:
                ph, _ = g2p(word)
                broken = ph.strip().rstrip(".").endswith("t")
            except Exception:
                broken = False
            fixed = word[:-1] + "َ" if broken else word
            _marbuta_cache[word] = fixed
        return fixed

    return _MARBUTA_WORD.sub(repl, text)


def normalize_arabic(text, g2p):
    """Full normalization: punctuation + lexicon + taa-marbuta fix."""
    text = text.translate(PUNCT_MAP)
    lex, lex_re = _load_lexicon()
    if lex_re is not None:
        text = lex_re.sub(lambda m: lex[m.group(1)], text)
    return normalize_taa_marbuta(text, g2p)


def text_to_phonemes(text, g2p):
    """text -> Kokoro-compatible phoneme string (frontend + G2P + vocab fixups)."""
    ps, _ = g2p(normalize_arabic(text, g2p))
    for old, new in PHONEME_FIXUPS.items():
        ps = ps.replace(old, new)
    return ps.strip()
