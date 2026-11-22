"""Yallah Say, lesson script (v2 format, 75-95 s): hook, five phrases with time to think, quiz, hard word in a sentence, end.
One lesson in every dialect.   usage: python3 gen2.py <lesson> <locale> <page_dir> <lines.txt>
The lesson is yallah/lessons/<lesson>.json (YS_LESSONS points somewhere else): the hard word, the four English phrases
both dialects share, and for each dialect the hook, the five phrases, the fifth English phrase and the home sentence.
Writes <page_dir>/script.js (what the page draws) and the voice lines file (SPEAKER | id | text)."""
import json, os, sys

LESSONS = os.environ.get("YS_LESSONS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lessons")
# what never changes from one episode to the next, in each dialect
LOCALES = {
    "ma": {
        "L": {"lang": "Darija", "TAB": "DARIJA", "think": "شنو هي بالإنجليزية؟", "quizAr": "نعاودو!", "quizSub": "N3awdou!  ·  Quick quiz", "hardAr": "الكلمة الصعيبة", "turnAr": "دورك! قولها بصوت عالي",
              "endQ": "عجبك الدرس؟", "endWord": "الكلمة الصعيبة ديال اليوم", "cta": "كتبها فالتعليقات!", "ctaEn": "Write the hard word in the comments!", "follow": "تابعنا", "sub": "باش تتعلم كل نهار", "handle": "@YallahSayMa"},
        "kids": [("Adam", "boy"), ("Lina", "girl"), ("Yassine", "boy2"), ("Imane", "girl2"), ("Mehdi", "boy3"), ("Kenza", "girl3")],
        "quiz": ("N3awdou!", "نعاودو!", "Quick quiz!"),
        "w0": ("Wdaba, lkelma s3iba dyal lyoum!", "ودابا، الكلمة الصعيبة ديال اليوم!", "And now, today's hard word!"),
        "w2": ("Chwiya b-chwiya.", "شوية بشوية.", "Little by little."), "w3": ("Daba b-zzerba!", "دابا بالزربة!", "Now faster!"),
        "w4": ("Daba kamla!", "دابا كاملة!", "Now the whole word!"), "v0": ("Wdaba f-jumla!", "ودابا فجملة!", "And now in a sentence!"),
        "o1": "عجبك الدرس؟ كتب الكلمة فالتعليقات! وباش تشوف فيديوهات كثر، تابعنا هنا وفاليوتيوب!",
    },
    "pa": {
        "L": {"lang": "Palestinian", "TAB": "PALESTINIAN", "think": "شو يعني بالإنجليزي؟", "quizAr": "تعالوا نعيد!", "quizSub": "Ta3alu n3id!  ·  Quick quiz", "hardAr": "كلمة اليوم الصعبة", "turnAr": "دورك! احكيها بصوت عالي",
              "endQ": "عجبك الدرس؟", "endWord": "كلمة اليوم الصعبة", "cta": "اكتبها بالتعليقات!", "ctaEn": "Write the hard word in the comments!", "follow": "تابعنا", "sub": "عشان تتعلم كل يوم", "handle": "@YallahSayPa"},
        "kids": [("Adam", "boy"), ("Lina", "girl"), ("Omar", "boy2"), ("Yara", "girl2"), ("Kareem", "boy3"), ("Tala", "girl3")],
        "quiz": ("Ta3alu n3id!", "تعالوا نعيد!", "Quick quiz!"),
        "w0": ("Hassa, kilmet el-yom es-sa3beh!", "هسا، كلمة اليوم الصعبة!", "And now, today's hard word!"),
        "w2": ("Shwayy shwayy.", "شوي شوي.", "Little by little."), "w3": ("Hassa b-sur3a!", "هسا بسرعة!", "Now faster!"),
        "w4": ("Hassa el-kilmeh kamleh!", "هسا الكلمة كاملة!", "Now the whole word!"), "v0": ("W-hassa b-jumleh!", "وهسا بجملة!", "And now in a sentence!"),
        "o1": "عجبك الدرس؟ اكتب الكلمة بالتعليقات! ولفيديوهات أكثر، تابعنا هون وعلى اليوتيوب!",
        "tts": {"مبروك": "مَبْروك"},      # vowel marks where this voice was heard wrong (the page shows the plain spelling)
    },
}

