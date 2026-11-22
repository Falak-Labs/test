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
- One Google login holds four channels, and switching is shared by every chat that uses the browser:
  Yallah Say MA `@YallahSayMa` (UC_c7QhlukkSAR-qHKeSvkPA), Congrats Engineer `@congratsengineer`
  (UCDkfxHa7q5Ea0OoiSSi8DHA), Kef Tenbeni `@kef.tenbeni` (UC8qDuZpMDQXRrowaNp29vow), Yalla Say PS `@YallaSayPa`.
  Check the channel name in the same call that loads the file, and again before the last click. The daily task
  "Build-It 4-minute show" uses the browser between about 1:15 and 3 pm PT: do not switch channels then.

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
The owner, Nov 21 2026: Buffer keeps Instagram and TikTok; YouTube goes up here.
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
   // call 2: fill, schedule, report
   const KEY='ep58-ferriswheel-en'; const META='https://raw.githubusercontent.com/Falak-Labs/test/uploads/sheet.json';
   const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const norm=s=>s.replace(/\s+/g,' ').trim(); await sleep(3500);
   const m=(await (await fetch(META)).json())[KEY]; const d=document.querySelector('ytcp-uploads-dialog');
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
   const out={title, titleOk: title.trim()===m.title, descLen: desc.length, wantLen: m.desc.length, kidsNo:st('VIDEO_MADE_FOR_KIDS_NOT_MFK'),
     paidNo:st('VIDEO_PAID_PRODUCT_PLACEMENT_NO'), alteredNo:st('VIDEO_HAS_ALTERED_CONTENT_NO'), lang:norm(d.querySelector('#language-input').innerText)};
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
     for(let i=0;i<30;i++){ out.prog=(d.querySelector('.progress-label')||{innerText:''}).innerText; if(!/Uploading/i.test(out.prog)) break; await sleep(2000); }
     out.link=[...new Set(Array.from(d.querySelectorAll('a')).map(a=>a.href).filter(h=>/youtu\.be|youtube\.com\/(watch|shorts)/.test(h)).map(h=>h.split('?')[0]))];
     const btn=d.querySelector('#done-button'); out.button=norm(btn.innerText);
     if(out.time!==m.time || out.button!=='Schedule'){ out.error='stopped: time or button is not as planned'; }
     else { btn.click(); await sleep(6000);
       out.answer=Array.from(document.querySelectorAll('ytcp-dialog, ytcp-video-share-dialog')).filter(e=>e.offsetParent!==null)
         .map(e=>norm(e.innerText).replace(/https?:\/\/\S+/g,x=>x.split('?')[0]).slice(0,170)).filter(s=>s.length>16)[0]; } }
   JSON.stringify(out)
   ```
   A good answer ends with `"answer":"Video processing Your video will be set to public on November 22, 2026 at 6:00 AM ..."`.
   The time field holds a narrow no-break space ("6:00 AM"): compare it only after `norm()`.
   This sheet schedules for TOMORROW only (the date Studio offers by default); the calls refuse any other date.
4. Switch back to the channel you found, close the tab, empty the `uploads` branch.

## Known limits
- The tappable "Related video" link on a Short is refused for this login ("Only channel owner can gain access").
- End screens and cards were not tried.
