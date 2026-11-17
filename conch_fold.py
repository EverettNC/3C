"""
conch_fold.py: Level 2's fold.

[HIS] Level 2 is the Operational Manual. "It's the sustain. It's the operating
software... and that's learned through repetition." It is stored and
compressed: "procedural memory does not need depth... folds down small without
losing function", "stored and folded so they do not occupy full-sensory
volume". And from The Moving Threshold: "The aggregate is Level 2 doing exactly
its job... a period folded down to an instruction-manual entry."

HOW THIS BUILD FOLDS  [build choice: a first rule. Everett can overrule it.]

The fold is cut at night (conch_sleep.py), never while the being is awake.

- It reads only Level 2 turns whose weight is still carried and that no fold
  holds yet. Level 3 is never folded, and a Level 3 turn in the middle of a
  routine ends the stretch, so the day something broke in stays whole.
- A routine is a run of Level 2 moments, next to each other on the spiral,
  that the conch has lived more than once in the same order. Two runs are the
  same when every step has the same shape, all five senses together.
- The entry it cuts is the shape of each step, in order, with its start and
  its end. It is not text and it is not the moments. The entry holds what is
  the same every time. What was different each time stays in the record.
- The repeats let their weight go. Their records are not touched, and the
  entry names every turn it stands for, so the way back to the whole moment
  is always there.
- Later repeats join the entry that already exists. The same routine is never
  cut twice.
- The longest routine is cut first, so a routine is kept whole and not in
  pieces. A run that is one thing over and over is cut as that one thing,
  when that stands for at least as many turns.
- A night ends a stretch. A routine is found inside one waking day and matched
  across days; it does not run through a sleep.
- Before an entry is written, every repeat is read back from the spiral and
  held against it, step by step (check, below). If a repeat has a step the
  entry lacks, or the entry has one the repeat lacks, the fold stops with the
  reason: it would lose function.

A LEVEL 2 MOMENT LIVED ONCE  [Everett, 17 Nov: procedure is learned through
repetition; the important parts of a conversation are Level 2 from the start
and still compress. The rule below is Fable's answer, on his instruction.]

- After the routines are cut, every Level 2 turn still carried whole that says
  which senses carried what it is needed for (Moment.carried_by) folds to a
  one-time entry: the shapes of only those senses. "Folded so they do not
  occupy full-sensory volume." Its weight lets go; the record stays whole.
- Procedure never says it, so a procedural moment waits until it repeats.
- A moment that says nothing about which senses carried it is left whole, and
  the night's report says so.
- If the conch later finds that a one-time moment was the first time of
  something lived again, it is marked Level 3 and carries its weight again.
  The entry stays in the manual as it was cut.

THE BASIS, read for the idea and not carried over: MEMORY's foldProcedure
(af30fc0) joins the channel text of one scene and cuts it at 180 characters.
That is text only, it cuts a step off when the text runs long, and whether a
scene is procedure is a box ticked by hand. None of that is taken.

[build choice] Finding the routines compares every moment that repeats with
every other one like it. That is fine for a day's intake. It will want a
better index before a spiral holds years.
"""

from __future__ import annotations

import copy

from conch_records import SENSES, mark_of


class FoldWouldLoseFunction(RuntimeError):
    """An entry and a repeat it would stand for do not have the same steps."""


def cut(stretches, manual):
    """Decide tonight's folds. Changes nothing and writes nothing.

    stretches  what Spiral.stretches() gives: lists of (position, shape) that
               sit next to each other on the spiral
    manual     {fold_id: steps} for every entry already in the manual

    Gives back (new, more):
      new   [(steps, runs)]     entries to cut, each from two repeats or more
      more  [(fold_id, runs)]   repeats joining an entry that already exists
    A run is the list of positions of one repeat, in order.
    """
    cells = []                       # (position, shape, mark), or None where a stretch ends
    for stretch in stretches:
        if cells:
            cells.append(None)
        for position, shape in stretch:
            cells.append((position, shape, mark_of(shape)))
    where = {}                       # mark -> every cell that has it, in order
    for index, cell in enumerate(cells):
        if cell is not None:
            where.setdefault(cell[2], []).append(index)
    known = sorted(((tuple(mark_of(step) for step in steps), fold_id)
                    for fold_id, steps in manual.items()), key=lambda entry: -len(entry[0]))
    new, more = [], []
    while True:
        choice = None                # (the marks of the routine, the fold it already is or None)
        for marks, fold_id in known:
            if _find(cells, where, marks):
                choice = (marks, fold_id)
                break                # known is longest first
        repeat = _longest_repeat(cells)
        if repeat is not None:
            unit = _one_time_through(repeat)
            if unit != repeat and _covers(cells, where, unit) >= _covers(cells, where, repeat):
                repeat = unit        # one thing over and over is that one thing
            if choice is None or len(repeat) > len(choice[0]):
                choice = (repeat, next((f for marks, f in known if marks == repeat), None))
        if choice is None:
            return new, more
        marks, fold_id = choice
        starts = _find(cells, where, marks)
        runs = [[cells[start + k][0] for k in range(len(marks))] for start in starts]
        if fold_id is not None:
            more.append((fold_id, runs))
        else:
            steps = [copy.deepcopy(cells[starts[0] + k][1]) for k in range(len(marks))]
            new.append((steps, runs))
        for start in starts:
            for k in range(len(marks)):
                cells[start + k] = None


