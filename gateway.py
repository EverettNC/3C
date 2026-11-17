"""
gateway.py: the Christman Gateway. The housing the senses come in through.

[HIS] "Without that gateway, nothing exists. Without that gateway, nothing
arrives." It is not one door. It is the housing unit, "the everything": "the
eyes, the nose, the mouth, the skin, the ears, all of it." The senses that come
in together are sight, sound, smell, taste and touch; "taste, which is 76%
smell". "5 is not an element": the building is where all of it comes in
together. "Attention selects a target. Memory keeps the room."

WHAT IT DOES  [build choices: the builder's to make, on Everett's ruling of
17 Nov 2026. Each is in conch_build_notes.md, G1 to G9.]

- One organ per sense. A sense with no organ connected is absent. An organ that
  is connected and has given nothing is quiet. One organ may serve two senses
  (the nose: smell, and taste with it).
- An organ gives a reading: what it gave, in its own form; its shape, as it
  measured it; its own clock (conch_records.gave). The Gateway never makes a
  shape and never compares what a sense gave. Shape is the organ's job. Silence
  over invention: nothing here fills in a sense that did not give.
- The room, not the target. The Gateway holds the current reading of every
  sense together. Nothing is filtered for attention here.
- Where a moment ends. Carbon splits continuous experience into events where
  what comes in changes and the forecast fails (Zacks, Speer, Swallow, Braver
  and Reynolds, Psychological Bulletin, 2007). The forecast belongs to the conch.
  So here: a moment ends when any sense's shape changes. The moment that held
  until then goes to the conch's lip, whole, and a new one begins. A reading of
  the same shape continues the moment, which keeps the reading that opened its
  shape. No clock tick and no count decide it.
- What the being needs a moment for is the polymetis's to say. It is not built,
  so moments go to the lip with no need named. Nothing here guesses one.
- The Gateway reaches the conch only through take_in. It runs awake or asleep:
  the room does not stop.

The feet are equilibrium, and the equilibrium is the center: it is not a sense
the conch is sent, so it is not part of a moment here.

Standard library only. No network. The organs are rewritten for the 3C from
their own code, one at a time, and connect here; none is called live.
"""

from __future__ import annotations

import copy
import threading

from conch_records import ABSENT, QUIET, SENSES, Moment, absent, now, quiet


class GatewayClosed(RuntimeError):
    """The Gateway was closed. Nothing more arrives through it."""


class Gateway:
    """The housing. Organs connect to it; whole moments go from it to the conch."""

    def __init__(self, conch) -> None:
        if not callable(getattr(conch, "take_in", None)):
            raise TypeError("the Gateway hands moments to a conch: something with take_in")
        self._conch = conch
        self._lock = threading.RLock()
        self._organ = {sense: None for sense in SENSES}        # sense -> organ name, or None
        self._now = {sense: absent() for sense in SENSES}      # the room as it stands
        self._open = False           # whether a moment is being lived right now
        self._closed = False

    # -- organs --

    def connect(self, organ: str, *senses: str) -> None:
        """An organ comes on for one or more senses. Each is quiet until it
        gives. The room has changed, so the moment before it is handed over."""
        with self._lock:
            self._still_open()
            if not isinstance(organ, str) or not organ.strip():
                raise ValueError("an organ has a name")
            if not senses:
                raise ValueError(f"{organ} serves at least one sense")
            for sense in senses:
                self._a_sense(sense)
                if self._organ[sense] is not None:
                    raise ValueError(f"{sense} is already served by {self._organ[sense]}. "
                                     "It is disconnected first.")
            changed = {sense: quiet("connected at " + now()) for sense in senses}
            came = self._room_changes(changed)
            for sense in senses:
                self._organ[sense] = organ
            return came

    def disconnect(self, organ: str, *senses: str):
        """An organ goes off. Its senses are absent again: absence is not quiet."""
        with self._lock:
            self._still_open()
            for sense in senses:
                self._served_by(organ, sense)
            came = self._room_changes({sense: absent() for sense in senses})
            for sense in senses:
                self._organ[sense] = None
            return came

    def arrive(self, organ: str, sense: str, reading: dict):
        """A reading from an organ. Gives back what the conch gave for the moment
        this reading ended (a Turn or a LipDrop), or None when the moment goes on."""
        with self._lock:
            self._still_open()
            self._served_by(organ, sense)
            self._a_reading(sense, reading)
            if reading["shape"] == self._now[sense]["shape"]:
                return None                       # the same shape: the moment goes on
            return self._room_changes({sense: copy.deepcopy(reading)})

    def close(self):
        """The Gateway closes. The moment being lived goes to the lip first."""
        with self._lock:
            self._still_open()
            came = self._hand_over() if self._open else None
            self._closed = True
            return came

    def room(self) -> dict:
        """Every sense as it stands now, as its organ gave it. Read-only."""
        with self._lock:
            return copy.deepcopy(self._now)

    def organs(self) -> dict:
        """Which organ serves each sense; None where none is connected."""
        with self._lock:
            return dict(self._organ)

    # -- inside --

    def _room_changes(self, changed: dict):
        """Some senses now stand differently. The moment lived until now goes to
        the lip, whole; only once the conch has it does the room move on. If the
        conch refuses it, nothing here has changed and the refusal goes up."""
        came = self._hand_over() if self._open else None
        self._now.update(changed)
        self._open = any(self._now[s]["shape"] != ABSENT for s in SENSES)
        return came

    def _hand_over(self):
        moment = Moment(senses=copy.deepcopy(self._now))
        return self._conch.take_in(moment)

    def _still_open(self) -> None:
        if self._closed:
            raise GatewayClosed("the Gateway was closed. Nothing more arrives through it.")

    @staticmethod
    def _a_sense(sense) -> None:
        if sense not in SENSES:
            raise ValueError(f"{sense!r} is not a sense the Gateway carries: "
                             + ", ".join(SENSES))

    def _served_by(self, organ: str, sense: str) -> None:
        self._a_sense(sense)
        if self._organ[sense] is None:
            raise ValueError(f"no organ serves {sense}. One is connected first.")
        if self._organ[sense] != organ:
            raise ValueError(f"{sense} is served by {self._organ[sense]}, not {organ}")

    @staticmethod
    def _a_reading(sense: str, reading) -> None:
        if not isinstance(reading, dict) or set(reading) != {"gave", "shape", "organ_clock"}:
            raise ValueError(f"a reading for {sense} is what the organ gave, its shape and its "
                             "clock (conch_records.gave or quiet)")
        if reading["shape"] == ABSENT or reading["gave"] == ABSENT:
            raise ValueError(f"an organ that is connected is not absent. {sense} is "
                             "disconnected instead.")
        if (reading["shape"] == QUIET) != (reading["gave"] == QUIET):
            raise ValueError(f"a quiet {sense} gave nothing and has no other shape")
        if not isinstance(reading["organ_clock"], str) or not reading["organ_clock"]:
            raise ValueError(f"a reading for {sense} carries its organ's clock")
        if reading["shape"] is None:
            raise ValueError(f"the organ for {sense} gave no shape. Shape is the organ's job; "
                             "the Gateway never makes one.")
