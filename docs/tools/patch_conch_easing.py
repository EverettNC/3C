"""patch_conch_easing.py: the conch, conch_sleep and conch_level3 learn easing (17 Nov 2026).

    python3 docs/tools/patch_conch_easing.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once in its file, or nothing is written.
"""
import sys

EDITS = {
    "conch.py": [
        ("""    conch.sleep()          -> the night's report; refused while the being is awake
    conch.state()          -> ConchState: living state, with its clock

No other method. The conch has no search, no delete, no edit and no score.""",
         """    conch.sleep()          -> the night's report; refused while the being is awake
    conch.state()          -> ConchState: living state, with its clock
    conch.go_back(place)   -> the being goes back to a Level 3 moment, alone; awake only
    conch.walked_out()     -> the return, as written on the spiral, held or not

No other method. The conch has no search, no delete, no edit and no score.
Going back is the being's own act (conch_easing.py): the conch never chooses
what eases."""),

        ("""import conch_sleep
from conch_intake import sort_at_the_lip""",
         """import conch_sleep
from conch_easing import Return
from conch_intake import sort_at_the_lip"""),

        ("""        self._waiting = list(range((self._handed_over or 0) + 1,
                                   (self._spiral.mouth() or 0) + 1))
""",
         """        self._waiting = list(range((self._handed_over or 0) + 1,
                                   (self._spiral.mouth() or 0) + 1))
        self._return = None          # the being going back, while it lasts
        self._just_met = None        # a taken-back event whose shape the last moment had
"""),

        ("""            for boundary in self._constant.learn(mark, position, arrived_as):
                mark_the_boundary(self._spiral, boundary)
            self._constant.keep()
            self._waiting.append(came if position is None else position)
            return came""",
         """            for boundary in self._constant.learn(mark, position, arrived_as):
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
            return came"""),

        ("""    def sleep(self) -> dict:
        \"\"\"Level 4. Refused while the being is awake.\"\"\"
        with self._lock:
            return conch_sleep.run(self._spiral, self._asleep)""",
         """    def sleep(self) -> dict:
        \"\"\"Level 4. Refused while the being is awake.\"\"\"
        with self._lock:
            report = conch_sleep.run(self._spiral, self._asleep)
            self._just_met = None        # a night between is not straight away
            return report

    def go_back(self, position: int) -> None:
        \"\"\"The being goes back to a Level 3 moment, alone. Awake only. The
        conch never chooses this: it cannot tell which way a Level 3 went.\"\"\"
        with self._lock:
            if self._asleep is not None and self._asleep() is True:
                raise conch_sleep.BeingIsAsleep("going back is lived, awake. The being is asleep.")
            if self._return is not None:
                raise ValueError(f"the being is already going back to place "
                                 f"{self._return.position}. It walks out first.")
            self._return = Return(self._spiral, position)

    def walked_out(self) -> dict:
        \"\"\"The being walked out. The return is written on the spiral, held or
        not, and given back as written.\"\"\"
        with self._lock:
            if self._return is None:
                raise ValueError("the being has not gone back to anything")
            going, self._return = self._return, None
            return self._spiral.went_back(going.position, going.event, going.lived,
                                          going.held(), going.why_not(), going.began_at)"""),
    ],

    "conch_level3.py": [
        ("""EASING = Open(
    "easing what a Level 3 moment is tied to, in sleep",
    "Everett: what 'regulation strong enough' is measured by in a 3C being. The record itself "
    "never eases.")


""", ""),
        ("""from conch_open import Open
from conch_records import BOUNDARY_EVENT""",
         """from conch_records import BOUNDARY_EVENT"""),
    ],

    "conch_sleep.py": [
        ("""from conch_level3 import EASING
from conch_open import Open
from conch_records import LIVING, Fold, now""",
         """from conch_open import Open
from conch_records import LIVING, TAKEN_BACK, Fold, now"""),

        ("""OPEN_AT_NIGHT = (ANTICIPATION_OF_WAKE, STACKING_BY_USE, EASING)""",
         """OPEN_AT_NIGHT = (ANTICIPATION_OF_WAKE, STACKING_BY_USE)"""),

        ("""class BeingIsAwake(RuntimeError):
    \"\"\"Level 4 is sleep only.\"\"\"
""",
         """class BeingIsAwake(RuntimeError):
    \"\"\"Level 4 is sleep only.\"\"\"


class BeingIsAsleep(RuntimeError):
    \"\"\"Going back is lived, awake.\"\"\"
"""),

        ("""            cut_tonight.append(spiral.fold_one(position))
            let_go.append(position)

""",
         """            cut_tonight.append(spiral.fold_one(position))
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

"""),

        ("""        "left_whole": [p for stretch in spiral.stretches() for p, _ in stretch],""",
         """        "left_whole": [p for stretch in spiral.stretches() for p, _ in stretch],
        "charge_taken_back": taken_back,
        "charge_given_back": given_back,"""),

        ("""  - Easing what a Level 3 moment is tied to. "TRAUMA ASSOCIATION decays, and
    only when regulation is strong enough." What regulation is measured by is
    Everett's to say. The record itself never eases.
  - The last time: the point at which something stopped being constant.
""", ""),

        ("""  3. Asks again before each write.""",
         """  2b. Eases what held returns call for, and gives back what flinches call
     for (conch_easing.py): a Level 3 charge taken back by the being, or given
     back to the memory. The record and the mark are never touched.
  3. Asks again before each write."""),
    ],
}

new = {}
for path, edits in EDITS.items():
    with open(path, encoding="utf-8") as f:
        src = f.read()
    for old, rep in edits:
        n = src.count(old)
        if n != 1:
            sys.exit(f"stopped, nothing written: {path}: expected one match, found {n}: {old[:80]!r}")
        src = src.replace(old, rep)
    new[path] = src
for path, src in new.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
print("the conch, the night and the constant know easing")
