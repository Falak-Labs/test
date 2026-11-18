# Darija → English lessons: voices

The voices for the lesson videos (teacher, Adam, Lina) are made on GitHub's runner with ElevenLabs. The key is the
Actions secret `ELEVENLABS_API_KEY` and is never in a file here.

For each episode:

1. Write `darija/lines/<episode>.txt`, one line per sentence: `SPEAKER | id | text to say`
   (`T` teacher, `A` Adam, `L` Lina, see `voices.json`). Lines that start with `#` are notes.
2. Commit it, then start the workflow once:
   `gh api -X POST repos/Falak-Labs/test/actions/workflows/darija-voice.yml/dispatches -f ref=main`
   With no inputs it voices the last script by name. `-f 'inputs[episode]=ep03'` picks one.
3. When the run has finished, `git pull`. Each line is in `darija/voice/<episode>/<id>.mp3` with `<id>.json`
   (ElevenLabs' character timings), and `manifest.json` gives the status, the model and the characters requested.

One request and one take per line. A second run only asks for lines whose text, voice, model or settings changed,
so credits are spent once per line.
