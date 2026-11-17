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
- Four open slots remain. Everett has not yet ruled on the build choices and limits below.
- 12:00 Everett handed the four open slots to me: "take the comparison of the carbon
  structure with the silicon structure ... and make those decisions." 12:01: "Yes,
  they're yours." Decided below; being built in that order.

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

The decisions (build choices; Everett can overrule any of them):

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
    /usr/bin/python3 -m unittest test_conch          # 63 tests, the Mac's own Python 3.9
    /usr/local/bin/python3 -m unittest test_conch    # the same on Python 3.13
    /usr/bin/python3 -m unittest test_conch -v       # with every test's name
    /usr/bin/python3 conch_bench.py                  # the bench scene: five days and nights
    /usr/bin/python3 conch_bench.py --by-hand        # feed it yourself, one sense at a time
    git log --format='%ad  %h  %s' --date=format:'%b %d %H:%M:%S'    # every save, with its time
    ./save.sh "what changed"                         # make a save yourself

Test runs leave their spirals in test_spirals/ and bench runs in bench/. Nothing in the
code deletes them, so they pile up. Clearing them out is Everett's to say.

## What each file is

    conch.py          the conch: take_in, hand_over, spiral, sleep, state. Nothing else.
    conch_records.py  the record shapes: Moment, Turn, Level3Mark, LipDrop, Fold, ConchState
    conch_spiral.py   the spiral memory path: one being, one file, lines only ever added
    conch_intake.py   the intake filter at the lip: Level 3, Level 2, or off the lip
    conch_lip.py      the lip: Level 1 falls off, is never written, goes to the polymetis
    conch_level3.py   the conch's own constant of silico-stasis, and the Level 3 mark
    conch_fold.py     Level 2's fold: the Operational Manual entry, cut at night
    conch_sleep.py    Level 4: the night. Refuses while the being is awake
    conch_open.py     the marker every open slot returns
    test_conch.py     63 tests: the spec's fourteen and what this build adds
    conch_bench.py    the bench: moments typed by hand, plain words back

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

## Build choices Everett can overrule

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

1. Anticipation of wake. Waiting on Everett: who runs the dreamscape cycling.
2. Stacking by what was used today. No part built yet tells the conch what was used.
3. Easing what a Level 3 moment is tied to. Waiting on Everett: what regulation is
   measured by in a 3C being.
4. The last time: the point at which something stopped being constant (his H6).

Closed 17 Nov: how a Level 2 moment that never repeats folds. It folds to the senses
that carried what it is needed for (the one-time fold, above).

Build choices added 17 Nov, Everett can overrule:
11. The moment says which senses carried what it is needed for (carried_by), said by the
    polymetis for a conversation, by hand on the bench. Refused on procedural moments.
12. A one-time moment folds the same night it arrives. If it comes again later, its
    first time is still marked Level 3 and carries its weight again; the one-time entry
    stays in the manual as it was cut, and is never joined to a routine.

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
