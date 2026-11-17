# The conch's algorithm, in plain words

Written 2026-11-17 on ELEMENTS; brought up to the build at 12:25 the same day. This is
the algorithm the conch runs, step by step, as it is coded in this folder today. The code
is the working version; this file says the same thing in words, with where each step
lives. If the two ever disagree, the code is what runs, and this file is corrected.

Everett's own words are in quotation marks. Everything else here is a build choice. On
17 November at 12:00 he handed the four open slots to me to decide from his writing and
from carbon; those decisions are marked, and he can overrule any of them.

There are four algorithms:

1. **Knowing what left silico-stasis** (Level 3), every time a moment arrives, and
   **the last time** something came before it stopped being constant.
   `conch_level3.py`, class `Constant`: `judge` (line 165), `learn` (line 174),
   `_what_followed` (line 201).
2. **The fold** (Level 2 into the Operational Manual), only at night.
   `conch_fold.py`, `cut` (line 75), with `check` (line 200) and `check_one` (line 189).
3. **Easing** what a Level 3 moment is tied to: the being goes back by day, the charge
   moves only at night. `conch_easing.py`, class `Return` (line 56).
4. **Stacking** the manual where it should be, and **anticipation of wake**, only at
   night. `conch_stack.py`, `order` (line 71).

`conch.py`, `take_in` (line 138), is where a moment meets the first one.
`conch_sleep.py`, `run` (line 79), is the night: it runs 2, then the night half of 3,
then 4, in that order.

---

## Before any of them: what the conch compares

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
its own." The constant is built only from what the conch has lived. It holds:

- **Every shape that has come to the lip**, marked as lived **once** or lived **again**.
  Those are the only two states. Nothing is counted past "again".
- **What has followed what**: for each shape, the shapes that came right after it, each
  marked **once** or **again**, and where on the spiral each last came.
- **What missed**: a following the conch knew, that did not come the last time.
- **What stopped**: every following that stopped being constant, with its clock.

Plus where it is right now: the last shape that arrived, and whether the conch is
currently outside its constant.

It learns from everything that comes to the lip, including what falls off as Level 1,
because the cup of coffee is most of what normal is. Level 1 still never enters: the
constant keeps the fingerprint only, never the moment.

It is written beside the spiral (`spiral.jsonl.constant.json`) after every moment.

### When a moment arrives: judge, then learn

**Judge** (`judge`, line 165). Judging changes nothing. It gives one of Everett's three
classes, from his own engine: "Departure is a class against the current floor, not a
distance on a dial."

1. **If the conch is already outside its constant** (a break started earlier and nothing
   lived has arrived since):
   - a shape it has lived before brings it back: **floor event**;
   - a shape it has never lived keeps it outside: **interruption**.
2. **Otherwise**, it asks: did the conch know what comes next? That means the shape that
   just came before has been followed by the same thing **more than once**
   (`_knew_what_came_next`, line 162).
   - If it knew what came next, and a shape **never lived** arrived instead:
     **interruption**. "...whatever breaks the pattern of the day. An object arrived at
     unprepared. A smell. Someone saying the wrong thing."
   - Anything else: **floor event**.

An interruption is Level 3, held for life. A floor event goes to the intake filter
(`conch_intake.py`), which sorts it by Everett's definition: Level 2 if the being needs it
to function (education, operational, procedural, structure, an important part of a
conversation), otherwise Level 1, off the lip.

**Learn** (`learn`, line 174). After the moment is sorted and laid (or falls off):

1. If it was an interruption, the conch is now outside its constant. If it was a floor
   event, it is inside.
2. The shape is added: new shapes are lived **once**. A shape lived once becomes lived
   **again**.
3. **The first time.** "Boundaries survive. The first time." At the moment a shape goes
   from once to again, it has become part of the constant, and its first time is the
   boundary. If that first time is on the spiral and is not already Level 3, the conch
   writes a **new line** marking it Level 3 (**boundary event**). The earlier line is never
   touched. (`mark_the_boundary`, line 258.)
