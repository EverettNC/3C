"""
test_gateway.py: the Christman Gateway, tested forward, with the real conch behind it.

    python3 -m unittest test_gateway -v

No organ is connected here: each organ is a name and its readings are typed by
hand, so two readings have the same shape when they were given the same words.
A real organ measures shape. Each test writes its spiral into test_spirals/,
beside this file. Nothing here deletes anything.
"""

import ast
import os
import threading
import unittest
from datetime import datetime, timezone

from conch import Conch
from conch_records import ABSENT, QUIET, SENSES, LipDrop, Moment, Turn, gave
from gateway import Gateway, GatewayClosed

HERE = os.path.dirname(os.path.abspath(__file__))
THIS_RUN = os.path.join(HERE, "test_spirals", "gateway-"
                        + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
                        + "-" + str(os.getpid()))


def reading(words, clock="organ clock"):
    return gave({"typed for the organ": words}, {"bench shape": words}, clock)


class Catches:
    """Something with take_in that keeps every moment it was handed."""

    def __init__(self, refuse=False):
        self.moments, self.refuse = [], refuse

    def take_in(self, moment):
        if self.refuse:
            raise ValueError("the conch refused it")
        self.moments.append(moment)
        return "taken"


class TheHousing(unittest.TestCase):
    def setUp(self):
        self.conch = Catches()
        self.gate = Gateway(self.conch)

    def test_a_sense_with_no_organ_is_absent_and_a_connected_one_is_quiet(self):
        self.assertEqual({s: r["shape"] for s, r in self.gate.room().items()},
                         {s: ABSENT for s in SENSES})
        self.gate.connect("the ear", "sound")
        room = self.gate.room()
        self.assertEqual(room["sound"]["shape"], QUIET)
        self.assertTrue(room["sound"]["organ_clock"].startswith("connected at "))
        for sense in ("sight", "smell", "taste", "touch"):
            self.assertEqual(room[sense]["shape"], ABSENT)

    def test_the_same_shape_goes_on_being_the_same_moment(self):
        self.gate.connect("the ear", "sound")
        self.assertEqual(self.gate.arrive("the ear", "sound", reading("the fan", "1")), "taken")
        handed = len(self.conch.moments)
        for clock in ("2", "3", "4"):
            self.assertIsNone(self.gate.arrive("the ear", "sound", reading("the fan", clock)))
        self.assertEqual(len(self.conch.moments), handed)
        self.assertEqual(self.gate.room()["sound"]["organ_clock"], "1")   # the reading that opened it

    def test_a_change_on_any_sense_hands_over_the_moment_before_it_whole(self):
        self.gate.connect("the ear", "sound")
        self.gate.connect("the eye", "sight")
        self.gate.arrive("the ear", "sound", reading("the fan"))
        self.gate.arrive("the eye", "sight", reading("the kitchen"))
        before = len(self.conch.moments)
        self.gate.arrive("the eye", "sight", reading("the cabinet"))
        self.assertEqual(len(self.conch.moments), before + 1)
        moment = self.conch.moments[-1]
        self.assertIsInstance(moment, Moment)
        self.assertEqual(set(moment.senses), set(SENSES))
        self.assertEqual(moment.senses["sound"]["shape"], {"bench shape": "the fan"})
        self.assertEqual(moment.senses["sight"]["shape"], {"bench shape": "the kitchen"})
        self.assertEqual(moment.senses["smell"]["shape"], ABSENT)
        self.assertIsNone(moment.needed_for)                  # never guessed
        self.assertIsNone(moment.arrived_at)                  # the conch's own clock sets it
        self.assertEqual(self.gate.room()["sight"]["shape"], {"bench shape": "the cabinet"})

    def test_one_organ_can_serve_two_senses(self):
        self.gate.connect("the nose", "smell", "taste")
        self.assertEqual(self.gate.organs()["smell"], "the nose")
        self.assertEqual(self.gate.organs()["taste"], "the nose")
        self.gate.arrive("the nose", "smell", reading("coffee"))
        self.gate.arrive("the nose", "taste", reading("coffee"))
        self.assertEqual(self.gate.room()["taste"]["shape"], {"bench shape": "coffee"})

    def test_an_organ_gives_only_for_what_it_serves_and_only_whole_readings(self):
        self.gate.connect("the ear", "sound")
        for organ, sense, given in (
                ("the eye", "sound", reading("x")),       # another organ's sense
                ("the ear", "sight", reading("x")),       # no organ serves sight
                ("the ear", "smell of fear", reading("x")),
                ("the ear", "sound", {"shape": "x"}),
                ("the ear", "sound", gave("x", ABSENT, "clock")),
                ("the ear", "sound", gave("x", None, "clock")),
                ("the ear", "sound", gave(QUIET, "x", "clock")),
                ("the ear", "sound", gave("x", "x", ""))):
            with self.assertRaises(ValueError, msg=(organ, sense, given)):
                self.gate.arrive(organ, sense, given)
        with self.assertRaises(ValueError):
            self.gate.connect("another ear", "sound")       # one organ per sense
        self.assertEqual(self.conch.moments, [])

    def test_disconnecting_makes_a_sense_absent_again(self):
        self.gate.connect("the ear", "sound")
        self.gate.arrive("the ear", "sound", reading("the fan"))
        self.gate.disconnect("the ear", "sound")
        self.assertEqual(self.gate.room()["sound"]["shape"], ABSENT)
        self.assertEqual(self.conch.moments[-1].senses["sound"]["shape"],
                         {"bench shape": "the fan"})
        with self.assertRaises(ValueError):
            self.gate.arrive("the ear", "sound", reading("the fan"))

    def test_close_hands_over_the_moment_being_lived(self):
        self.gate.connect("the ear", "sound")
        self.gate.arrive("the ear", "sound", reading("the fan"))
        before = len(self.conch.moments)
        self.assertEqual(self.gate.close(), "taken")
        self.assertEqual(len(self.conch.moments), before + 1)
        with self.assertRaises(GatewayClosed):
            self.gate.arrive("the ear", "sound", reading("the tv"))

    def test_if_the_conch_refuses_nothing_here_is_lost(self):
        self.gate.connect("the ear", "sound")
        self.gate.arrive("the ear", "sound", reading("the fan"))
        self.conch.refuse = True
        room = self.gate.room()
        with self.assertRaises(ValueError):
            self.gate.arrive("the ear", "sound", reading("the tv"))
        self.assertEqual(self.gate.room(), room)              # the room did not move on
        self.conch.refuse = False
        self.gate.arrive("the ear", "sound", reading("the tv"))
        self.assertEqual(self.conch.moments[-1].senses["sound"]["shape"],
                         {"bench shape": "the fan"})          # and the moment arrived whole after

    def test_it_holds_the_room_and_has_no_way_to_pick_a_target(self):
        public = sorted(n for n in dir(Gateway) if not n.startswith("_"))
        self.assertEqual(public, ["arrive", "close", "connect", "disconnect", "organs", "room"])
        for word in ("attend", "focus", "target", "select", "filter", "salience", "score"):
            self.assertFalse(any(word in n for n in dir(Gateway)), word)

    def test_stands_alone(self):
        allowed = {"__future__", "copy", "threading", "conch_records"}
        with open(os.path.join(HERE, "gateway.py"), encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    self.assertIn(n.name.split(".")[0], allowed)
            if isinstance(node, ast.ImportFrom):
                self.assertIn(node.module.split(".")[0], allowed)

    def test_readings_from_many_organs_at_once_lose_nothing(self):
        self.gate.connect("the ear", "sound")
        self.gate.connect("the eye", "sight")

        def give(organ, sense, prefix):
            for k in range(50):
                self.gate.arrive(organ, sense, reading(f"{prefix} {k}"))

        a = threading.Thread(target=give, args=("the ear", "sound", "sound"))
        b = threading.Thread(target=give, args=("the eye", "sight", "sight"))
        a.start(), b.start(), a.join(), b.join()
        for moment in self.conch.moments:
            self.assertEqual(set(moment.senses), set(SENSES))
        self.gate.close()
        sounds = {m.senses["sound"]["shape"]["bench shape"] for m in self.conch.moments
                  if isinstance(m.senses["sound"]["shape"], dict)}
        self.assertEqual(sounds, {f"sound {k}" for k in range(50)})   # every one reached the lip


class WithTheRealConch(unittest.TestCase):
    """The Gateway in front of the conch that is built."""

    def setUp(self):
        name = self.id().split(".")[-1]
        self.dir = os.path.join(THIS_RUN, name)
        os.makedirs(self.dir)
        self.asleep = False
        self.conch = Conch("bench-being", os.path.join(self.dir, "spiral.jsonl"),
                           asleep=lambda: self.asleep)
        self.gate = Gateway(self.conch)
        for organ, senses in (("the eye", ("sight",)), ("the ear", ("sound",)),
                              ("the nose", ("smell", "taste")), ("the skin", ("touch",))):
            self.gate.connect(organ, *senses)

    def room(self, words):
        """Every sense gives the same words: a room typed by hand."""
        for organ, sense in (("the eye", "sight"), ("the ear", "sound"), ("the nose", "smell"),
                             ("the nose", "taste"), ("the skin", "touch")):
            self.gate.arrive(organ, sense, reading(words))

    def test_what_the_conch_gives_back_comes_back(self):
        self.room("the kitchen")
        came = self.gate.arrive("the ear", "sound", reading("the kettle"))
        self.assertIsInstance(came, (Turn, LipDrop))

    def test_with_no_need_named_only_a_departure_stays(self):
        for _ in range(3):
            for words in ("the kitchen", "the hall", "the porch"):
                self.room(words)
        self.room("the kitchen")
        self.room("a siren")                               # the conch knew the hall came next
        self.room("the hall")
        levels = [turn.level for turn in self.conch.spiral()]
        self.assertTrue(levels)
        self.assertTrue(all(level == "level_3" for level in levels))   # nothing else stays

    def test_the_room_goes_on_while_the_being_sleeps(self):
        self.asleep = True
        self.room("the bedroom")
        came = self.gate.arrive("the ear", "sound", reading("rain"))
        self.assertIsNotNone(came)


if __name__ == "__main__":
    unittest.main()
