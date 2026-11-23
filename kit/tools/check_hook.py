"""Check a build's scripts against the hook rules of Nov 23 2026 (NIGHT_NOTES "Nov 23 2026: the hook rules").
    python3 -I tools/check_hook.py <kit> [<kit> ...]        (from the kit folder; exit code 1 when a line says FAIL)

Run it twice: after writing the scripts (word counts and reading level) and again after the voices exist (it then
also reads the spoken seconds from series/voice/<kit>.json and <kit>_ar_sa.json).

Where the limits come from: builds 1-20, the best-watched era on Instagram, had hooks of 13-20 English words
(median 17) spoken in 3.4-4.9 s, and the first problem was told by 8.4 s. From build 31 on the hook grew to about
25 words and 6.6 s, and people stayed for less of the video.
"""
import json
import os
import re
import sys

KIT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_HOOK_WORDS, EN_HOOK_SECS, EN_HOOK_GRADE = 18, 5.0, 7.0      # line 1, English
EN_PROBLEM_BY = 9.5                                             # line 2 has ended by this second (English voice)
EN_SCRIPT_GRADE = 4.5                                           # whole English script (Flesch-Kincaid grade): an aim, listed, not failed
                                                                # (in our numbers the HOOK's grade goes with watch time, the script's does not)
AR_HOOK_WORDS, AR_HOOK_SECS, AR_PROBLEM_BY = 13, 5.5, 10.0      # Arabic (Mansour reads slower)
LONG_LINE = 22                                                  # words; lines over it are listed, not failed
PLAIN = set("""every everyone everything everywhere another anyone anything family animal different together tomorrow
yesterday remember already understand important beautiful favorite energy area idea video radio camera computer
hospital library holiday vacation umbrella elephant dinosaur bicycle banana potato tomato grandfather grandmother
eleven seventeen seventy ninety million billion thousandth electric electricity suddenly finally actually
nobody somebody underground underwater upside overhead""".split())


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w2 = w if w.endswith(("le", "ted", "ded")) else re.sub(r"(?:es|ed|e)$", "", w)
    return max(1, len(re.findall(r"[aeiouy]+", w2)))


def sentences(text):
    return [s.strip() for s in re.split(r"[.!?:]+", text) if s.strip()]


def grade(text):
    words = re.findall(r"[A-Za-z']+", text)
    if not words:
        return 0.0
    return round(0.39 * len(words) / max(1, len(sentences(text))) + 11.8 * sum(syl(w) for w in words) / len(words) - 15.59, 1)


def read_lines(path):
    return [x.strip() for x in open(path, encoding="utf-8") if x.strip()]


def spoken(kit, suffix):
    p = os.path.join(KIT_DIR, "series", "voice", f"{kit}{suffix}.json")
    if not os.path.exists(p):
        return None
    try:
        return [ln["end"] for ln in json.load(open(p, encoding="utf-8"))["lines"]]
    except (KeyError, ValueError):
        return None


def verdict(ok, limit):
    return "ok" if ok else f"FAIL: {limit}"


