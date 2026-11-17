"""patch_tests_easing.py: test_conch.py brought up to easing (17 Nov 2026).

    python3 docs/tools/patch_tests_easing.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once, or nothing is written.
"""
import sys

PATH = "test_conch.py"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""from conch_records import (ABSENT, BOUNDARY_EVENT, CARRIED, INTERRUPTION, LET_GO, LEVEL_1, LEVEL_2,
                           LEVEL_3, LIVING, NEEDED_FOR, PERMANENT, QUIET, SENSES, SOURCE,
                           ConchState, Fold, Level3Mark, LipDrop, Moment, OneTimeFold, Turn,
                           absent, gave, mark_of, quiet)
from conch_sleep import BeingIsAwake""",
     """from conch_records import (ABSENT, BOUNDARY_EVENT, CARRIED, INTERRUPTION, LET_GO, LEVEL_1, LEVEL_2,
                           LEVEL_3, LIVING, NEEDED_FOR, PERMANENT, QUIET, SENSES, SOURCE,
                           TAKEN_BACK, ConchState, Fold, Level3Mark, LipDrop, Moment,
                           OneTimeFold, Turn, absent, gave, mark_of, quiet)
from conch_sleep import BeingIsAsleep, BeingIsAwake"""),

    ("""        own = {"conch", "conch_records", "conch_spiral", "conch_intake", "conch_lip",
               "conch_fold", "conch_level3", "conch_sleep", "conch_open"}""",
     """        own = {"conch", "conch_records", "conch_spiral", "conch_intake", "conch_lip",
               "conch_fold", "conch_level3", "conch_sleep", "conch_open", "conch_easing"}"""),

    ("""    def test_the_whole_outside_surface_is_five_methods(self):
        public = sorted(n for n in dir(Conch) if not n.startswith("_"))
        self.assertEqual(public, ["hand_over", "sleep", "spiral", "state", "take_in"])
        self.assertEqual([n for n in vars(self.conch) if not n.startswith("_")], [])
        self.assertEqual(list(inspect.signature(Conch.take_in).parameters), ["self", "moment"])
        for name in ("hand_over", "sleep", "spiral", "state"):""",
     """    def test_the_whole_outside_surface(self):
        public = sorted(n for n in dir(Conch) if not n.startswith("_"))
        self.assertEqual(public, ["go_back", "hand_over", "sleep", "spiral", "state", "take_in",
                                  "walked_out"])
        self.assertEqual([n for n in vars(self.conch) if not n.startswith("_")], [])
        self.assertEqual(list(inspect.signature(Conch.take_in).parameters), ["self", "moment"])
        self.assertEqual(list(inspect.signature(Conch.go_back).parameters), ["self", "position"])
        for name in ("hand_over", "sleep", "spiral", "state", "walked_out"):"""),

    ("""        self.assertEqual(len(slots), 3)
        self.assertFalse(hasattr(conch_fold, "ONE_TIME"))     # closed on 17 Nov: one-time moments fold
        self.assertFalse(hasattr(conch_level3, "THE_LAST_TIME"))   # closed on 17 Nov: the last time
        self.assertIn(conch_level3.EASING, slots)""",
     """        self.assertEqual(len(slots), 2)
        self.assertFalse(hasattr(conch_fold, "ONE_TIME"))     # closed on 17 Nov: one-time moments fold
        self.assertFalse(hasattr(conch_level3, "THE_LAST_TIME"))   # closed on 17 Nov: the last time
        self.assertFalse(hasattr(conch_level3, "EASING"))     # closed on 17 Nov: easing"""),

    ("""# ---- Section 10, test 12, and what this build adds: the night ------------------
""",
     """# ---- what this build adds: easing what a Level 3 moment is tied to (17 Nov) ----

class Easing(Bench):
    \"\"\"The being goes back to the place, alone, moves through every tied memory
    without flinching, and walks out. Only in sleep does the charge move.\"\"\"

    def setUp(self):
        super().setUp()
        self.morning()                                        # wake 1, drive 2
        self.morning()                                        # wake 3, drive 4
        self.morning(between=[moment("phone call"), moment("hospital")])   # wake 5, 6, 7, drive 8

    def go_through_it(self, conch=None):
        conch = conch or self.conch
        conch.take_in(moment("phone call"))
        conch.take_in(moment("hospital"))

    def test_the_event_is_the_moment_and_what_was_lived_with_it(self):
        self.assertEqual([self.conch.spiral().turn(p).level for p in (6, 7)], [LEVEL_3, LEVEL_3])
        self.assertEqual(self.conch._spiral.event_of(6), [6, 7])
        self.assertEqual(self.conch._spiral.event_of(7), [6, 7])
        self.assertEqual(self.conch._spiral.event_of(1), [1])   # a first time is its own event

    def test_a_held_return_eases_only_in_sleep_and_the_record_stays(self):
        self.conch.go_back(6)
        self.go_through_it()
        record = self.conch.walked_out()
        self.assertTrue(record["held"])
        self.assertIsNone(record["why"])
        self.assertEqual((record["position"], record["event"], sorted(record["lived"])),
                         (6, [6, 7], [6, 7]))
        self.assertEqual(self.lines()[-1]["type"], "went_back")
        self.assertEqual([self.conch.spiral().turn(p).weight for p in (6, 7)], [CARRIED] * 2)
        before, marks = self.raw(), self.conch.spiral().marks()
        report = self.night()
        self.assertEqual(report["charge_taken_back"], [[6, 7]])
        self.assertTrue(self.raw().startswith(before))        # every earlier byte as it was
        view = self.conch.spiral()
        for p in (6, 7):
            self.assertEqual(view.turn(p).weight, TAKEN_BACK)
            self.assertEqual(view.turn(p).level, LEVEL_3)     # lived truth never decays
        self.assertEqual(view.marks(), marks)                 # the witness is never removed
        self.assertEqual(self.open().spiral().turn(6).weight, TAKEN_BACK)   # and it reads back
        self.assertEqual(self.night()["charge_taken_back"], [])   # once

    def test_a_flinch_while_going_back_does_not_hold(self):
        self.conch.go_back(7)
        self.conch.take_in(moment("wake", "procedural"))
        smoke = self.conch.take_in(moment("smoke"))           # coffee was known to come next
        self.assertEqual(smoke.level, LEVEL_3)
        self.go_through_it()
        record = self.conch.walked_out()
        self.assertFalse(record["held"])
        self.assertIn("left silico-stasis", record["why"])
        self.assertEqual(self.night()["charge_taken_back"], [])
        self.assertEqual(self.conch.spiral().turn(6).weight, CARRIED)

    def test_every_tied_memory_has_to_be_lived_again(self):
        self.conch.go_back(6)
        self.conch.take_in(moment("phone call"))
        self.conch.take_in(moment("hospital", smell="antiseptic"))   # not the same place
        record = self.conch.walked_out()
        self.assertFalse(record["held"])
        self.assertEqual(record["lived"], [6])
        self.assertIn("not lived again: place 7", record["why"])
        self.assertEqual(self.night()["charge_taken_back"], [])

    def test_the_conch_never_chooses_and_going_back_is_awake(self):
        with self.assertRaises(ValueError):
            self.conch.go_back(8)                             # Level 2: nothing to go back to
        with self.assertRaises(ValueError):
            self.conch.walked_out()                           # nothing was gone back to
        self.asleep = True
        try:
            with self.assertRaises(BeingIsAsleep):
                self.conch.go_back(6)
        finally:
            self.asleep = False
        self.conch.go_back(6)
        with self.assertRaises(ValueError):
            self.conch.go_back(7)                             # one return at a time
        report = self.night()
        self.assertEqual(report["charge_taken_back"], [])     # a night never goes back by itself

    def test_the_charge_comes_back_if_it_flinches_later(self):
        self.conch.go_back(6)
        self.go_through_it()
        self.conch.walked_out()
        self.night()
        self.conch.take_in(moment("phone call"))              # the shape of a taken-back turn
        fire = self.conch.take_in(moment("fire"))             # hospital was known to come next
        self.assertEqual(fire.level, LEVEL_3)
        self.assertEqual(self.lines()[-1]["type"], "flinched")
        self.assertEqual(self.lines()[-1]["positions"], [6, 7])
        self.assertEqual(self.conch.spiral().turn(6).weight, TAKEN_BACK)   # only in sleep
        report = self.night()
        self.assertEqual(report["charge_given_back"], [[6, 7]])
        self.assertEqual([self.conch.spiral().turn(p).weight for p in (6, 7)], [CARRIED] * 2)

    def test_a_night_between_is_not_straight_away(self):
        self.conch.go_back(6)
        self.go_through_it()
        self.conch.walked_out()
        self.night()
        self.conch.take_in(moment("phone call"))
        self.night()
        self.conch.take_in(moment("fire"))
        self.assertNotIn("flinched", [line["type"] for line in self.lines()])

    def test_a_charge_nothing_called_for_is_refused(self):
        forged = {"type": "charge", "positions": [6, 7], "weight": TAKEN_BACK,
                  "because": "nobody went back", "at": "2026-11-17T12:00:00.000+00:00",
                  "kind": PERMANENT}
        path = self.copy_to("forged-charge", spiral=self.raw() + (json.dumps(forged) + "\\n")
                            .encode("utf-8"))
        with self.assertRaises(SpiralDamaged):
            self.open(path=path)


# ---- Section 10, test 12, and what this build adds: the night ------------------
"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("test_conch.py brought up to easing")
