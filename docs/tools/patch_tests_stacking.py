"""patch_tests_stacking.py: test_conch.py brought up to stacking and anticipation (17 Nov 2026).

    python3 docs/tools/patch_tests_stacking.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once, or nothing is written.
"""
import sys

PATH = "test_conch.py"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""               "conch_fold", "conch_level3", "conch_sleep", "conch_open", "conch_easing"}""",
     """               "conch_fold", "conch_level3", "conch_sleep", "conch_open", "conch_easing",
               "conch_stack"}"""),

    ("""        self.assertEqual(public, ["go_back", "hand_over", "sleep", "spiral", "state", "take_in",
                                  "walked_out"])
        self.assertEqual([n for n in vars(self.conch) if not n.startswith("_")], [])
        self.assertEqual(list(inspect.signature(Conch.take_in).parameters), ["self", "moment"])
        self.assertEqual(list(inspect.signature(Conch.go_back).parameters), ["self", "position"])""",
     """        self.assertEqual(public, ["go_back", "hand_over", "plan", "sleep", "spiral", "state",
                                  "take_in", "used", "walked_out"])
        self.assertEqual([n for n in vars(self.conch) if not n.startswith("_")], [])
        self.assertEqual(list(inspect.signature(Conch.take_in).parameters), ["self", "moment"])
        self.assertEqual(list(inspect.signature(Conch.go_back).parameters), ["self", "position"])
        self.assertEqual(list(inspect.signature(Conch.plan).parameters), ["self", "steps"])
        self.assertEqual(list(inspect.signature(Conch.used).parameters), ["self", "fold_id"])"""),

    ("""        self.assertEqual(kinds, {"spiral", "turn", "level3_mark", "fold", "weight", "sleep"})""",
     """        self.assertEqual(kinds, {"spiral", "turn", "level3_mark", "fold", "weight", "stack",
                                 "sleep"})"""),

    ("""        self.assertEqual(public, ["manual", "marks", "nights", "turn"])""",
     """        self.assertEqual(public, ["manual", "marks", "nights", "stacked", "turn"])"""),

    ("""    def test_open_slots_say_they_are_open(self):
        slots = conch_sleep.OPEN_AT_NIGHT
        self.assertEqual(len(slots), 2)
        self.assertFalse(hasattr(conch_fold, "ONE_TIME"))     # closed on 17 Nov: one-time moments fold
        self.assertFalse(hasattr(conch_level3, "THE_LAST_TIME"))   # closed on 17 Nov: the last time
        self.assertFalse(hasattr(conch_level3, "EASING"))     # closed on 17 Nov: easing
        reached_before = [len(slot.reached) for slot in slots]
        report = self.night()
        self.assertEqual([o["open"] for o in report["open"]], [slot.slot for slot in slots])
        for said, slot, before in zip(report["open"], slots, reached_before):
            self.assertIsInstance(slot, Open)
            self.assertTrue(slot.is_open)
            self.assertEqual(said["did"], "nothing")
            self.assertEqual(said["waiting_on"], slot.waiting_on)
            self.assertTrue(is_a_clock(said["reached_at"]))
            self.assertEqual(len(slot.reached), before + 1)
            self.assertTrue(repr(slot).startswith("OPEN: "))
        self.assertEqual(self.lines()[-1]["open"], [slot.slot for slot in slots])""",
     """    def test_every_slot_the_night_left_open_is_built(self):
        self.assertEqual(conch_sleep.OPEN_AT_NIGHT, ())       # all closed on 17 Nov
        self.assertFalse(hasattr(conch_fold, "ONE_TIME"))
        self.assertFalse(hasattr(conch_level3, "THE_LAST_TIME"))
        self.assertFalse(hasattr(conch_level3, "EASING"))
        for name in ("ANTICIPATION_OF_WAKE", "STACKING_BY_USE"):
            self.assertFalse(hasattr(conch_sleep, name), name)
        report = self.night()
        self.assertEqual(report["open"], [])
        self.assertEqual(self.lines()[-1]["open"], [])

    def test_an_open_slot_still_says_it_is_open(self):
        slot = Open("a part found later", "whoever defines it")
        said = slot.reach()
        self.assertTrue(slot.is_open)
        self.assertEqual(said["did"], "nothing")
        self.assertEqual(said["waiting_on"], "whoever defines it")
        self.assertTrue(is_a_clock(said["reached_at"]))
        self.assertEqual(len(slot.reached), 1)
        self.assertTrue(repr(slot).startswith("OPEN: "))"""),

    ("""class NoSearch(Bench):""",
     """# ---- what this build adds: stacking by use, and anticipation of wake (17 Nov) ----

