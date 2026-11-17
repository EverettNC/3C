"""
conch_records.py: the record shapes of the conch.

Every record carries its clock and says whether it is living state or
permanent record. None of them carries a score, a weight value or a salience
number. (Everett: "you're putting numbers on shit that don't require numbers.")

A MOMENT is what the Christman Gateway delivers: every sense together, each
exactly as its organ gave it, with that organ's own clock. "No carbon processes
text. It's sound, speech." The five are sight, sound, smell, taste and touch.
The housing is not a sense of its own: "5 is not an element."

A sense that gave nothing says "quiet". A sense with no organ says "absent".
Absence is not quiet.

Two things come in with a moment, because the conch is not the part that makes
them [build choice]:

- Each sense carries its SHAPE, as its own organ measured it. "The relay
  carries shape, not identity." The conch only ever asks whether two shapes
  are the same. How an organ measures a shape is not built here.
- NEEDED_FOR says what the being needs the moment for, in Everett's five
  kinds, or nothing at all. The sorting rule is his and is built in
  conch_intake.py. The part of the 3C that reads which kind a moment is has
  not been built, so on the bench a person says it.

Nothing here says which way a moment left silico-stasis. Level 3 is
valence-blind, so a field for direction does not exist.
"""

from __future__ import annotations

import copy
import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

SENSES = ("sight", "sound", "smell", "taste", "touch")
QUIET = "quiet"
ABSENT = "absent"

# What the being needs in order to function (Everett, 12 and 14 November 2026):
# education, operational and procedural information, structure, and the
# important parts of a conversation.
NEEDED_FOR = ("education", "operational", "procedural", "structure", "conversation")

LEVEL_1 = "level_1"      # the lip. It never becomes a turn and is never written.
LEVEL_2 = "level_2"      # the Operational Manual
LEVEL_3 = "level_3"      # the PTSD layer
CARRIED = "carried"      # weight is a state, not a number
LET_GO = "let go"
PERMANENT = "permanent record"
LIVING = "living state"
SOURCE = "the conch's own silico-stasis"

# How the conch came to know. These are classes, never amounts, and none of
# them says which way. They are Everett's three, from his own engine.
FLOOR_EVENT = "floor_event"          # it sat inside what the conch has lived
INTERRUPTION = "interruption"        # it broke the pattern as it arrived
BOUNDARY_EVENT = "boundary_event"    # the first time of what later became constant


def now() -> str:
    """Every record carries its clock."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


# ---- what an organ hands the Gateway for one sense ---------------------------

def gave(what, shape, organ_clock: str) -> dict:
    """A sense that gave something: what it gave, its shape, its organ's clock."""
    return {"gave": what, "shape": shape, "organ_clock": organ_clock}


def quiet(organ_clock: str) -> dict:
    """A sense whose organ is there and gave nothing."""
    return {"gave": QUIET, "shape": QUIET, "organ_clock": organ_clock}


def absent() -> dict:
    """A sense with no organ. Absence is not quiet."""
    return {"gave": ABSENT, "shape": ABSENT, "organ_clock": None}


def check_senses(senses) -> None:
    """All five, together, each as its organ gave it, and able to come back
    from the spiral exactly as they went in. Anything else stops here."""
    if not isinstance(senses, dict) or set(senses) != set(SENSES):
        raise ValueError("a moment carries all five senses together, no more and no fewer: "
                         + ", ".join(SENSES))
    for name in SENSES:
        s = senses[name]
        if not isinstance(s, dict) or set(s) != {"gave", "shape", "organ_clock"}:
            raise ValueError(f"{name}: a sense is what it gave, its shape, and its organ's clock")
        if s["gave"] == ABSENT:
            if s["shape"] != ABSENT or s["organ_clock"] is not None:
                raise ValueError(f"{name}: an absent sense has no organ, so no shape and no clock")
            continue
        if not isinstance(s["organ_clock"], str) or not s["organ_clock"]:
            raise ValueError(f"{name}: every sense carries its organ's own clock")
        if s["gave"] == QUIET:
            if s["shape"] != QUIET:
                raise ValueError(f"{name}: a quiet sense has the shape of quiet")
        elif s["shape"] is None or s["shape"] == QUIET or s["shape"] == ABSENT:
            raise ValueError(f"{name} gave something, so it carries the shape its organ measured")
    try:
        back = json.loads(json.dumps(senses, allow_nan=False))
    except (TypeError, ValueError) as why:
        raise ValueError(f"the senses cannot be kept whole on the spiral: {why}") from None
    if back != senses:
        raise ValueError("the senses would not come back from the spiral exactly as the organs "
                         "gave them")


