"""Microsoft's Arabic voices for the Build-It series. Run this on your own PC (it needs the internet).

1) Listen to six male voices (free, no account needed):
     python3 -m venv ~/msvoice && ~/msvoice/bin/pip install -q edge-tts
     ~/msvoice/bin/python ms_voices.py audition
   -> folder ms_audition/ with one MP3 per voice (the first and last line of the Elevator episode).
   Gulf voices read the Saudi script, Levantine voices read the Palestinian one.

   Hear one voice read the whole episode (listening only):
     ~/msvoice/bin/python ms_voices.py preview ar-SY-LaithNeural      (Syrian voice + Syrian script)

2) Make the real voiceover with the voice you picked, through Microsoft's official free tier
   (Azure Speech, free F0 tier: 500,000 characters a month, it stops instead of charging):
     ~/msvoice/bin/pip install -q azure-cognitiveservices-speech
     export AZURE_SPEECH_KEY=<key>  AZURE_SPEECH_REGION=<region, e.g. eastus>
     ~/msvoice/bin/python ms_voices.py full ar-SA-HamedNeural
   Optional: --rate +8% (faster), --script sa|ps|sy (Saudi, Palestinian, Syrian; default follows the voice's country).
   -> elevator_ar_ms.zip (14 WAV lines + exact word times). Attach that zip in the chat.
"""
import asyncio
import json
import os
import sys
import time
import zipfile
from xml.sax.saxutils import escape