ep, loc, page, lines_path = sys.argv[1:5]
EP = json.load(open(os.path.join(LESSONS, ep + ".json"), encoding="utf-8"))
LC, X = LOCALES[loc], EP[loc]
WORD = dict({k: EP["word"][k] for k in ("full", "parts", "say", "tts")}, ah=X["ah"], sent={k: X["sent"][k] for k in ("en", "hot", "dz", "ar")})
mean, tr = EP["word"]["mean"], EP["word"]["ar"]          # what the word means, and how it sounds in Arabic letters
L = dict(LC["L"], meanAr="المعنى: " + mean, endEq=tr[loc] + " = " + mean.rstrip("!"))
if X.get("sub"):
    L["sub"] = X["sub"]
O1 = X.get("o1") or LC["o1"]
PH = [(dz, ar, en, who, icon, fl) for (dz, ar), (en, who, icon, fl) in zip(X["ph"], EP["en"] + [X["ph5"]])]
assert len(PH) == 5
B, LINES = [], []
add = lambda **k: B.append(k)
def say(s):          # what the teacher's voice reads: no quote marks, and this dialect's spelling fixes
    s = s.replace("«", "").replace("»", "")
    for a, b in LC.get("tts", {}).items():
        s = s.replace(a, b)
    return s


line = lambda sp, tid, text: LINES.append((sp, tid, say(text) if sp == "T" else text))
SY = [s.lower() for s in WORD["tts"]]

for n, (dz, ar, gl) in enumerate(X["hook"]):     # the hook: a question, and a promise for the end
    add(id=f"h{n + 1}", sp="T", shot="T", p=-1, dz=dz, ar=ar, gl=gl, board=X["board"], pre=0.25 if n == 0 else 0.3); line("T", f"h{n + 1}", say(ar))
for i, (dz, ar, en, who, icon, fl) in enumerate(PH):
    n = i + 1
    add(id=f"p{n:02d}t", sp="T", shot="T", p=i, dz=dz, ar=ar, pre=0.4)
    add(id=f"p{n:02d}k", sp=who, shot="K", p=i, en=en, fx="ding", pre=1.12, lead=1.0, post=0.7)     # the pupil thinks for a second first
    line("T", f"p{n:02d}t", ar); line(who, f"p{n:02d}k", en)
# quiz: the five answers again, each hidden until it is heard
qd, qa, qg = LC["quiz"]
add(id="rb0", shot="R", round=0, sil=0.7, fx="jingle", pre=0.25)
add(id="rc0", clip="r0", sp="T", shot="R", round=0, dz=qd, ar=qa, gl=qg, pre=0.05); line("T", "r0", qa)
for k in range(5):
    add(id=f"rc0_{k}", clip=f"p{k + 1:02d}k", sp=PH[k][3], shot="R", round=0, row=k, p=k, en=PH[k][2], fx="ding2", pre=0.8, post=0.45 if k == 4 else 0.12)
# the hard word
T3 = lambda key: dict(dz=LC[key][0], ar=LC[key][1], gl=LC[key][2])
add(id="hb", shot="H", sil=0.7, fx="drum", pre=0.2)
add(id="w0", sp="T", shot="H", pre=0.1, **T3("w0")); line("T", "w0", LC["w0"][1])
add(id="tw", sp="T", shot="H", en=WORD["full"] + ".", pre=0.4); line("T", "tw", WORD["full"] + ".")
add(id="w2", sp="T", shot="H", pre=0.4, **T3("w2")); line("T", "w2", LC["w2"][1])
for i, s in enumerate(SY):       # slowly: the teacher, then the class
    add(id=f"s{i}t", clip=f"T_{s}", sp="T", shot="H", syl=i, pre=0.32)
    add(id=f"s{i}a", clip=f"A_{s}", cho=f"L_{s}", sp="AL", shot="H", syl=i, pre=0.14)
