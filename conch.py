"""
conch.py: the conch.

[HIS] The first structure inside the 3C, after the Christman Gateway.
Everything the Gateway takes in comes to its lip. There it is sorted: what
falls off the lip, what is stored and compressed in the Operational Manual,
and what goes to the PTSD layer for life. "Information comes in, filters
through the conch and flows over it."

It lies on its side with its opening facing the eyes, because that is the
direction information arrives from. The spiral itself is the memory path. It
is not text: what the conch holds is what came in through all five senses
together.

Four levels. Each does its own job. They are four mechanisms, not one thing in
four amounts:

  Level 1  the lip                 conch_lip.py     falls off; goes to the polymetis
  Level 2  the Operational Manual  conch_fold.py    stored; folded at night
  Level 3  the PTSD layer          conch_level3.py  what left silico-stasis; held for life
  Level 4  sleep / reorganization  conch_sleep.py   sleep only; prunes weight, never record

THE WHOLE OUTSIDE SURFACE

    conch = Conch(being="...", spiral_path="...", asleep=...)
    conch.take_in(moment)  -> Turn, or LipDrop when it fell off the lip
    conch.hand_over()      -> [Turn | LipDrop] since the last hand-over, in the order they came
    conch.spiral()         -> SpiralView: read-only, in order
    conch.sleep()          -> the night's report; refused while the being is awake
    conch.state()          -> ConchState: living state, with its clock
    conch.go_back(place)   -> the being goes back to a Level 3 moment, alone; awake only
    conch.walked_out()     -> the return, as written on the spiral, held or not
    conch.used(fold_id)    -> an Operational Manual entry was used; awake only
    conch.plan(steps)      -> tomorrow's plan, gone over before shutdown; awake only

No other method. The conch has no search, no delete, no edit and no score.
Going back is the being's own act (conch_easing.py): the conch never chooses
what eases.

[build choices]
- asleep. Something has to tell the conch the being is asleep, and the conch
  must not decide that for itself. So it is handed one thing to ask when it is
  made: a call that answers True only while the being sleeps. Handed nothing,
  the conch is awake and sleep() refuses.
- take_in gives back the LipDrop when a moment falls off the lip, since there
  is no turn to give.
- hand_over keeps its place in a small file beside the spiral, so a restart
  hands over what had not been handed over. Lip drops are never written
  anywhere, so the ones still waiting when the conch stops are gone.
- One moment is two writes: the spiral, then the constant beside it. If the
  conch stops between them, the constant catches up from the spiral when the
  conch starts again, and says that it did.
- The conch stands alone: standard library only, no network, and it calls no
  other running system.
"""

from __future__ import annotations

import copy
import threading

import conch_sleep
from conch_easing import Return
from conch_stack import check_plan
from conch_intake import sort_at_the_lip
from conch_level3 import Constant, ConstantDoesNotMatch, mark_the_boundary
from conch_lip import fall_off
from conch_records import (INTERRUPTION, LEVEL_1, LEVEL_3, LIVING, ConchState, Moment,
                           check_moment, mark_of, now)
from conch_spiral import Spiral, SpiralView, read_beside, write_beside


