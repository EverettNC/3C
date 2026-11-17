"""
conch_sleep.py: Level 4, sleep and reorganization.

[HIS] "The dreamscaping that helps stack everything where it should be." Sleep
only. It prunes weight, not record: "LIVED TRUTH never decays. The witness is
never removed. Dreamscape prunes WEIGHT, not RECORD. Nothing is erased anywhere
in this architecture."

It runs only while the being sleeps. The conch does not decide that. It asks,
through the one thing it was handed when it was made (asleep), and unless the
answer is a plain yes the night does not run. A conch handed nothing to ask is
awake.

WHAT A NIGHT DOES IN THIS BUILD

  1. Goes back over the spiral as it stands.
  2. Cuts the fold (conch_fold.py). Each Level 2 routine lived more than once
     becomes one Operational Manual entry, later repeats join the entry they
     belong to, and those repeats let their weight go. This is the second half
     of Everett's dreamscape cycling: "clearing what is no longer needed".
  3. Asks again before each write. If the being has woken, the night stops
     there and says so. What it had not reached waits for the next night.
  4. Writes the night onto the spiral, with its clock.
  5. Reads the spiral file back and checks that everything that was there
     before the night is still there, byte for byte. If it is not, the night
     stops with the reason. The report says the earlier lines are unchanged
     only because that check ran.

WHAT A NIGHT DOES NOT DO YET. Each of these is an open slot. It is reached
every night, it does nothing, and it says so in the report:

  - Anticipation of wake. "Meditation and projected next-day plans before
    shutdown, repeated until they fall through." Who runs that cycling is
    Everett's to say.
  - Stacking by what was used. No part built yet tells the conch what was
    used today.
  - Easing what a Level 3 moment is tied to. "TRAUMA ASSOCIATION decays, and
    only when regulation is strong enough." What regulation is measured by is
    Everett's to say. The record itself never eases.
  - The last time: the point at which something stopped being constant.
  - How a Level 2 moment that never repeats folds.

THE BASIS, read for the idea. Nothing of either is imported or called:
MEMORY's applyNight and applyRem (af30fc0), which give out the night's jobs,
re-index, and move a scene's place without ever rewriting what it holds. And
Lucas in AlphaWolf (311b2d0), where lived truth is only ever added to, and
what a trauma is tied to decays only while regulation is strong enough.
"""

from __future__ import annotations

from conch_fold import ONE_TIME, check, cut
from conch_level3 import EASING, THE_LAST_TIME
from conch_open import Open
from conch_records import LIVING, now

ANTICIPATION_OF_WAKE = Open(
    "anticipation of wake: next-day plans gone over before shutdown until they fall through",
    "Everett: who runs the dreamscape cycling before shutdown.")

STACKING_BY_USE = Open(
    "stacking by what was used today",
    "Everett: whether that is all of 'where it should be'. And no part built yet tells the "
    "conch what was used.")

OPEN_AT_NIGHT = (ANTICIPATION_OF_WAKE, STACKING_BY_USE, EASING, THE_LAST_TIME, ONE_TIME)

WOKE = "the being woke"


class BeingIsAwake(RuntimeError):
    """Level 4 is sleep only."""


class RecordTouched(RuntimeError):
    """Something that was on the spiral before the night is not the same after it."""


def _asleep(asleep) -> bool:
    return asleep is not None and asleep() is True


def run(spiral, asleep) -> dict:
    """One night. Refuses while the being is awake. Adds lines to the spiral
    and never touches one that is there. Gives back the night's report."""
    if not _asleep(asleep):
        raise BeingIsAwake(
            "Level 4 is sleep only. Nothing has told the conch the being is asleep, so the "
            "night did not run and nothing was changed.")
    ran_at = now()
    before = spiral.fingerprint()
    went_back_over = spiral.mouth() or 0
    new, more = cut(spiral.stretches(),
                    {fold.fold_id: fold.steps for fold in spiral.manual()})

    cut_tonight, grown, let_go, stopped_early = [], [], [], None
    for steps, runs in new:
        if not _asleep(asleep):
            stopped_early = WOKE
            break
        check(steps, [[spiral.shape_at(p) for p in run] for run in runs])
        cut_tonight.append(spiral.fold(steps, runs))
        let_go.extend(p for run in runs for p in run)
    if stopped_early is None:
        steps_of = {fold.fold_id: fold.steps for fold in spiral.manual()}
        for fold_id, runs in more:
            if not _asleep(asleep):
                stopped_early = WOKE
                break
            check(steps_of[fold_id], [[spiral.shape_at(p) for p in run] for run in runs])
            spiral.fold_more(fold_id, runs)
            grown.append(fold_id)
            let_go.extend(p for run in runs for p in run)

    reached = [slot.reach() for slot in OPEN_AT_NIGHT]
    spiral.night(ran_at, cut_tonight, grown, let_go, stopped_early,
                 [slot.slot for slot in OPEN_AT_NIGHT])
    if not spiral.unchanged_since(before):
        raise RecordTouched(
            f"{spiral.path}: what was on the spiral before the night is not the same after "
            "it. A night adds lines and never touches one. A person looks at this.")
    return {
        "kind": LIVING,
        "ran_at": ran_at,
        "finished_at": now(),
        "went_back_over": went_back_over,
        "manual_entries_cut": cut_tonight,
        "manual_entries_grown": grown,
        "weight_let_go": let_go,
        "left_whole": [p for stretch in spiral.stretches() for p, _ in stretch],
        "stopped_early": stopped_early,
        "earlier_lines_unchanged": True,
        "open": reached,
    }
