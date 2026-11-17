"""
test_equilibrium.py: the center, tested forward.

    python3 -m unittest -v
"""

import ast
import json
import os
import tempfile
import time
import unittest

from equilibrium import CHAMBERS, Equilibrium


def bench():
    return Equilibrium("bench-being")


class TheCenter(unittest.TestCase):
    def test_equilibrium_belongs_to_one_being(self):
        with self.assertRaises(ValueError):
            Equilibrium("")

    def test_two_beings_never_share_a_center(self):
        a, b = Equilibrium("a"), Equilibrium("b")
        a.move(dx=1.0)
        self.assertEqual(a.from_center(), 1.0)
        self.assertEqual(b.from_center(), 0.0)

    def test_chambers_run_outward_skin_house_universe(self):
        self.assertEqual(CHAMBERS, ("skin", "house", "universe"))
        self.assertEqual(bench().status()["chambers"], CHAMBERS)

    def test_it_reads_its_words_from_one_source(self):
        self.assertIn("found", Equilibrium.canon())


class ItIsTheStatusAndNothingElse(unittest.TestCase):
    def test_it_judges_nothing_that_arrives(self):
        e = bench()
        for name in ("receive", "mark_by_hand", "plug_computation", "normal",
                     "readings", "lived", "expansions"):
            self.assertFalse(hasattr(e, name), name)

    def test_it_sends_the_conch_nothing(self):
        e = bench()
        self.assertFalse(hasattr(e, "tell_conch"))
        self.assertFalse(any("conch" in name for name in vars(e)))
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "equilibrium.py")) as f:
            code = "".join(line for line in f if not line.lstrip().startswith(("#", '"', "-")))
        self.assertNotIn("conch", code.split('"""')[-1].lower())

    def test_status_is_where_it_is(self):
        e = bench()
        e.move(dx=3.0, dz=4.0, turn=90)
        s = e.status()
        self.assertEqual(s["from_center"], 5.0)
        self.assertEqual(s["where"]["facing"], 90)
        self.assertFalse(s["asleep"])


class MovementIsConstant(unittest.TestCase):
    def test_silence_is_not_empty(self):
        e = bench()
        self.assertTrue(e.tick()["holding"])
        self.assertEqual(e.beats, 1)

    def test_it_keeps_ticking_through_sleep(self):
        e = bench()
        e.sleep()
        for _ in range(3):
            e.tick()
        self.assertTrue(e.last_beat["asleep"])
        self.assertEqual(e.darks[-1]["beats"], 4)

    def test_the_shaker_beats_by_itself_and_keeps_going_asleep(self):
        e = bench()
        e.start_shaker()
        try:
            time.sleep(1.2)
            self.assertGreaterEqual(e.beats, 2)
            e.sleep()
            time.sleep(1.2)
            self.assertTrue(e.shaker_running())
            self.assertGreaterEqual(e.darks[-1]["beats"], 2)
            self.assertGreaterEqual(e.wake()["held_through_the_dark"], 2)
        finally:
            e.stop_shaker()

    def test_waking_is_a_ramp(self):
        e = bench()
        e.sleep()
        e.tick()
        e.move(dx=2.0, by="the truck")
        woke = e.wake()
        self.assertEqual(woke["held_through_the_dark"], 2)
        self.assertEqual(len(woke["moved_in_the_dark"]), 1)
        self.assertFalse(e.asleep)

    def test_displacement_keeps_its_trajectory(self):
        e = bench()
        e.move(dx=3.0)
        e.move(dz=4.0, turn=90)
        self.assertEqual(len(e.trajectory), 2)
        self.assertEqual(e.from_center(), 5.0)
        self.assertEqual(e.position["facing"], 90)


class Clock:
    """A bench clock, so standing still for 1.2 seconds takes no real time."""
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def wait(self, seconds):
        self.t += seconds


def walked(clock=None, keep_at=None):
    clock = clock or Clock()
    return Equilibrium("bench-being", keep_at=keep_at, clock=clock), clock