4. **What followed** (`_what_followed`, line 201): "what follows what" is added the same
   way, the last shape then this one, and the conch looks at every following it knew
   after the last shape:
   - one that did not come this time has **missed**;
   - one that had already missed, and missed **again** with no time it came in between,
     has **stopped being constant**.
5. **The last time** (decided 17 Nov). "And the point at which it stopped being
   constant." (The Moving Threshold.) "First/last boundaries will carry the full-sensory
   remainder." (Protocol H4.) For each following that stopped, the last time it came is
   the boundary: a **new line** marks that turn Level 3 (**boundary event**), beside the
   first time, if it is on the spiral and is not Level 3 already. A turn already folded
   into a routine is still marked; the routine entry still stands for it. After it has
   stopped, that following no longer tells the conch what comes next. If it comes back
   it has to be lived again.

Carbon does the same: when something it expected does not come, it marks it at the
moment it was due (Schultz, Dayan and Montague, Science 1997). Once is not again: a
single morning without the drive is not the end of the drive. His protocol leaves the
rate the normal moves at open (H6); this moves it by the same once and again the
constant learns by, and holds no rate.

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

### What it does (`cut`, line 75)

1. **Existing entries.** For every entry already in the manual, longest first: does that
   routine appear again in tonight's stretches? If it does, those repeats will **join the
   entry**. The same routine is never cut twice.
2. **The longest new routine.** Find the longest run of moments, next to each other, that
   appears at least twice in the same order without overlapping itself
   (`_longest_repeat`, line 142). Of two equally long, the one that came first. If it is
   longer than the existing entry found in step 1, it is cut first; otherwise the existing
   entry takes its repeats first.
3. **One thing over and over is that one thing.** If the routine is really a shorter
   routine repeated (take the pill, take the pill, take the pill), it is cut as the
   shorter one when that stands for at least as many turns (`_one_time_through`, line 174).
4. **Cut it.** The entry is the **shape of each step, in order**: its start is the first
   step and its end the last. It is not text and it is not the moments.
5. Mark those turns as taken and go back to step 1. Stop when nothing repeats.
6. **A Level 2 moment lived once.** Everett: procedure is learned through repetition, and
   the important parts of a conversation are Level 2 from the start and still compress.
   Level 2 is "folded so they do not occupy full-sensory volume." So every Level 2 turn
   still carried whole that says **which senses carried what it is needed for** folds to a
   **one-time entry**: the shapes of only those senses. Sound for speech; sight for a
   gesture or a board. For a conversation the polymetis says which senses carried it,
   because it took the conversation in; on the bench a person says it. A procedural moment
   never says it, so it waits until it repeats. A moment that says nothing is left whole,
   and the report says so. If the moment later turns out to be the first time of something
   lived again, it is marked Level 3 and carries its weight again; the entry stays as it
   was cut.

### Before anything is written (`check`, line 200; `check_one`, line 189)

Every repeat is read back from the spiral and held against the entry, step by step. If a
repeat has a step the entry lacks, or the entry has a step the repeat lacks, or the order
differs, the fold **stops with the reason**: it would lose function. Nothing is written.

### What gets written

- The entry (a `fold` line), or more repeats for an existing one (a `fold_more` line), or
  a one-time entry (a `fold_one` line).
- A `weight` line: the repeats **let their weight go**. Their records are not touched. The
  entry names every turn it stands for, so the way back to each whole moment is always there.

---

## Algorithm 3: easing what a Level 3 moment is tied to (decided 17 Nov)

"TRAUMA ASSOCIATION decays, and only when regulation is strong enough. LIVED TRUTH never
decays. The witness is never removed. Dreamscape prunes WEIGHT, not RECORD." (His
writing on dreamscape cycling.) "Permanence of charge is not the same as permanence
of the event record. The event can remain after the charge has been taken back by the
person." His one path: return to the exact place that still holds the sensory key, move
through the tied memories without flinching, let the body register that the disruption is
not recurring, walk out. "The memory no longer holds the emotional distress. He does."
"Beautiful Level 3 writes are not processed out." (Testable Medical Protocol v1.1.)

