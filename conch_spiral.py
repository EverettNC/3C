"""
conch_spiral.py: the spiral memory path.

The spiral itself is the memory path. What enters is laid on it whole, in the
order it came, and nothing on it is ever edited or erased. A change of state is
a new line: a Level 3 mark found later, an entry cut for the Operational
Manual, weight let go in sleep. The lines written before stay exactly as they
were.

One being per spiral. The first line says whose it is, and a conch opened for
another being is refused.

The lines, one JSON object each:

  spiral       the first line: whose spiral this is
  turn         a moment laid on the spiral, whole
  level3_mark  a moment left the conch's own silico-stasis (no direction)
  fold         an Operational Manual entry, cut in sleep
  fold_more    more repeats joining an entry that already exists
  weight       weight let go, in sleep (the record is untouched)
  sleep        a night ran

Every line carries its clock and its kind. A line that cannot be read, or that
says something the spiral cannot be holding, stops the conch with the line
number. Nothing is repaired quietly: a repair would be an edit.

There is no search here: no lookup by word, no index by meaning, no ranking.
The view the rest of the 3C gets is the turns in the order they came.

[build choice] This build holds the whole spiral in memory while it runs. That
is fine on the bench. It is not how a lifetime's spiral will be held.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import uuid

from conch_records import (BOUNDARY_EVENT, CARRIED, FLOOR_EVENT, INTERRUPTION, LET_GO, LEVEL_2,
                           LEVEL_3, LIVING, PERMANENT, SENSES, SOURCE, Fold, Level3Mark, Moment,
                           Turn, check_moment, mark_of, now)

# The name each kind of line gives its clock.
CLOCK_OF = {"spiral": "at", "turn": "written_at", "level3_mark": "at", "fold": "cut_at",
            "fold_more": "at", "weight": "at", "sleep": "at"}

# Exactly the fields each kind of line has. A line with one more or one fewer
# is not a line this spiral wrote. There is no field for direction anywhere.
FIELDS = {
    "spiral": {"type", "being", "at", "kind"},
    "turn": {"type", "position", "moment", "level", "weight", "written_at", "kind"},
    "level3_mark": {"type", "at", "moment_id", "position", "event_class", "source", "kind"},
    "fold": {"type", "fold_id", "steps", "folded_from", "cut_at", "kind"},
    "fold_more": {"type", "fold_id", "folded_from", "at", "kind"},
    "weight": {"type", "positions", "weight", "folded_into", "at", "kind"},
    "sleep": {"type", "at", "went_back_over", "manual_entries_cut", "manual_entries_grown",
              "weight_let_go", "stopped_early", "open", "kind"},
}
MOMENT_FIELDS = {"moment_id", "arrived_at", "senses", "needed_for"}


class SpiralDamaged(RuntimeError):
    """The spiral file says something a spiral cannot hold. A person looks."""


class NotThisBeingsSpiral(RuntimeError):
    """One being, one spiral."""


class SpiralChangedUnderneath(RuntimeError):
    """Something else wrote to this spiral while this conch held it."""


# ---- living state that sits beside the spiral --------------------------------

def write_beside(path: str, state: dict) -> None:
    """Living state is written whole, then swapped into place, so a stop in the
    middle leaves the last good one."""
    if state.get("kind") != LIVING or not state.get("written_at"):
        raise ValueError("living state carries its clock and says it is living state")
    writing = path + ".writing"
    with open(writing, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1, allow_nan=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(writing, path)


def read_beside(path: str):
    """The living state kept at path, or None when none has been kept yet. One
    that cannot be read stops the conch with the reason."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        state = json.load(f)
    if not isinstance(state, dict) or state.get("kind") != LIVING or not state.get("written_at"):
        raise ValueError(f"{path} does not hold living state with its clock")
    return state


# ---- the spiral ---------------------------------------------------------------

