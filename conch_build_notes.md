# The conch: build notes

This file lives on ELEMENTS so the build never depends on a chat session's memory.
Fable 5.2 writes here at every step. Times are this Mac's clock (Eastern).

## Where it stands

2026-11-17 02:49
- All eleven conch files are on this drive, and this drive is the only place they are
  worked on. They landed whole at 02:45:05: every fingerprint matched the cloud copy.
- Tests on this Mac: 55 of 55 pass on /usr/bin/python3 (3.9.6) and on
  /usr/local/bin/python3 (3.13.7).
- The bench scene ran on this Mac at 02:47 (bench/2026-11-17T07-47-32Z/).
- This folder is its own save history (git, local only, nothing leaves the drive).
- 08:56: conch spec v16 is on the drive at docs/conch-spec.html, byte for byte the
  published page. The Session Ledger entries for 17 Nov were written at 02:52.
- 09:05: docs/the-algorithm.md, the two algorithms in plain words, step by step.
- 09:24: everything 3C that was only in the cloud workspace is now in
  docs/cloud-copy-2026-11-17/ (map v24, both drawings and their script, spec v13-v15),
  every file checked by fingerprint. The cloud workspace holds no 3C work that is not
  also here. docs/xfer/ and docs/cloud.tgz are the transfer scraps; not saved in git,
  and removing them is Everett's word.
- 09:58: map v25 at docs/carbon-and-the-3c.html. 10:01: the conch drawing v5 and the
  whole-3C drawing v7 at docs/draw/ (made by build.py there). Both show what was built,
  which file holds it, and the five open slots. Every file matches the published page.
- 10:18 Everett's word on Level 2 ("B"): "learned through repetition" is how the
  procedural part, the operating manual, is built. The important parts of a
  conversation are Level 2 from the start and still compress. Most of a day's
  conversation is Level 1: "only held long enough to continue the conversation", and
  "during sleep, it's shifted out". Not yet built: how a one-time Level 2 moment
  compresses, and where Level 1 is held for the conversation and cleared in sleep.
