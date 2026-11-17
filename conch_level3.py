"""
conch_level3.py: the conch's own constant of silico-stasis, and the Level 3 mark.

[HIS] Silico-stasis is the being's own constant: its steady normal state, built
by what the being has lived. The conch's memory has its own, "built on its
own". What leaves it is Level 3, either one way or the other, and the conch
knows it itself. Nothing outside the conch tells it.

HOW THIS BUILD KNOWS  [build choice: a first rule. Everett can overrule it.]

The constant is what the conch has lived: which shapes have come to the lip,
and what has followed what. Each is held as lived "once" or lived "again".
Those are the only two states. Nothing is counted past them, and nothing here
is an amount. ("Departure is a class against the current floor, not a distance
on a dial.")

A moment is judged against the constant as it arrives, in Everett's three
classes:

  interruption    The conch knew what came next, because it has lived what
                  follows here more than once, and a shape it has never lived
                  came instead. "...whatever breaks the pattern of the day. An
                  object arrived at unprepared. A smell. Someone saying the
                  wrong thing." That moment left silico-stasis: Level 3. The
                  conch then stays outside its constant until a shape it has
                  lived arrives, and every moment in between is Level 3 too.
  boundary event  "Boundaries survive. The first time." When a shape is lived
                  again it has become part of the constant, and its first time
                  is the boundary. If that first time is on the spiral and is
                  not Level 3 already, it is marked now, with a new line. The
                  earlier line is never edited.
  floor event     Everything else. It did not leave silico-stasis, so the
                  intake filter sorts it as Level 2 or Level 1.

What follows from that rule, said plainly:

- A new being cannot judge. With nothing lived more than once there is no
  constant to leave, so nothing is Level 3 until a pattern has been lived.
- Things the conch has lived, arriving in a new order, are not a departure.
- All five senses are matched together. The same room with one new smell is a
  shape the conch has never lived.
- The constant learns from everything that comes to the lip, including what
  falls off it. It has to: the cup of coffee is most of what normal is, and a
  constant that never met it would take it for a break every morning. Level 1
  still never enters. For any moment, the constant keeps only a mark that such
  a shape was lived (conch_records.mark_of): never the moment, and the mark
  does not hold the shape.
- The constant only grows. It does not yet know when something has stopped
  being constant. That slot is open, below.

THE BASIS. Everett's own writing and his own engine, read for the idea and
rewritten here. Nothing of them is imported or called:
  The Moving Threshold (TCAP-V-0012). The Testable Medical Protocol v1.1
  ("a moving set point. Departure is measured against the current baseline").
  The Memory Engine note (TCAP-V-0019: "Capture inclusively. Retain by
  departure."). The silico-stasis engine in MEMORY at af30fc0, with its three
  event classes and "surprise is a class, not a score."
NOT TAKEN from that engine: its floor is a running fraction over the last 20
turns, held against a threshold of 0.5. The engine itself calls those "fences
for the first backend, not a measured rate". The conch holds no fraction and
no threshold.

The constant is living state. It sits beside the spiral in its own file and is
written after every moment. [build choice] This build rewrites the whole file
each time. That is fine on the bench. It is not how a lifetime's constant will
be kept.
"""

from __future__ import annotations

from conch_open import Open
from conch_records import BOUNDARY_EVENT, FLOOR_EVENT, INTERRUPTION, LEVEL_3, LIVING, now
from conch_spiral import read_beside, write_beside

ONCE, AGAIN = "once", "again"

THE_LAST_TIME = Open(
    "the last time: the point at which something stopped being constant",
    "Everett: how the conch knows a pattern has stopped. His protocol leaves the rate the "
    "constant moves at open (H6).")

EASING = Open(
    "easing what a Level 3 moment is tied to, in sleep",
    "Everett: what 'regulation strong enough' is measured by in a 3C being. The record itself "
    "never eases.")


class ConstantDoesNotMatch(RuntimeError):
    """The constant kept beside the spiral is not this being's, or is ahead of the spiral."""