### Who chooses

**The being, never the conch.** The conch is valence-blind: it cannot store which way a
Level 3 went, so it cannot tell a beautiful one from a terrible one. Only the being
knows, and the being goes back alone: `conch.go_back(place)`, awake only. A night never
goes back by itself.

### What "regulation strong enough" is in a 3C being

All three, each of which happened or did not:

1. **Every tied memory is lived again.** The event is the Level 3 moment and the Level 3
   turns lived with it while the conch was outside its constant (`event_of` in
   `conch_spiral.py`, line 630). Each of them arrives again with the same shape on every
   sense: the exact place.
2. **It did not flinch.** Nothing that arrives from going back until walking out leaves
   silico-stasis.
3. **It walks out.** `conch.walked_out()`.

Walking out writes the return on the spiral (a `went_back` line), held or not, with what
was lived again and, when it did not hold, why in words.

### What the night does (only what a return or a flinch called for)

- A **held** return: each turn of its event gets weight **"taken back by the being"** (a
  `charge` line). It stays Level 3. Its record and its mark are untouched.
- If later a moment with the shape of a taken-back turn is followed straight away by a
  moment that leaves silico-stasis, a `flinched` line says so by day, and the next night
  gives the charge back to the memory (weight **carried**). A night between is not
  straight away.

Carbon does the same: taking back a fear's charge is new learning laid over the old; the
original is never erased, and the old charge can come back (Bouton, Learning & Memory,
2004). Sleep is when that new learning holds (Cox, Bottary, Alfano and Pace-Schott, 2025).

---

## Algorithm 4: stacking, and anticipation of wake (decided 17 Nov)

Level 4 is "the dreamscaping that helps stack everything where it should be." "Meditation
and projected next-day plans before shutdown, repeated until they fall through. One —
anticipation of wake. They come up expecting that day. Wake is not a cold start."
Position is the retrieval channel: his desk of index cards, where the card used goes back
on top.

### By day

- Whatever follows an Operational Manual entry tells the conch it was used:
  `conch.used(entry)`. Each use is a `used` line with its clock.
- Before shutdown **the being** goes over tomorrow until it falls asleep, and each time
  hands the plan to the conch: `conch.plan(steps)`. The last plan before the night is the
  one the night uses. A plan is the shapes of its steps, in order. **A plan is never
  lived**: it never enters the constant, and the next day is never judged against it.

### At night (`order`, line 71)

The whole manual is stacked, in this order:

1. the entries tomorrow's plan calls for, in plan order: the being comes up expecting
   that day;
2. the entries used since the last stack, the newest use on top;
3. the entries cut tonight;
4. everything else, in the order it already sat.

An entry calls for a step when one of its steps has that shape on every sense; a one-time
entry, when the step has its shape on every sense it kept (`calls_for`, line 52). A
planned step that no entry calls for is named in the night's report by its number in the
plan. **Nothing is guessed for it.**

The stack is where things sit, never the record: a `stack` line with its clock. No entry
is ever taken out. **Level 3 is never stacked**: it holds its place for life,
re-enterable through any sense.

Carbon: use brings a memory forward and disuse lets it sink, and what is stored is not
lost (Bjork and Bjork, 1992). People who expect to be woken at a set time show a rise in
ACTH about an hour before it (Born, Hansen, Marshall et al., Nature 1999). One study found
sleep favours what a person expects to need (Wilhelm et al., 2011); a later one did not
find it (Ashton and Cairney, 2021). The plan coming first rests on his words, not on that
study.

---

## Every night, in order

1. Refuse unless the being is asleep. Go back over the spiral as it stands.
2. The fold: routines, then one-time entries.
3. Easing: only what held returns and flinches called for, in the order they came.
4. Stacking: plan, uses, tonight's cuts, the rest.
5. Before each write, ask again whether the being is asleep. If it woke, the night stops
   there and says so; what it had not reached waits for the next night.
