"""
conch_stack.py: Level 4 stacks the Operational Manual where it should be.

[HIS] Level 4 is "the dreamscaping that helps stack everything where it
should be." Dreamscape cycling: "Meditation and projected next-day plans
before shutdown, repeated until they fall through. One — anticipation of wake.
They come up expecting that day. Wake is not a cold start. Two — clearing what
is no longer needed." (His writing on dreamscape cycling, section 8.)
Position is the retrieval channel: his desk of index cards, where the card
used goes back on top.

HOW THIS BUILD DOES IT  [build choice: the builder's to make, on Everett's ruling of 17 Nov 2026]

- Anticipation of wake is run by the being, not the conch. Before shutdown it
  goes over tomorrow's plans until it falls asleep, and each time it hands
  them to the conch (conch.plan). The last plan handed before the night is the
  one the night uses. A plan is the shapes of its steps, in order. A plan is
  not lived, so it never enters the constant and the next day is never judged
  against it.
- Whatever follows an Operational Manual entry tells the conch it was used
  (conch.used). Each use is a line on the spiral with its clock.
- Each night stacks the whole manual, in this order:
    1. the entries tonight's plan calls for, in plan order: the being comes up
       expecting that day;
    2. the entries used since the last stack, the newest use on top;
    3. the entries cut tonight;
    4. everything else, in the order it already sat.
  A planned step that no entry calls for is said in the night's report, by
  its number in the plan. Nothing is guessed for it.
- An entry calls for a step when one of its steps has that shape on every
  sense; a one-time entry, when that step has its shape on every sense it
  kept.
- The stack is where things sit, never the record: a stack line on the
  spiral, with its clock. No entry is ever taken out of the stack. Level 3 is
  never stacked: it holds its place for life, re-enterable through any sense.

Carbon checked: Bjork and Bjork (1992), a new theory of disuse: use brings a
memory forward and disuse lets it sink, and what is stored is not lost. Born,
Hansen, Marshall et al., Nature 397 (1999): people who expect to be woken at
a set time show a rise in ACTH about an hour before it; the body comes up
expecting the day. Wilhelm et al., J Neurosci 31 (2011) found sleep favours
what the person expects to need; Ashton and Cairney, PLOS ONE (2021) did not
find it. The plan coming first rests on his words, not on that study.
"""

from __future__ import annotations

from conch_records import Fold, SENSES


def calls_for(entry, step: dict) -> bool:
    """Whether an Operational Manual entry calls for one planned step."""
    if isinstance(entry, Fold):
        return any(held == step for held in entry.steps)
    return all(entry.step[sense] == step[sense] for sense in entry.carried_by)


def check_plan(steps) -> list:
    """A plan is a list of steps, each the shape of every sense. Anything else
    is refused with the reason."""
    if not isinstance(steps, (list, tuple)) or not steps:
        raise ValueError("a plan is its steps, in order: at least one")
    for number, step in enumerate(steps, start=1):
        if not isinstance(step, dict) or set(step) != set(SENSES):
            raise ValueError(f"step {number} of the plan is not the shape of every sense: "
                             + ", ".join(SENSES))
    return [dict(step) for step in steps]


def order(manual, stacked, plan, used, cut_tonight):
    """The night's stack. manual: every entry, by fold_id. stacked: fold_ids as
    they sat before tonight. plan: tonight's plan, or None. used: fold_ids used
    since the last stack, in the order they were used. Gives back the order,
    the entries the plan called for, and the plan's step numbers no entry
    called for."""
    planned, nothing_for = [], []
    for number, step in enumerate(plan or [], start=1):
        hits = [fold_id for fold_id in stacked if calls_for(manual[fold_id], step)]
        if not hits:
            nothing_for.append(number)
        for fold_id in hits:
            if fold_id not in planned:
                planned.append(fold_id)
    newest_first = []
    for fold_id in reversed(used):
        if fold_id not in planned and fold_id not in newest_first:
            newest_first.append(fold_id)
    placed = planned + newest_first
    tonight = [fold_id for fold_id in cut_tonight if fold_id not in placed]
    placed += tonight
    return placed + [f for f in stacked if f not in placed], planned, nothing_for