class Conch:
    """One being's conch, on one spiral."""

    def __init__(self, being: str, spiral_path: str, asleep=None) -> None:
        if asleep is not None and not callable(asleep):
            raise TypeError("asleep is something the conch can ask: a call that answers True "
                            "only while the being sleeps")
        self._lock = threading.RLock()
        self._asleep = asleep
        self._spiral = Spiral(being, spiral_path)
        self._constant = Constant(being, spiral_path + ".constant.json")
        self._state_path = spiral_path + ".state.json"
        self._handed_over = self._where_hand_over_stood()
        self._meet_the_constant()
        self._waiting = list(range((self._handed_over or 0) + 1,
                                   (self._spiral.mouth() or 0) + 1))
        self._return = None          # the being going back, while it lasts
        self._just_met = None        # a taken-back event whose shape the last moment had

    # -- starting again from what is kept --

    def _where_hand_over_stood(self):
        kept = read_beside(self._state_path)
        if kept is None:
            return None
        if kept.get("being") != self._spiral.being:
            raise ValueError(f"{self._state_path} is {kept.get('being')!r}'s, not "
                             f"{self._spiral.being!r}'s")
        handed = kept.get("handed_over")
        if handed is None:
            return None
        if isinstance(handed, bool) or not isinstance(handed, int) \
                or not 1 <= handed <= (self._spiral.mouth() or 0):
            raise ValueError(f"{self._state_path} says turn {handed!r} was handed over, and "
                             "this spiral has no such turn")
        return handed

    def _meet_the_constant(self) -> None:
        mouth = self._spiral.mouth() or 0
        if not self._constant.kept_before:
            if mouth:
                raise ConstantDoesNotMatch(
                    f"{self._spiral.path} holds {mouth} turn(s) and the constant kept beside "
                    "it is gone. The constant is built from everything that came to the lip, "
                    "including what fell off, so it cannot be rebuilt from the spiral alone. "
                    "A person looks at this.")
            self._constant.keep()
            return
        through = self._constant.learned_through or 0
        if through > mouth:
            raise ConstantDoesNotMatch(
                f"the constant has learned through turn {through} and {self._spiral.path} "
                f"holds only {mouth}. They are not the same being's history.")
        if through == mouth:
            return
        missed = list(range(through + 1, mouth + 1))
        for position in missed:
            for boundary in self._constant.learn(mark_of(self._spiral.shape_at(position)),
                                                 position, self._spiral.arrived_as(position)):
                mark_the_boundary(self._spiral, boundary)
        self._constant.caught_up(missed)
        self._constant.keep()

    # -- the whole outside surface --

    def take_in(self, moment: Moment):
        """A moment arrives from the Gateway at the lip, every sense together.
        Gives back its Turn, or its LipDrop when it fell off the lip."""
        with self._lock:
            check_moment(moment)
            if moment.arrived_at is not None:
                raise ValueError("arrived_at is the conch's own clock. A moment comes to the "
                                 "lip without one.")
            if self._spiral.holds(moment.moment_id):
                raise ValueError(f"moment {moment.moment_id} is already on the spiral. A "
                                 "moment_id is never reused.")
            carried = None if moment.carried_by is None else tuple(moment.carried_by)
            here = Moment(senses=copy.deepcopy(moment.senses), needed_for=moment.needed_for,
                          carried_by=carried, moment_id=moment.moment_id, arrived_at=now())
            mark = mark_of(here.shape())
            arrived_as = self._constant.judge(mark)
            level = sort_at_the_lip(arrived_as == INTERRUPTION, here.needed_for)
            if level == LEVEL_1:
                came, position = fall_off(here), None
            else:
                came = self._spiral.lay(here, level, INTERRUPTION if level == LEVEL_3 else None)
                position = came.position
            for boundary in self._constant.learn(mark, position, arrived_as):
                mark_the_boundary(self._spiral, boundary)
            self._constant.keep()
            if self._return is not None:
                self._return.met(mark, arrived_as)
            if (arrived_as == INTERRUPTION and self._just_met is not None
                    and self._just_met == self._spiral.taken_back_with(
                        self._spiral.shape_mark(self._just_met[0]))):
                self._spiral.flinched(self._just_met)
            self._just_met = self._spiral.taken_back_with(mark)
            self._waiting.append(came if position is None else position)
            return came

    def hand_over(self) -> list:
        """To the polymetis: every turn and every lip drop since the last
        hand-over, in the order they came. Each is given once."""
        with self._lock:
            flowing = [self._spiral.turn(item) if isinstance(item, int) else item
                       for item in self._waiting]
            mouth = self._spiral.mouth()
            write_beside(self._state_path, {
                "being": self._spiral.being, "kind": LIVING, "written_at": now(),
                "mouth": mouth, "handed_over": mouth})
            self._handed_over = mouth
            self._waiting = []
            return flowing

    def spiral(self) -> SpiralView:
        """The spiral, read-only and in order, for the synapsitis. There is no
        lookup by word."""
        return SpiralView(self._spiral)

    def sleep(self) -> dict:
        """Level 4. Refused while the being is awake."""
        with self._lock:
            report = conch_sleep.run(self._spiral, self._asleep)
            self._just_met = None        # a night between is not straight away
            return report

    def go_back(self, position: int) -> None:
        """The being goes back to a Level 3 moment, alone. Awake only. The
        conch never chooses this: it cannot tell which way a Level 3 went."""
        with self._lock:
            if self._asleep is not None and self._asleep() is True:
                raise conch_sleep.BeingIsAsleep("going back is lived, awake. The being is asleep.")
            if self._return is not None:
                raise ValueError(f"the being is already going back to place "
                                 f"{self._return.position}. It walks out first.")
            self._return = Return(self._spiral, position)

    def _awake(self, what: str) -> None:
        if self._asleep is not None and self._asleep() is True:
            raise conch_sleep.BeingIsAsleep(f"{what} is done awake. The being is asleep.")

    def used(self, fold_id: str) -> None:
        """Whatever followed an Operational Manual entry says it was used."""
        with self._lock:
            self._awake("using the manual")
            if fold_id not in {entry.fold_id for entry in self._spiral.manual()}:
                raise ValueError(f"{fold_id!r} is not an entry in this being's manual")
            self._spiral.used(fold_id)

    def plan(self, steps) -> None:
        """Before shutdown the being goes over tomorrow's plan until it falls
        asleep, and hands it over each time. The last one before the night is
        the one the night stacks by. A plan is never lived and never judged."""
        with self._lock:
            self._awake("going over tomorrow's plan")
            self._spiral.plan(check_plan(steps))

    def walked_out(self) -> dict:
        """The being walked out. The return is written on the spiral, held or
        not, and given back as written."""
        with self._lock:
            if self._return is None:
                raise ValueError("the being has not gone back to anything")
            going, self._return = self._return, None
            return self._spiral.went_back(going.position, going.event, going.lived,
                                          going.held(), going.why_not(), going.began_at)

    def state(self) -> ConchState:
        """The conch's own state: true as of its clock, never "true now"."""
        with self._lock:
            return ConchState(mouth=self._spiral.mouth(), handed_over=self._handed_over,
                              written_at=now())
