# Posting a long video to YouTube from a Claude chat

Worked out and used on Nov 21 2026 for the Build-It 4-minute show (four uploads, two channels, published and
scheduled). Any chat of the owner can follow it.

## Why the usual ways fail
- Buffer cannot publish a YouTube video over 3 minutes, and its free plan sends only 2 YouTube posts per 24 hours.
- The browser tool's `file_upload` stops at 3.8 MB, so it cannot carry a video.
- What works: YouTube Studio in the owner's own Chrome (Claude in Chrome tools). He is already signed in. The page
  itself downloads the video from a public link and puts it in the upload box.
- A vertical video up to 3:00 becomes a Short. Over 3:00, or any horizontal video, is a regular video.

## Rules
- Making a video public needs the owner's yes in that chat. Without it, upload as Private and ask him.
- Never type a password or a code. If Studio asks for a sign-in or a verification, stop and tell him.
- Screenshots hang in that browser. Read the page with `javascript_tool` and `find` instead.
- `javascript_tool` blocks any answer that contains a URL with "?" in it. Print `location.pathname`, and cut links
  at "?".
- A call that makes the page reload dies. Start that click inside `setTimeout` and read the result in the next call.
- One Google login holds six channels, and switching is shared by every chat that uses the browser:
  Yallah Say MA `@YallahSayMa` (UC_c7QhlukkSAR-qHKeSvkPA), Congrats Engineer `@congratsengineer`
  (UCDkfxHa7q5Ea0OoiSSi8DHA), Kef Tenbeni `@kef.tenbeni` (UC8qDuZpMDQXRrowaNp29vow), Yallah Say PS `@YallahSay-Pa`
  (UCXJLd8EVa_XOLnQwnfxtoxw; renamed by the owner on Nov 21 2026, before that Yalla Say `@YallaSayPa`), The Dark Told Me `@TheDarkToldMe` (UCXm0SVD8jw0hv7dhL2KsjXA) and its Arabic channel
  `@TheDarkToldMeAR` (UCzwjwEz-9pso6UiPg9-6QSA). Check the channel name in the same call that loads the file, and
  again before the last click. Remember the channel you found and switch back to it. The main Build-It chat uploads
  at about 4:45 pm and 9:30 pm PT: do not switch channels in those half hours.
- **The daily limit.** YouTube can answer an upload with "Daily upload limit reached. Upload more videos daily after a
  one-time verification or wait 24 hours." On Nov 21 2026 it came after 10 Studio uploads by this login in under a day
  (6 on Congrats Engineer, 4 on Kef Tenbeni), and from then on every channel that is not verified was refused (both
  Build-It channels, both The Dark Told Me channels, Yallah Say PS), while Yallah Say MA, whose Advanced features are
  enabled, still uploaded. So count on about 10 uploads per rolling 24 hours, shared by ALL the owner's unverified
  channels. When you see the message: close the box with its X, do not try again that day, NEVER click "Verify", and
  tell the owner. The cure is his: Studio > Settings > Channel > Feature eligibility > Advanced features (a video
  selfie or an ID; "Only channel owners can complete the one-time verification"; the login in this Chrome is not the
  owner of the Build-It channels and gets no button). Advanced features also carry "Eligible to apply for
  monetization".