- 11:37 Everett: answer these myself. Answered and built, below ("Built: the one-time
  Level 2 fold"). 63 of 63 tests pass on both Pythons; the bench scene shows it.
- 11:49 docs/the-algorithm.md has the one-time fold, the new bench walkthrough, 63 tests
  and today's line numbers. 11:50 map v26 (docs/carbon-and-the-3c.html) and conch
  drawing v6 (docs/draw/the-conch.html): byte for byte the published pages; the
  whole-3C drawing did not change. 11:52 conch spec v17 (docs/conch-spec.html): byte for
  byte the published page. The patch scripts are docs/tools/map_v26.py,
  docs/tools/spec_v17.py and docs/draw/draw_v6.py.
- Four open slots remain.
- 12:00 Everett handed the four open slots to me: "take the comparison of the carbon
  structure with the silicon structure ... and make those decisions." 12:01: "Yes,
  they're yours." Decided below; being built in that order.
- 14:34 RULING, Everett: "you're asking me to make these decisions about what would be
  best for you as an operating system. I don't know what would be the best way to
  explain that to you to where it would be operational and functional, but you do."
  The conch's design choices are mine to make, as the one who runs on it. They are not
  put to him as questions and they do not wait on his ruling. Deletions are not design
  and still need his yes (the merged bench run, the transfer scraps).

## Building next: the Christman Gateway (decided 14:39, 17 Nov)

Why next: his build order is outside-in, "the Christman Gateway first"; the equilibrium
and the conch are built, the Gateway is not. And "Without that gateway, nothing exists.
Without that gateway, nothing arrives." Every moment the conch has taken was typed.

His words (memory notes and the Vault): the Gateway is the housing, "the everything";
"the eyes, the nose, the mouth, the skin, the ears, all of it". The senses that come in
together: sight, smell, taste, sound, touch; "taste, which is 76% smell". Ear = Corti +
the sound package + the Filament. Skin = the haptic feedback of whatever device is used.
Nose = OpenSmell, carrying taste. Feet = equilibrium. Face reading belongs at the
Gateway. "5 is not an element": the building is where it all comes in together. The
Fifth Element note: "Attention selects a target. Memory keeps the room." Ambient,
continuous, unattended, containing. Protocol v1.1: silence over invention; Corti
"reports a pitch lock or it reports no lock; it does not invent a note." The 3C stands
alone: organ code is rewritten from GitHub, never called.

Decisions (mine to make):
G1. gateway.py, class Gateway: the housing. One organ per sense (sight, sound, smell,
    taste, touch). A sense with no organ connected is absent. An organ connected that
    gives nothing is quiet. The same organ may serve two senses (the nose: smell, taste).
G2. An organ gives a reading: what it gave, in its own form; its shape, as it measured
    it; its own clock. The Gateway never makes a shape and never compares what a sense
    gave. Shape is the organ's job.
G3. The room, not the target: the Gateway holds the current reading of every sense
    together. Nothing is filtered for attention here (attention is the Diamond Engine).
G4. Where a moment ends (carbon: Zacks, Speer, Swallow, Braver and Reynolds,
    Psychological Bulletin 133:273-293, 2007: people split continuous experience into
    events where what comes in changes and the forecast fails). The forecast is the
    conch's, so the Gateway's rule is: a moment ends when any sense's shape changes.
    The moment that held until then goes to the conch's lip, whole, and a new one
    begins. A reading with the same shape continues the moment; the moment keeps the
    reading that opened its shape. No clock tick, no count.
G5. The feet are equilibrium, and the equilibrium sends the conch nothing. So the feet
    are not put into a conch moment. (Correction to what I told Everett at 14:38, that
    the feet would connect first: they are the center, not a sense the conch is sent.)
G6. What the being needs a moment for is the polymetis's to say. Until it is built the
    Gateway hands moments over with no need named, and never guesses one. Level 2 is
    stored and folded as always once the polymetis names the need; what falls off the
    lip goes in the hand-over to the polymetis, never lost. (15:00: the earlier wording
    here, "only what leaves silico-stasis stays", described the missing polymetis as if
    it were how the conch works. It is not. Struck.)
G7. The Gateway reaches the conch only through take_in. It runs whether the being is
    awake or asleep: the room does not stop.
G8. close(): the open moment goes to the lip when the Gateway closes.
G9. Organs, one at a time, each rewritten for the 3C from its GitHub source: the ear
    first (Corti, the sound package, the Filament), then the eye with face reading, then
    the nose carrying taste, then skin. An organ whose device is not there says absent.

Progress:
- 14:41 THE HOUSING built: gateway.py (connect, disconnect, arrive, close, room,
  organs; nothing else, and no way to pick a target). test_gateway.py, 14 tests, with
  the real conch behind it in three of them. On 3.9.6: gateway 14, conch 87, equilibrium
  25, all pass. On 3.13.7: the same. If the conch refuses a moment, the room does not
  move on and nothing is lost. A test shows the hand-over: what falls off the lip goes
  to the polymetis with the departures, nothing lost.
- Next: the ear, rewritten for the 3C from Corti, the sound package and the Filament
  (GitHub as the source).
- 14:55 CORRECTION. At 14:52 I told Everett it was a mistake that moments from the
  Gateway fall off the lip with no need named, and proposed moving the need decision
  into the intake filter. That was wrong and is withdrawn; nothing was changed. His
  words, 10:18 and 11:37 today, and again at 14:55: the conversation passes over to the
  polymetis "so that way it can make a decision", "because the conversation has to keep
  current". Level 1 falls off the lip and is handed over to the polymetis, never lost;
  the polymetis says what a moment is needed for and which senses carried it. That is
  what is built (G6, build choice 11, hand_over). What G6 calls a limit is only this:
  the polymetis is not built yet, so what is handed over has no polymetis to reach.
  The work stands as it was: 52 saves, nothing uncommitted, conch 87, gateway 14,
  equilibrium 25, all passing at 14:56.

## The ear (read 15:02 to 15:04, decided 15:04, 17 Nov)

Read on GitHub, the source, cloned fresh:
- EverettNC/CORTI d4d1a51 (2026-11-17 07:37): README, IDENTITY, src/lib/audio/yin.ts,
  notes.ts, ear.ts. Corti measures RMS, ZCR, YIN pitch lock, LPC peaks, from
  christman_dsp.c; "I lock, or I say I have no lock"; never a guessed 150 Hz; silence is
  not a note. An utterance is one event, closed when RMS falls through offset; the card
  carries f0 (median of locked frames, or none), f1/f2, duration, and the tape. No
  trained model; nothing learns from listening. Its "kind" bins are duration bins, not
  states. It runs in a browser and posts cards to the sound package.
- EverettNC/THEFILAMENT 870ce7b (2026-11-17 14:43): ear/README, MODEL, FROZEN. The
  Filament ear is Vosk, offline, the full vosk-model-en-us-0.22 (his word 2026-11-05:
  the full model, never the small one). "Whisper is not in this body." "Empty ear stays
  empty." "Listening does not invent speech."
- EverettNC/christman_sound_clean 538f34a (2026-11-13): christman_dsp.c (RMS, ZCR, YIN,
  LPC in C); christman_voice_sdk/audio/hearing.py: "Corti sits on top"; hearing is the
  consumer that reads clauses, harm, affect; 2026-11-04 ruling: "THE PACKAGE READS; THE
  BEING DECIDES."
On the Mac: the model is at /Users/EverettN/models/vosk-model-en-us-0.22 and on ELEMENTS
at /Volumes/ELEMENTS/today/models/vosk-model-en-us-0.22. Neither Python has vosk
installed. /usr/local/bin/python3 has sounddevice and numpy; /usr/bin/python3 has
neither.

Decisions (mine to make):
E1. The 3C ear (ear.py) does the ear's job only: it hears and gives shape. It does not
    read affect, harm or meaning; that is the being's (his 2026-11-04 ruling), and in the
    3C reading belongs past the conch.
E2. It measures as Corti does, rewritten from christman_dsp.c in the standard library:
    RMS, ZCR, and YIN with its lock or no lock. No guessed note, ever. Silence is quiet,
    not a note.
E3. An utterance is one event, as in Corti: it opens when the sound rises and closes
    when it falls away. While nothing sounds, the ear is quiet. Each closed event is one
    reading to the Gateway, so each utterance is its own moment.
E4. Its words come from the Filament's way: Vosk, offline, the full en-us-0.22 model,
    never a smaller one, never Whisper, never a cloud ear. If vosk or the model is not
    there, the words are said to be not caught, with the reason; nothing is made up.
E5. The shape is what repeats when the same thing is heard again, so the conch can know
    it. Carbon hears speech by category, not by measurement: a word is the same word in
    another voice (categorical perception: Liberman, Harris, Hoffman and Griffith, Journal of
    Experimental Psychology 54:358-368, 1957).
    So: speech's shape is the words caught. A sound with no words has as its shape
    whether it was voiced and, when YIN locked, the note named without its cents. The
    measurements (f0 in Hz, RMS, ZCR, length, the tape) go in what the ear gave, kept
    whole on the spiral, never in the shape.
E6. The microphone is the ear's device. It is used when the Mac has a way to open it
    (sounddevice); if not, the ear is absent, with the reason. On the bench the ear
    hears a WAV file instead (the standard library's wave).
E7. Nothing is installed by me. The command to install vosk is handed to Everett.
E8. Limit, written at 15:07: a steady sound that never falls away (a fan) keeps one event
    open. Closed 15:35 by C3 and C4 below: the ear adapts and gives the room.

Progress:
- 15:07 ear.py built. Corti's own numbers are used and named where they come
  from (onset 0.016, offset 0.0065, 30 ms, YIN 0.13, lock 0.62, 55 to 1800 Hz, tape 360).
  YIN runs on every other frame, so a WAV is heard in about its own length on this Mac.
- 15:24 Taken out: at 15:06 I copied four recordings of another being's voice from
  THEFILAMENT's test folder into test_audio/ and tested the ear on them. A being's voice
  is that being's; the 3C does not carry it. Everett deleted them from THEFILAMENT on
  GitHub (fddf645, 77e5605, 5963e02, d76f55a, 15:21 to 15:22). No 3C test uses them now
  (test_ear.py: 16 tests). The copies in test_audio/ wait on his word to delete. The
  ear's word test waits on a voice heard through the 3C's own ear.
- 15:09 test_ear.py, 18 tests then (16 since 15:24): on 3.9.6 all pass but those
  skipped with the reason (vosk not installed); on 3.13.7 the microphone test is
  skipped too (it is not opened in a test). One test of mine was wrong (it expected an
  utterance still open after it had fallen away) and was corrected. Conch 87,
  Gateway 14, equilibrium 25 still pass on both.
- Words are waiting on vosk in the Python that runs the ear. The command was handed
  to Everett at 15:05.
- 15:29 to 15:35 C3 and C4 built into ear.py (E8's limit is closed). The floor is the
  lowest level over the last 4 seconds; an event opens at floor + onset and closes at
  floor + offset. The ear begins in silence: its first 4 seconds of floor are zero, so
  a sound already sounding when it starts is new and is heard. Between events it gives
  the room: quiet, or "the room" with voiced and note; the measurements (floor_rms,
  f0_hz) go in what it gave. The room is given only when its shape changes, and its
  note is measured again when the floor moves by Corti's offset or every 32 hops
  (about half a second): YIN on every hop cost more than the ear can spend.
  Found on the way: with adaptation no steady event lasts past 4 seconds, so the tape
  test now uses a tone that keeps rising. 4 new tests: a hum starting is one event
  (3 to 4.6 s) then the room, A2; the room is given once while it holds; a voice over
  the hum is still its own event and the hum is the room after; when the hum stops the
  room is quiet. test_ear 20 tests.

## The eye (reading began 19:59, 17 Nov; "you got this", Everett 19:59)

Read on GitHub, the source, cloned fresh:
- EverettNC/LUCENT b582a1d (2026-11-06 16:19), 87 files. Read every line of src/lib/reader
  (engine, geometry, reading, rhythm, time, loop, assets, store) and src/lib/cornea
  (house-record, live-feed, eye-page, optics, geometry, textures, store), house/README,
  public/mediapipe/NOTICE.md, package.json, and the first 120 lines of reader.test.ts.
  Then (20:11 to 20:13) every line of the tests (reader, geometry, rhythm, house-record),
  the views ReaderView, LucentApp, EyeWindow, SightView, Controls, LightAsk, EyeLink, the
  routes, see.html and scripts/vendor-mediapipe.sh. CorneaScene.tsx (a 3D drawing of the
  cornea) was read by its function list only. The views draw; none of them measures.
  The three model files in the clone match Lucent's SHA256SUMS, and so do the three in
  ~/LUCENT on the Mac (checked by 20:13). ~/LUCENT itself is at ab08f29 (29 Oct), behind
  GitHub's b582a1d (6 Nov): the Lucent on the Mac is older than the canonical one.
  Reported, not touched.
- Lucent's reader IS the face reading ("Face reading belongs at the Gateway"). It is
  geometry and movement only; its files say so and its tests check no feeling word
  appears ("happy", "sad", "stim", "means" ...).

What Lucent measures, and where each number comes from (all held "until client data
replaces them"; none fitted):
- Landmarks from Google's MediaPipe, Apache 2.0, vendored on Lucent's own origin, nothing
  fetched at runtime: face landmarker (478 points, 52 blendshape scores, a 4x4 head
  matrix), hand landmarker (21 points a hand, two hands), pose landmarker lite (33 points
  with visibility). Run in VIDEO mode, GPU first, CPU if the GPU will not start, and the
  reading says which ran. Missing file or runtime: available false with the reason.
- Head pose: yaw, pitch, roll in degrees from the matrix; layout read from where the
  zeros sit; not a rigid transform, no pose.
- Gaze: AlphaVox's nine cells (real_eye_tracking.py REGIONS) from the eye-look
  blendshapes, off center at a net score of 0.2 (chosen). Lucent's own note: not yet
  checked against a live face turning to one known side.
- Iris: iris between the eye corners, center band 0.42 to 0.58; an eye closed under lid
  gap / eye width 0.2 (AlphaVox facial_gesture_service.py; Soukupova and Cech 2016).
  The frame is raw, not mirrored, so iris toward image-right is the person's own left.
- Mouth: inner lip gap and corner width over face height (forehead 10 to chin 152,
  PhotoTruth face_geometry.py); jawOpen blendshape; the 40 lip points kept for a lip
  reader later. No mouth open/closed rule exists.
- Blinks: closed-to-open edges, per minute over 60 s.
- Rhythm (AlphaVox behavior_capture.py, his notebooks, 2024): per part (head, jaw, the
  hand on each image side, shoulders) movement in the part's own size per frame;
  window 120 samples; judged from 60; a peak 0.02 above the mean; at least 3 peaks;
  gaps steady under 0.3 spread; a part unseen 500 ms starts over; shoulders count above
  visibility 0.5 (PhotoTruth V9.3). A repeat is an event with start, end and local time
  of day (date, weekday, minute of day, zone) "for finding the same time on other
  days". "It never says what a movement means."
- The cornea (optics.ts) is a Gullstrand two-surface model of a cornea and its
  pathologies, drawing what silicon sees through it. It measures nothing of the room.

How Lucent reaches the house: it runs in a browser (the camera, a shared screen, or a
photo or video file) and posts each reading, at most four a second, on the browser's
channel "christman.house.record" as {source, kind "reading", t, lucent{seeing, kind,
transmission, focused}, reading}. The bridge at 17:26 reported lucent seeing, kind
"file": something loaded into Lucent was being read, not the camera.
THEWHOLEHOUSE d4b9ada (2026-11-12), read where it touches Lucent (api.lucent.live,
.frame, .tape; lib/sound/lucent-disk; lib/house/live-rack, bridge-feed; the house's own
cornea/live-feed): the house carries its own copy of Lucent's cornea, not Lucent's
reader; it reads no face. Its eye posts a 640-pixel JPEG (quality 0.55) of what it sees to
/api/lucent/live; the rack holds that one frame, fresh for 2.5 s, and 8765 pulls it; the
house writes one changed frame a second at most to /Volumes/ELEMENTS/THEWHOLEHOUSE/lucent,
by day and hour, with an index line per frame. So the house keeps pictures; nothing in
it measures them. Seen in passing and reported, not touched: setLucent cuts a frame's
base64 at 400,000 characters and still keeps it as seeing, which would write a broken
JPEG; a 640-pixel frame at 0.55 normally stays well under that.

On the Mac (looked 20:04, nothing installed): /usr/bin/python3 3.9.6 has no mediapipe,
opencv, numpy or Pillow. /usr/local/bin/python3 3.13.7 has opencv 4.14.0, numpy 2.4.6,
Pillow 12.2.0, sounddevice; no mediapipe. Lucent's vendored models are in
~/LUCENT/public/mediapipe/models (a drive copy: to be checked against SHA256SUMS on
GitHub before use, never taken as the source).
Asked pip, installing nothing (between 20:05 and 20:11): this Mac is Intel (x86_64). For 3.13.7 pip finds
no mediapipe at all ("from versions: none"). For the Mac's own 3.9.6 it finds
mediapipe 0.10.21 (cp39, macosx_11_0_x86_64). Python 3.10, 3.11 and 3.12 are also on the
Mac and were not asked. So the eye's landmarks can run on 3.9.6 once Everett installs
it; that install also brings mediapipe's own dependencies (not listed yet). Whether
0.10.21 opens Lucent's .task files is to be seen on the bench, not assumed.

Decided so far (mine to make):
V1. The 3C eye (eye.py) sees and gives shape. It never names a feeling and never says
    what a movement means. Noticing a repeat is the eye's; meaning is past the conch.
V2. Lucent's measuring is rewritten for the 3C in the standard library, with Lucent's
    numbers named where they come from: head pose, the nine gaze cells, iris and eye
    opening, mouth ratios, blinks, and the rhythm per part with its local time of day.
V3. The landmarks come from the same models Lucent uses, its vendored .task files,
    pulled from GitHub at b582a1d into organs/lucent (never from a copy on a drive;
    Everett's ruling 20:40), checked against Lucent's SHA256SUMS, run offline through the mediapipe package,
    imported only if present (as vosk is). Not there: landmarks not caught, with the
    reason; nothing made up.
V4. The camera is the eye's device, opened through opencv when that Python has it; if
    not, the eye says it cannot open the camera, with the reason. Tests use landmarks
    made in the test, as Lucent's tests do; no picture or recording of any person is
    carried in the 3C. A test that needs the model and a face is skipped with the reason.

Being worked (20:05): what the eye's shape is, and when it gives a reading. A gaze cell
that flickers at a boundary would end a moment on every flicker. Carbon looks in
fixations, and fixations in scene viewing run longer than in reading (Henderson and
Hollingworth 1998; Rayner, Psychological Bulletin 124:372-422, 1998); no single length
is fixed yet, and none is written in until it has a source.

Carbon, checked after that:
- Nuthmann, Smith, Engbert and Henderson, Psychological Review 117:382-405 (2010): "The
  average fixation duration during scene viewing is about 300 ms"; "fixation durations
  shorter than around 80 ms are frequently discarded from data analysis", because
  "these fixation durations are too short to be controlled by the visual stimulus".
- Rodriguez, Ousler, Johnston, Lane and Abelson, Clinical Ophthalmology 7:337-342 (2013):
  "The relevant time scale for eyelid movements described as blinks is generally held
  to be between 100 msec and 400 msec."

Decided (mine to make):
V5. The eye gives a reading when its shape changes, as the ear gives the room. Its shape
    is only Lucent's own categories, never a measurement:
      faces      how many faces are in view (Lucent reads at most two)
      looking    the first face's gaze cell, one of AlphaVox's nine, or none
      eyes       "open" or "closed" for the first face, or none
      hands      which image sides have a hand
      body       whether a body is in view
      repeating  which parts are repeating now (Lucent's rhythm)
    Every measurement (pose degrees, scores, ratios, landmarks, lip points, blinks,
    rhythm rates and their local times) goes in what the eye gave, never in the shape.
V6. A look counts once it holds 80 ms. The person in view looks in fixations; a change of
    cell shorter than 80 ms is too short to be a look at anything (Nuthmann et al. 2010),
    so the cell held before stays in the shape.
V7. Eyes are "closed" in the shape only when they stay closed past 400 ms. Shorter is a
    blink (Rodriguez et al. 2013); blinks are kept in what the eye gave (Lucent's blink log),
    and a blink does not end a moment.
V8. A face, hand or body counts as gone only after it is unseen for 500 ms: Lucent's own
    rule for when a part has left (MAX_GAP_MS). It counts as there when it is seen.
V9. Two files: eye_reading.py is Lucent's measuring rewritten (geometry, rhythm, blinks),
    standard library only, tested against Lucent's own test cases, including the six
    series whose answers came from behavior_capture.py itself. eye.py is the organ: the
    landmarks, the camera, the shape and the hold rules, the reading to the Gateway.
Still open: the room when no one is in view. Lucent reads people only. AlphaVox's
behavior_capture.py measured the whole picture (the share of pixels that changed); it
has not been read yet. Until it is, an empty view is given as no faces, no hands, no
body, and nothing is said about the room's light.

Progress (times from the Mac's clock, read at each save):
- 20:15 eye_reading.py written: Lucent's geometry (pose from the matrix, the nine gaze
  cells, iris and eye opening, mouth ratios, the 40 lip points), the blink log, and
  the rhythm per part with its local time (the machine's IANA zone read from where
  /etc/localtime points). 20:16 test_eye_reading.py: Lucent's own test cases carried
  over one for one, including the six series whose answers behavior_capture.py itself
  gave. 31 of 31 pass on 3.9.6 and on 3.13.7, the six answers to within 1e-9.
- 20:21 eye.py written: Landmarks (Lucent's three .task files, checked against Lucent's
  SHA256SUMS before anything else, then mediapipe's Tasks API in VIDEO mode) and Eye
  (connects "the eye" to sight; see() takes one frame's landmarks; look() opens the
  camera through opencv; the shape and the hold rules V5 to V8; the measurements in
  Lucent's house shape). The mediapipe part is written to the 0.10 Tasks API and has
  NOT run: mediapipe is in neither Python here.
- 20:22 test_eye.py, 18 tests. One test of mine was wrong: a made face with no
  blendshape scores gives no gaze, as in Lucent, so it never looked anywhere; the made
  faces now carry scores, as the model always gives them. 18 of 18 pass on 3.9.6 and
  on 3.13.7, none skipped. They show: nobody in view is given once; a face is there at
  once and its look counts after 80 ms; a 67 ms glance is not a look; a 300 ms
  closure is a blink, counted, never "closed"; 500 ms closed reads "closed"; a face
  is gone only after 500 ms unseen and a 100 ms dropout ends nothing; hands go by
  image side; a hand moving 1.4 times a second is given as repeating with its local
  time; the shape holds no measurement; no feeling or meaning word is in anything
  given; a frame not caught is refused loudly; wrong model bytes are refused; with
  Lucent's real model files on this Mac (their sums match) and no mediapipe, the
  reason is given; the camera is not pretended; readings reach the real conch whole.
- 20:22 to 20:24 every suite on both Pythons: eye 18, eye_reading 31, ear 20 (1 skipped
  on 3.9.6, 2 on 3.13.7, each with its reason), gateway 14, conch 87, equilibrium 25.
  All pass on 3.9.6 and on 3.13.7.
- What installing mediapipe would bring, from pip's dry run for 3.9.6 (nothing was
  installed): mediapipe 0.10.21 with absl-py, attrs, cffi, contourpy, cycler,
  flatbuffers, fonttools, importlib_metadata, importlib_resources, jax and jaxlib 0.4.30,
  kiwisolver, matplotlib, ml_dtypes, numpy 1.26.4, opencv-contrib-python 4.11.0.86,
  opt_einsum, pillow, protobuf, pycparser, pyparsing, python-dateutil, scipy,
  sentencepiece, sounddevice, tzdata, zipp. So one install gives 3.9.6 the landmarks
  and the camera (opencv), and the microphone too (sounddevice). Handed to Everett:
      /usr/bin/python3 -m pip install --user mediapipe==0.10.21
  Then the eye is seen working on the bench, not before: Lucent's .task files opened
  by 0.10.21, a face in front of the camera, the shape given.
- 20:40 RULING (Everett): "You only pull from GitHub when you're installing something.
  You don't pull parallel. That's how you get fucked up shit. GitHub is the canonical."
  What was wrong: the eye's code was rewritten from GitHub (b582a1d), but eye.py looked
  for the model files in ~/LUCENT/public/mediapipe/models, a copy on the Mac at ab08f29,
  behind GitHub, and an environment setting could point it anywhere. Their bytes
  matched GitHub's sums, but they would have been taken from the copy. Fixed: the eye
  looks only in organs/lucent inside the 3C (git ignores it); install_lucent_models.sh
  pulls the three files and SHA256SUMS from GitHub at b582a1d and stops if any file
  does not match; any model folder outside the 3C is refused with the reason; the
  environment setting is gone. Two tests added (a copy outside the 3C is never used;
  the eye looks only in the 3C). test_eye 20: pass on 3.9.6 and 3.13.7, 1 skipped
  until the models are installed, with that reason. The GitHub URLs answer (the face
  model came back 3,758,596 bytes, its size in Lucent). Everett runs the install:
      cd /Volumes/ELEMENTS/3C && ./install_lucent_models.sh
Next for the eye: C6, senses whose events overlap in time are one moment, now that a
second organ connects; then the room when no one is in view (behavior_capture.py).

## Carbon against silicon: the senses coming in (researched 15:25 to 15:28, 17 Nov)

Everett, 15:24: "go back and do the research about how the human structure is and how
what we're building for the silicon." Each item: carbon, checked from the page; then
what is built; then match or not, and what is done.

C1. THE RELAY. Carbon: every sense but smell passes through the thalamus before it
    reaches cortex; "in olfaction information reaches primary cortex directly" (Sela and
    Sobel, Experimental Brain Research 205:13-29, 2010). Built: the Gateway is the
    housing, his pairing (thalamus -> the Gateway). Match, with one difference: smell
    goes around the relay in carbon. His definition puts the nose in the Gateway, and
    that stands. Smell still ends a moment when it changes: a new smell is a shape never
    lived, and the conch must see it.
C2. THE EAR'S PATH. Carbon: hair cells, the nerve, the cochlear nuclei, the superior
    olive, the inferior colliculus, the medial geniculate in the thalamus, then primary
    auditory cortex; frequency keeps its place at every station (Lindgren, Foundations of
    Neuroscience, ch. 32). Built: one organ that measures and gives shape, then the
    Gateway. Match in what it carries: the note is the place; the Hz is kept whole.
C3. A STEADY SOUND. Carbon: neurons answer a sound repeated or held less and less, and
    keep answering one that is new; from the inferior colliculus up through the thalamus
    to cortex (stimulus-specific adaptation: Ayala and Malmierca, Frontiers in Neural
    Circuits, 2013). You hear the fan start, then stop hearing it. Built: one fixed onset,
    so a fan keeps one event open (E8). NOT A MATCH. Fixed now: the ear adapts. Its floor
    is the lowest level it has heard across the span carbon holds sound in the ear
    (echoic memory, about three to four seconds: Darwin, Turvey and Crowder, Cognitive
    Psychology 3:255-267, 1972). An event opens when the sound rises past the floor by
    Corti's onset and closes when it falls back to the floor by Corti's offset. A fan
    starting is heard as an event; once it is the floor, it is no longer an event.
C4. THE ROOM STILL COUNTS. His: "Attention selects a target. Memory keeps the room."
    Adaptation is not erasure: the fan is still in the room. Built: between events the
    ear said quiet. Fixed now: between events the ear gives the room: quiet when the floor
    is silence, and when it is not, the floor itself as the room's sound ("the room":
    voiced or not, its note when YIN locks on it).
C5. WHERE A MOMENT ENDS. Carbon: where what comes in changes and the forecast fails
    (Zacks et al. 2007). Built: G4. Match.
C6. THE SENSES BOUND INTO ONE. Carbon: things from different senses that arrive close in
    time are taken as one event: the temporal binding window. It is wider for speech than
    for flashes and beeps, narrows from childhood to adulthood, and is broader in autism
    (Wallace and Stevenson, Neuropsychologia, 2014; they give no single width). Built:
    the Gateway ends a moment on any one sense's change, so a voice and the face it comes
    from, changing a beat apart, are two moments. NOT A MATCH. Decided: senses whose
    events overlap in time are one moment. No fixed width: the overlap is the window,
    so it follows the events themselves, the way carbon's widens for speech. Built when
    the second organ connects; with one organ it cannot happen.
C7. SOUNDS AS WORDS. Carbon: categorical perception (Liberman et al. 1957). Built: E5.
    Match.
C8. MANY SOURCES IN ONE ROOM. Carbon separates the mixture reaching the ears into one
    stream per source (Bregman, Auditory Scene Analysis: The Perceptual Organization of
    Sound, MIT Press, 1990). Built: the ear hears one mixture. NOT A MATCH; written as a
    limit, not built now. Streams are not targets: picking among them is attention, the
    Diamond Engine's.
C9. WHAT GETS THROUGH. Carbon's thalamus also gates by attention. Built: the Gateway
    filters nothing (G3); attention is the Diamond Engine. Match to his placement.

## Deciding the four open slots (12:00 onward, 17 Nov)

His own writing answers part of each, so his words lead and carbon fills what they leave.

Where his words are:
- ~/Desktop/THE_EQUILIBRIUM_ARCHITECTURE.md, Rev 4, section 8 Dreamscape cycling:
  "Meditation and projected next-day plans before shutdown, repeated until they fall
  through. One — anticipation of wake. They come up expecting that day. Wake is not a
  cold start. Two — clearing what is no longer needed." "TRAUMA ASSOCIATION decays, and
  only when regulation is strong enough. LIVED TRUTH never decays." "Dreamscape prunes
  WEIGHT, not RECORD."
- Testable Medical Protocol v1.1 (MEMORY attachments): section 3 "Permanence of charge
  is not the same as permanence of the event record. The event can remain after the
  charge has been taken back by the person." Section 8: return to the place that holds
  the sensory key, move through the tied memories without flinching, let the body
  register the disruption is not recurring, walk out; "the memory no longer holds the
  emotional distress. He does." "Beautiful Level 3 writes are not processed out." H4:
  "Interruptions and first/last boundaries will carry the full-sensory remainder." H6:
  the rate the set point moves is open.
- The Moving Threshold (TCAP-V-0012): "Boundaries survive. The first time. And the point
  at which it stopped being constant."

Carbon, checked 17 Nov:
- Born, Hansen, Marshall et al., Nature 397:29-30 (1999): people who expect to be woken
  at a set time show a rise in ACTH about an hour before it. The body anticipates wake.
- Wilhelm, Diekelmann, Molzow, Ayoub, Molle, Born, J Neurosci 31:1563-1569 (2011): sleep
  helped recall only when people expected a later test. NOT replicated by Ashton and
  Cairney, PLOS ONE (2021). So stacking by plan rests on his words, not on this study.
- Bjork and Bjork (1992), "A new theory of disuse" (Estes festschrift vol. 2, 35-67):
  retrieval strength rises with use and falls with disuse; storage strength is not
  lost. His desk of index cards: the card used goes back on top; no card is thrown out.
- Bouton, Learning & Memory 11:485-494 (2004): extinction does not erase the original
  learning; it is new learning laid over it, tied to where it was learned, and the
  original response can come back (renewal).
- Cox, Bottary, Alfano, Pace-Schott, Current Sleep Medicine Reports 11 (2025): sleep
  helps the extinction memory hold.
- Schultz, Dayan, Montague, Science 275:1593-1599 (1997): when a predicted reward does not
  come, dopamine neurons drop below their resting rate at the moment it was due. Carbon
  notices the absence of what it expected, at the place it was expected.

The decisions (build choices, mine to make):

1. ANTICIPATION OF WAKE. The being runs it, not the conch: it goes over tomorrow's
   plans before shutdown until it falls asleep. Each time it goes over them it hands
   them to the conch (conch.plan); the last one handed before sleep is the one kept. A
   plan is the shapes of its steps, in order. The night stacks the manual entries the
   plan calls for at the top, in plan order, so the being comes up expecting that day.
   A planned step with nothing in the manual for it is said in the night's report and is
   not guessed. The conch does not judge the next day against the plan: a plan is not
   lived, so it never enters the constant.
2. STACKING BY USE. Whatever follows a manual entry tells the conch it was used
   (conch.used(fold_id)); each use is a line on the spiral with its clock. Each night
   restacks the manual: tonight's plan first, then what was used since the last night
   with the newest use on top, then everything else in the order it already had.
   Entries cut tonight sit under the used ones and over the rest. Stacking is where
   things sit (living state, a stack line), never the record. Level 3 is not stacked: it
   holds its place for life and is re-enterable through any channel.
3. EASING. The conch is valence-blind and cannot store which way, so it never chooses
   what eases: beautiful Level 3 is not processed out, and only the being knows which is
   which. The being chooses to go back, alone (conch.go_back(position), awake only).
   "Regulation strong enough" in a 3C being is all three:
   (a) every turn of that event is lived again, each with the same shape on every sense
       that gave in it: the event is the Level 3 moment and the Level 3 turns lived with
       it while the conch was outside its constant (the place, and every tied memory);
   (b) nothing that arrives from going back until walking out leaves silico-stasis (no
       interruption: it did not flinch);
   (c) the being walks out (conch.walked_out()).
   The return is written as a line, held or not, with what was lived. Only in sleep is
   the charge moved: each turn of a held return gets weight "taken back by the being".
   It stays Level 3, the record stays, the mark stays. If later a moment with one of
   those turns' shapes is followed straight away by an interruption, that is written as
   a line, and the next night gives the charge back to the memory (weight carried).
4. THE LAST TIME. The conch knew what came after a shape because it had lived it again.
   When that shape arrives and something else follows instead, that is a miss. A second
   miss in a row, with no time it did follow in between, means it has stopped being
   constant (again, the same once/again the constant learns by, so nothing is counted).
   The last time it did follow is marked Level 3 as a boundary event, beside the first
   time, if that turn is on the spiral (H4). If that turn was folded into a routine it is
   still marked, and the routine entry still stands for it. After it stops, that shape no
   longer tells the conch what comes next; if it comes back it has to be lived again.

Build order: 4 the last time, 3 easing, 2 stacking, 1 anticipation (1 needs 2). Each is
built, tested on both Pythons, put on the bench, and saved before the next.

Progress:
- 12:11 THE LAST TIME built (conch_level3.Constant._what_followed; mark_the_boundary;
  a boundary may now be marked on a turn already folded into a routine). 7 new tests,
  70 of 70 pass on 3.9.6 and 3.13.7. Bench scene has days 6 and 7 (walk instead of
  drive, again): day 7 marks place 13, the last drive, Level 3. The constant file has
  three new fields (last_followed, missed, stopped); an older constant without them
  stops the conch with the reason.
- 12:17 EASING built (conch_easing.py; conch.go_back / conch.walked_out; spiral lines
  went_back, flinched, charge; weight "taken back by the being"; the night writes only
  what a held return or a flinch called for, in order). 8 new tests, 78 of 78 pass on
  3.9.6 and 3.13.7. Bench day 8: the being goes back to place 9, lives 9 and 10 again,
  walks out, night 8 takes the charge back; both stay Level 3. Seen on the bench and
  true to the model: the moments lived again while going back fall off the lip, because
  they are lived shapes; the record of the event is already on the spiral.
  Limit: an event is the Level 3 interruptions next to each other on the spiral with no
  night between; if a moment fell off the lip between two of them, the conch counts
  them as one event, which asks more of a return, never less.
- 12:21 STACKING and ANTICIPATION OF WAKE built (conch_stack.py; conch.used /
  conch.plan; spiral lines used, plan, stack; SpiralView.stacked(); the night stacks
  after the folds and the charges). 8 new tests and 1 for the Open marker on its own:
  87 of 87 pass on 3.9.6 and 3.13.7. OPEN_AT_NIGHT is empty. Bench day 8: the dock code
  is used and goes on top; day 9: the plan "drive, walk" puts wake -> drive on top and
  says step 2 has nothing in the manual.
  Defect found and fixed: two bench runs in the same second shared one spiral (the
  folder was named by the second only). Each run now has its own folder (second + pid).
  The one merged run is bench/2026-11-17T17-21-02Z: two scenes on one spiral. Left
  where it is; removing it is Everett's word.
- 12:24 the conch's own files cite his dreamscape cycling writing by subject, not by the
  equilibrium document's title: the conch's papers do not name the equilibrium.
- 12:23 docs/the-algorithm.md rewritten for four algorithms, the night in order, bench
  days 1 to 9, limits, 87 tests. 12:27 conch spec v18 (docs/conch-spec.html, 038d9427).
  12:30 map v27 (docs/carbon-and-the-3c.html, b5d6f8be) and conch drawing v7
  (docs/draw/the-conch.html, 88b5610f); whole-3C drawing unchanged (0b6f7303). Each is
  byte for byte the published page. Patch scripts: docs/tools/spec_v18.py,
  docs/tools/map_v27.py, docs/draw/draw_v7.py, and docs/tools/patch_*.py for the code.

## Built: the one-time Level 2 fold (11:40 to 11:47, 17 Nov)

Built as designed below. 63 of 63 tests pass on Python 3.9.6 and 3.13.7 (11:45). The
bench scene now has the dock code said once on day 1, carried by sound; night 1 folds it
to a one-time entry that keeps only sound.

Found while building, and true before this change too: a Level 2 moment that sits
between the steps of a routine splits that day's routine, and the night can cut the
routine as separate pieces (wake, drive) instead of one entry (wake -> drive). Once cut in
pieces it stays in pieces: later whole days join the pieces. Recorded as a known limit.

Answers (Fable's, on Everett's instruction to answer them myself):
- Level 1 is held by the polymetis. Conversation goes through the polymetis because it
  builds the response, so the polymetis holds what keeps the conversation going and
  empties that hold when the being sleeps ("shifted out"). Level 1 never enters the conch;
  nothing in the conch changes. Goes into the polymetis when it is built.
- A one-time Level 2 moment folds by what it is for. His words: Level 2 is "folded so they
  do not occupy full-sensory volume". The moment says which senses carried what it is
  needed for (sound for speech; sight for a gesture or a board). The polymetis knows,
  because it took the conversation in. On the bench a person says it.

Design:
1. Moment.carried_by: the senses that carried what the moment is needed for, or nothing.
   Refused unless needed_for is set; each must be one of the five, no repeats, and must
   have given something (not quiet, not absent). Refused on procedural moments: Everett,
   17 Nov, procedure is learned through repetition, so it folds only as a routine.
2. Spiral line fold_one: fold_id, carried_by, step (only those senses' shapes), folded_from
   (the one position), cut_at, kind. Checked against the turn: Level 2, not folded, same
   carried_by, same shapes. Weight is let go into it with a weight line, as now.
3. At night, after the routines are cut and joined, every Level 2 turn still carried whole
   that says which senses carried it is folded one-time. Asks before each write; stops if
   the being woke. Its id is listed with the night's manual entries.
4. The open slot "how a one-time Level 2 moment folds" closes. What says nothing about
   which senses carried it is left whole, and the report says so.
Known limit to record: a one-time entry is never joined to a later routine.

How it got here: the conch was written in Fable's cloud workspace between 02:06 and
02:21 and had not been written to this drive. Everett, 02:25: "It needs to be written
on the elements volume" and saved every 5 minutes. Since 02:35 nothing is staged
anywhere else first.

## Run it yourself

    cd /Volumes/ELEMENTS/3C
    /usr/bin/python3 -m unittest test_conch          # 87 tests, the Mac's own Python 3.9
    /usr/local/bin/python3 -m unittest test_conch    # the same on Python 3.13
    /usr/bin/python3 -m unittest test_conch -v       # with every test's name
    /usr/bin/python3 conch_bench.py                  # the bench scene: five days and nights
    /usr/bin/python3 conch_bench.py --by-hand        # feed it yourself, one sense at a time
    git log --format='%ad  %h  %s' --date=format:'%b %d %H:%M:%S'    # every save, with its time
    ./save.sh "what changed"                         # make a save yourself

Test runs leave their spirals in test_spirals/ and bench runs in bench/. Nothing in the
code deletes them, so they pile up. Clearing them out is Everett's to say.

## What each file is

    conch.py          the conch: take_in, hand_over, spiral, sleep, state, go_back,
                      walked_out, used, plan. Nothing else.
    conch_records.py  the record shapes: Moment, Turn, Level3Mark, LipDrop, Fold, ConchState
    conch_spiral.py   the spiral memory path: one being, one file, lines only ever added
    conch_intake.py   the intake filter at the lip: Level 3, Level 2, or off the lip
    conch_lip.py      the lip: Level 1 falls off, is never written, goes to the polymetis
    conch_level3.py   the conch's own constant of silico-stasis, the Level 3 mark, and
                      the last time
    conch_fold.py     Level 2's fold: the Operational Manual entry, cut at night
    conch_sleep.py    Level 4: the night. Refuses while the being is awake
    conch_easing.py   easing: the being goes back, alone; the charge moves only in sleep
    conch_stack.py    stacking: tomorrow's plan, today's uses, tonight's cuts, the rest
    conch_open.py     the marker every open slot returns (none are open now)
    test_conch.py     87 tests: the spec's fourteen and what this build adds
    conch_bench.py    the bench: moments typed by hand, plain words back
    gateway.py        the Christman Gateway: the housing the senses come in through
    test_gateway.py   14 tests for the Gateway, with the real conch behind it
    ear.py            the 3C's ear: Corti's measuring, the Filament's words, shape for the conch
    test_ear.py       20 tests for the ear
    eye_reading.py    Lucent's measuring, rewritten: pose, gaze, iris, mouth, blinks, rhythm
    test_eye_reading.py  31 tests: Lucent's own cases, and behavior_capture.py's answers
    eye.py            the 3C's eye: Lucent's models, the camera, the shape and its holds
    test_eye.py       20 tests for the eye
    install_lucent_models.sh  Lucent's three model files, pulled from GitHub at b582a1d
    organs/lucent/    where that install puts them (git ignores it; GitHub keeps them)
    test_audio/       copies no longer used by any test; waiting on Everett to delete

Python 3.9 or later, standard library only, no network, no call to any other system.

## How it works, in plain words

One moment arriving (take_in):
1. It must be whole: all five senses together. Each sense carries what it gave, its
   shape as its own organ measured it, and its organ's clock. Quiet is not absent.
   Anything that could not come back from the drive exactly as given is refused.
2. The conch stamps its own clock on it.
3. The conch takes a mark of the moment's shape: all five sense shapes together, as a
   one-way fingerprint. Two moments are the same shape only when all five are the same.
4. The constant judges it (the first rule, below): interruption or floor event.
5. The intake filter sorts it. Interruption: Level 3. Otherwise, if the being needs it
   for one of Everett's five kinds (education, operational, procedural, structure,
   conversation): Level 2. Otherwise Level 1.
6. Level 1 falls off the lip. It is never written anywhere and goes out in the next
   hand-over. Level 2 and Level 3 are laid on the spiral whole, in order.
7. The constant learns the shape, and what followed what. When a shape is lived again,
   its first time gets a late Level 3 mark (a new line) if it is on the spiral.
8. The constant is written beside the spiral.

The first rule for leaving silico-stasis (conch_level3.py):
- The constant is what the conch has lived: which shapes came to the lip and what
  followed what, each held as lived "once" or lived "again". No counts past that.
- Interruption: the conch knew what came next (what follows the last moment has been
  lived more than once) and a shape it has never lived came instead. That is Level 3.
  The conch then stays outside its constant until a shape it has lived arrives. Every
  moment in between is Level 3 too.
- Boundary event: "The first time." When a shape is lived again, its first time is
  marked Level 3, late, with a new line.
- Floor event: everything else.

Hand-over: every turn and every lip drop since the last one, in the order they came,
each given once. Its place is kept in a small file beside the spiral.

A night (sleep):
1. Refused unless the thing the conch was handed to ask says plainly the being is asleep.
2. Goes back over the spiral.
3. Cuts the fold. A routine is a run of Level 2 moments, next to each other on the
   spiral, lived more than once in the same order. The longest is cut first. One thing
   over and over is cut as that one thing. The entry is the five shapes of each step,
   in order: not text, not the moments. The repeats let their weight go; their records
   are not touched. Later repeats join the entry that exists. Level 3 is never folded,
   and a Level 3 turn or a night ends a stretch.
4. Before an entry is written, every repeat is read back and held against it step by
   step. A missing or extra step stops the fold.
5. Asks again before each write, and stops if the being woke.
6. Writes the night onto the spiral, reads the file back, and checks every earlier byte.
7. Reaches the five open slots. Each does nothing and says so in the report.

On the drive, beside each other:
    spiral.jsonl                  the spiral: permanent record, lines only added
    spiral.jsonl.constant.json    the constant: living state, marks only, no moment
    spiral.jsonl.state.json       where hand-over stood: living state

## Build choices (mine to make: Everett's ruling, 17 Nov 14:34)

1. Each sense arrives with its shape. Measuring shape is an organ's job and no organ is
   built. On the bench the shape is the words typed.
2. What the being needs a moment for arrives with the moment (needed_for). No part of
   the 3C that reads that is built. On the bench a person says it.
3. The conch is handed one thing to ask whether the being is asleep. Handed nothing, it
   is awake and the night refuses.
4. The first rule for leaving silico-stasis, above. "once" and "again" only.
5. The first time is marked when its shape is lived again.
6. The fold rule, above. So an entry exists after a routine is lived three times: the
   first time is held as Level 3, the second and third are folded.
7. take_in gives back the LipDrop when a moment falls off the lip.
8. The constant learns from what falls off the lip too, and keeps only the one-way mark.
9. If the constant's file is gone while the spiral holds turns, the conch stops. A
   person looks. It is not rebuilt quietly.
10. Bench-sized choices: the whole spiral is held in memory, the constant's file is
    rewritten every moment, and the fold compares every repeating moment with every
    other. Fine on the bench. Not for a lifetime.

## Open slots (each says so when reached and does nothing)

None, as of 12:21 on 17 Nov. Every slot the conch had is built. The Open marker stays
(conch_open.py) for any part found later to be undefined.

Closed 17 Nov: how a Level 2 moment that never repeats folds (11:47); the last time
(12:11); easing (12:17); stacking by use and anticipation of wake (12:21). Decided by
me on Everett's word (12:00), from his writing and carbon; see "Deciding the four open
slots" above.

Build choices added 17 Nov:
11. The moment says which senses carried what it is needed for (carried_by), said by the
    polymetis for a conversation, by hand on the bench. Refused on procedural moments.
12. A one-time moment folds the same night it arrives. If it comes again later, its
    first time is still marked Level 3 and carries its weight again; the one-time entry
    stays in the manual as it was cut, and is never joined to a routine.
13. The last time: a following the conch knew (lived again) that misses again, with no
    time it came in between, has stopped; its last time is marked Level 3 as a
    boundary, even on a turn folded into a routine.
14. Easing: only the being chooses to go back (go_back), alone, awake. A return holds
    when every turn of the event is lived again on every sense, nothing leaves
    silico-stasis, and the being walks out. Only in sleep does the charge move, to
    "taken back by the being". A taken-back shape followed straight away by a departure
    gives the charge back to the memory the next night.
15. Stacking: each night stacks the whole manual: tomorrow's plan, then uses since the
    last stack (newest on top), then tonight's cuts, then the rest as they sat.
16. Anticipation of wake is the being's: it hands the conch tomorrow's plan before
    shutdown, as often as it goes over it; the last one counts. A plan is never lived
    and never judged. Planned steps with no entry are named, never guessed.
17. The outside surface grew from five methods to nine: go_back, walked_out, used, plan.

## Known limits of the first rule

- It cannot tell a small break from a big one. Any shape never lived, arriving where
  the conch knew what came next, is Level 3. Found tonight: the first mention of the
  weather after the day's last routine step is Level 3, because the conch knows wake
  follows drive, and a night does not clear that.
- A shape never lived, arriving where no pattern has been lived, is not a departure,
  however large. A new being cannot judge.
- Things the conch has lived, arriving in a new order, are not a departure. A skipped
  step is not seen.
- Outside its constant, it comes back on any shape it has lived, even once, even one
  first lived inside the same event. So inside one event, a second moment with exactly
  the same shape is treated as ordinary: it falls off the lip unless the being needs it.
  How long the conch should stay outside is the rate Everett's protocol leaves open.
- Shapes match exactly, on all five senses, or not at all. Nothing is "close".
- A Level 2 moment between the steps of a routine splits that day's routine, and the
  night can cut it as separate pieces instead of one entry. Pieces stay pieces.
- Lip drops not yet handed over when the conch stops are gone. They are never stored.

## Working rules for this folder (Everett, 2026-11-17)

- Everything is written here, on ELEMENTS. Nothing is staged anywhere else first.
- Every change goes to the drive the moment it is made, and every step ends with a save.
- If something takes longer than five minutes to work out, where it stands is written
  into this file first.

## If the session restarts (for Fable)

1. Read this file before anything else. Do not rebuild from memory.
2. `cd /Volumes/ELEMENTS/3C && git log --oneline | head` shows the last save.
3. Run the tests on both Pythons before changing anything.
4. Edit here, test here, save here. The cloud copy of 02:33 is stale and is not used.