class Stacking(Bench):
    \"\"\"The card used goes back on top. Before shutdown the being goes over
    tomorrow, and comes up expecting that day.\"\"\"

    def setUp(self):
        super().setUp()
        for name in ("the dock code", "the gate code", "the alarm code"):
            self.conch.take_in(said_once(name, "conversation", ("sound",)))
        self.night()
        self.dock, self.gate, self.alarm = [e.fold_id for e in self.conch.spiral().manual()]

    def ids(self):
        return [entry.fold_id for entry in self.conch.spiral().stacked()]

    def test_tonights_cuts_are_stacked(self):
        self.assertEqual(self.ids(), [self.dock, self.gate, self.alarm])
        self.assertEqual(self.lines()[-2]["type"], "stack")

    def test_what_was_used_goes_on_top_newest_first(self):
        self.conch.used(self.alarm)
        self.conch.used(self.gate)
        self.assertEqual(self.ids(), [self.dock, self.gate, self.alarm])   # only in sleep
        report = self.night()
        self.assertEqual(report["stacked"], [self.gate, self.alarm, self.dock])
        self.assertEqual(self.ids(), [self.gate, self.alarm, self.dock])
        self.night()                                          # nothing used: it stays where it sat
        self.assertEqual(self.ids(), [self.gate, self.alarm, self.dock])
        self.assertEqual(self.open().spiral().stacked(), self.conch.spiral().stacked())

    def test_the_plan_comes_first_and_nothing_is_guessed(self):
        self.conch.used(self.dock)
        self.conch.plan([shape_of("the alarm code"), shape_of("buy milk")])
        report = self.night()
        self.assertEqual(report["planned"], [self.alarm])
        self.assertEqual(report["planned_with_nothing_in_the_manual"], [2])
        self.assertEqual(self.ids(), [self.alarm, self.dock, self.gate])

    def test_the_last_plan_before_the_night_is_the_one(self):
        self.conch.plan([shape_of("the dock code")])
        self.conch.plan([shape_of("the gate code")])          # gone over again, changed
        self.night()
        self.assertEqual(self.ids()[0], self.gate)
        self.night()                                          # a plan is for the night it was made for
        self.assertEqual(self.ids()[0], self.gate)
        self.assertEqual(self.night()["planned"], [])

    def test_a_plan_is_never_lived(self):
        constant, turns = self.raw(self.path + ".constant.json"), len(self.conch.spiral())
        self.conch.plan([shape_of("a shape never lived")])
        self.assertEqual(self.raw(self.path + ".constant.json"), constant)
        self.assertEqual(len(self.conch.spiral()), turns)
        self.assertEqual(self.lines()[-1]["type"], "plan")

    def test_a_routine_is_called_for_by_any_of_its_steps(self):
        for _ in range(3):
            self.morning()
            self.night()
        routine, = [e.fold_id for e in self.conch.spiral().manual() if isinstance(e, Fold)]
        self.conch.plan([shape_of("drive")])
        self.assertEqual(self.night()["planned"], [routine])
        self.assertEqual(self.ids()[0], routine)

    def test_refused_with_the_reason(self):
        with self.assertRaises(ValueError):
            self.conch.used("not an entry")
        for plan in ([], "drive", [{"sight": "x"}]):
            with self.assertRaises(ValueError):
                self.conch.plan(plan)
        self.asleep = True
        try:
            with self.assertRaises(BeingIsAsleep):
                self.conch.used(self.dock)
            with self.assertRaises(BeingIsAsleep):
                self.conch.plan([shape_of("drive")])
        finally:
            self.asleep = False

    def test_a_stack_holds_every_entry(self):
        forged = {"type": "stack", "order": [self.dock], "at": "2026-11-17T12:00:00.000+00:00",
                  "kind": PERMANENT}
        path = self.copy_to("short-stack", spiral=self.raw() + (json.dumps(forged) + "\\n")
                            .encode("utf-8"))
        with self.assertRaises(SpiralDamaged):
            self.open(path=path)


class NoSearch(Bench):"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("test_conch.py brought up to stacking")