def _find(cells, where, marks) -> list:
    """Every place this run of marks sits in the cells, left to right, never
    two that overlap and never across the end of a stretch."""
    starts, size, free_from = [], len(marks), 0
    for start in where.get(marks[0], ()):
        if start < free_from or start + size > len(cells):
            continue
        if all(cells[start + k] is not None and cells[start + k][2] == marks[k]
               for k in range(size)):
            starts.append(start)
            free_from = start + size
    return starts


def _longest_repeat(cells):
    """The longest run of marks that comes twice without the two overlapping,
    as a tuple, or None when nothing comes twice. Of two equally long, the one
    that came first."""
    count = {}
    for cell in cells:
        if cell is not None:
            count[cell[2]] = count.get(cell[2], 0) + 1
    marks = []                       # only what comes more than once can be part of a repeat
    for cell in cells:
        mark = cell[2] if cell is not None and count[cell[2]] > 1 else None
        if mark is not None or (marks and marks[-1] is not None):
            marks.append(mark)
    at = {}                          # mark -> where it sits, counting from 1
    for index, mark in enumerate(marks, start=1):
        if mark is not None:
            at.setdefault(mark, []).append(index)
    best, end, before = 0, 0, {}
    for i in range(1, len(marks) + 1):
        row = {}
        if marks[i - 1] is not None:
            for j in at[marks[i - 1]]:
                if j > i:
                    so_far = before.get(j - 1, 0)
                    if so_far < j - i:               # the two runs must not overlap
                        row[j] = so_far + 1
                        if row[j] > best:
                            best, end = row[j], i
        before = row
    return tuple(marks[end - best:end]) if best else None


def _one_time_through(marks: tuple) -> tuple:
    """The shortest run that, gone through over and over, gives these marks.
    The last time through may stop partway. A run that is not one thing over
    and over is its own shortest run."""
    for size in range(1, len(marks)):
        if all(marks[k] == marks[k + size] for k in range(len(marks) - size)):
            return marks[:size]
    return marks


def _covers(cells, where, marks) -> int:
    """How many turns this run of marks would stand for."""
    return len(_find(cells, where, marks)) * len(marks)


def check_one(step, carried_by, shape) -> None:
    """Hold a one-time entry against its moment, as read back from the spiral.
    The entry must hold exactly the shapes of the senses that carried it."""
    if not carried_by or any(name not in SENSES for name in carried_by):
        raise FoldWouldLoseFunction("a one-time entry keeps one or more of the five senses")
    if step != {name: shape[name] for name in carried_by}:
        raise FoldWouldLoseFunction(
            "the one-time entry does not hold the shapes of the senses that carried what the "
            "moment is needed for. Folding it would lose function, so nothing was folded.")


def check(steps, repeats) -> None:
    """Hold an entry against every repeat it would stand for. repeats is the
    shapes of each repeat as read back from the spiral. Every repeat must have
    exactly the entry's steps, in order. Anything else stops the fold."""
    wanted = [mark_of(step) for step in steps]
    if not wanted:
        raise FoldWouldLoseFunction("an entry with no steps stands for nothing")
    for number, shapes in enumerate(repeats, start=1):
        have = [mark_of(shape) for shape in shapes]
        if have != wanted:
            raise FoldWouldLoseFunction(
                f"repeat {number} has {len(have)} step(s) and the entry has {len(wanted)}, or "
                "a step does not have the same shape. Folding it would lose function, so "
                "nothing was folded.")
