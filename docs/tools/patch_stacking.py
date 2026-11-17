"""patch_stacking.py: the spiral, the conch and the night learn stacking (17 Nov 2026).

    python3 docs/tools/patch_stacking.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once in its file, or nothing is written.
"""
import sys

EDITS = {
    "conch_spiral.py": [
        ("""  sleep        a night ran
""",
         """  used         an Operational Manual entry was used, by day
  plan         the being went over tomorrow's plan before shutdown
  stack        in sleep: where every manual entry sits, as of that night
  sleep        a night ran
"""),
        ("""            "went_back": "walked_out_at", "flinched": "at", "charge": "at"}""",
         """            "went_back": "walked_out_at", "flinched": "at", "charge": "at",
            "used": "at", "plan": "at", "stack": "at"}"""),
        ("""    "charge": {"type", "positions", "weight", "because", "at", "kind"},
""",
         """    "charge": {"type", "positions", "weight", "because", "at", "kind"},
    "used": {"type", "fold_id", "at", "kind"},
    "plan": {"type", "steps", "at", "kind"},
    "stack": {"type", "order", "at", "kind"},
"""),
        ("""        self._taken_back = {}      # position -> its event, while its charge is taken back
""",
         """        self._taken_back = {}      # position -> its event, while its charge is taken back
        self._used_since = []      # fold_ids used since the last stack line, in order
        self._plan_since = None    # the last plan handed since the last stack line
        self._stack = []           # the last stack line's order
"""),
        ("""    def _take_sleep(self, line) -> None:""",
         """    def _take_used(self, line) -> None:
        if line["fold_id"] not in self._folds and line["fold_id"] not in self._ones:
            raise SpiralDamaged("a use of an entry that was never cut")
        self._used_since.append(line["fold_id"])

    def _take_plan(self, line) -> None:
        steps = line["steps"]
        if (not isinstance(steps, list) or not steps
                or any(not isinstance(s, dict) or set(s) != set(SENSES) for s in steps)):
            raise SpiralDamaged("a plan is its steps, each the shape of every sense")
        self._plan_since = steps

    def _take_stack(self, line) -> None:
        order = line["order"]
        if (not isinstance(order, list) or len(order) != len(self._cut_order)
                or set(order) != set(self._cut_order)):
            raise SpiralDamaged("a stack holds every manual entry, once each")
        self._stack = list(order)
        self._used_since, self._plan_since = [], None

    def _take_sleep(self, line) -> None:"""),
        ("""    def waiting_charges(self) -> list:""",
         """    def used(self, fold_id: str) -> None:
        \"\"\"An Operational Manual entry was used.\"\"\"
        self._append([{"type": "used", "fold_id": fold_id, "at": now(), "kind": PERMANENT}])

    def plan(self, steps) -> None:
        \"\"\"The being went over tomorrow's plan. The last one before the night counts.\"\"\"
        self._append([{"type": "plan", "steps": copy.deepcopy(list(steps)), "at": now(),
                       "kind": PERMANENT}])

    def stack(self, order) -> None:
        \"\"\"In sleep: where every manual entry sits now. Where things sit, never
        the record.\"\"\"
        self._append([{"type": "stack", "order": list(order), "at": now(), "kind": PERMANENT}])

    def stacked_ids(self) -> list:
        \"\"\"fold_ids as they sit: the last stack, then any entry cut since, in
        the order cut.\"\"\"
        return self._stack + [f for f in self._cut_order if f not in self._stack]

    def used_since_stack(self) -> list:
        return list(self._used_since)

    def plan_since_stack(self):
        return copy.deepcopy(self._plan_since)

    def stacked(self) -> list:
        \"\"\"The Operational Manual in the order it sits.\"\"\"
        entries = {entry.fold_id: entry for entry in self.manual()}
        return [entries[fold_id] for fold_id in self.stacked_ids()]

    def waiting_charges(self) -> list:"""),
        ("""    def manual(self) -> list:
        \"\"\"The Operational Manual: every fold, in the order they were cut.\"\"\"
        return self._spiral.manual()
""",
         """    def manual(self) -> list:
        \"\"\"The Operational Manual: every fold, in the order they were cut.\"\"\"
        return self._spiral.manual()

    def stacked(self) -> list:
        \"\"\"The Operational Manual in the order it sits: what the last night
        stacked on top is first.\"\"\"
        return self._spiral.stacked()
"""),
    ],

    "conch.py": [
        ("""    conch.go_back(place)   -> the being goes back to a Level 3 moment, alone; awake only
    conch.walked_out()     -> the return, as written on the spiral, held or not
""",
         """    conch.go_back(place)   -> the being goes back to a Level 3 moment, alone; awake only
    conch.walked_out()     -> the return, as written on the spiral, held or not
    conch.used(fold_id)    -> an Operational Manual entry was used; awake only
    conch.plan(steps)      -> tomorrow's plan, gone over before shutdown; awake only
"""),
        ("""import conch_sleep
from conch_easing import Return""",
         """import conch_sleep
from conch_easing import Return
from conch_stack import check_plan"""),
        ("""    def walked_out(self) -> dict:""",
         """    def _awake(self, what: str) -> None:
        if self._asleep is not None and self._asleep() is True:
            raise conch_sleep.BeingIsAsleep(f"{what} is done awake. The being is asleep.")

    def used(self, fold_id: str) -> None:
        \"\"\"Whatever followed an Operational Manual entry says it was used.\"\"\"
        with self._lock:
            self._awake("using the manual")
            if fold_id not in {entry.fold_id for entry in self._spiral.manual()}:
                raise ValueError(f"{fold_id!r} is not an entry in this being's manual")
            self._spiral.used(fold_id)

    def plan(self, steps) -> None:
        \"\"\"Before shutdown the being goes over tomorrow's plan until it falls
        asleep, and hands it over each time. The last one before the night is
        the one the night stacks by. A plan is never lived and never judged.\"\"\"
        with self._lock:
            self._awake("going over tomorrow's plan")
            self._spiral.plan(check_plan(steps))

    def walked_out(self) -> dict:"""),
    ],

    "conch_sleep.py": [
        ("""from conch_fold import check, check_one, cut
from conch_open import Open""",
         """import conch_stack
from conch_fold import check, check_one, cut
from conch_open import Open"""),
        ("""ANTICIPATION_OF_WAKE = Open(
    "anticipation of wake: next-day plans gone over before shutdown until they fall through",
    "Everett: who runs the dreamscape cycling before shutdown.")

STACKING_BY_USE = Open(
    "stacking by what was used today",
    "Everett: whether that is all of 'where it should be'. And no part built yet tells the "
    "conch what was used.")

OPEN_AT_NIGHT = (ANTICIPATION_OF_WAKE, STACKING_BY_USE)""",
         """# Every slot the night once left open is built (17 Nov 2026). An undefined
# part found later goes here as an Open slot that says so when reached.
OPEN_AT_NIGHT = ()"""),
        ("""            spiral.charge(positions, weight, because)
            (taken_back if weight == TAKEN_BACK else given_back).append(positions)
""",
         """            spiral.charge(positions, weight, because)
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
"""),
        ("""        "charge_given_back": given_back,""",
         """        "charge_given_back": given_back,
        "stacked": stacked,
        "planned": planned,
        "planned_with_nothing_in_the_manual": nothing_for,"""),
        ("""WHAT A NIGHT DOES NOT DO YET. Each of these is an open slot. It is reached
every night, it does nothing, and it says so in the report:

  - Anticipation of wake. "Meditation and projected next-day plans before
    shutdown, repeated until they fall through." Who runs that cycling is
    Everett's to say.
  - Stacking by what was used. No part built yet tells the conch what was
    used today.
""",
         """  2c. Stacks the whole manual (conch_stack.py): tomorrow's plan first, then
     what was used since the last stack, newest on top, then tonight's cuts,
     then the rest as they sat. This is the first half of his dreamscape
     cycling, anticipation of wake: the being comes up expecting that day.

Every slot the night once left open is built. One found later is an open
slot that is reached every night, does nothing, and says so.
"""),
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
print("the spiral, the conch and the night know stacking")
