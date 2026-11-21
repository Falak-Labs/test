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

## Known limits
- The tappable "Related video" link on a Short is refused for this login ("Only channel owner can gain access").
- End screens and cards were not tried.