add(id="w3", sp="T", shot="H", pre=0.4, **T3("w3")); line("T", "w3", LC["w3"][1])
for i, s in enumerate(SY):       # faster: the class says the five parts in a row
    add(id=f"f{i}k", clip=f"A_{s}", cho=f"L_{s}", sp="AL", shot="H", syl=i, fast=1, pre=0.34 if i == 0 else 0.03)
add(id="w4", sp="T", shot="H", pre=0.42, **T3("w4")); line("T", "w4", LC["w4"][1])
add(id="w5", sp="A", shot="H", en=WORD["full"] + "!", st="ok", pre=0.4, fx="ding"); line("A", "w5", WORD["full"] + "!")
add(id="w6", sp="T", shot="H", en="Good job! " + WORD["full"] + "!", pre=0.5, post=0.2); line("T", "w6", "Good job! " + WORD["full"] + "!")
# the word in a sentence close to home, what it means, then the viewer's turn
S = X["sent"]
add(id="v0", sp="T", shot="H", pre=0.4, **T3("v0")); line("T", "v0", LC["v0"][1])
add(id="v1", sp="L", shot="H", en=S["en"], hot=S["hot"], pre=0.4); line("L", "v1", S["en"])
if S.get("alt"):
    line("L", "v1b", S["alt"])           # a spare take with the local word spelled the way it sounds
add(id="v2", sp="T", shot="H", dz=S["dz"], ar=S["ar"], pre=0.45); line("T", "v2", S["ar"])
add(id="v3", shot="H", sil=2.1, en=S["en"], hot=S["hot"], fx="ticks", pre=0.3)
add(id="v4", clip="w5", cho="Lw", sp="AL", shot="H", en=WORD["full"] + "!", fx="tada0", pre=0.25, post=0.8); line("L", "Lw", WORD["full"] + "!")
add(id="o1", sp="T", shot="C", ar=O1, pre=0.5, fx="whoosh"); line("T", "o1", O1)
add(id="o2", sp="L", shot="C", en="See you next time!", pre=0.4); line("L", "o2", "See you next time!")
add(id="o3", sp="A", shot="C", en="Bye!", pre=0.25, post=1.1); line("A", "o3", "Bye!")
for sp in "TAL":                 # the five parts of the word, one take each, and one spare take with all five
    for s, w in zip(SY, WORD["tts"]):
        line(sp, f"{sp}_{s}", w + ".")
    line(sp, f"s{sp}", " [long pause] ".join(w + "." for w in WORD["tts"]))
for b in B:
    if b.get("dz"):
        assert len(b["dz"].split(" ")) == len(b["ar"].split(" ")), b["id"]
ids = [l[1] for l in LINES]; assert len(ids) == len(set(ids)), ids
kids = [{"name": n, "look": k} for n, k in LC["kids"]]
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
out = ['window.SCRIPT={"theme":' + J(loc) + ',"ep":' + J(ep) + ',"L":' + J(L) + ',', '"kids":' + J(kids) + ',', '"word":' + J(WORD) + ',', '"phrases":[',
       *[J({"dz": p[0], "ar": p[1], "en": p[2], "who": p[3], "icon": p[4], **p[5]}) + ("," if i < len(PH) - 1 else "") for i, p in enumerate(PH)], '],', '"beats":[',
       *[J(b) + ("," if i < len(B) - 1 else "") for i, b in enumerate(B)], ']};']
open(f"{page}/script.js", "w", encoding="utf-8").write("\n".join(out) + "\n")
txt = [f"# Yallah Say, episode {ep} ({loc}): five phrases, quiz, hard word ({WORD['full']}) in a sentence.", "# SPEAKER | id | text to say      (T teacher, A Adam, L Lina)"] + [f"{sp} | {tid} | {text}" for sp, tid, text in LINES]
open(lines_path, "w", encoding="utf-8").write("\n".join(txt) + "\n")
print(len(B), "beats,", len(LINES), "voice lines,", sum(len(l[2]) for l in LINES), "characters")
