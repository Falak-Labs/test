# Yallah Say on YouTube

YouTube goes up through YouTube Studio in the owner's Chrome (YOUTUBE_STUDIO_UPLOAD.md), not through Buffer.
Channels: Yallah Say MA @YallahSayMa (UC_c7QhlukkSAR-qHKeSvkPA), Yallah Say PS @YallahSay-Pa (UCXJLd8EVa_XOLnQwnfxtoxw).
- The owner renamed the Palestinian channel on Nov 21 2026 (evening, Pacific): it was "Yalla Say" with the handle
  @YallaSayPa. Its Instagram and TikTok are yallahsaypa, so YouTube now differs only by the hyphen.
- In Studio the two channels are now both called "Yallah Say" and differ only by the flag: tell them apart by the
  channel ID in the address or by the handle, never by the name alone.
- In captions write the YouTube handle without "@" (YallahSay-Pa): on Instagram "@YallahSay-Pa" would link another
  account. Episode 1's Palestinian captions on Instagram and TikTok went out with the old spelling, YallaSayPa.
- YouTube's link preview (oembed) still showed the old name and handle 90 minutes after the change.

## Uploads
- ep01 ma: public since 2026-11-22 02:42 UTC, https://youtube.com/shorts/N8ALrGF-4W0
  (Short, 1:34, category Education, language Arabic, not made for kids, AI question answered No; checks: no issues).
- ep01 pa: public since 2026-11-22 03:05 UTC, https://www.youtube.com/shorts/gwbWb56Hdfo. It went up through
  Buffer (the owner connected YouTube in the Palestinian Buffer account at about 02:50 UTC), because Studio refused the
  same file twice (02:39 and 02:51 UTC): "Daily upload limit reached. Upload more videos daily after a one-time
  verification or wait 24 hours." So on this channel Studio uploads wait for the owner's verification, while Buffer's
  upload worked. Buffer's free plan sends only a couple of YouTube posts a day and no long videos.

## Feature eligibility (Studio > Settings > Channel), read 2026-11-22
- Yallah Say MA: Standard, Intermediate and Advanced are all Enabled.
- Yallah Say PS: Standard Enabled; Intermediate and Advanced only "Eligible". Advanced is what gives "increased daily
  video uploads" and "eligibility to apply for monetization". Only the owner can do that verification.

## Nov 22 2026 uploads (all public, through Studio; uploaded private first, then made public after YouTube's checks)
- Shorts, lessons 4-6. ma: 8byi4cMX_e4 (ep04), U943H7A5JFE (ep05), ULaVuOqQkJA (ep06). pa: 8ieOrmdPHkc, X9VH1wgLALs, Od1RqWcZcvo.
- Long videos (about 4:30, 16:9, the three Shorts of the day joined over a blurred background): "day 1" = lessons 1-3, "day 2" = lessons 4-6.
  ma: ZDxMPceOSA0 is pa day 1; ma day 1 EhVkwfbWDjQ, ma day 2 -MKXTwc9m2k; pa day 1 ZDxMPceOSA0, pa day 2 6j380VBMtUs.
- Day 3 long videos (lessons 7-9) are on the yallah-media branch as yallah-say-ma-long3.mp4 and yallah-say-pa-long3.mp4, not uploaded yet.
- YouTube's checks take 5 to 10 minutes per video: publishing sooner gives a warning about limited visibility. Upload as private, switch to public later.
- Studio's /video/<id>/edit page works for either channel while the login holds both.
- post_due.py retries a YouTube target that failed on Buffer's 2-a-day limit: if the same Short was already uploaded through Studio, mark that target "sent" in yallah/state/<ep>.json first, or it is sent twice.
