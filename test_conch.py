"""
test_conch.py: the conch, tested forward.

    python3 -m unittest test_conch -v

The fourteen tests in Section 10 of the build specification are here under
their own names, with the tests for what this build adds: how the conch knows
a moment left its silico-stasis, the fold, and the night.

Every moment in this file is typed by hand. No organ, no Gateway and no
polymetis is connected. On this bench two readings have the same shape when
they were given the same name; a real organ measures shape.

Each test writes its spiral into test_spirals/, beside this file, so the
conch is tested on the drive it lives on. Nothing in this file deletes
anything: a run leaves its spirals there to be looked at.
"""

import ast
import dataclasses
import inspect
import itertools
import json
import os
import socket
import unittest
from datetime import datetime, timezone

import conch_fold
import conch_level3
import conch_sleep
from conch import Conch
from conch_fold import FoldWouldLoseFunction, check
from conch_intake import sort_at_the_lip
from conch_level3 import ConstantDoesNotMatch
from conch_open import Open
from conch_records import (ABSENT, BOUNDARY_EVENT, CARRIED, INTERRUPTION, LET_GO, LEVEL_1, LEVEL_2,
                           LEVEL_3, LIVING, NEEDED_FOR, PERMANENT, QUIET, SENSES, SOURCE,
                           ConchState, Fold, Level3Mark, LipDrop, Moment, OneTimeFold, Turn,
                           absent, gave, mark_of, quiet)
from conch_sleep import BeingIsAwake
from conch_spiral import (CLOCK_OF, FIELDS, NotThisBeingsSpiral, Spiral, SpiralChangedUnderneath,
                          SpiralDamaged, SpiralView, write_beside)

HERE = os.path.dirname(os.path.abspath(__file__))
THIS_RUN = os.path.join(HERE, "test_spirals",
                        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
                        + "-" + str(os.getpid()))

_reading = itertools.count(1)


def moment(name, needed_for=None, **different):
    """A bench moment, typed by hand. Every sense gives a reading of its own
    each time, so no two moments hold the same thing. The shape of each sense
    is the name it was given, so two moments with the same name have the same
    shape. One sense can be given another name, or handed in ready-made."""
    n = next(_reading)
    senses = {}
    for sense in SENSES:
        word = different.get(sense, name)
        if isinstance(word, dict):
            senses[sense] = word
        else:
            senses[sense] = gave({"bench reading": n, "what": f"{word}, as {sense} gave it"},
                                 {"bench shape": [word, sense]}, f"{sense} organ clock {n}")
    return Moment(senses=senses, needed_for=needed_for)


def shape_of(name):
    return moment(name).shape()


def is_a_clock(text):
    return isinstance(text, str) and datetime.fromisoformat(text).tzinfo is not None


class Bench(unittest.TestCase):
    """One conch on one fresh spiral, with a being that sleeps when told to."""

    def setUp(self):
        self.dir = os.path.join(THIS_RUN, ".".join(self.id().split(".")[-2:]))
        os.makedirs(self.dir)
        self.path = os.path.join(self.dir, "spiral.jsonl")
        self.asleep = False
        self.conch = self.open()

    def open(self, being="bench-being", path=None):
        return Conch(being, path or self.path, asleep=lambda: self.asleep)

    def night(self, conch=None):
        self.asleep = True
        try:
            return (conch or self.conch).sleep()
        finally:
            self.asleep = False

    def raw(self, path=None):
        with open(path or self.path, "rb") as f:
            return f.read()

    def lines(self, path=None):
        return [json.loads(line) for line in self.raw(path).decode("utf-8").splitlines()]

    def morning(self, between=(), conch=None):
        """wake (procedural), coffee (nothing), whatever comes between, drive
        (procedural). Gives back what the conch gave for each."""
        conch = conch or self.conch
        came = [conch.take_in(moment("wake", "procedural")), conch.take_in(moment("coffee"))]
        came += [conch.take_in(m) for m in between]
        came.append(conch.take_in(moment("drive", "procedural")))
        return came

    def copy_to(self, name, spiral=None, constant=None, state=None):
        """A new folder holding copies of what is beside the spiral. Nothing is
        changed where it was."""
        there = os.path.join(self.dir, name)
        os.makedirs(there)
        path = os.path.join(there, "spiral.jsonl")
        for suffix, given in (("", spiral), (".constant.json", constant), (".state.json", state)):
            if given is False:
                continue
            if given is None:
                if not os.path.exists(self.path + suffix):
                    continue
                given = self.raw(self.path + suffix)
            with open(path + suffix, "xb") as f:
                f.write(given)
        return path


# ---- Section 10, tests 1 and the outside surface ----------------------------------

class StandsAlone(Bench):
    def test_runs_alone_with_the_network_blocked(self):
        def blocked(*a, **k):
            raise AssertionError("the conch reached for the network")
        real = socket.socket, socket.create_connection, socket.getaddrinfo
        socket.socket = socket.create_connection = socket.getaddrinfo = blocked
        try:
            for _ in range(3):
                self.morning()
            self.morning(between=[moment("phone call")])
            handed = self.conch.hand_over()
            report = self.night()
        finally:
            socket.socket, socket.create_connection, socket.getaddrinfo = real
        self.assertEqual(len(handed), 13)
        self.assertEqual(len(report["manual_entries_cut"]), 1)

    def test_standard_library_and_its_own_files_only(self):
        own = {"conch", "conch_records", "conch_spiral", "conch_intake", "conch_lip",
               "conch_fold", "conch_level3", "conch_sleep", "conch_open"}
        allowed = own | {"__future__", "copy", "dataclasses", "datetime", "hashlib", "json",
                         "os", "sys", "threading", "uuid"}
        for name in sorted(own | {"conch_bench"}):
            with open(os.path.join(HERE, name + ".py"), encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        self.assertIn(n.name.split(".")[0], allowed, name)
                if isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module.split(".")[0], allowed, name)

    def test_the_whole_outside_surface_is_five_methods(self):
        public = sorted(n for n in dir(Conch) if not n.startswith("_"))
        self.assertEqual(public, ["hand_over", "sleep", "spiral", "state", "take_in"])
        self.assertEqual([n for n in vars(self.conch) if not n.startswith("_")], [])
        self.assertEqual(list(inspect.signature(Conch.take_in).parameters), ["self", "moment"])
        for name in ("hand_over", "sleep", "spiral", "state"):
            self.assertEqual(list(inspect.signature(getattr(Conch, name)).parameters), ["self"])


# ---- Section 10, tests 2, 4, 9, 10, 13, 14 --------------------------------------