def mark_of(shape) -> str:
    """A mark that such a shape was lived. Two shapes are the same when their
    marks are the same, and that is the only question a mark answers. The mark
    is a one-way fingerprint (SHA-256): it does not hold the shape."""
    flat = json.dumps(shape, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False)
    return hashlib.sha256(flat.encode("utf-8")).hexdigest()


# ---- the records -------------------------------------------------------------

@dataclass(frozen=True)
class Moment:
    """What the Gateway delivers. The conch never changes what is inside senses."""
    senses: dict
    needed_for: str | None = None
    moment_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    arrived_at: str | None = None        # the conch's clock; the conch sets it

    def shape(self) -> dict:
        """The five shapes, sense by sense. Two moments have the same shape
        only when all five are the same."""
        return {name: copy.deepcopy(self.senses[name]["shape"]) for name in SENSES}

    def to_line(self) -> dict:
        return {"moment_id": self.moment_id, "arrived_at": self.arrived_at,
                "senses": copy.deepcopy(self.senses), "needed_for": self.needed_for}

    @staticmethod
    def from_line(line: dict) -> "Moment":
        return Moment(senses=copy.deepcopy(line["senses"]), needed_for=line["needed_for"],
                      moment_id=line["moment_id"], arrived_at=line["arrived_at"])


def check_moment(moment) -> None:
    """A moment that is not whole does not come to the lip."""
    if not isinstance(moment, Moment):
        raise TypeError("the lip takes a Moment: every sense together, not a "
                        + type(moment).__name__)
    if not isinstance(moment.moment_id, str) or not moment.moment_id:
        raise ValueError("a moment has an id of its own, never reused")
    if moment.needed_for is not None and moment.needed_for not in NEEDED_FOR:
        raise ValueError(f"needed_for is one of {', '.join(NEEDED_FOR)}, or nothing at all; "
                         f"not {moment.needed_for!r}")
    check_senses(moment.senses)


@dataclass(frozen=True)
class Turn:
    """One place on the spiral."""
    position: int            # its place in the order things arrived; the first is 1
    moment: Moment           # the whole moment, untouched
    level: str               # level_2 | level_3
    weight: str              # carried | let go
    written_at: str
    kind: str = PERMANENT


@dataclass(frozen=True)
class Level3Mark:
    """A moment left the conch's own silico-stasis. Either way; no direction."""
    at: str
    moment_id: str
    position: int
    event_class: str         # interruption | boundary_event
    source: str = SOURCE
    kind: str = PERMANENT


@dataclass(frozen=True)
class LipDrop:
    """What fell off the lip. Never on the spiral; handed to the polymetis."""
    moment: Moment
    fell_at: str
    kind: str = LIVING


@dataclass(frozen=True)
class Fold:
    """One entry in the Operational Manual: the shape of each step of something
    the conch has lived more than once, in order. It is not text, and it is not
    the moments: those stay whole on the spiral."""
    fold_id: str
    steps: list              # each step is the five shapes of one moment
    folded_from: list        # every repeat it stands for, each a list of positions
    cut_at: str
    kind: str = PERMANENT

    @property
    def start(self) -> dict:
        return self.steps[0]

    @property
    def end(self) -> dict:
        return self.steps[-1]


@dataclass(frozen=True)
class ConchState:
    """The conch's own state. Read as "true as of", never "true now"."""
    mouth: int | None        # the newest position on the spiral
    handed_over: int | None  # the last position passed to the polymetis
    written_at: str
    kind: str = LIVING