def check(kit):
    bad = False
    en = os.path.join(KIT_DIR, "series", f"{kit}_lines.txt")
    ar = os.path.join(KIT_DIR, "series", f"{kit}_lines_ar_sa.txt")
    if os.path.exists(en):
        L = read_lines(en)
        hook, ends = L[0], spoken(kit, "")
        hw = len(re.findall(r"[A-Za-z0-9']+", hook))
        clause = re.split(r",?\s*congrats", hook, flags=re.I)[0]
        print(f"== {kit} (English)\n  line 1: {hook}")
        ok = hw <= EN_HOOK_WORDS
        bad |= not ok
        print(f"  hook words: {hw}   {verdict(ok, f'at most {EN_HOOK_WORDS} words')}")
        ok = "," not in clause
        bad |= not ok
        print(f"  one picture: {'yes' if ok else 'no'}   {verdict(ok, 'the part before congrats has a comma: keep ONE picture, move the second fact to line 2')}")
        g = grade(hook)
        ok = g <= EN_HOOK_GRADE
        bad |= not ok
        print(f"  hook reading grade: {g}   {verdict(ok, f'at most {EN_HOOK_GRADE} (shorter sentence, plainer words)')}")
        if ends:
            ok = ends[0] <= EN_HOOK_SECS
            bad |= not ok
            print(f"  hook spoken: {ends[0]:.1f} s   {verdict(ok, f'at most {EN_HOOK_SECS} s')}")
            ok = ends[1] <= EN_PROBLEM_BY
            bad |= not ok
            print(f"  first problem told by: {ends[1]:.1f} s   {verdict(ok, f'by {EN_PROBLEM_BY} s (shorten line 1 or line 2)')}")
        else:
            print("  (no English voice yet: run again after the voice job for the spoken seconds)")
        body = " ".join(L)
        g = grade(body)
        ok = g <= EN_SCRIPT_GRADE
        nwords = len(re.findall(r"[A-Za-z0-9']+", body))
        print(f"  script: {nwords} words, reading grade {g}   {'ok' if ok else f'aim for {EN_SCRIPT_GRADE} or lower: shorten these'}")
        if not ok:
            longest = sorted(sentences(body), key=lambda s: -len(s.split()))[:3]
            for s in longest:
                print(f"      long sentence ({len(s.split())} words): {s[:110]}")
        hard = sorted({w.lower() for w in re.findall(r"[A-Za-z']+", body) if syl(w) >= 3 and not w[0].isupper() and w.lower() not in PLAIN})
        if hard:
            print(f"  words of 3+ syllables to swap where a plain word exists ({len(hard)}): {', '.join(hard)}")
        longl = [(i + 1, len(re.findall(r"[A-Za-z0-9']+", x))) for i, x in enumerate(L) if len(re.findall(r"[A-Za-z0-9']+", x)) > LONG_LINE]
        if longl:
            print("  long lines (cut the fluff): " + ", ".join(f"line {i} = {n} words" for i, n in longl))
        if len(L) >= 11:
            print(f"  open loop, read these together: does line 1 or 2 raise a question that only line 11 answers?\n      2: {L[1]}\n     11: {L[10]}")
    if os.path.exists(ar):
        A = read_lines(ar)
        ends = spoken(kit, "_ar_sa")
        aw = len(A[0].split())
        print(f"== {kit} (Arabic)\n  line 1: {A[0]}")
        ok = aw <= AR_HOOK_WORDS
        bad |= not ok
        print(f"  hook words: {aw}   {verdict(ok, f'at most {AR_HOOK_WORDS} words')}")
        clause = re.split(r"[،,]?\s*مبروك", A[0])[0]
        ok = "،" not in clause and "," not in clause
        bad |= not ok
        print(f"  one picture: {'yes' if ok else 'no'}   {verdict(ok, 'the part before مبروك has a comma: keep ONE picture')}")
        if ends:
            ok = ends[0] <= AR_HOOK_SECS
            bad |= not ok
            print(f"  hook spoken: {ends[0]:.1f} s   {verdict(ok, f'at most {AR_HOOK_SECS} s')}")
            ok = ends[1] <= AR_PROBLEM_BY
            bad |= not ok
            print(f"  first problem told by: {ends[1]:.1f} s   {verdict(ok, f'by {AR_PROBLEM_BY} s')}")
        else:
            print("  (no Arabic voice yet: run again after the voice job)")
    if not os.path.exists(en) and not os.path.exists(ar):
        print(f"== {kit}: no scripts found in series/")
        bad = True
    return bad


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    failed = [k for k in sys.argv[1:] if check(k)]
    print("\nRESULT: " + ("FAIL in " + ", ".join(failed) if failed else "all hook rules pass"))
    sys.exit(1 if failed else 0)