SCRIPTS = {
    "sa": [
        "لو ربطت حبل في صندوق وسحبته من فتحة في السقف، مبروك، كذا سويت لك مصعد.",
        "بس لا ركب فيه أربعة أشخاص، يدينك تفصل قبل الدور الثاني.",
        "فتركّب ماطور، وبكرة فوق السطح، وثقل موازن وزنه كثر الصندوق ونص الحمولة، عشان الماطور يادوب يتعب.",
        "الحين يطلع عشر أدوار زي الحرير، لين ينقطع الحبل.",
        "فتركّب سكك حديد، وكيابل احتياط، ومنظّم سرعة: لو الصندوق نزل بسرعة زايدة، تكمش الفرامل على السكك وتوقفه على طول.",
        "بس في الدور الخامس، واحد فتح الباب والصندوق للحين في الدور الأول.",
        "عشان كذا كل باب له قفل ما ينفتح إلا لا صار الصندوق قدامه، وشعاع ضوء بعرضه، وأطراف ترجع تنفتح أول ما تلمس أحد.",
        "الحين كل شي تمام، لين تطفي الكهربا وتعلق بين دورين مع إحدعش واحد غريب.",
        "فتركّب بطارية احتياط، وتلفون طوارئ، ونظام إنقاذ يمشي شوي شوي لأقرب دور ويفتح الأبواب.",
        "بس قبل لا تضغط أول زر، تابعني، لأن الجاي بنبني ناطحة سحاب.",
        "الحين بس خبّ المكينة ورا بابين يلمعون، وحط لوحة أزرار، ورنّة صغيرة.",
        "بير واحد، عشرين دور، وصفر درج.",
        "ومبروك، كذا سويت لك مصعد بيدك.",
        "وترى لو ضغطت الزر عشر مرات، ما راح يجي أسرع."
],
    "sy": [
        "إِذا رَبَطْت حَبِل بْصَنْدوق وشَدّيتو مِن فَتْحَة بِالسَّقْف، مَبْروك، هيك عْمِلْت مَصْعَد.",
        "بَس لَمّا يِرْكَبوا فيه أَرْبَع أَشْخاص، إيدَيك بيِسْتَسْلِموا قَبِل الطّابِق التّاني.",
        "فَبِتْرَكِّب موتور، وبَكَرَة فوق عَالسَّطِح، وثِقِل مْوازِن وَزْنو قَدّ الصَّنْدوق ونُصّ الحُمولِة، مِشان الموتور يادوب يِتْعَب.",
        "هَلَّق بيِطْلَع عَشِر طَوابِق مِتْل الحَرير، لَحَتّى يِنْقِطِع الحَبِل.",
        "فَبِتْرَكِّب سِكَك حَديد، وكَبْلات احْتِياط، ومْنَظِّم سُرْعَة: إِذا الصَّنْدوق نِزِل بِسُرْعَة زْيادِة، بْتِعَضّ الفَرامِل عَالسِّكَك وبِتْوَقّْفو دُغْري.",
        "بَس بِالطّابِق الخامِس، في حَدا فَتَح الباب والصَّنْدوق لِسّا بِالطّابِق الأَوَّل.",
        "مِشان هيك كِلّ باب إِلو قِفِل ما بيِنْفِتِح إِلّا لَمّا يْكون الصَّنْدوق قِدّامو، وشُعاع ضَو عَلى عَرْضو، وحَواف بْتِرْجَع بْتِنْفِتِح أَوَّل ما تِلْمُس حَدا.",
        "هَلَّق كِلّ شي تَمام، لَحَتّى تِقْطَع الكَهْرَبا وتِعْلَق بين طابْقين مَع إِحْدَعْش واحَد غَريب.",
        "فَبِتْرَكِّب بَطّاريّة احْتِياط، وتَلَفون طَوارِئ، ونِظام إِنْقاذ بيِمْشي شْوَيّ شْوَيّ لَأَقْرَب طابِق وبيِفْتَح الأَبْواب.",
        "بَس قَبِل ما تِكْبُس أَوَّل زِرّ، تابِعْني، لَأَنّو الجّاي رَح نْعَمِّر ناطْحِة سَحاب.",
        "هَلَّق بَس خَبّي المَكِنة وَرا بابين بيِلْمَعوا، وحُطّ لوحِة كَبْسات، ورَنّة زْغيرة.",
        "بير واحَد، عِشْرين طابِق، وصِفِر دَرَج.",
        "ومَبْروك، هيك عْمِلْت مَصْعَد بْإيدَك.",
        "وعَلى فِكْرَة، إِذا كَبَسْت الزِّرّ عَشِر مَرّات، ما رَح يِجي أَسْرَع."
],
    "ps": [
        "لو رَبَطِت حَبِل بْصَنْدوق وسَحَبْتو مِن فَتْحَة بِالسَّقِف، مَبْروك، إِنْتَ هيك عْمِلِت مَصْعَد.",
        "بَس لَمّا يِرْكَبوا فيه أَرْبَع أَشْخاص، إيديك بيِسْتَسْلِموا قَبِل الطّابِق التّاني.",
        "فَبِتْضيف موتور، وبَكَرَة فوق السَّطِح، وثِقِل مْوازِن وَزْنو قَدّ الصَّنْدوق ونُصّ الحُمولِة، عَشان الموتور بِالكاد يِتْعَب.",
        "هَلَّأ بيِطْلَع عَشَر طَوابِق زَيّ الحَرير، لَحَدّ ما الحَبِل يِنْقِطِع.",
        "فَبِتْضيف سِكَك حَديد، وكْوابِل احْتِياط، ومْنَظِّم سُرْعَة: إِذا الصَّنْدوق نِزِل بِسُرْعَة زْيادِة، بِتْعَضّ الفَرامِل عَ السِّكَك وبِتْوَقّْفو دُغْري.",
        "بَس بِالطّابِق الخامِس، في واحَد فَتَح الباب والصَّنْدوق لِسّاتو بِالطّابِق الأَوَّل.",
        "عَشان هيك كُلّ باب بياخُد قِفِل ما بيِنْفِتِح إِلّا لَمّا يْكون الصَّنْدوق قُدّامو، وشُعاع ضَوء عَلى عَرْضو، وحَواف بِتِرْجَع بِتِنْفِتِح أَوَّل ما تِلْمِس حَدا.",
        "هَلَّأ كُلّ إِشي تَمام، لَحَدّ ما تِقْطَع الكَهْرَبا وتِعْلَق بين طابْقين مَع إِحْدَعْش واحَد غَريب.",
        "فَبِتْضيف بَطّاريّة احْتِياط، وتَلَفون طَوارِئ، ووَضْع إِنْقاذ بيِمْشي شْوَيّ شْوَيّ لَأَقْرَب طابِق وبيِفْتَح الأَبْواب.",
        "بَس قَبِل ما تِكْبِس أَوَّل زِرّ، تابِعْني، لَإِنّو الجّاي رَح نِبْني ناطْحِة سَحاب.",
        "هَلَّأ بَس خَبّي الماكينِة وَرا بابين لامْعين، وحُطّ لوحِة أَزْرار، ورَنِّة زْغيرِة.",
        "بير واحَد، عِشْرين طابِق، وصِفِر دَرَج.",
        "ومَبْروك، إِنْتَ هيك عْمِلِت مَصْعَد بْإيدَك.",
        "وعَ فِكْرَة، إِذا كَبَسِت الزِّرّ عَشِر مَرّات، مِش رَح ييجي أَسْرَع."
],
}
GULF = ("SA", "KW", "AE", "QA", "BH", "OM", "YE", "IQ", "EG")
AUDITION = [
    ("ar-SA-HamedNeural", "1_Hamed_Saudi"),
    ("ar-KW-FahedNeural", "2_Fahed_Kuwait"),
    ("ar-AE-HamdanNeural", "3_Hamdan_UAE"),
    ("ar-JO-TaimNeural", "4_Taim_Jordan"),
    ("ar-SY-LaithNeural", "5_Laith_Syria"),
    ("ar-LB-RamiNeural", "6_Rami_Lebanon"),
]