class NothingThatEntersIsLost(Bench):
    def test_every_moment_that_enters_is_on_the_spiral_in_order(self):
        entered = []
        for name, kind in [("lesson", "education"), ("the weather", None),
                           ("how the valve opens", "operational"), ("the parking", None),
                           ("what she asked for", "conversation"), ("lesson", "education")]:
            m = moment(name, kind)
            if isinstance(self.conch.take_in(m), Turn):
                entered.append(m.moment_id)
        on_the_spiral = [turn.moment.moment_id for turn in self.conch.spiral()]
        self.assertEqual(on_the_spiral, entered)
        self.assertEqual([turn.position for turn in self.conch.spiral()], [1, 2, 3, 4])

    def test_the_moment_is_kept_whole(self):
        senses = {
            "sight": gave({"frames": [[0, 1, 2], [3, 4, 5]], "light": 0.25, "note": "café ☕"},
                          {"edges": [1, 0, 1]}, "sight clock 09:00:00.120"),
            "sound": gave([0.5, -0.5, 0.125], {"band": "low"}, "sound clock 09:00:00.118"),
            "smell": gave({"present": ["coffee", "rain"]}, "coffee-and-rain", "smell clock 09:00:00.300"),
            "taste": quiet("taste clock 09:00:00.300"),
            "touch": absent(),
        }
        given = json.loads(json.dumps(senses))
        turn = self.conch.take_in(Moment(senses=senses, needed_for="education"))
        self.assertEqual(turn.moment.senses, given)
        self.assertEqual(self.conch.spiral().turn(1).moment.senses, given)
        self.assertEqual(self.open().spiral().turn(1).moment.senses, given)
        self.assertEqual(senses, given)                       # the conch changed nothing it was handed
        turn.moment.senses["sight"]["gave"] = "changed by whoever was reading"
        self.assertEqual(self.conch.spiral().turn(1).moment.senses, given)
        self.assertEqual(set(self.conch.spiral().turn(1).moment.senses), set(SENSES))

    def test_append_only(self):
        seen = self.raw()

        def still_a_prefix():
            nonlocal seen
            now = self.raw()
            self.assertTrue(now.startswith(seen))
            seen = now

        for _ in range(3):
            self.morning()                                    # Level 2, Level 1, late marks
            still_a_prefix()
        self.morning(between=[moment("phone call")])          # Level 3 as it arrives
        still_a_prefix()
        self.conch.hand_over()
        still_a_prefix()
        self.night()                                          # the fold, weight let go
        still_a_prefix()
        self.open().take_in(moment("lesson", "education"))    # a restart
        still_a_prefix()

    def test_every_line_has_its_clock_and_its_kind(self):
        for _ in range(3):
            self.morning()
        self.morning(between=[moment("phone call")])
        self.conch.hand_over()
        self.night()
        kinds = set()
        for line in self.lines():
            kinds.add(line["type"])
            self.assertTrue(is_a_clock(line[CLOCK_OF[line["type"]]]), line)
            self.assertEqual(line["kind"], PERMANENT)
            self.assertEqual(set(line), FIELDS[line["type"]])
        self.assertEqual(kinds, {"spiral", "turn", "level3_mark", "fold", "weight", "sleep"})
        for beside in (".constant.json", ".state.json"):
            with open(self.path + beside, encoding="utf-8") as f:
                state = json.load(f)
            self.assertEqual(state["kind"], LIVING)
            self.assertTrue(is_a_clock(state["written_at"]))
        state = self.conch.state()
        self.assertIsInstance(state, ConchState)
        self.assertEqual(state.kind, LIVING)
        self.assertTrue(is_a_clock(state.written_at))
        drop = self.conch.take_in(moment("coffee"))           # lived before and needed for nothing: it falls off
        self.assertIsInstance(drop, LipDrop)
        self.assertEqual(drop.kind, LIVING)
        self.assertTrue(is_a_clock(drop.fell_at))
        for turn in self.conch.spiral():
            self.assertTrue(is_a_clock(turn.moment.arrived_at))

    def test_one_being_one_spiral(self):
        hers = os.path.join(self.dir, "her", "spiral.jsonl")
        other = self.open(being="another-being", path=hers)
        self.conch.take_in(moment("lesson", "education"))
        other.take_in(moment("how the valve opens", "operational"))
        self.assertEqual(len(self.conch.spiral()), 1)
        self.assertEqual(len(other.spiral()), 1)
        self.assertNotEqual(self.conch.spiral().turn(1).moment.moment_id,
                            other.spiral().turn(1).moment.moment_id)
        mine, theirs = self.raw(), self.raw(hers)
        with self.assertRaises(NotThisBeingsSpiral):
            self.open(being="another-being", path=self.path)
        with self.assertRaises(NotThisBeingsSpiral):
            self.open(being="bench-being", path=hers)
        self.assertEqual(self.raw(), mine)
        self.assertEqual(self.raw(hers), theirs)
        with self.assertRaises(ValueError):
            Conch("", os.path.join(self.dir, "nobody", "spiral.jsonl"))

    def test_restart_holds(self):
        for _ in range(3):
            self.morning()
        self.morning(between=[moment("phone call")])
        self.night()
        before = self.raw()
        turns = list(self.conch.spiral())
        marks, manual = self.conch.spiral().marks(), self.conch.spiral().manual()
        again = self.open()
        self.assertEqual(self.raw(), before)                  # starting again wrote nothing
        self.assertEqual(list(again.spiral()), turns)
        self.assertEqual(again.spiral().marks(), marks)
        self.assertEqual(again.spiral().manual(), manual)
        nxt = again.take_in(moment("lesson", "education"))
        self.assertEqual(nxt.position, len(turns) + 1)
        self.assertTrue(self.raw().startswith(before))

    def test_a_moment_id_is_never_reused(self):
        m = moment("lesson", "education")
        self.conch.take_in(m)
        before = self.raw()
        with self.assertRaises(ValueError):
            self.conch.take_in(m)
        self.assertEqual(self.raw(), before)

    def test_arrived_at_is_the_conchs_own_clock(self):
        with self.assertRaises(ValueError):
            self.conch.take_in(dataclasses.replace(moment("lesson", "education"),
                                                   arrived_at="2020-01-01T00:00:00+00:00"))
        m = moment("lesson", "education")
        turn = self.conch.take_in(m)
        self.assertIsNone(m.arrived_at)
        self.assertTrue(is_a_clock(turn.moment.arrived_at))

    def test_what_comes_back_cannot_be_changed(self):
        turn = self.conch.take_in(moment("lesson", "education"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            turn.level = LEVEL_3
        with self.assertRaises(dataclasses.FrozenInstanceError):
            turn.weight = LET_GO


# ---- Section 10, tests 3 and 8: the lip ---------------------------------------

class TheLip(Bench):
    def test_level_1_falls_off_the_lip(self):
        self.conch.take_in(moment("lesson", "education"))
        self.conch.hand_over()
        before = self.raw()
        drop = self.conch.take_in(moment("the weather zebra-7731"))
        self.assertIsInstance(drop, LipDrop)
        self.assertEqual(self.raw(), before)                  # it took no space on the spiral
        self.assertEqual(len(self.conch.spiral()), 1)
        self.assertEqual(self.conch.hand_over(), [drop])      # and went to the polymetis
        for name in os.listdir(self.dir):                     # nothing of it is kept anywhere
            with open(os.path.join(self.dir, name), "rb") as f:
                self.assertNotIn(b"zebra-7731", f.read(), name)

    def test_level_1_and_level_2_sort_by_everetts_definition(self):
        for kind in ("education", "operational", "procedural", "structure", "conversation"):
            self.assertIn(kind, NEEDED_FOR)
            turn = self.conch.take_in(moment("a " + kind + " moment", kind))
            self.assertIsInstance(turn, Turn)
            self.assertEqual(turn.level, LEVEL_2)
        self.assertEqual(len(NEEDED_FOR), 5)
        self.assertIsInstance(self.conch.take_in(moment("the cup of coffee")), LipDrop)
        before = self.raw()
        with self.assertRaises(ValueError):                   # a word the filter does not know is never guessed
            self.conch.take_in(moment("something", "important"))
        self.assertEqual(self.raw(), before)
        self.assertEqual(sort_at_the_lip(False, "education"), LEVEL_2)
        self.assertEqual(sort_at_the_lip(False, None), LEVEL_1)
        self.assertEqual(sort_at_the_lip(True, None), LEVEL_3)
        self.assertEqual(sort_at_the_lip(True, "procedural"), LEVEL_3)
        with self.assertRaises(TypeError):
            sort_at_the_lip("yes", None)
        with self.assertRaises(ValueError):
            sort_at_the_lip(False, "level_3")

    def test_coming_around_again_does_not_make_level_2(self):
        for _ in range(6):
            self.assertIsInstance(self.conch.take_in(moment("the cup of coffee")), LipDrop)
        self.assertEqual(len(self.conch.spiral()), 0)
        self.assertIsNone(self.conch.state().mouth)

    def test_all_five_senses_come_together(self):
        whole = moment("lesson", "education").senses
        missing = {k: v for k, v in whole.items() if k != "smell"}
        extra = dict(whole, balance=gave("level", "level", "balance clock"))
        no_clock = dict(whole, sound={"gave": "a bell", "shape": "bell", "organ_clock": None})
        no_shape = dict(whole, sound={"gave": "a bell", "shape": None, "organ_clock": "sound clock"})
        loud_quiet = dict(whole, taste={"gave": QUIET, "shape": "salt", "organ_clock": "taste clock"})
        clocked_absent = dict(whole, touch={"gave": ABSENT, "shape": ABSENT, "organ_clock": "touch clock"})
        text_alone = "she said the valve sticks"
        before = self.raw()
        for senses in (missing, extra, no_clock, no_shape, loud_quiet, clocked_absent, text_alone):
            with self.assertRaises(ValueError):
                self.conch.take_in(Moment(senses=senses, needed_for="education"))
        for not_a_moment in (text_alone, whole, None):
            with self.assertRaises(TypeError):
                self.conch.take_in(not_a_moment)
        self.assertEqual(self.raw(), before)

    def test_quiet_is_not_absent(self):
        a = moment("lesson", "education", taste=quiet("taste clock"))
        b = moment("lesson", "education", taste=absent())
        self.assertNotEqual(mark_of(a.shape()), mark_of(b.shape()))
        self.assertEqual(self.conch.take_in(a).moment.senses["taste"],
                         {"gave": QUIET, "shape": QUIET, "organ_clock": "taste clock"})
        self.assertEqual(self.conch.take_in(b).moment.senses["taste"],
                         {"gave": ABSENT, "shape": ABSENT, "organ_clock": None})
        self.assertEqual(self.conch.spiral().marks(), [])     # two shapes, each lived once

    def test_what_cannot_be_kept_whole_does_not_enter(self):
        before = self.raw()
        for reading in ({1, 2, 3}, b"raw bytes", float("nan"), (1, 2), {1: "a number for a name"}):
            with self.assertRaises(ValueError):
                self.conch.take_in(moment("lesson", "education",
                                          sight=gave(reading, "a shape", "sight clock")))
        self.assertEqual(self.raw(), before)

    def test_hand_over_gives_each_thing_once_in_the_order_it_came(self):
        self.assertEqual(self.conch.hand_over(), [])
        self.assertIsNone(self.conch.state().handed_over)
        a = self.conch.take_in(moment("lesson", "education"))
        b = self.conch.take_in(moment("the weather"))
        c = self.conch.take_in(moment("how the valve opens", "operational"))
        self.assertEqual(self.conch.hand_over(), [a, b, c])
        self.assertEqual(self.conch.hand_over(), [])
        self.assertEqual(self.conch.state().handed_over, 2)
        d = self.conch.take_in(moment("the parking"))
        self.assertEqual(self.conch.hand_over(), [d])
        self.assertEqual((self.conch.state().mouth, self.conch.state().handed_over), (2, 2))

    def test_hand_over_keeps_its_place_across_a_restart(self):
        a = self.conch.take_in(moment("lesson", "education"))
        self.conch.hand_over()
        b = self.conch.take_in(moment("how the valve opens", "operational"))
        self.conch.take_in(moment("the weather"))             # a drop still waiting when the conch stops
        again = self.open()
        self.assertEqual(again.state().handed_over, a.position)
        self.assertEqual(again.hand_over(), [b])              # the turn is handed; the drop was never stored
        self.assertEqual(self.open().hand_over(), [])


# ---- Section 10, tests 5, 6, 7: Level 3 ------------------------------------------

class Level3(Bench):
    def lived_mornings(self, times=2):
        for _ in range(times):
            self.morning()

    def test_a_break_in_a_lived_pattern_is_level_3(self):
        self.lived_mornings()
        self.conch.take_in(moment("wake", "procedural"))
        self.conch.take_in(moment("coffee"))
        m = moment("phone call")                              # not needed for anything, and it still enters
        turn = self.conch.take_in(m)
        self.assertIsInstance(turn, Turn)
        self.assertEqual(turn.level, LEVEL_3)
        self.assertEqual(turn.weight, CARRIED)
        mark = self.conch.spiral().marks()[-1]
        self.assertEqual((mark.position, mark.moment_id, mark.event_class, mark.source),
                         (turn.position, m.moment_id, INTERRUPTION, SOURCE))
        self.assertEqual(self.lines()[-2]["level"], LEVEL_3)

    def test_a_new_being_cannot_judge(self):
        for name in ("one", "two", "three", "four", "five", "six"):
            self.assertIsInstance(self.conch.take_in(moment(name)), LipDrop)
        for name in ("one", "two", "three"):                  # each lived twice now, the order only once more
            self.conch.take_in(moment(name))
        self.assertEqual(self.conch.spiral().marks(), [])
        self.assertEqual(len(self.conch.spiral()), 0)

    def test_one_time_is_not_a_pattern(self):
        for name in ("a", "b", "c", "a"):
            self.conch.take_in(moment(name))
        self.assertIsInstance(self.conch.take_in(moment("never lived")), LipDrop)   # a then b was lived once

    def test_lived_things_in_a_new_order_are_not_a_departure(self):
        self.lived_mornings()
        self.conch.take_in(moment("wake", "procedural"))
        turn = self.conch.take_in(moment("drive", "procedural"))     # coffee was expected; drive is lived
        self.assertEqual(turn.level, LEVEL_2)
        self.assertNotIn(INTERRUPTION, [m.event_class for m in self.conch.spiral().marks()])

    def test_one_new_sense_is_a_shape_never_lived(self):
        self.lived_mornings()
        self.conch.take_in(moment("wake", "procedural"))
        self.conch.take_in(moment("coffee"))
        turn = self.conch.take_in(moment("drive", "procedural", smell="smoke"))
        self.assertEqual(turn.level, LEVEL_3)
        self.assertEqual(self.conch.spiral().marks()[-1].event_class, INTERRUPTION)

    def test_it_stays_outside_until_something_it_has_lived_arrives(self):
        self.lived_mornings()
        self.conch.take_in(moment("wake", "procedural"))
        self.conch.take_in(moment("coffee"))
        outside = [self.conch.take_in(moment(name))
                   for name in ("phone call", "hospital", "waiting room")]
        self.assertEqual([t.level for t in outside], [LEVEL_3] * 3)
        back = self.conch.take_in(moment("drive", "procedural"))
        self.assertEqual(back.level, LEVEL_2)
        # Inside again: after something lived that nothing has followed twice,
        # a shape never lived is no break. Outside, it would have been Level 3.
        self.assertIsInstance(self.conch.take_in(moment("hospital")), LipDrop)
        self.assertIsInstance(self.conch.take_in(moment("the parking")), LipDrop)
        marks = self.conch.spiral().marks()
        self.assertEqual([m.event_class for m in marks if m.position >= outside[0].position],
                         [INTERRUPTION] * 3)

    def test_a_late_mark_still_lands(self):
        first = self.conch.take_in(moment("lesson", "education"))
        self.assertEqual(first.level, LEVEL_2)
        as_laid = self.raw()
        second = self.conch.take_in(moment("lesson", "education"))
        self.assertEqual(second.level, LEVEL_2)
        self.assertTrue(self.raw().startswith(as_laid))       # the earlier line is unchanged
        self.assertEqual(self.lines()[1]["level"], LEVEL_2)   # and still says how it was laid
        self.assertEqual(self.lines()[-1]["type"], "level3_mark")
        self.assertEqual(self.conch.spiral().turn(1).level, LEVEL_3)
        mark, = self.conch.spiral().marks()
        self.assertEqual((mark.position, mark.event_class, mark.source, mark.moment_id),
                         (1, BOUNDARY_EVENT, SOURCE, first.moment.moment_id))

    def test_the_first_time_is_marked_once_and_what_keeps_coming_is_the_floor(self):
        for _ in range(6):
            turn = self.conch.take_in(moment("lesson", "education"))
            self.assertEqual(turn.level, LEVEL_2)
        self.assertEqual([(m.position, m.event_class) for m in self.conch.spiral().marks()],
                         [(1, BOUNDARY_EVENT)])
        self.assertEqual([t.level for t in self.conch.spiral()], [LEVEL_3] + [LEVEL_2] * 5)

    def test_a_first_time_that_fell_off_the_lip_cannot_be_marked(self):
        self.conch.take_in(moment("the cup of coffee"))
        self.conch.take_in(moment("the cup of coffee"))
        self.assertEqual(self.conch.spiral().marks(), [])
        self.assertEqual(len(self.conch.spiral()), 0)

    def test_only_leaving_its_own_silico_stasis_makes_level_3(self):
        self.assertEqual({f.name for f in dataclasses.fields(Moment)},
                         {"senses", "needed_for", "carried_by", "moment_id", "arrived_at"})
        with self.assertRaises(TypeError):
            self.conch.take_in(moment("lesson", "education"), level=LEVEL_3)
        with self.assertRaises(ValueError):
            self.conch.take_in(moment("lesson", LEVEL_3))
        asking = moment("lesson", "education",
                        sight=gave({"level": LEVEL_3, "left_silico_stasis": True},
                                   "a shape that asks", "sight clock"))
        self.assertEqual(self.conch.take_in(asking).level, LEVEL_2)
        self.lived_mornings(3)
        self.morning(between=[moment("phone call"), moment("hospital")])
        marked = {m.position for m in self.conch.spiral().marks()}
        self.assertTrue(marked)
        for m in self.conch.spiral().marks():
            self.assertEqual(m.source, SOURCE)
            self.assertIn(m.event_class, (INTERRUPTION, BOUNDARY_EVENT))
        for turn in self.conch.spiral():
            self.assertEqual(turn.level == LEVEL_3, turn.position in marked)
        view = self.conch.spiral()
        for name in ("mark", "mark_level3", "lay", "set_level"):
            self.assertFalse(hasattr(view, name), name)
            self.assertFalse(hasattr(self.conch, name), name)

    def test_no_direction_can_be_stored(self):
        self.assertEqual({f.name for f in dataclasses.fields(Level3Mark)},
                         {"at", "moment_id", "position", "event_class", "source", "kind"})
        with self.assertRaises(TypeError):
            Level3Mark(at="now", moment_id="m", position=1, event_class=INTERRUPTION,
                       direction="bad")
        self.lived_mornings()
        self.morning(between=[moment("phone call")])
        mark_lines = [line for line in self.lines() if line["type"] == "level3_mark"]
        self.assertTrue(mark_lines)
        for line in mark_lines:
            self.assertEqual(set(line), FIELDS["level3_mark"])
        for fields in FIELDS.values():
            for name in ("direction", "valence", "good", "bad", "score", "salience",
                         "importance", "rank"):
                self.assertNotIn(name, fields)
        with_direction = [dict(line, direction="bad") if line["type"] == "level3_mark" else line
                          for line in self.lines()]
        path = self.copy_to("with-a-direction", spiral="".join(
            json.dumps(line) + "\n" for line in with_direction).encode("utf-8"))
        with self.assertRaises(SpiralDamaged):
            self.open(path=path)

    def test_the_constant_holds_marks_and_no_moment(self):
        self.conch.take_in(moment("lesson quagga-4410", "education"))
        self.conch.take_in(moment("the weather okapi-9902"))
        self.conch.take_in(moment("lesson quagga-4410", "education"))
        with open(self.path + ".constant.json", encoding="utf-8") as f:
            text = f.read()
        self.assertNotIn("quagga-4410", text)
        self.assertNotIn("okapi-9902", text)
        self.assertNotIn("bench reading", text)
        kept = json.loads(text)
        self.assertEqual(len(kept["lived"]), 2)
        for mark, lived in kept["lived"].items():
            self.assertRegex(mark, "^[0-9a-f]{64}$")
            self.assertIn(lived["lived"], ("once", "again"))
        for after in kept["follows"].values():
            self.assertTrue(set(after.values()) <= {"once", "again"})
        self.assertEqual(kept["being"], "bench-being")
        self.assertEqual(kept["learned_through"], 2)

    def test_the_constant_catches_up_after_a_stop_between_the_two_writes(self):
        self.conch.take_in(moment("lesson", "education"))
        constant_then, spiral_then = self.raw(self.path + ".constant.json"), self.raw()
        self.conch.take_in(moment("lesson", "education"))     # a turn line, then the late mark, then the constant
        turn_line = self.raw()[len(spiral_then):].split(b"\n")[0] + b"\n"
        # The conch stopped after it laid the second turn: no mark yet, and the constant not yet written.
        path = self.copy_to("stopped-between", spiral=spiral_then + turn_line,
                            constant=constant_then, state=False)
        again = self.open(path=path)
        self.assertEqual(again.spiral().turn(1).level, LEVEL_3)   # the first time was marked on the way back up
        self.assertEqual([m.event_class for m in again.spiral().marks()], [BOUNDARY_EVENT])
        with open(path + ".constant.json", encoding="utf-8") as f:
            kept = json.load(f)
        self.assertEqual(kept["learned_through"], 2)
        self.assertEqual([c["positions"] for c in kept["caught_up"]], [[2]])
        self.assertTrue(is_a_clock(kept["caught_up"][0]["at"]))
        self.assertEqual(self.open(path=path).spiral().marks(), again.spiral().marks())   # and only once

    def test_a_lost_constant_stops_the_conch(self):
        self.conch.take_in(moment("lesson", "education"))
        path = self.copy_to("constant-gone", constant=False)
        with self.assertRaises(ConstantDoesNotMatch):
            self.open(path=path)
        behind = self.copy_to("spiral-behind", spiral=self.raw().split(b"\n")[0] + b"\n")
        with self.assertRaises(ConstantDoesNotMatch):
            self.open(path=behind)
        kept = json.loads(self.raw(self.path + ".constant.json"))
        theirs = self.copy_to("their-constant", constant=json.dumps(
            dict(kept, being="another-being")).encode("utf-8"))
        with self.assertRaises(ConstantDoesNotMatch):
            self.open(path=theirs)


# ---- what this build adds: the last time (17 Nov) ------------------------------

class TheLastTime(Bench):
    """"Boundaries survive. The first time. And the point at which it stopped
    being constant." The conch knew drive came after coffee; then walk came
    instead, again."""

    def walk_morning(self, conch=None):
        conch = conch or self.conch
        return [conch.take_in(moment("wake", "procedural")), conch.take_in(moment("coffee")),
                conch.take_in(moment("walk", "procedural"))]

    def kept(self):
        return json.loads(self.raw(self.path + ".constant.json"))

    def test_when_it_stops_coming_again_the_last_time_is_marked(self):
        self.morning()                                        # wake 1, drive 2
        self.morning()                                        # wake 3, drive 4: the last drive
        first_walk = self.walk_morning()[2]                   # wake 5, walk 6
        self.assertEqual(first_walk.level, LEVEL_3)           # never lived, where drive was known
        self.assertEqual(self.conch.spiral().turn(4).level, LEVEL_2)   # once is not again
        self.walk_morning()                                   # wake 7, walk 8: missed again
        view = self.conch.spiral()
        self.assertEqual(view.turn(4).level, LEVEL_3)
        self.assertEqual(view.turn(4).weight, CARRIED)
        self.assertEqual(view.turn(2).level, LEVEL_3)         # the first time, still there
        last = view.marks()[-1]
        self.assertEqual((last.position, last.event_class, last.source),
                         (4, BOUNDARY_EVENT, SOURCE))
        self.assertEqual(self.lines()[4]["level"], LEVEL_2)   # the turn's own line is untouched
        stop, = self.kept()["stopped"]
        self.assertEqual(stop["last"], 4)
        self.assertEqual(stop["stopped"], mark_of(shape_of("drive")))
        self.assertEqual(stop["after"], mark_of(shape_of("coffee")))
        self.assertTrue(is_a_clock(stop["at"]))

    def test_one_miss_is_not_the_end(self):
        self.morning()
        self.morning()
        self.walk_morning()                                   # missed once
        self.morning()                                        # drive came after coffee again
        self.walk_morning()                                   # missed once, not again
        self.assertEqual(self.kept()["stopped"], [])
        self.assertEqual([m.position for m in self.conch.spiral().marks()
                          if m.event_class == BOUNDARY_EVENT], [1, 2])
        self.conch.take_in(moment("wake", "procedural"))
        self.conch.take_in(moment("coffee"))
        self.assertEqual(self.conch.take_in(moment("phone call")).level, LEVEL_3)   # still known

    def test_after_it_stops_it_has_to_be_lived_again(self):
        self.morning()
        self.morning()
        self.walk_morning()
        self.walk_morning()                                   # coffee -> drive has stopped
        coffee = mark_of(shape_of("coffee"))
        self.assertNotIn(mark_of(shape_of("drive")), self.kept()["follows"][coffee])
        self.morning()                                        # drive after coffee: lived once again
        self.assertEqual(self.kept()["follows"][coffee][mark_of(shape_of("drive"))], "once")
        self.assertEqual(len(self.kept()["stopped"]), 1)

    def test_a_last_time_folded_into_a_routine_is_still_marked(self):
        for _ in range(3):
            self.morning()
            self.night()                                      # night 3 cuts wake -> drive
        entry, = self.conch.spiral().manual()
        self.assertIn([5, 6], entry.folded_from)              # day 3: wake 5, drive 6
        self.assertEqual(self.conch.spiral().turn(6).weight, LET_GO)
        self.walk_morning()
        self.walk_morning()
        view = self.conch.spiral()
        self.assertEqual(view.turn(6).level, LEVEL_3)
        self.assertEqual(view.turn(6).weight, CARRIED)        # the boundary carries its weight
        entry_now, = view.manual()
        self.assertEqual(entry_now.folded_from, entry.folded_from)   # the entry still stands for it
        self.assertEqual(self.open().spiral().turn(6).level, LEVEL_3)   # and the spiral reads back
        self.night()                                          # a night after it changes nothing of it
        self.assertEqual(self.conch.spiral().turn(6).level, LEVEL_3)

    def test_a_last_time_that_fell_off_the_lip_cannot_be_marked(self):
        self.morning()                                        # coffee follows wake, and falls off
        self.morning()
        before = [m.position for m in self.conch.spiral().marks()]
        for _ in range(2):
            self.conch.take_in(moment("wake", "procedural"))
            self.conch.take_in(moment("drive", "procedural"))  # no coffee, again
        self.assertEqual([m.position for m in self.conch.spiral().marks()], before)
        stop, = self.kept()["stopped"]
        self.assertIsNone(stop["last"])
        self.assertEqual(stop["stopped"], mark_of(shape_of("coffee")))

    def test_a_constant_without_its_stops_is_not_a_constant(self):
        self.morning()
        kept = self.kept()
        for name in ("stopped", "missed", "last_followed"):
            path = self.copy_to("without-" + name, constant=json.dumps(
                {k: v for k, v in kept.items() if k != name}).encode("utf-8"))
            with self.assertRaises(ConstantDoesNotMatch):
                self.open(path=path)

    def test_the_last_time_holds_no_count(self):
        source = inspect.getsource(conch_level3.Constant._what_followed)
        for word in ("+= 1", "count", "len(", ">=", "threshold", "rate"):
            self.assertNotIn(word, source)


# ---- Section 10, test 12, and what this build adds: the night ------------------

class TheNight(Bench):
    def test_sleep_is_sleep_only(self):
        for _ in range(3):
            self.morning()
        before = self.raw()
        with self.assertRaises(BeingIsAwake):
            self.conch.sleep()
        self.assertEqual(self.raw(), before)                  # refused, and nothing was changed
        turns = [(t.position, t.moment, t.written_at) for t in self.conch.spiral()]
        report = self.night()
        self.assertTrue(self.raw().startswith(before))        # every record byte for byte as it was
        self.assertGreater(len(self.raw()), len(before))
        self.assertEqual([(t.position, t.moment, t.written_at) for t in self.conch.spiral()], turns)
        self.assertIs(report["earlier_lines_unchanged"], True)

    def test_a_conch_handed_nothing_to_ask_is_awake(self):
        alone = Conch("bench-being", os.path.join(self.dir, "alone", "spiral.jsonl"))
        with self.assertRaises(BeingIsAwake):
            alone.sleep()
        for n, answer in enumerate(("yes", 1, None, False)):   # only a plain True is asleep
            said = Conch("bench-being", os.path.join(self.dir, "said-%d" % n, "spiral.jsonl"),
                         asleep=lambda answer=answer: answer)
            with self.assertRaises(BeingIsAwake):
                said.sleep()
        with self.assertRaises(TypeError):
            Conch("bench-being", os.path.join(self.dir, "not-a-call", "spiral.jsonl"), asleep=True)

    def test_repeats_fold_into_one_entry(self):
        for _ in range(3):
            self.morning()
        moments = [t.moment for t in self.conch.spiral()]
        report = self.night()
        entry, = self.conch.spiral().manual()
        self.assertEqual(report["manual_entries_cut"], [entry.fold_id])
        self.assertEqual(entry.steps, [shape_of("wake"), shape_of("drive")])
        self.assertEqual((entry.start, entry.end), (shape_of("wake"), shape_of("drive")))
        self.assertEqual(entry.folded_from, [[3, 4], [5, 6]])
        self.assertEqual([t.weight for t in self.conch.spiral()], [CARRIED] * 2 + [LET_GO] * 4)
        self.assertEqual([t.level for t in self.conch.spiral()], [LEVEL_3] * 2 + [LEVEL_2] * 4)
        self.assertEqual([t.moment for t in self.conch.spiral()], moments)    # every record whole
        self.assertTrue(is_a_clock(entry.cut_at))
        self.assertEqual(entry.kind, PERMANENT)

    def test_the_entry_is_the_shapes_and_the_readings_stay_in_the_record(self):
        for _ in range(3):
            self.morning()
        self.night()
        fold_line, = [line for line in self.lines() if line["type"] == "fold"]
        self.assertNotIn("bench reading", json.dumps(fold_line))
        self.assertNotIn("organ clock", json.dumps(fold_line))
        for step in fold_line["steps"]:
            self.assertEqual(set(step), set(SENSES))          # all five senses, not text
        readings = [t.moment.senses["sight"]["gave"]["bench reading"] for t in self.conch.spiral()]
        self.assertEqual(len(set(readings)), len(readings))   # each time was its own, and still is

    def test_level_3_is_never_folded(self):
        for _ in range(4):
            self.morning()
        self.morning(between=[moment("phone call")])
        self.morning()
        self.night()
        level_3 = [t.position for t in self.conch.spiral() if t.level == LEVEL_3]
        self.assertEqual(level_3, [1, 2, 10])
        folded = {p for entry in self.conch.spiral().manual() for run in entry.folded_from for p in run}
        self.assertFalse(folded & set(level_3))
        for position in level_3:
            self.assertEqual(self.conch.spiral().turn(position).weight, CARRIED)
        before = self.raw()
        spiral = Spiral("bench-being", self.path)
        with self.assertRaises(SpiralDamaged):                # and the spiral itself refuses it
            spiral.fold([shape_of("wake")], [[1], [9]])
        self.assertEqual(self.raw(), before)

    def test_a_broken_day_is_not_folded_across_the_break(self):
        for _ in range(3):
            self.morning()
        self.night()
        broken = self.morning(between=[moment("phone call")])
        report = self.night()
        wake, drive = broken[0].position, broken[-1].position
        self.assertEqual(report["left_whole"], [wake, drive])
        self.assertEqual(report["manual_entries_cut"], [])
        self.assertEqual(report["manual_entries_grown"], [])
        for position in (wake, drive):
            self.assertEqual(self.conch.spiral().turn(position).weight, CARRIED)

    def test_later_repeats_join_the_same_entry(self):
        for _ in range(3):
            self.morning()
        first = self.night()
        for _ in range(2):
            self.morning()
        second = self.night()
        entry, = self.conch.spiral().manual()
        self.assertEqual(second["manual_entries_cut"], [])
        self.assertEqual(second["manual_entries_grown"], first["manual_entries_cut"])
        self.assertEqual(entry.folded_from, [[3, 4], [5, 6], [7, 8], [9, 10]])
        self.assertEqual(second["weight_let_go"], [7, 8, 9, 10])
        third = self.night()                                  # a night with nothing new does nothing
        self.assertEqual((third["manual_entries_cut"], third["manual_entries_grown"],
                          third["weight_let_go"]), ([], [], []))

    def test_one_thing_over_and_over_is_that_one_thing(self):
        for _ in range(5):
            self.conch.take_in(moment("take the pill", "procedural"))
        self.night()
        entry, = self.conch.spiral().manual()
        self.assertEqual(entry.steps, [shape_of("take the pill")])
        self.assertEqual(entry.folded_from, [[2], [3], [4], [5]])

    def test_the_longest_routine_is_kept_whole(self):
        for _ in range(3):
            for name in ("open the valve", "read the gauge", "close the valve"):
                self.conch.take_in(moment(name, "operational"))
        self.night()
        entry, = self.conch.spiral().manual()
        self.assertEqual(entry.steps, [shape_of("open the valve"), shape_of("read the gauge"),
                                       shape_of("close the valve")])
        self.assertEqual(entry.folded_from, [[4, 5, 6], [7, 8, 9]])

    def test_a_level_2_moment_that_never_repeats_is_left_whole(self):
        said = self.conch.take_in(moment("what she asked for", "conversation"))
        report = self.night()
        self.assertEqual(report["left_whole"], [said.position])
        self.assertEqual(self.conch.spiral().turn(said.position).weight, CARRIED)
        self.assertEqual(self.conch.spiral().manual(), [])

    def test_the_fold_refuses_to_lose_a_step(self):
        a, b, c = shape_of("open the valve"), shape_of("read the gauge"), shape_of("close the valve")
        check([a, b, c], [[a, b, c], [a, b, c]])
        with self.assertRaises(FoldWouldLoseFunction):
            check([a, c], [[a, b, c], [a, b, c]])             # the entry dropped a step every repeat has
        with self.assertRaises(FoldWouldLoseFunction):
            check([a, b, c], [[a, b, c], [a, c]])             # a repeat lacks a step the entry has
        with self.assertRaises(FoldWouldLoseFunction):
            check([a, b, c], [[a, b, c], [a, c, b]])          # the same steps in another order
        with self.assertRaises(FoldWouldLoseFunction):
            check([], [[a], [a]])
        for _ in range(3):
            for name in ("open the valve", "read the gauge", "close the valve"):
                self.conch.take_in(moment(name, "operational"))
        before = self.raw()
        spiral = Spiral("bench-being", self.path)
        with self.assertRaises(SpiralDamaged):                # the spiral holds the same line itself
            spiral.fold([a, c], [[4, 6], [7, 9]])
        with self.assertRaises(SpiralDamaged):
            spiral.fold([a, b], [[4, 5], [8, 9]])
        self.assertEqual(self.raw(), before)

    def test_the_fold_survives_a_restart(self):
        for _ in range(4):
            self.morning()
        self.night()
        manual = self.conch.spiral().manual()
        weights = [t.weight for t in self.conch.spiral()]
        again = self.open()
        self.assertEqual(again.spiral().manual(), manual)
        self.assertEqual([t.weight for t in again.spiral()], weights)
        self.morning(conch=again)
        report = self.night(again)
        self.assertEqual(report["manual_entries_grown"], [manual[0].fold_id])
        self.assertEqual(len(again.spiral().manual()), 1)

    def test_the_report_is_what_happened(self):
        for _ in range(3):
            self.morning()
            for name in ("open the valve", "close the valve"):
                self.conch.take_in(moment(name, "operational"))
        before = self.lines()
        report = self.night()
        tonight = self.lines()[len(before):]
        folds = [line for line in tonight if line["type"] == "fold"]
        weights = [line for line in tonight if line["type"] == "weight"]
        sleep, = [line for line in tonight if line["type"] == "sleep"]
        self.assertEqual(report["manual_entries_cut"], [line["fold_id"] for line in folds])
        self.assertEqual(report["weight_let_go"], [p for line in weights for p in line["positions"]])
        self.assertEqual(report["went_back_over"], len(self.conch.spiral()))
        self.assertEqual(sorted(report["weight_let_go"] + report["left_whole"]
                                + [t.position for t in self.conch.spiral() if t.level == LEVEL_3]),
                         [t.position for t in self.conch.spiral()])
        for name in ("went_back_over", "manual_entries_cut", "manual_entries_grown",
                     "weight_let_go", "stopped_early"):
            self.assertEqual(sleep[name], report[name], name)
        self.assertEqual(sleep["at"], report["ran_at"])
        self.assertEqual(report["kind"], LIVING)
        self.assertTrue(is_a_clock(report["ran_at"]) and is_a_clock(report["finished_at"]))
        self.assertEqual(self.conch.spiral().nights(), [sleep])

    def test_open_slots_say_they_are_open(self):
        slots = conch_sleep.OPEN_AT_NIGHT
        self.assertEqual(len(slots), 3)
        self.assertFalse(hasattr(conch_fold, "ONE_TIME"))     # closed on 17 Nov: one-time moments fold
        self.assertFalse(hasattr(conch_level3, "THE_LAST_TIME"))   # closed on 17 Nov: the last time
        self.assertIn(conch_level3.EASING, slots)
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
        self.assertEqual(self.lines()[-1]["open"], [slot.slot for slot in slots])

    def test_a_night_stops_if_the_being_wakes(self):
        for _ in range(3):
            for name in ("open the valve", "close the valve"):
                self.conch.take_in(moment(name, "operational"))
        for _ in range(3):
            for name in ("lift", "set down"):
                self.conch.take_in(moment(name, "procedural"))
        asked = []

        def asleep_for_two_asks():
            asked.append(len(asked))
            return len(asked) <= 2

        waking = Conch("bench-being", self.path, asleep=asleep_for_two_asks)
        report = waking.sleep()
        self.assertEqual(report["stopped_early"], "the being woke")
        self.assertEqual(len(report["manual_entries_cut"]), 1)
        self.assertEqual(report["weight_let_go"], [3, 4, 5, 6])
        self.assertEqual(report["left_whole"], [9, 10, 11, 12])
        self.assertEqual(self.lines()[-1]["stopped_early"], "the being woke")
        rest = self.night(self.open())                        # what it had not reached waits for the next night
        self.assertIsNone(rest["stopped_early"])
        self.assertEqual(rest["weight_let_go"], [9, 10, 11, 12])
        self.assertEqual(len(self.open().spiral().manual()), 2)


# ---- a Level 2 moment lived once (17 Nov) ----------------------------------------------

def said_once(name, needed_for, carried_by, **different):
    """A moment that says which senses carried what it is needed for."""
    return dataclasses.replace(moment(name, needed_for, **different), carried_by=carried_by)


class LivedOnce(Bench):
    def test_a_one_time_part_of_a_conversation_folds_to_the_senses_that_carried_it(self):
        m = said_once("the dock code is 4471", "conversation", ("sound",))
        turn = self.conch.take_in(m)
        self.assertEqual(turn.moment.carried_by, ("sound",))
        report = self.night()
        entry, = self.conch.spiral().manual()
        self.assertIsInstance(entry, OneTimeFold)
        self.assertEqual(report["manual_entries_cut"], [entry.fold_id])
        self.assertEqual(entry.carried_by, ("sound",))
        self.assertEqual(entry.step, {"sound": shape_of("the dock code is 4471")["sound"]})
        self.assertEqual(entry.folded_from, 1)
        self.assertEqual(report["weight_let_go"], [1])
        self.assertEqual(report["left_whole"], [])
        kept = self.conch.spiral().turn(1)
        self.assertEqual((kept.level, kept.weight), (LEVEL_2, LET_GO))
        self.assertEqual(kept.moment.senses, m.senses)        # the record stays whole
        line, = [l for l in self.lines() if l["type"] == "fold_one"]
        self.assertEqual(set(line["step"]), {"sound"})        # the entry holds nothing else
        self.assertNotIn("bench reading", json.dumps(line))
        self.assertEqual(self.open().spiral().manual(), [entry])   # and survives a restart

    def test_a_nonverbal_conversation_keeps_sight(self):
        self.conch.take_in(said_once("points at the cup", "conversation", ("sight", "touch")))
        self.night()
        entry, = self.conch.spiral().manual()
        self.assertEqual(entry.carried_by, ("sight", "touch"))
        self.assertEqual(set(entry.step), {"sight", "touch"})

    def test_what_says_nothing_about_its_senses_is_left_whole(self):
        turn = self.conch.take_in(moment("a lesson heard once", "education"))
        report = self.night()
        self.assertEqual(self.conch.spiral().manual(), [])
        self.assertEqual(report["left_whole"], [turn.position])
        self.assertEqual(self.conch.spiral().turn(turn.position).weight, CARRIED)

    def test_which_senses_carried_it_is_checked_and_never_guessed(self):
        before = self.raw()
        for needed, carried, different in [
                (None, ("sound",), {}),                       # nothing it is needed for
                ("procedural", ("touch",), {}),               # procedure folds only as a routine
                ("conversation", (), {}),
                ("conversation", ("hearing",), {}),
                ("conversation", ("sound", "sound"), {}),
                ("conversation", ("taste",), {"taste": quiet("taste clock")}),
                ("conversation", ("touch",), {"touch": absent()})]:
            with self.assertRaises(ValueError):
                self.conch.take_in(said_once("something said", needed, carried, **different))
        self.assertEqual(self.raw(), before)

    def test_a_routine_folds_as_a_routine_first(self):
        for _ in range(3):
            self.conch.take_in(said_once("the safety talk", "education", ("sound",)))
        self.night()
        entry, = self.conch.spiral().manual()
        self.assertIsInstance(entry, Fold)
        self.assertEqual(entry.folded_from, [[2], [3]])
        self.assertEqual(self.conch.spiral().turn(1).level, LEVEL_3)   # the first time, never folded

    def test_level_3_is_never_folded_one_time(self):
        for _ in range(2):
            self.morning()
        broke = self.morning(between=[said_once("the phone call", "conversation", ("sound",))])
        self.night()
        self.assertEqual(self.conch.spiral().turn(broke[2].position).level, LEVEL_3)
        held = [e.folded_from for e in self.conch.spiral().manual() if isinstance(e, OneTimeFold)]
        self.assertNotIn(broke[2].position, held)

    def test_a_one_time_moment_that_comes_again_is_still_its_first_time(self):
        self.conch.take_in(said_once("the dock code is 4471", "conversation", ("sound",)))
        self.night()
        entry, = self.conch.spiral().manual()
        again = self.conch.take_in(said_once("the dock code is 4471", "conversation", ("sound",)))
        first = self.conch.spiral().turn(1)
        self.assertEqual((first.level, first.weight), (LEVEL_3, CARRIED))
        self.assertEqual([m.event_class for m in self.conch.spiral().marks()], [BOUNDARY_EVENT])
        self.assertEqual(self.conch.spiral().manual()[0], entry)      # the entry stays as it was cut
        self.assertEqual(again.level, LEVEL_2)
        self.assertEqual(self.open().spiral().turn(1).level, LEVEL_3)

    def test_a_one_time_entry_that_lost_a_sense_stops_the_conch(self):
        self.conch.take_in(said_once("the dock code is 4471", "conversation", ("sound", "sight")))
        self.night()
        lines = self.lines()
        for line in lines:
            if line["type"] == "fold_one":
                line["step"].pop("sight")
        path = self.copy_to("lost-a-sense", spiral="".join(
            json.dumps(line) + "\n" for line in lines).encode("utf-8"))
        with self.assertRaises(SpiralDamaged):
            self.open(path=path)


# ---- Section 10, test 11 -----------------------------------------------------------

class NoSearch(Bench):
    def test_no_search_surface(self):
        view = self.conch.spiral()
        self.assertIsInstance(view, SpiralView)
        public = sorted(n for n in dir(SpiralView) if not n.startswith("_"))
        self.assertEqual(public, ["manual", "marks", "nights", "turn"])
        for name in public:
            takes = list(inspect.signature(getattr(SpiralView, name)).parameters)
            self.assertEqual(takes, ["self", "position"] if name == "turn" else ["self"], name)
        self.conch.take_in(moment("lesson", "education"))
        for asked in ("lesson", "1", None, 1.0, True, [1]):
            with self.assertRaises(TypeError):
                view.turn(asked)
        with self.assertRaises(IndexError):
            view.turn(2)
        for thing in (view, self.conch):
            for name in ("search", "find", "query", "lookup", "match", "filter", "where", "index",
                         "rank", "score", "embed", "delete", "remove", "edit", "update", "write"):
                self.assertFalse(hasattr(thing, name), name)
        with self.assertRaises(TypeError):
            view["lesson"]
        with self.assertRaises(AttributeError):
            view.anything_new = 1


# ---- failing loud ------------------------------------------------------------------

class FailsLoud(Bench):
    def test_a_torn_spiral_stops_the_conch_and_nothing_is_repaired(self):
        self.conch.take_in(moment("lesson", "education"))
        torn = self.raw()[:-40]
        path = self.copy_to("torn", spiral=torn)
        with self.assertRaises(SpiralDamaged):
            self.open(path=path)
        self.assertEqual(self.raw(path), torn)
        empty = self.copy_to("empty", spiral=b"")
        with self.assertRaises(SpiralDamaged):
            self.open(path=empty)

    def test_a_line_that_was_changed_stops_the_conch_with_its_number(self):
        self.conch.take_in(moment("lesson", "education"))
        self.conch.take_in(moment("how the valve opens", "operational"))
        lines = self.lines()
        lines[2]["position"] = 7
        path = self.copy_to("changed", spiral="".join(
            json.dumps(line) + "\n" for line in lines).encode("utf-8"))
        with self.assertRaises(SpiralDamaged) as stopped:
            self.open(path=path)
        self.assertIn("line 3", str(stopped.exception))
        lines = self.lines()
        lines[1]["moment"]["senses"].pop("smell")
        path = self.copy_to("a-sense-gone", spiral="".join(
            json.dumps(line) + "\n" for line in lines).encode("utf-8"))
        with self.assertRaises(SpiralDamaged) as stopped:
            self.open(path=path)
        self.assertIn("line 2", str(stopped.exception))

    def test_a_spiral_written_underneath_stops_the_conch(self):
        self.conch.take_in(moment("lesson", "education"))
        second = self.open()
        second.take_in(moment("how the valve opens", "operational"))
        before = self.raw()
        with self.assertRaises(SpiralChangedUnderneath):
            self.conch.take_in(moment("what she asked for", "conversation"))
        self.assertEqual(self.raw(), before)

    def test_a_line_the_spiral_cannot_hold_is_refused_before_it_is_written(self):
        self.conch.take_in(moment("lesson", "education"))
        before = self.raw()
        spiral = Spiral("bench-being", self.path)
        with self.assertRaises(SpiralDamaged):
            spiral.mark_level3(1, "sideways")
        with self.assertRaises(SpiralDamaged):
            spiral.mark_level3(1, INTERRUPTION)               # an interruption is only marked as it arrives
        with self.assertRaises(ValueError):
            spiral.lay(moment("lesson", "education"), LEVEL_1)
        with self.assertRaises(ValueError):
            spiral.lay(moment("lesson", "education"), LEVEL_3)
        self.assertEqual(self.raw(), before)
        self.assertEqual(spiral.mouth(), 1)                   # and it still knows what the file says
        spiral.mark_level3(1, BOUNDARY_EVENT)
        self.assertTrue(self.raw().startswith(before))

    def test_living_state_always_carries_its_clock_and_its_kind(self):
        with self.assertRaises(ValueError):
            write_beside(os.path.join(self.dir, "no-clock.json"), {"kind": LIVING})
        with self.assertRaises(ValueError):
            write_beside(os.path.join(self.dir, "no-kind.json"), {"written_at": "now"})
        self.assertEqual([n for n in os.listdir(self.dir) if n.startswith("no-")], [])


if __name__ == "__main__":
    unittest.main()
