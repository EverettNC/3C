# The conch's algorithm, in plain words

Written 2026-11-17 on ELEMENTS. This is the algorithm the conch runs, step by step, as it
is coded in this folder today. The code is the working version; this file says the same
thing in words, with where each step lives. If the two ever disagree, the code is what
runs, and this file is corrected.

Everett's own words are in quotation marks. Everything else here is a build choice he has
not yet ruled on.

There are two algorithms:

1. **Knowing what left silico-stasis** (Level 3), every time a moment arrives.
   `conch_level3.py`, class `Constant`, methods `judge` (line 136) and `learn` (line 145).
2. **The fold** (Level 2 into the Operational Manual), only at night.
   `conch_fold.py`, function `cut` (line 70), with `check` (line 184).
   Run by `conch_sleep.py`, function `run` (line 83).

`conch.py`, `take_in` (line 129), is where a moment meets both.

---

## Before either one: what the conch compares

A moment is all five senses at once: sight, sound, smell, taste, touch. Each sense arrives
with its **shape**, as its own organ measured it. ("The relay carries shape, not identity.")

The conch never compares what a sense gave. It only asks one question of two moments:
**are all five shapes the same?** Yes or no. Nothing is "close". The same room with one
new smell is a different shape.

To ask that fast, the conch takes a one-way fingerprint of the five shapes together
(`mark_of` in `conch_records.py`). Two moments with the same fingerprint have the same shape.
The fingerprint does not hold the shape and the shape cannot be read back out of it.

---

## Algorithm 1: knowing what left silico-stasis

### What the conch keeps (its constant)

"The memory, the basis or the constant of the homeostasis or the silica stasis is built on
its own." The constant is built only from what the conch has lived. It holds two things,
and nothing else:

- **Every shape that has come to the lip**, marked as lived **once** or lived **again**.
  Those are the only two states. Nothing is counted past "again".
- **What has followed what**: for each shape, the shapes that came right after it, each
  marked **once** or **again**.

Plus where it is right now: the last shape that arrived, and whether the conch is
currently outside its constant.

It learns from everything that comes to the lip, including what falls off as Level 1,
because the cup of coffee is most of what normal is. Level 1 still never enters: the
constant keeps the fingerprint only, never the moment.

It is written beside the spiral (`spiral.jsonl.constant.json`) after every moment.

### When a moment arrives: judge, then learn

**Judge** (`judge`, line 136). Judging changes nothing. It gives one of Everett's three
classes, from his own engine: "Departure is a class against the current floor, not a
distance on a dial."

1. **If the conch is already outside its constant** (a break started earlier and nothing
   lived has arrived since):
   - a shape it has lived before brings it back: **floor event**;
   - a shape it has never lived keeps it outside: **interruption**.
2. **Otherwise**, it asks: did the conch know what comes next? That means the shape that
   just came before has been followed by the same thing **more than once**
   (`_knew_what_came_next`, line 133).
   - If it knew what came next, and a shape **never lived** arrived instead:
     **interruption**. "...whatever breaks the pattern of the day. An object arrived at
     unprepared. A smell. Someone saying the wrong thing."
   - Anything else: **floor event**.

An interruption is Level 3, held for life. A floor event goes to the intake filter
(`conch_intake.py`), which sorts it by Everett's definition: Level 2 if the being needs it
to function (education, operational, procedural, structure, an important part of a
conversation), otherwise Level 1, off the lip.

**Learn** (`learn`, line 145). After the moment is sorted and laid (or falls off):

1. If it was an interruption, the conch is now outside its constant. If it was a floor
   event, it is inside.
2. The shape is added: new shapes are lived **once**. A shape lived once becomes lived
   **again**.
3. "What follows what" is added the same way: the last shape, then this one.
4. **The first time.** "Boundaries survive. The first time." At the moment a shape goes
   from once to again, it has become part of the constant, and its first time is the
   boundary. If that first time is on the spiral and is not already Level 3, the conch
   writes a **new line** marking it Level 3 (**boundary event**). The earlier line is never
   touched. (`mark_the_first_time`, line 190.)

### Worked through: the bench scene (`conch_bench.py`)

Every day is: wake (procedural), coffee (needed for nothing), drive (procedural).

- **Day 1.** Nothing lived yet. Wake and drive are floor events and go in as Level 2.
  Coffee falls off the lip. A new being cannot judge: with nothing lived more than once,
  there is no constant to leave.
- **Day 2.** Wake arrives again, so wake is now part of the constant, and Day 1's wake is
  marked Level 3 with a new line: the first time survives. Same for drive.