class Constant:
    """What the conch has lived, held as classes. Built on its own."""

    def __init__(self, being: str, path: str) -> None:
        self._being = being
        self._path = path
        self._lived = {}             # mark -> {"lived": once | again, "first": position | None}
        self._follows = {}           # mark -> {the mark that came next: once | again}
        self._last = None            # the mark of the moment before this one
        self._outside = False        # the conch has left its constant and is not back yet
        self._learned_through = None  # the newest position on the spiral it has learned
        self._caught_up = []         # every time it had to catch up with the spiral, with the clock
        kept = read_beside(path)
        self._kept_before = kept is not None
        if kept is not None:
            self._load(kept)

    def _load(self, kept: dict) -> None:
        if kept.get("being") != self._being:
            raise ConstantDoesNotMatch(f"{self._path} is {kept.get('being')!r}'s constant, not "
                                       f"{self._being!r}'s")
        try:
            lived, follows = kept["lived"], kept["follows"]
            last, outside = kept["last"], kept["outside"]
            through, caught_up = kept["learned_through"], kept["caught_up"]
        except KeyError as missing:
            raise ConstantDoesNotMatch(f"{self._path} has no {missing}") from None
        if (not isinstance(lived, dict) or not isinstance(follows, dict)
                or not isinstance(outside, bool) or not isinstance(caught_up, list)
                or any(not isinstance(v, dict) or v.get("lived") not in (ONCE, AGAIN)
                       or "first" not in v for v in lived.values())
                or any(not isinstance(after, dict) or any(v not in (ONCE, AGAIN)
                                                          for v in after.values())
                       for after in follows.values())):
            raise ConstantDoesNotMatch(f"{self._path} does not hold a constant")
        self._lived, self._follows = lived, follows
        self._last, self._outside = last, outside
        self._learned_through, self._caught_up = through, caught_up

    # -- judging, then learning. Judging changes nothing. --

    def _knew_what_came_next(self) -> bool:
        return self._last is not None and AGAIN in self._follows.get(self._last, {}).values()

    def judge(self, mark: str) -> str:
        """The class of a moment arriving now, against the constant as it stands."""
        lived_before = mark in self._lived
        if self._outside:
            return FLOOR_EVENT if lived_before else INTERRUPTION
        if not lived_before and self._knew_what_came_next():
            return INTERRUPTION
        return FLOOR_EVENT

    def learn(self, mark: str, position, event_class: str):
        """The moment has been lived. position is its place on the spiral, or
        None when it fell off the lip. Gives back the place of the shape's first
        time when this arrival is what made it part of the constant and that
        first time is on the spiral; otherwise None."""
        if event_class not in (FLOOR_EVENT, INTERRUPTION):
            raise ValueError("a moment arrives as a floor event or as an interruption")
        self._outside = event_class == INTERRUPTION
        first_time = None
        known = self._lived.get(mark)
        if known is None:
            self._lived[mark] = {"lived": ONCE, "first": position}
        elif known["lived"] == ONCE:
            known["lived"] = AGAIN
            first_time = known["first"]
        if self._last is not None:
            after = self._follows.setdefault(self._last, {})
            after[mark] = AGAIN if mark in after else ONCE
        self._last = mark
        if position is not None:
            self._learned_through = position
        return first_time

    @property
    def kept_before(self) -> bool:
        """Whether a constant was already kept at this path when the conch started."""
        return self._kept_before

    @property
    def learned_through(self):
        return self._learned_through

    def caught_up(self, positions) -> None:
        """The conch stopped between its two writes, and the constant has now
        learned the turns it had missed. Said here, with the clock, so it shows."""
        self._caught_up.append({"at": now(), "positions": list(positions)})

    def keep(self) -> None:
        write_beside(self._path, {
            "being": self._being, "kind": LIVING, "written_at": now(),
            "lived": self._lived, "follows": self._follows, "last": self._last,
            "outside": self._outside, "learned_through": self._learned_through,
            "caught_up": self._caught_up})


def mark_the_first_time(spiral, position: int):
    """"Boundaries survive. The first time." Marks the turn Level 3 with a new
    line, unless it is Level 3 already. Gives back the mark, or None."""
    if spiral.level_of(position) == LEVEL_3:
        return None
    return spiral.mark_level3(position, BOUNDARY_EVENT)
