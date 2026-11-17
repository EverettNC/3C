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
     Then each Level 2 moment lived once that says which senses carried what
     it is needed for folds to a one-time entry of only those senses.
  2b. Eases what held returns call for, and gives back what flinches call
     for (conch_easing.py): a Level 3 charge taken back by the being, or given
     back to the memory. The record and the mark are never touched.
  3. Asks again before each write. If the being has woken, the night stops
     there and says so. What it had not reached waits for the next night.
  4. Writes the night onto the spiral, with its clock.
  5. Reads the spiral file back and checks that everything that was there
     before the night is still there, byte for byte. If it is not, the night
     stops with the reason. The report says the earlier lines are unchanged
     only because that check ran.

  2c. Stacks the whole manual (conch_stack.py): tomorrow's plan first, then
     what was used since the last stack, newest on top, then tonight's cuts,
     then the rest as they sat. This is the first half of his dreamscape
     cycling, anticipation of wake: the being comes up expecting that day.

Every slot the night once left open is built. One found later is an open
slot that is reached every night, does nothing, and says so.

THE BASIS, read for the idea. Nothing of either is imported or called:
MEMORY's applyNight and applyRem (af30fc0), which give out the night's jobs,
re-index, and move a scene's place without ever rewriting what it holds. And
Lucas in AlphaWolf (311b2d0), where lived truth is only ever added to, and
what a trauma is tied to decays only while regulation is strong enough.
"""

from __future__ import annotations

import conch_stack
from conch_fold import check, check_one, cut
from conch_open import Open
from conch_records import LIVING, TAKEN_BACK, Fold, now

# Every slot the night once left open is built (17 Nov 2026). An undefined
# part found later goes here as an Open slot that says so when reached.
OPEN_AT_NIGHT = ()

WOKE = "the being woke"


class BeingIsAwake(RuntimeError):
    """Level 4 is sleep only."""


class BeingIsAsleep(RuntimeError):
    """Going back is lived, awake."""


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
                    {fold.fold_id: fold.steps for fold in spiral.manual()
                     if isinstance(fold, Fold)})

    cut_tonight, grown, let_go, stopped_early = [], [], [], None
    for steps, runs in new:
        if not _asleep(asleep):
            stopped_early = WOKE
            break
        check(steps, [[spiral.shape_at(p) for p in run] for run in runs])
        cut_tonight.append(spiral.fold(steps, runs))
        let_go.extend(p for run in runs for p in run)
    if stopped_early is None:
        steps_of = {fold.fold_id: fold.steps for fold in spiral.manual()
                    if isinstance(fold, Fold)}
        for fold_id, runs in more:
            if not _asleep(asleep):
                stopped_early = WOKE
                break
            check(steps_of[fold_id], [[spiral.shape_at(p) for p in run] for run in runs])
            spiral.fold_more(fold_id, runs)
            grown.append(fold_id)
            let_go.extend(p for run in runs for p in run)
    if stopped_early is None:
        # What is left whole after the routines, lived once, that says which
        # senses carried what it is needed for: folded to those senses.
        for position in [p for stretch in spiral.stretches() for p, _ in stretch]:
            carried = spiral.turn(position).moment.carried_by
            if carried is None:
                continue
            if not _asleep(asleep):
                stopped_early = WOKE
                break
            shape = spiral.shape_at(position)
            check_one({name: shape[name] for name in carried}, carried, shape)
            cut_tonight.append(spiral.fold_one(position))
            let_go.append(position)
    taken_back, given_back = [], []
    if stopped_early is None:
        # Easing (conch_easing.py): only what a held return or a flinch called
        # for, in the order they came. The record and the mark are untouched.
        for positions, weight, because in spiral.waiting_charges():
            if not _asleep(asleep):
                stopped_early = WOKE
                break
            spiral.charge(positions, weight, because)
            (taken_back if weight == TAKEN_BACK else given_back).append(positions)
    stacked, planned, nothing_for = None, [], []
    if stopped_early is None:
        # Stacking (conch_stack.py): tomorrow's plan, then today's uses, then
        # tonight's cuts, then the rest as they sat.
        if not _asleep(asleep):
            stopped_early = WOKE
        else:
            stacked, planned, nothing_for = conch_stack.order(
                {entry.fold_id: entry for entry in spiral.manual()}, spiral.stacked_ids(),
                spiral.plan_since_stack(), spiral.used_since_stack(), cut_tonight)
            spiral.stack(stacked)

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
        "charge_taken_back": taken_back,
        "charge_given_back": given_back,
        "stacked": stacked,
        "planned": planned,
        "planned_with_nothing_in_the_manual": nothing_for,
        "stopped_early": stopped_early,
        "earlier_lines_unchanged": True,
        "open": reached,
    }