- **Shares until he verifies:** Build-It uploads 6 a day in Studio (the show's four and one build in both languages)
  and records every upload in `youtube/ledger.json` (`scripts/yt_desk.py`). That leaves 2 for the other channels and
  2 spare, because the 24 hours roll. A chat that needs more should ask the owner, not take it. Uploads through Buffer
  are separate (they worked while Studio refused), but Buffer's free plan sends only 2 YouTube posts per channel in 24
  hours and no video over 3 minutes.

## Steps
1. **Make the file small enough:** under 95 MB (GitHub takes 100 MB a file).
   `ffmpeg -i in.mp4 -c:v libx264 -preset medium -crf 22 -pix_fmt yuv420p -movflags +faststart -c:a copy out.mp4`
   Raise crf (24, 26) until it fits. Not tested: for a bigger file, split it (`split -b 90m`), fetch the parts in
   order in step 4 and join them with `new File([part1, part2, ...], name)`.
2. **Put it where the page can fetch it:** a throwaway branch of the public repo Falak-Labs/test.
   ```
   rm -rf /tmp/up && mkdir /tmp/up && cd /tmp/up && git init -q && git checkout -q --orphan uploads
   cp <video> <thumbnail.jpg> . && git add . && git commit -qm "temporary upload files"
   git remote add origin "$(git -C /home/claude/test remote get-url origin)" && git push -q --force origin uploads
   ```
   Check: `curl -sI https://raw.githubusercontent.com/Falak-Labs/test/uploads/<file>` must answer 200. Use this raw
   link; the github.io link does not work from Studio. (No clone yet: attach Falak-Labs/test with push access.)
3. **Browser:** load the Claude in Chrome tools in one ToolSearch call, `tabs_context_mcp` with `createIfEmpty`,
   open https://studio.youtube.com. The channel's name is in `ytcp-navigation-drawer #entity-name`. Remember which
   channel you found. To switch: click the "Account" button (find tool), then with JavaScript click the visible item
   whose text starts with "Switch account", wait 2.5 s, and click the `ytd-account-item-renderer` whose text
   contains the handle.
4. **Load the file.** Open `https://studio.youtube.com/channel/<CHANNEL ID>/videos/upload?d=ud` and run in the page:
   ```js
   const r = await fetch(RAW_LINK); const b = await r.blob();
   const f = new File([b], 'name.mp4', {type: 'video/mp4'});
   const dt = new DataTransfer(); dt.items.add(f);
   const inp = document.querySelector('ytcp-uploads-file-picker input[type=file]');
   inp.files = dt.files; inp.dispatchEvent(new Event('change', {bubbles: true}));
   ```
   The upload starts by itself (90 MB took about a minute and a half).
5. **Fill the dialog** (`d = document.querySelector('ytcp-uploads-dialog')`):
   - Title and description: for `#title-textarea #textbox` and `#description-textarea #textbox`, focus it, select
     its contents with a Range, then `document.execCommand('insertText', false, text)`. Line breaks survive. Title up
     to 100 characters. Lines like `0:00 Intro` in the description become chapters (first one 0:00, at least three).
   - Thumbnail (1280x720 jpg): the same File trick on `ytcp-thumbnail-uploader input#file-loader`. Skip it if the
     channel refuses.
   - Click the radio buttons by name: `tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]`; click
     `#toggle-button` (Show more); then `VIDEO_PAID_PRODUCT_PLACEMENT_NO` and `VIDEO_HAS_ALTERED_CONTENT_NO` or
     `_YES`. Read that AI question on the page, answer it truthfully for this video, and tell the owner what you
     answered.
   - Language: click `#language-input ytcp-dropdown-trigger`, wait 1.5 s, click the visible `tp-yt-paper-item` whose
     text is exactly "English" or "Arabic".
   - Read the radios back now (`aria-checked`). After the next step they are gone from the page.
6. **Publish or schedule.** Click `#next-button` three times, 2 s apart. On the last step:
   - Now: click `tp-yt-paper-radio-button[name=PUBLIC]` (or `PRIVATE`), then `#done-button`.
   - Tomorrow at a time: click `#second-container-expand-button`. The date already says tomorrow (the browser is on
     Pacific time). Put the time in `ytcp-datetime-picker #time-of-day-container input`: focus, select, insertText
     "10:00 AM", send an `input` event, Enter, a `change` event, blur. Wait until `.progress-label` no longer says
     "Uploading", then click `#done-button` (it reads "Schedule"). Studio answers "Your video will be set to public
     on ...". Not tested: any date other than tomorrow.
   - Never click "Promote" in the box that follows.
7. **Check.** The link is among the dialog's `<a>` tags (youtu.be/ID). Regular videos are listed at
   `/channel/<ID>/videos/upload`, Shorts at `/channel/<ID>/videos/short`; each `ytcp-video-row` has
   `.tablecell-visibility` and `.tablecell-date`. A public video answers 200 here:
   `fetch('https://www.youtube.com/oembed?format=json&url=' + encodeURIComponent('https://youtu.be/ID'), {credentials: 'omit'})`
   To make a private video public later: open `/video/<ID>/edit`, click inside `ytcp-video-metadata-visibility`,
   choose `PUBLIC` in `ytcp-video-visibility-edit-popup`, click its `#save-button`, then `ytcp-button#save`. Studio
   says "Changes saved".
8. **Clean up:** switch back to the channel you found, close your tab, and replace the `uploads` branch with an
   empty commit (force-push; the branch cannot be deleted from a chat).
9. **Report** in a few lines: the link, the channel, public or scheduled for when, and anything you could not do.

## Builds: every build's Short from an upload sheet (used Nov 21 for builds 58 and 60, both languages)
The owner, Nov 21 2026: Buffer keeps Instagram and TikTok; YouTube goes up here. Who does it and when: "The desk" below.
1. `python3 scripts/yt_meta.py <slug> [<slug> ...] > sheet_<date>.json` (slug = a posts file). One entry per
   language, keyed `<slug>-en` / `<slug>-ar`: the video's raw link on main, the channel, the title and description
   post.py would have sent, the language, and the slot as Studio wants it (`date` "Nov 22, 2026", `time` "6:00 AM",
   Pacific time).
2. Push that one file to the `uploads` branch (step 2 above). Give it a new name each time: raw links are cached for
   a few minutes.
3. Per channel: switch Studio to it, then for each video one `browser_batch`: navigate to
   `https://studio.youtube.com/channel/<CHANNEL ID>/videos/upload?d=ud`, wait 5 s, and run these two calls (set KEY
   and META in both). They stop by themselves when the channel, the date, the title or the time is not what the
   sheet says.
   ```js
   // call 1: load the file
   const KEY='ep58-ferriswheel-en'; const META='https://raw.githubusercontent.com/Falak-Labs/test/uploads/sheet.json';
   const m=(await (await fetch(META)).json())[KEY];
   const chan=Array.from(document.querySelectorAll('ytcp-navigation-drawer #entity-name')).map(e=>e.textContent.trim())[0];
   const inp=document.querySelector('ytcp-uploads-file-picker input[type=file]'); let res;
   if(!inp || chan!==m.channel){ res={error:'wrong channel or no upload box', chan}; }
   else { const r=await fetch(m.url); const b=await r.blob(); const f=new File([b], KEY+'.mp4', {type:'video/mp4'});
     const dt=new DataTransfer(); dt.items.add(f); inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
     res={chan, status:r.status, size:b.size}; }
   JSON.stringify(res)
   ```
   ```js
   // only for an entry that has "thumb" (the show's full videos): after call 1, before call 2
   // (written from the steps done by hand on Nov 21: read its answer)
   const KEY='sm03-en-full'; const META='https://raw.githubusercontent.com/Falak-Labs/test/uploads/sheet.json';
   const m=(await (await fetch(META)).json())[KEY]; await new Promise(r=>setTimeout(r,3500));
   const b=await (await fetch(m.thumb)).blob(); const f=new File([b], KEY+'.jpg', {type:'image/jpeg'});
   const dt=new DataTransfer(); dt.items.add(f);
   const inp=document.querySelector('ytcp-uploads-dialog ytcp-thumbnail-uploader input#file-loader');
   if(inp){ inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true})); await new Promise(r=>setTimeout(r,4000)); }
   JSON.stringify({box: !!inp, size: b.size, shown: !!document.querySelector('ytcp-uploads-dialog ytcp-thumbnail-uploader img')})
   ```
   ```js
   // call 2: fill, schedule, report (it stops by itself when YouTube refuses the upload)
   const KEY='ep58-ferriswheel-en'; const META='https://raw.githubusercontent.com/Falak-Labs/test/uploads/sheet.json';
   const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const norm=s=>s.replace(/\s+/g,' ').trim(); await sleep(4000);
   const m=(await (await fetch(META)).json())[KEY]; const d=document.querySelector('ytcp-uploads-dialog');
   const errs=()=>d?Array.from(d.querySelectorAll('.error-short, .error-details')).filter(e=>e.offsetParent!==null).map(e=>norm(e.innerText)).filter(Boolean):[];
   let out={};
   if(errs().length || !d || !d.querySelector('#title-textarea #textbox')){ out={error:'stopped: upload refused or no details form', errs:errs()}; }
   else {
   const setBox=(sel,txt)=>{ const el=d.querySelector(sel); el.focus(); const s=getSelection(); const r=document.createRange();
     r.selectNodeContents(el); s.removeAllRanges(); s.addRange(r); document.execCommand('insertText', false, txt); return el.innerText; };
   const title=setBox('#title-textarea #textbox', m.title); const desc=setBox('#description-textarea #textbox', m.desc);
   d.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]').click();
   const more=d.querySelector('#toggle-button'); if(more && /more/i.test(more.innerText)) more.click(); await sleep(1500);
   const q=n=>d.querySelector('tp-yt-paper-radio-button[name='+n+']');
   q('VIDEO_PAID_PRODUCT_PLACEMENT_NO').click(); await sleep(300); q('VIDEO_HAS_ALTERED_CONTENT_NO').click(); await sleep(400);
   d.querySelector('#language-input ytcp-dropdown-trigger, #language-input ytcp-text-dropdown-trigger').click(); await sleep(1500);
   const it=Array.from(document.querySelectorAll('ytcp-text-menu tp-yt-paper-item, tp-yt-paper-listbox tp-yt-paper-item'))
     .filter(e=>e.offsetParent!==null).find(e=>e.innerText.trim()===m.language); if(it) it.click(); await sleep(2000);
   const st=n=>q(n).getAttribute('aria-checked');
   out={title, titleOk: title.trim()===m.title, descLen: desc.length, wantLen: m.desc.length, kidsNo:st('VIDEO_MADE_FOR_KIDS_NOT_MFK'),
     paidNo:st('VIDEO_PAID_PRODUCT_PLACEMENT_NO'), alteredNo:st('VIDEO_HAS_ALTERED_CONTENT_NO'), lang:norm(d.querySelector('#language-input').innerText)};
   if(errs().length){ out.error='stopped: upload refused'; out.errs=errs(); }
   else {
   for(let i=0;i<3;i++){ d.querySelector('#next-button').click(); await sleep(1800); }
   d.querySelector('#second-container-expand-button').click(); await sleep(1500);
   const dp=d.querySelector('ytcp-datetime-picker'); out.date=norm(dp.querySelector('#datepicker-trigger').innerText);
   out.chan=Array.from(document.querySelectorAll('ytcp-navigation-drawer #entity-name')).map(e=>e.textContent.trim())[0];
   if(out.date!==m.date || out.chan!==m.channel || out.kidsNo!=='true' || !out.titleOk){ out.error='stopped before scheduling'; }
   else { const inp=dp.querySelector('#time-of-day-container input'); inp.focus(); inp.select();
     document.execCommand('insertText', false, m.time); inp.dispatchEvent(new Event('input',{bubbles:true})); await sleep(600);
     inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}));
     inp.dispatchEvent(new KeyboardEvent('keyup',{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}));
     inp.dispatchEvent(new Event('change',{bubbles:true})); inp.blur(); await sleep(1000); out.time=norm(inp.value);
     for(let i=0;i<60;i++){ out.prog=(d.querySelector('.progress-label')||{innerText:''}).innerText; if(!/Uploading/i.test(out.prog)) break; await sleep(2000); }
     out.link=[...new Set(Array.from(d.querySelectorAll('a')).map(a=>a.href).filter(h=>/youtu\.be|youtube\.com\/(watch|shorts)/.test(h)).map(h=>h.split('?')[0]))];
     const btn=d.querySelector('#done-button'); out.button=norm(btn.innerText);
     if(out.time!==m.time || out.button!=='Schedule'){ out.error='stopped: time or button is not as planned'; }
     else { btn.click(); await sleep(6000);
       out.answer=Array.from(document.querySelectorAll('ytcp-dialog, ytcp-video-share-dialog')).filter(e=>e.offsetParent!==null)
         .map(e=>norm(e.innerText).replace(/https?:\/\/\S+/g,x=>x.split('?')[0]).slice(0,170)).filter(s=>s.length>16)[0]; } }
   } }
   JSON.stringify(out)
   ```
   A good answer ends with `"answer":"Video processing Your video will be set to public on November 22, 2026 at 6:00 AM ..."`.
   The time field holds a narrow no-break space ("6:00 AM"): compare it only after `norm()`.
   This sheet schedules for TOMORROW only (the date Studio offers by default); the calls refuse any other date.
   A refused upload answers `"error":"stopped: upload refused or no details form","errs":["Daily upload limit
   reached", ...]` (seen Nov 21 at 9:30 pm PT on both channels): close the box with
   `document.querySelector('ytcp-uploads-dialog #ytcp-uploads-dialog-close-button').click()`, and stop for the day.
   Never print a link with "?" or raw page text with links in it: the tool blocks the whole answer.
4. Switch back to the channel you found, close the tab, empty the `uploads` branch.

## The desk: the main chat's two daily rounds (about 4:45 pm and 9:30 pm PT)
Scheduled runs have no browser (the evening run of Nov 21 found no Claude in Chrome tools), so they never upload to
YouTube. They leave the work here: the show run pushes its full cuts, thumbnails and `sheet.json` to the `show`
branch (`kit/show/handoff.py`); the build runs mark the build the desk should upload with `studio: 1` (and a spare
one with `studio: 2`) next to `hold: [en.youtube, ar.youtube]` in its posts file. The main chat (the one the owner
talks to about Build-It; it has his Chrome) does the uploads:
1. `cd /home/claude/test && git pull --rebase && python3 scripts/yt_desk.py plan` (add `--last` in the evening
   round). It lists what to upload now, in order (the show's full videos, the show's shorts, builds marked 1; with
   `--last` also builds marked 2), only as many as `youtube/desk.yml` allows for the day, and writes the upload
   sheet. A line that says NOT BEFORE a time must wait until then (an older upload has to leave the 24 hours first).
   "Nothing to upload now": stop here.
2. Push the sheet to the `uploads` branch under the name it was given (step 2 of "Steps").
3. Open Studio, remember the channel you found. Per channel, in the plan's order: switch to it, then per video one
   `browser_batch`: the upload page, wait 5 s, call 1, the thumbnail call if the entry has `thumb`, call 2.
   - Good answer ("Your video will be set to public on ..."): `python3 scripts/yt_desk.py done <key> <video id>`
     (the id is the end of the link in the answer) before the next video.
   - "Daily upload limit reached": close the box, `python3 scripts/yt_desk.py refused en|ar`, stop the whole round
     (the other channel is refused too) and tell the owner in one line what stayed off YouTube.
   - Any other stop: read the page, fix what the answer names, or leave that video and go on.
4. When the show's four videos are recorded: `python3 scripts/yt_desk.py release <show id>` takes its TikTok and
   Instagram posts off hold. Commit `youtube/ledger.json` (and the posts file) with `[skip ci]` left OUT when a posts
   file changed (post.yml must run), pull --rebase, push.
5. Switch Studio back to the channel you found, close the tab, empty the `uploads` branch.
6. Browser out of reach (no connected browser, the computer asleep): try once more 45 minutes later. If the evening
   round still cannot reach it, tell the owner in one line what waits; with Chrome open he only has to say "go".
7. Each round sets the same round for the next day (send_later into this chat), so the chain does not stop.
When `youtube/desk.yml` says `verified: true`, there is no share any more: every build is marked `studio: 1` and the
desk uploads them all.

## Known limits
- The tappable "Related video" link on a Short is refused for this login ("Only channel owner can gain access").
- End screens and cards were not tried.