- **Day 3.** Everything is floor. "Wake then coffee" and "coffee then drive" have now been
  lived more than once, so the conch knows what comes next.
- **Day 4.** Wake, coffee, then **a phone call**. After coffee the conch knew drive comes
  next, and a shape it has never lived came instead: **interruption**, Level 3. Then **the
  hospital**: still outside, never lived: Level 3. Then **drive**: lived before, so the
  conch is back inside, and drive goes in as Level 2.
- **Day 5.** Floor again.

### What this first rule cannot do yet (also in the build notes)

- It cannot tell something merely new from something that left silico-stasis. The first
  mention of the weather where the conch knew what came next is Level 3, the same as the
  phone call.
- A new being cannot judge until something has been lived more than once.
- Lived things in a new order are not a break. A skipped step is not seen.
- Outside its constant, any shape lived before brings it back, even one first lived inside
  the same event.
- **The last time**, the point at which something stopped being constant, is open. The
  constant only grows. Everett's protocol leaves the rate it moves at open.

---

## Algorithm 2: the fold (Level 2 into the Operational Manual)

"The aggregate is Level 2 doing exactly its job... a period folded down to an
instruction-manual entry." It "folds down small without losing function."

It runs only at night (`conch_sleep.py`, `run`). It refuses unless the one thing the conch
was handed to ask says plainly that the being is asleep.

### What it looks at

Only Level 2 turns whose weight is still carried and that no entry holds yet. They are
taken in stretches that sit next to each other on the spiral. A stretch ends at:

- a Level 3 turn (so the day something broke stays whole, never folded across the break),
- a turn already folded,
- a night (a routine is found inside one waking day, and matched across days).

### What it does (`cut`, line 70)

1. **Existing entries.** For every entry already in the manual, longest first: does that
   routine appear again in tonight's stretches? If it does, those repeats will **join the
   entry**. The same routine is never cut twice.
2. **The longest new routine.** Find the longest run of moments, next to each other, that
   appears at least twice in the same order without overlapping itself
   (`_longest_repeat`, line 137). Of two equally long, the one that came first. If it is
   longer than the existing entry found in step 1, it is cut first; otherwise the existing
   entry takes its repeats first.
3. **One thing over and over is that one thing.** If the routine is really a shorter
   routine repeated (take the pill, take the pill, take the pill), it is cut as the
   shorter one when that stands for at least as many turns (`_one_time_through`, line 169).
4. **Cut it.** The entry is the **shape of each step, in order**: its start is the first
   step and its end the last. It is not text and it is not the moments.
5. Mark those turns as taken and go back to step 1. Stop when nothing repeats.

### Before anything is written (`check`, line 184)

Every repeat is read back from the spiral and held against the entry, step by step. If a
repeat has a step the entry lacks, or the entry has a step the repeat lacks, or the order
differs, the fold **stops with the reason**: it would lose function. Nothing is written.

### What gets written

- The entry (a `fold` line), or more repeats for an existing one (a `fold_more` line).
- A `weight` line: the repeats **let their weight go**. Their records are not touched. The
  entry names every turn it stands for, so the way back to each whole moment is always there.
- At the end of the night, a `sleep` line with what was done. Then the spiral file is read
  back and every byte that was there before the night is checked unchanged.

Before each write it asks again whether the being is asleep. If it woke, the night stops
there and says so; what it had not reached waits for the next night.

### Worked through: the bench scene

- Night 1, night 2: nothing has been lived twice in a stretch, so nothing folds. The first
  times (Day 1's wake and drive) are Level 3 by then and are never folded.
- **Night 3:** Day 2's wake-drive and Day 3's wake-drive are the same routine lived twice.
  One entry is cut: **wake -> drive**. Those four turns let their weight go.
- Night 4: Day 4's wake and drive are split by the phone call and the hospital (Level 3),
  so they are left whole.
- **Night 5:** Day 5's wake-drive joins the existing entry.

(Coffee is never in the routine because it fell off the lip. It was never stored.)

### What the fold cannot do yet

- **A Level 2 moment that never repeats** is left whole. One time gives the fold nothing
  to hold it against. Open.
- A night also reaches four other open slots, does nothing in each, and says so in its
  report: anticipation of wake, stacking by what was used today, easing what a Level 3
  moment is tied to, and the last time.

---

## Run it

    cd /Volumes/ELEMENTS/3C
    /usr/bin/python3 conch_bench.py              # the scene above, start to finish
    /usr/bin/python3 conch_bench.py --by-hand    # feed it moments yourself
    /usr/bin/python3 -m unittest test_conch -v   # the 55 tests, by name