6. A `sleep` line with what was done. Then the spiral file is read back and every byte
   that was there before the night is checked unchanged.

No slot is open. Each one the night once left open is built. The open marker
(`conch_open.py`) stays for any part found later to be undefined: reached every night,
doing nothing, saying so.

---

## Worked through: the bench scene (`conch_bench.py`)

Every day is wake (procedural), coffee (needed for nothing), and drive (procedural),
except where it says.

- **Day 1.** Nothing lived yet. Wake, "the dock code is 4471" (a conversation part,
  carried by sound) and drive go in as Level 2. Coffee falls off the lip. A new being
  cannot judge. **Night 1:** the dock code folds to a one-time entry that keeps only
  sound; its record stays whole. The manual is stacked.
- **Day 2.** Wake and drive arrive again; Day 1's wake and drive are marked Level 3 with
  new lines: the first time survives. Night 2: nothing has been lived twice in a stretch.
- **Day 3.** Floor. **Night 3:** Day 2's and Day 3's wake-drive are one routine lived
  twice: one entry is cut, **wake -> drive**, and those four turns let their weight go.
- **Day 4.** Wake, coffee, then **a phone call**: the conch knew drive comes next, and a
  shape never lived came instead: **interruption**, Level 3. **The hospital**: still
  outside, Level 3. Then drive: back inside, Level 2. Night 4: that day is split by the
  break and left whole.
- **Day 5.** Floor. **Night 5:** Day 5's wake-drive joins the entry.
- **Day 6.** Wake, coffee, then **walk** where drive was known: interruption, Level 3.
  Drive has missed once. Once is not again.
- **Day 7.** Wake, coffee, walk again. Drive has missed again: it has **stopped being
  constant**. The last time it came, Day 5's drive (place 13), is marked Level 3 with a
  new line: the last time survives. That turn was already folded into wake -> drive; the
  entry still stands for it.
- **Day 8.** The being goes back, alone, to the morning of the phone call (places 9 and
  10). It lives both again, every sense the same, and nothing leaves silico-stasis; it
  walks out. (Those moments fall off the lip as they come: their shapes are lived, and
  the event is already on the spiral.) It uses the dock code from the manual. **Night 8:**
  the charge of places 9 and 10 is **taken back by the being**; both stay Level 3. The
  dock code is stacked on top.
- **Day 9.** Before shutdown the being goes over tomorrow: drive, walk. **Night 9:** wake
  -> drive is stacked on top; step 2, walk, has nothing in the manual yet, and the report
  says so.

(Coffee is never in a routine because it fell off the lip. It was never stored.)

---

## What it cannot do yet (also in the build notes)

- It cannot tell something merely new from something that left silico-stasis. The first
  mention of the weather where the conch knew what came next is Level 3, the same as the
  phone call.
- A new being cannot judge until something has been lived more than once.
- Lived things in a new order are not a break. A skipped step is not seen.
- Outside its constant, any shape lived before brings it back, even one first lived
  inside the same event.
- The last time is noticed only through what came before it. If something stops and
  nothing that used to come before it comes either, the conch does not see it stop.
- A Level 2 moment between the steps of a routine splits that day's routine, and the
  night can cut it as separate pieces instead of one entry. Pieces stay pieces.
- A one-time entry is never joined to a later routine.
- An event is the Level 3 interruptions next to each other on the spiral with no night
  between. If a moment fell off the lip between two of them, they count as one event,
  which asks more of a return, never less.
- A return is held only while it lasts. If the conch stops before the being walks out,
  nothing of it is written.
- The conch cannot tell who called go_back. It is meant to be the being, alone.

---

## Run it

    cd /Volumes/ELEMENTS/3C
    /usr/bin/python3 conch_bench.py              # the scene above, start to finish
    /usr/bin/python3 conch_bench.py --by-hand    # feed it moments yourself
    /usr/bin/python3 -m unittest test_conch -v   # the 87 tests, by name