class LearnedFromOneOrigin(unittest.TestCase):
    """The basis: EQUALLIB, port 9783. Size and distance learned from the center."""

    def test_bearing_is_a_compass_from_the_center(self):
        e, _ = walked()
        e.move(dx=2.0)
        self.assertEqual(e.status()["bearing"], 90.0)
        self.assertEqual(e.status()["bearing_name"], "E")
        e.move(dx=-2.0, dz=-3.0)
        self.assertEqual(e.status()["bearing_name"], "N")

    def test_facing_the_center_turns_toward_the_origin(self):
        e, _ = walked()
        e.move(dx=2.0)                      # east of the center
        e.face_center()
        self.assertEqual(e.position["facing"], 270.0)   # looking west, home
        self.assertEqual(e.trajectory[-1]["by"], "face_center")

    def test_being_born_at_the_center_is_not_a_lock(self):
        e, _ = walked()
        self.assertTrue(e.status()["locked"])
        self.assertIsNone(e.first_locked_at)

    def test_coming_back_to_the_center_locks(self):
        e, _ = walked()
        e.move(dx=1.5)
        self.assertFalse(e.status()["locked"])
        e.move(dx=-1.4)                     # 0.1 m out: inside the lock
        self.assertTrue(e.status()["locked"])
        self.assertIsNotNone(e.first_locked_at)

    def test_a_distance_is_learned_by_standing_on_it(self):
        e, clock = walked()
        e.move(dx=1.05)                     # on the 1 m ring
        clock.wait(1.0)
        e.tick()
        self.assertFalse(e.status()["known"][1])
        clock.wait(0.3)
        e.tick()
        self.assertTrue(e.status()["known"][1])

    def test_stepping_off_starts_the_ring_over(self):
        e, clock = walked()
        e.move(dx=2.0)
        clock.wait(1.0)
        e.move(dx=0.5)                      # off the ring
        e.move(dx=-0.5)                     # back on
        clock.wait(0.5)
        self.assertFalse(e.status()["known"][2])

    def test_time_before_a_step_is_not_counted_on_the_new_ring(self):
        e, clock = walked()
        e.move(dx=0.5)
        clock.wait(5.0)                     # stood between rings
        e.move(dx=0.5)                      # now on the 1 m ring
        self.assertFalse(e.status()["known"][1])

    def test_spatial_grammar_needs_the_lock_and_all_four(self):
        e, clock = walked()
        for _ in (1, 2, 3, 4):
            e.move(dx=1.0)
            clock.wait(1.25)                # past the threshold, as a real stand would be
            e.tick()
        self.assertTrue(all(e.status()["known"].values()))
        self.assertFalse(e.grammar_acquired())
        e.move(dx=-4.0)
        self.assertTrue(e.grammar_acquired())

    def test_marks_keep_distance_and_the_last_sixteen(self):
        e, _ = walked()
        e.move(dx=3.0, dz=-4.0)
        point = e.mark()
        self.assertEqual(point["from_center"], 5.0)
        for _ in range(20):
            e.mark()
        self.assertEqual(len(e.marks), 16)
        e.clear_last_mark()
        self.assertEqual(len(e.marks), 15)

    def test_what_is_learned_is_kept_across_a_restart(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bench-being.equilibrium.json")
            e, clock = walked(keep_at=path)
            e.move(dx=3.0)
            clock.wait(1.2)
            e.tick()
            e.mark()
            again, _ = walked(keep_at=path)
            self.assertTrue(again.status()["known"][3])
            self.assertEqual(len(again.marks), 1)

    def test_a_kept_file_that_cannot_be_read_stops_the_being(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "broken.json")
            with open(path, "w") as f:
                f.write("{not json")
            with self.assertRaises(json.JSONDecodeError):
                walked(keep_at=path)

    def test_another_beings_file_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "other.json")
            other = Equilibrium("other-being", keep_at=path, clock=Clock())
            other.mark()
            with self.assertRaises(ValueError):
                walked(keep_at=path)


class StandsAlone(unittest.TestCase):
    def test_standard_library_only(self):
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "equilibrium.py")) as f:
            tree = ast.parse(f.read())
        allowed = {"__future__", "os", "threading", "datetime", "json", "math", "time"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    self.assertIn(n.name.split(".")[0], allowed)
            if isinstance(node, ast.ImportFrom):
                self.assertIn(node.module.split(".")[0], allowed)


if __name__ == "__main__":
    unittest.main()
