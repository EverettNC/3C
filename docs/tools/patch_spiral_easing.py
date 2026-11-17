"""patch_spiral_easing.py: conch_spiral.py learns the three lines of easing (17 Nov 2026).

    python3 docs/tools/patch_spiral_easing.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once, or nothing is written.
"""
import sys

PATH = "conch_spiral.py"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""  weight       weight let go, in sleep (the record is untouched)
  sleep        a night ran
""",
     """  weight       weight let go, in sleep (the record is untouched)
  went_back    the being went back to a Level 3 moment and walked out: held or not
  flinched     a moment with the shape of a taken-back turn was followed straight
               away by a moment that left silico-stasis
  charge       in sleep: a Level 3 charge taken back by the being, or given back to
               the memory (the record and the mark are untouched)
  sleep        a night ran
"""),

    ("""                           LEVEL_3, LIVING, PERMANENT, SENSES, SOURCE, Fold, Level3Mark, Moment,
                           OneTimeFold, Turn, check_moment, mark_of, now)""",
     """                           LEVEL_3, LIVING, PERMANENT, SENSES, SOURCE, TAKEN_BACK, Fold,
                           Level3Mark, Moment, OneTimeFold, Turn, check_moment, mark_of, now)"""),

    ("""            "fold_more": "at", "fold_one": "cut_at", "weight": "at", "sleep": "at"}""",
     """            "fold_more": "at", "fold_one": "cut_at", "weight": "at", "sleep": "at",
            "went_back": "walked_out_at", "flinched": "at", "charge": "at"}"""),

    ("""    "weight": {"type", "positions", "weight", "folded_into", "at", "kind"},
""",
     """    "weight": {"type", "positions", "weight", "folded_into", "at", "kind"},
    "went_back": {"type", "return_id", "position", "event", "lived", "held", "why", "began_at",
                  "walked_out_at", "kind"},
    "flinched": {"type", "flinch_id", "positions", "at", "kind"},
    "charge": {"type", "positions", "weight", "because", "at", "kind"},
"""),

    ("""        self._nights = []          # the sleep lines
""",
     """        self._nights = []          # the sleep lines
        self._reasons = []         # ("return" | "flinch", its line), in the order written
        self._reason_ids = set()   # every return_id and flinch_id
        self._charges = []         # the charge lines, in order
        self._taken_back = {}      # position -> its event, while its charge is taken back