class Spiral:
    """One being's spiral. Only the conch writes to it, and only by adding."""

    def __init__(self, being: str, path: str) -> None:
        if not isinstance(being, str) or not being.strip():
            raise ValueError("a spiral belongs to one being, by name")
        if not isinstance(path, str) or not path:
            raise ValueError("a spiral has one place it is kept")
        self._being = being
        self._path = path
        self._forget()
        if os.path.exists(path):
            self._load()
        else:
            self._begin()

    # -- reading it back from where it is kept --

    def _forget(self) -> None:
        self._turns = []           # the turn lines, in order; turn 1 is first
        self._shape_marks = []     # the mark of each turn's shape
        self._ids = set()          # every moment_id on the spiral
        self._marks = {}           # position -> its Level 3 mark line
        self._folds = {}           # fold_id -> the entry, in the order they were cut
        self._claimed = {}         # position -> the fold that holds it
        self._let_go = set()       # positions whose weight was let go
        self._nights = []          # the sleep lines
        self._night_after = set()  # how many turns were on the spiral when each night ran
        self._size = 0             # how many bytes of the file this conch knows

    def _begin(self) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(self._path)), exist_ok=True)
        first = self._bytes([{"type": "spiral", "being": self._being, "at": now(),
                              "kind": PERMANENT}])
        with open(self._path, "xb") as f:
            f.write(first)
            f.flush()
            os.fsync(f.fileno())
        self._size = len(first)

    def _load(self) -> None:
        with open(self._path, "rb") as f:
            raw = f.read()
        if not raw:
            raise SpiralDamaged(f"{self._path} is there but empty: no first line says whose "
                                "it is")
        if not raw.endswith(b"\n"):
            raise SpiralDamaged(f"{self._path}: the last line is torn. Nothing was repaired.")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as why:
            raise SpiralDamaged(f"{self._path} cannot be read: {why}") from None
        for number, written in enumerate(text.split("\n")[:-1], start=1):
            try:
                line = json.loads(written)
            except json.JSONDecodeError as why:
                raise SpiralDamaged(f"{self._path} line {number} cannot be read: {why}") from None
            try:
                if number == 1:
                    self._whose(line)
                else:
                    self._take(line)
            except SpiralDamaged as why:
                raise SpiralDamaged(f"{self._path} line {number}: {why}") from None
        if self._turns and self._turns[-1]["level"] == LEVEL_3 and len(self._turns) not in self._marks:
            raise SpiralDamaged(f"{self._path}: the last turn was laid as Level 3 and its mark "
                                "is missing")
        self._size = len(raw)

    def _whose(self, line) -> None:
        if (not isinstance(line, dict) or line.get("type") != "spiral"
                or set(line) != FIELDS["spiral"] or line["kind"] != PERMANENT
                or not isinstance(line["at"], str) or not line["at"]):
            raise SpiralDamaged("the first line does not say whose spiral this is")
        if line["being"] != self._being:
            raise NotThisBeingsSpiral(f"{self._path} is {line['being']!r}'s spiral. It is not "
                                      f"{self._being!r}'s, and no being reads or writes another's.")

    # -- taking a line: every line passes here, read from the file or about to be written --

    def _take(self, line) -> None:
        if not isinstance(line, dict):
            raise SpiralDamaged("a line that is not a record")
        what = line.get("type")
        if what not in FIELDS or what == "spiral":
            raise SpiralDamaged(f"a line of a kind the spiral does not hold: {what!r}")
        if set(line) != FIELDS[what]:
            raise SpiralDamaged(f"a {what} line with the wrong fields: "
                                f"{sorted(set(line) ^ FIELDS[what])}")
        if line["kind"] != PERMANENT:
            raise SpiralDamaged(f"a {what} line that does not say it is a permanent record")
        clock = line[CLOCK_OF[what]]
        if not isinstance(clock, str) or not clock:
            raise SpiralDamaged(f"a {what} line with no clock")
        getattr(self, "_take_" + what)(line)

    def _place(self, position) -> int:
        if isinstance(position, bool) or not isinstance(position, int) \
                or not 1 <= position <= len(self._turns):
            raise SpiralDamaged(f"{position!r} is not a place on this spiral")
        return position

    def _take_turn(self, line) -> None:
        position = line["position"]
        if isinstance(position, bool) or position != len(self._turns) + 1:
            raise SpiralDamaged(f"turn {position!r} is out of order: the next place is "
                                f"{len(self._turns) + 1}")
        if self._turns and self._turns[-1]["level"] == LEVEL_3 and len(self._turns) not in self._marks:
            raise SpiralDamaged(f"turn {len(self._turns)} was laid as Level 3 and its mark is "
                                "missing")
        if line["level"] not in (LEVEL_2, LEVEL_3):
            raise SpiralDamaged(f"turn {position} is laid as {line['level']!r}: only Level 2 and "
                                "Level 3 enter. Level 1 falls off the lip.")
        if line["weight"] != CARRIED:
            raise SpiralDamaged(f"turn {position}: a turn is laid with its weight carried")
        held = line["moment"]
        if not isinstance(held, dict) or set(held) != MOMENT_FIELDS:
            raise SpiralDamaged(f"turn {position} does not hold a moment")
        moment = Moment.from_line(held)
        try:
            check_moment(moment)
        except (TypeError, ValueError) as why:
            raise SpiralDamaged(f"turn {position} does not hold a whole moment: {why}") from None
        if not isinstance(moment.arrived_at, str) or not moment.arrived_at:
            raise SpiralDamaged(f"turn {position}: the moment has no arrival clock")
        if moment.moment_id in self._ids:
            raise SpiralDamaged(f"moment {moment.moment_id} is on the spiral twice")
        self._turns.append(line)
        self._shape_marks.append(mark_of(moment.shape()))
        self._ids.add(moment.moment_id)

    def _take_level3_mark(self, line) -> None:
        position = self._place(line["position"])
        turn = self._turns[position - 1]
        if position in self._marks:
            raise SpiralDamaged(f"turn {position} is marked Level 3 twice")
        if line["moment_id"] != turn["moment"]["moment_id"]:
            raise SpiralDamaged(f"the Level 3 mark for turn {position} names another moment")
        if line["source"] != SOURCE:
            raise SpiralDamaged("a Level 3 mark that did not come from the conch's own "
                                "silico-stasis")
        if position in self._claimed:
            raise SpiralDamaged(f"turn {position} is folded, and Level 3 is never folded")
        if line["event_class"] == INTERRUPTION:
            if turn["level"] != LEVEL_3 or position != len(self._turns):
                raise SpiralDamaged("an interruption is marked as it arrives, with its turn")
        elif line["event_class"] == BOUNDARY_EVENT:
            if turn["level"] != LEVEL_2:
                raise SpiralDamaged("a first time is marked later, on a turn laid as Level 2")
        else:
            raise SpiralDamaged(f"a Level 3 mark of a class the conch does not have: "
                                f"{line['event_class']!r}")
        self._marks[position] = line

    def _take_fold(self, line) -> None:
        fold_id, steps, runs = line["fold_id"], line["steps"], line["folded_from"]
        if not isinstance(fold_id, str) or not fold_id or fold_id in self._folds:
            raise SpiralDamaged("a fold needs an id of its own")
        if (not isinstance(steps, list) or not steps
                or any(not isinstance(s, dict) or set(s) != set(SENSES) for s in steps)):
            raise SpiralDamaged("a fold holds the five shapes of each step, in order")
        if not isinstance(runs, list) or len(runs) < 2:
            raise SpiralDamaged("a fold is cut from something lived more than once")
        self._folds[fold_id] = {"steps": steps, "marks": [mark_of(s) for s in steps],
                                "folded_from": [], "cut_at": line["cut_at"]}
        self._join(fold_id, runs)

    def _take_fold_more(self, line) -> None:
        fold_id, runs = line["fold_id"], line["folded_from"]
        if fold_id not in self._folds:
            raise SpiralDamaged(f"more repeats for a fold that was never cut: {fold_id!r}")
        if not isinstance(runs, list) or not runs:
            raise SpiralDamaged("a fold_more line with no repeats in it")
        self._join(fold_id, runs)

    def _join(self, fold_id, runs) -> None:
        fold = self._folds[fold_id]
        for run in runs:
            if not isinstance(run, list) or len(run) != len(fold["marks"]):
                raise SpiralDamaged("a repeat has every step of its fold, no more and no fewer")
            for k, position in enumerate(run):
                self._place(position)
                if k and position != run[k - 1] + 1:
                    raise SpiralDamaged("the steps of a repeat sit next to each other on the "
                                        "spiral")
                if position in self._marks:
                    raise SpiralDamaged(f"turn {position} is Level 3, and Level 3 is never folded")
                if position in self._claimed:
                    raise SpiralDamaged(f"turn {position} is already folded")
                if self._shape_marks[position - 1] != fold["marks"][k]:
                    raise SpiralDamaged(f"turn {position} does not have the shape of step "
                                        f"{k + 1} of its fold: the fold would lose function")
            for position in run:
                self._claimed[position] = fold_id
            fold["folded_from"].append(list(run))

    def _take_weight(self, line) -> None:
        if line["weight"] != LET_GO:
            raise SpiralDamaged("a weight line lets weight go; it does nothing else")
        fold_id, positions = line["folded_into"], line["positions"]
        if fold_id not in self._folds:
            raise SpiralDamaged("weight let go into a fold that was never cut")
        if not isinstance(positions, list) or not positions:
            raise SpiralDamaged("a weight line that names no turn")
        for position in positions:
            self._place(position)
            if self._claimed.get(position) != fold_id:
                raise SpiralDamaged(f"turn {position}'s weight can only be let go into the fold "
                                    "that holds it")
            if position in self._let_go:
                raise SpiralDamaged(f"turn {position}'s weight was already let go")
            self._let_go.add(position)

    def _take_sleep(self, line) -> None:
        went = line["went_back_over"]
        if isinstance(went, bool) or not isinstance(went, int) or went != len(self._turns):
            raise SpiralDamaged("a night that did not go back over the spiral as it stood")
        for name in ("manual_entries_cut", "manual_entries_grown"):
            if not isinstance(line[name], list) or any(f not in self._folds for f in line[name]):
                raise SpiralDamaged(f"a night that names a fold which was never cut ({name})")
        if not isinstance(line["weight_let_go"], list) \
                or any(p not in self._let_go for p in line["weight_let_go"]):
            raise SpiralDamaged("a night that names weight which was never let go")
        if line["stopped_early"] is not None and not isinstance(line["stopped_early"], str):
            raise SpiralDamaged("a night that stopped early says why, in words")
        if not isinstance(line["open"], list) or any(not isinstance(s, str) for s in line["open"]):
            raise SpiralDamaged("a night names its open slots, in words")
        self._nights.append(line)
        self._night_after.add(went)

    # -- adding to it: the only way anything is written --

    @staticmethod
    def _bytes(lines) -> bytes:
        return "".join(json.dumps(line, ensure_ascii=False, separators=(",", ":"),
                                  allow_nan=False) + "\n" for line in lines).encode("utf-8")

    def _append(self, lines) -> None:
        if os.path.getsize(self._path) != self._size:
            raise SpiralChangedUnderneath(
                f"{self._path} is not the length this conch left it. Something else wrote to "
                "it. One being, one spiral, one conch at a time.")
        written = self._bytes(lines)
        try:
            for line in lines:
                self._take(line)         # anything the spiral cannot hold is refused before it is written
            with open(self._path, "ab") as f:
                f.write(written)
                f.flush()
                os.fsync(f.fileno())
        except BaseException:
            self._forget()               # what this conch remembers goes back to what the file says
            self._load()
            raise
        self._size += len(written)

    def lay(self, moment: Moment, level: str, event_class=None) -> Turn:
        """Lay a moment on the spiral, whole, at the next place. A moment that
        left silico-stasis as it arrived is laid with its mark in one write."""
        if (level, event_class) not in ((LEVEL_2, None), (LEVEL_3, INTERRUPTION)):
            raise ValueError("a moment is laid as Level 2, or as Level 3 because it left "
                             "silico-stasis as it arrived")
        position, at = len(self._turns) + 1, now()
        lines = [{"type": "turn", "position": position, "moment": moment.to_line(),
                  "level": level, "weight": CARRIED, "written_at": at, "kind": PERMANENT}]
        if level == LEVEL_3:
            lines.append(self._mark_line(position, moment.moment_id, INTERRUPTION, at))
        self._append(lines)
        return self.turn(position)

    def mark_level3(self, position: int, event_class: str) -> Level3Mark:
        """A turn found later to have left silico-stasis. A new line; the turn's
        own line is not touched."""
        self._seat(position)
        at = now()
        moment_id = self._turns[position - 1]["moment"]["moment_id"]
        self._append([self._mark_line(position, moment_id, event_class, at)])
        return self._mark(self._marks[position])

    @staticmethod
    def _mark_line(position, moment_id, event_class, at) -> dict:
        return {"type": "level3_mark", "at": at, "moment_id": moment_id, "position": position,
                "event_class": event_class, "source": SOURCE, "kind": PERMANENT}

    def fold(self, steps, runs) -> str:
        """Cut one Operational Manual entry and let the weight of its repeats go."""
        fold_id, at = uuid.uuid4().hex, now()
        self._append([
            {"type": "fold", "fold_id": fold_id, "steps": copy.deepcopy(steps),
             "folded_from": [list(run) for run in runs], "cut_at": at, "kind": PERMANENT},
            {"type": "weight", "positions": [p for run in runs for p in run], "weight": LET_GO,
             "folded_into": fold_id, "at": at, "kind": PERMANENT}])
        return fold_id

    def fold_more(self, fold_id: str, runs) -> None:
        """More repeats join an entry that is already in the manual."""
        at = now()
        self._append([
            {"type": "fold_more", "fold_id": fold_id, "folded_from": [list(run) for run in runs],
             "at": at, "kind": PERMANENT},
            {"type": "weight", "positions": [p for run in runs for p in run], "weight": LET_GO,
             "folded_into": fold_id, "at": at, "kind": PERMANENT}])

    def night(self, at, cut, grown, let_go, stopped_early, open_slots) -> None:
        """A night ran. What it did is on the spiral with its clock."""
        self._append([{"type": "sleep", "at": at, "went_back_over": len(self._turns),
                       "manual_entries_cut": list(cut), "manual_entries_grown": list(grown),
                       "weight_let_go": list(let_go), "stopped_early": stopped_early,
                       "open": list(open_slots), "kind": PERMANENT}])

    # -- reading it: in order, and never by word --

    @property
    def being(self) -> str:
        return self._being

    @property
    def path(self) -> str:
        return self._path

    def mouth(self):
        """The newest position on the spiral, or None when nothing has entered."""
        return len(self._turns) or None

    def holds(self, moment_id: str) -> bool:
        return moment_id in self._ids

    def _seat(self, position) -> int:
        if isinstance(position, bool) or not isinstance(position, int):
            raise TypeError("a turn is found by its position on the spiral, a whole number")
        if not 1 <= position <= len(self._turns):
            raise IndexError(f"there is no turn {position} on this spiral")
        return position

    def level_of(self, position: int) -> str:
        return LEVEL_3 if self._seat(position) in self._marks else LEVEL_2

    def weight_of(self, position: int) -> str:
        return LET_GO if self._seat(position) in self._let_go else CARRIED

    def arrived_as(self, position: int) -> str:
        """The class the conch gave this turn as it arrived."""
        mark = self._marks.get(self._seat(position))
        return INTERRUPTION if mark and mark["event_class"] == INTERRUPTION else FLOOR_EVENT

    def shape_at(self, position: int) -> dict:
        senses = self._turns[self._seat(position) - 1]["moment"]["senses"]
        return {name: copy.deepcopy(senses[name]["shape"]) for name in SENSES}

    def turn(self, position: int) -> Turn:
        line = self._turns[self._seat(position) - 1]
        return Turn(position=position, moment=Moment.from_line(line["moment"]),
                    level=self.level_of(position), weight=self.weight_of(position),
                    written_at=line["written_at"])

    def turns(self):
        for position in range(1, len(self._turns) + 1):
            yield self.turn(position)

    @staticmethod
    def _mark(line) -> Level3Mark:
        return Level3Mark(at=line["at"], moment_id=line["moment_id"], position=line["position"],
                          event_class=line["event_class"], source=line["source"])

    def marks(self) -> list:
        """Every Level 3 mark, in the order the conch came to know."""
        return [self._mark(line) for line in self._marks.values()]

    def manual(self) -> list:
        """The Operational Manual: every fold, in the order they were cut."""
        return [Fold(fold_id=fold_id, steps=copy.deepcopy(fold["steps"]),
                     folded_from=[list(run) for run in fold["folded_from"]],
                     cut_at=fold["cut_at"]) for fold_id, fold in self._folds.items()]

    def nights(self) -> list:
        return [copy.deepcopy(line) for line in self._nights]

    def stretches(self) -> list:
        """For the fold: the Level 2 turns whose weight is still carried and that
        no fold holds, as stretches that sit next to each other on the spiral.
        A Level 3 turn, a folded turn or a night ends a stretch."""
        out, stretch = [], []
        for position in range(1, len(self._turns) + 1):
            if stretch and position - 1 in self._night_after:
                out.append(stretch)
                stretch = []
            if position in self._marks or position in self._claimed:
                if stretch:
                    out.append(stretch)
                    stretch = []
            else:
                stretch.append((position, self.shape_at(position)))
        if stretch:
            out.append(stretch)
        return out

    def fingerprint(self) -> tuple:
        """The spiral file exactly as it stands: its length and its SHA-256."""
        with open(self._path, "rb") as f:
            raw = f.read()
        return len(raw), hashlib.sha256(raw).hexdigest()

    def unchanged_since(self, fingerprint) -> bool:
        """Read the file back and say whether everything that was there then is
        still there now, byte for byte."""
        length, digest = fingerprint
        with open(self._path, "rb") as f:
            then = f.read(length)
        return len(then) == length and hashlib.sha256(then).hexdigest() == digest


class SpiralView:
    """The spiral as the rest of the 3C sees it: read-only, in the order things
    came. It has no method that takes a word or a query, because memory comes to
    the sentence through the synapsitis and is never searched for."""

    __slots__ = ("_spiral",)

    def __init__(self, spiral: Spiral) -> None:
        self._spiral = spiral

    def __len__(self) -> int:
        return self._spiral.mouth() or 0

    def __iter__(self):
        return self._spiral.turns()

    def turn(self, position: int) -> Turn:
        """The turn at one place on the spiral."""
        return self._spiral.turn(position)

    def marks(self) -> list:
        """Every Level 3 mark, in the order the conch came to know."""
        return self._spiral.marks()

    def manual(self) -> list:
        """The Operational Manual: every fold, in the order they were cut."""
        return self._spiral.manual()

    def nights(self) -> list:
        """Every night that ran, in order."""
        return self._spiral.nights()
