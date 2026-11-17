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
- Not done yet: conch spec v16, the carbon-to-3C map, the conch drawing, the Session
  Ledger entry. Everett has not yet ruled on the build choices and limits below.

How it got here: the conch was written in Fable's cloud workspace between 02:06 and
02:21 and had not been written to this drive. Everett, 02:25: "It needs to be written
on the elements volume" and saved every 5 minutes. Since 02:35 nothing is staged
anywhere else first.

## Run it yourself

    cd /Volumes/ELEMENTS/3C
    /usr/bin/python3 -m unittest test_conch          # 55 tests, the Mac's own Python 3.9
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
    test_conch.py     55 tests: the spec's fourteen and what this build adds
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
5. How a Level 2 moment that never repeats folds.

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