"""),

    ("""    def _take_sleep(self, line) -> None:""",
     """    def _new_reason(self, reason_id) -> None:
        if not isinstance(reason_id, str) or not reason_id or reason_id in self._reason_ids:
            raise SpiralDamaged("a return or a flinch needs an id of its own")
        self._reason_ids.add(reason_id)

    def _take_went_back(self, line) -> None:
        position = self._place(line["position"])
        if position not in self._marks:
            raise SpiralDamaged(f"a return to turn {position}, which is not Level 3")
        event, lived, held, why = line["event"], line["lived"], line["held"], line["why"]
        if event != self.event_of(position):
            raise SpiralDamaged(f"a return to turn {position} that does not name its whole event")
        if (not isinstance(lived, list) or len(set(lived)) != len(lived)
                or any(isinstance(p, bool) or p not in event for p in lived)):
            raise SpiralDamaged("a return says which turns of its event were lived again, once each")
        if not isinstance(held, bool):
            raise SpiralDamaged("a return held or it did not")
        if held and (sorted(lived) != event or why is not None):
            raise SpiralDamaged("a return that held lived its whole event again, and gives no "
                                "reason")
        if not held and (not isinstance(why, str) or not why):
            raise SpiralDamaged("a return that did not hold says why, in words")
        if not isinstance(line["began_at"], str) or not line["began_at"]:
            raise SpiralDamaged("a return carries the clock it began at")
        self._new_reason(line["return_id"])
        self._reasons.append(("return", line))

    def _take_flinched(self, line) -> None:
        group = line["positions"]
        if not isinstance(group, list) or tuple(group) not in set(self._taken_back.values()):
            raise SpiralDamaged("a flinch names an event whose charge is not taken back")
        self._new_reason(line["flinch_id"])
        self._reasons.append(("flinch", line))

    def _take_charge(self, line) -> None:
        due = self.waiting_charges()
        if not due or (line["positions"], line["weight"], line["because"]) != due[0]:
            raise SpiralDamaged("a charge line that no return or flinch called for, or out of "
                                "its turn")
        group = tuple(line["positions"])
        if line["weight"] == TAKEN_BACK:
            for position in group:
                self._taken_back[position] = group
        else:
            for position in group:
                del self._taken_back[position]
        self._charges.append(line)

    def _take_sleep(self, line) -> None:"""),

    ("""    def night(self, at, cut, grown, let_go, stopped_early, open_slots) -> None:""",
     """    def went_back(self, position, event, lived, held, why, began_at) -> dict:
        \"\"\"The being walked out of a return. Written whether it held or not.\"\"\"
        line = {"type": "went_back", "return_id": uuid.uuid4().hex, "position": position,
                "event": list(event), "lived": list(lived), "held": held, "why": why,
                "began_at": began_at, "walked_out_at": now(), "kind": PERMANENT}
        self._append([line])
        return copy.deepcopy(line)

    def flinched(self, group) -> None:
        \"\"\"A moment with the shape of a taken-back turn was followed straight
        away by a moment that left silico-stasis.\"\"\"
        self._append([{"type": "flinched", "flinch_id": uuid.uuid4().hex,
                       "positions": list(group), "at": now(), "kind": PERMANENT}])

    def charge(self, positions, weight, because) -> None:
        \"\"\"In sleep: a charge taken back by the being, or given back to the
        memory. Only what a return or a flinch called for, in its turn.\"\"\"
        self._append([{"type": "charge", "positions": list(positions), "weight": weight,
                       "because": because, "at": now(), "kind": PERMANENT}])

    def waiting_charges(self) -> list:
        \"\"\"What the returns and flinches on the spiral call for that no night
        has written yet, in order: (positions, weight, because).\"\"\"
        held_back, due = set(), []
        for what, line in self._reasons:
            if what == "return":
                group = tuple(line["event"])
                if line["held"] and group not in held_back:
                    held_back.add(group)
                    due.append((list(group), TAKEN_BACK, line["return_id"]))
            else:
                group = tuple(line["positions"])
                if group in held_back:
                    held_back.discard(group)
                    due.append((list(group), CARRIED, line["flinch_id"]))
        return due[len(self._charges):]

    def taken_back_with(self, mark: str):
        \"\"\"The event, taken back, that has a turn of this shape; or None.\"\"\"
        for group in sorted(set(self._taken_back.values())):
            if any(self._shape_marks[p - 1] == mark for p in group):
                return list(group)
        return None

    def event_of(self, position: int) -> list:
        \"\"\"The event a Level 3 turn belongs to: the turn, and the Level 3 turns
        lived with it while the conch was outside its constant, next to each
        other on the spiral with no night between. A first or last time is an
        event of its own.\"\"\"
        self._seat(position)
        if position not in self._marks:
            raise ValueError(f"turn {position} is Level 2. Only a Level 3 moment is gone back to.")

        def outside(place):
            return place in self._marks and self._marks[place]["event_class"] == INTERRUPTION

        if not outside(position):
            return [position]
        start, end = position, position
        while start > 1 and outside(start - 1) and start - 1 not in self._night_after:
            start -= 1
        while end < len(self._turns) and outside(end + 1) and end not in self._night_after:
            end += 1
        return list(range(start, end + 1))

    def shape_mark(self, position: int) -> str:
        \"\"\"The one-way mark of a turn's shape.\"\"\"
        return self._shape_marks[self._seat(position) - 1]

    def night(self, at, cut, grown, let_go, stopped_early, open_slots) -> None:"""),

    ("""    def weight_of(self, position: int) -> str:
        \"\"\"Level 3 carries its weight for life, even a turn whose weight was let
        go before the conch found out it was a boundary.\"\"\"
        self._seat(position)
        if position in self._marks:
            return CARRIED""",
     """    def weight_of(self, position: int) -> str:
        \"\"\"Level 3 carries its weight for life, even a turn whose weight was let
        go before the conch found out it was a boundary, unless the being took
        the charge back (conch_easing.py). Its record and its mark stay.\"\"\"
        self._seat(position)
        if position in self._marks:
            return TAKEN_BACK if position in self._taken_back else CARRIED"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("conch_spiral.py knows the lines of easing")
