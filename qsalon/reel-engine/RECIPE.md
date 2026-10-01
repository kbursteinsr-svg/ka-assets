# Q Salon reel recipe (locked 2026-10-01, approved on Monday evening reel)

Reference build: mon/v4/reel.json -> qsalon_mon_reelB_final.mp4 (31.5s)

- Voice: ElevenLabs "Will - Relaxed Optimist" (bIHbv24MWmeRgasZH58o), model eleven_multilingual_v2.
  One continuous take. Plain punctuation only: short sentences, a blank line between beats. No audio tags, no ellipses.
- Music: Epidemic "Champagne Toast (Instrumental Version)" (267dc7f4-0f5b-419b-81ab-d252b9ddb7fe), upbeat hip hop,
  trimmed with EditRecording to the reel length. Bed volume 0.34, sidechain ratio 5, threshold 0.04. Voice loudnorm I=-18 TP=-2 (I=-15 sounded like yelling).
  Never smooth jazz / lounge (Kris: sounded like a massage parlor).
- Visuals: engine/build_html.py. Navy/brass Q Salon kit, Marcellus + Hanken Grotesk + DM Mono.
  At least one photo per reel as a framed .shot (16:9) or .shot.tall (4:5) with slow zoom.
  Susy's photo on the CTA scene. Captions synced to silencedetect phrase onsets (+0.4s lead).
- Length: 30-35s for evening explainers. Lead-in 0.4s, 1.5-1.6s tail.
- Render: 30fps, crf 18, AAC 256k/48k, loudnorm I=-15.
- Copy rules: no "one man at a time", no session-length lines ("45 minutes", "a full hour").
  Talk about Susy in third person (Will is the narrator).
- Delivery: upload MP4 to ka-assets/qsalon/reels/, serve via
  https://cdn.jsdelivr.net/gh/kbursteinsr-svg/ka-assets@main/qsalon/reels/<file>.mp4 (video/mp4),
  add a row to n8n data table qsalon_ig_reels (status queued, scheduledAt UTC). Scheduler: gJuWHnhFBsLMEoKR.