def script_for(voice, forced=None):
    if forced:
        return forced
    country = voice.split("-")[1].upper() if voice.count("-") >= 2 else "SA"
    return "sy" if country == "SY" else ("sa" if country in GULF else "ps")


def audition():
    import edge_tts  # listening only; the posted voiceover goes through the official Azure free tier

    os.makedirs("ms_audition", exist_ok=True)

    async def run():
        for voice, name in AUDITION:
            lines = SCRIPTS[script_for(voice)]
            path = os.path.join("ms_audition", name + ".mp3")
            for attempt in range(3):
                try:
                    await edge_tts.Communicate(lines[0] + " " + lines[-1], voice).save(path)
                    print("made", path)
                    break
                except Exception as e:  # noqa: BLE001
                    print("  retry", voice, e)
                    await asyncio.sleep(2)
    asyncio.run(run())
    print("\nPlay the files in ms_audition/ (e.g. xdg-open ms_audition) and pick a voice.")


def preview(voice, rate="+0%", forced=None):
    import edge_tts  # listening only, like audition

    lines = SCRIPTS[script_for(voice, forced)]
    name = voice.split("-")[2].replace("Neural", "") if voice.count("-") >= 2 else voice
    path = f"ms_preview_{name}.mp3"

    async def run():
        for attempt in range(4):
            try:
                await edge_tts.Communicate(" ".join(lines), voice, rate=rate).save(path)
                return True
            except Exception as e:  # noqa: BLE001
                print("  retry", e)
                await asyncio.sleep(3)
        return False
    if asyncio.run(run()):
        print(f"made {path}: the whole episode in {voice}, script '{script_for(voice, forced)}', rate {rate}")
    else:
        sys.exit("Microsoft's service did not answer; run it again in a minute.")


def full(voice, rate="+0%", forced=None):
    import azure.cognitiveservices.speech as sdk

    key, region = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        sys.exit("Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION first (Azure portal > your Speech resource > Keys and Endpoint).")
    which = script_for(voice, forced)
    lines = SCRIPTS[which]
    cfg = sdk.SpeechConfig(subscription=key, region=region)
    cfg.set_speech_synthesis_output_format(sdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
    syn = sdk.SpeechSynthesizer(speech_config=cfg, audio_config=None)
    words = []

    def on_word(evt):
        if evt.boundary_type == sdk.SpeechSynthesisBoundaryType.Word:
            d = evt.duration
            d = d.total_seconds() if hasattr(d, "total_seconds") else d / 1e7
            words.append({"text": evt.text, "start": evt.audio_offset / 1e7, "dur": d})
    syn.synthesis_word_boundary.connect(on_word)
    lang = "-".join(voice.split("-")[:2])
    out = "elevator_ar_ms"
    os.makedirs(out, exist_ok=True)
    for i, line in enumerate(lines, 1):
        ssml = (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang}">'
                f'<voice name="{voice}"><prosody rate="{rate}">{escape(line)}</prosody></voice></speak>')
        for attempt in range(5):
            words.clear()
            res = syn.speak_ssml_async(ssml).get()
            if res.reason == sdk.ResultReason.SynthesizingAudioCompleted:
                break
            det = res.cancellation_details
            print(f"  line {i}: {det.reason} {det.error_details}")
            if "429" in str(det.error_details) or "Too many" in str(det.error_details):
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit("Stopped: check the key, the region and the voice name.")
        else:
            sys.exit("Stopped: Azure kept refusing (free tier limit?). Try again in a minute.")
        with open(os.path.join(out, f"L{i:02d}.wav"), "wb") as fh:
            fh.write(res.audio_data)
        with open(os.path.join(out, f"L{i:02d}.json"), "w", encoding="utf-8") as fh:
            json.dump({"line": i, "text": line, "words": list(words)}, fh, ensure_ascii=False, indent=1)
        print(f"line {i:>2}: {len(words)} words")
        time.sleep(0.5)
    with open(os.path.join(out, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump({"voice": voice, "rate": rate, "script": which, "engine": "azure-speech"}, fh, ensure_ascii=False)
    with zipfile.ZipFile(out + ".zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(out)):
            z.write(os.path.join(out, name))
    print(f"\nDone: {out}.zip ({os.path.getsize(out + '.zip') / 1e6:.1f} MB). Attach it in the chat.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] not in ("audition", "preview", "full") or (args[0] != "audition" and len(args) < 2):
        sys.exit(__doc__)
    rate = args[args.index("--rate") + 1] if "--rate" in args else "+0%"
    forced = args[args.index("--script") + 1] if "--script" in args else None
    if args[0] == "audition":
        audition()
    elif args[0] == "preview":
        preview(args[1], rate, forced)
    else:
        full(args[1], rate, forced)
