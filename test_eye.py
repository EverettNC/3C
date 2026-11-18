"""
test_eye.py: the 3C's eye, tested forward.

    python3 -m unittest test_eye -v

Landmarks are made here, as Lucent's own tests make them; no picture or
recording of anyone is used. A test that needs mediapipe or the camera, and this
Python does not have it, is skipped with the reason; it never counts as a pass.
Files written here go into test_spirals/, beside this file, and nothing is deleted.
"""

import ast
import json
import math
import os
import unittest
from datetime import datetime, timezone

import eye
import eye_reading as er
from conch import Conch
from conch_records import QUIET, LipDrop, Turn
from eye import Eye, Landmarks
from gateway import Gateway

HERE = os.path.dirname(os.path.abspath(__file__))
THIS_RUN = os.path.join(HERE, "test_spirals", "eye-"
                        + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
                        + "-" + str(os.getpid()))
FRAME_MS = 1000 / 30
W, H = 640, 480
T0 = 1_790_000_000_000.0          # a fixed start, epoch ms

LOOKS = {"center": {}, "left": {"eyeLookOutLeft": 0.6, "eyeLookInRight": 0.6},
         "right": {"eyeLookInLeft": 0.6, "eyeLookOutRight": 0.6}}


def a_face(look="center", closed=False, dx=0.0):
    pts = [[0.5 + dx, 0.5, 0.0] for _ in range(478)]
    pts[10], pts[1] = [0.5 + dx, 0.3, 0.0], [0.5 + dx, 0.5, 0.0]
    pts[152], pts[234], pts[454] = [0.5 + dx, 0.65, 0.0], [0.4 + dx, 0.5, 0.0], [0.6 + dx, 0.5, 0.0]
    gap = 0.015 if closed else 0.04
    for name, x0 in (("image_left", 0.35 + dx), ("image_right", 0.55 + dx)):
        e = er.EYE_INDICES[name]
        pts[e["corners"][0]], pts[e["corners"][1]] = [x0, 0.4, 0.0], [x0 + 0.1, 0.4, 0.0]
        pts[e["lids"][0]] = [x0 + 0.05, 0.4 - gap / 2, 0.0]
        pts[e["lids"][1]] = [x0 + 0.05, 0.4 + gap / 2, 0.0]
        pts[e["iris"]] = [x0 + 0.05, 0.4, 0.0]
    # The face model always gives its blendshape scores; a face with none gives no gaze.
    shapes = {"eyeBlinkLeft": 0.0, "eyeBlinkRight": 0.0, "jawOpen": 0.0}
    shapes.update(LOOKS[look])
    return {"landmarks": pts, "blendshapes": shapes, "matrix": None}


def a_hand(cx, cy):
    return {"landmarks": [[cx + (i % 5) * 0.01, cy - (i // 5) * 0.02, 0.0] for i in range(21)],
            "model_handedness": "Left", "handedness_score": 0.9}


def frame(faces=(), hands=(), bodies=()):
    return {"caught": True, "why": None, "frame_w": W, "frame_h": H,
            "faces": list(faces), "hands": list(hands), "bodies": list(bodies),
            "parts": {"face": {"available": True, "reason": None}}}


class Recording(Gateway):
    """The real Gateway, with each reading the eye gave written down."""

    def __init__(self, conch):
        super().__init__(conch)
        self.given = []

    def arrive(self, organ, sense, reading):
        self.given.append(reading)
        return super().arrive(organ, sense, reading)


class Catches:
    def __init__(self):
        self.moments = []

    def take_in(self, moment):
        self.moments.append(moment)
        return "taken"


class Seeing(unittest.TestCase):
    def setUp(self):
        self.gate = Recording(Catches())
        self.eye = Eye(self.gate)
        self.i = 0
        self.when = []                       # the time each reading was given

    def run_frames(self, n, **what):
        for _ in range(n):
            t = T0 + self.i * FRAME_MS
            before = len(self.gate.given)
            self.eye.see(frame(**what), t)
            if len(self.gate.given) > before:
                self.when.append(t)
            self.i += 1

    def shapes(self):
        return [g["shape"] for g in self.gate.given]

    def test_nobody_in_view_is_given_once_and_says_so(self):
        self.run_frames(30)
        self.assertEqual(self.shapes(), [{"faces": 0, "looking": None, "eyes": None, "hands": [],
                                          "body": False, "repeating": []}])

    def test_a_face_is_there_at_once_and_its_look_counts_after_80_ms(self):
        self.run_frames(10, faces=[a_face("center")])
        s = self.shapes()
        self.assertEqual(len(s), 2)
        self.assertEqual((s[0]["faces"], s[0]["looking"], s[0]["eyes"]), (1, None, "open"))
        self.assertEqual(s[1]["looking"], "center")
        self.assertGreaterEqual(self.when[1] - self.when[0], eye.LOOK_HOLD_MS)

    def test_a_glance_shorter_than_80_ms_is_not_a_look(self):
        self.run_frames(9, faces=[a_face("center")])
        self.run_frames(2, faces=[a_face("left")])          # 67 ms of left
        self.run_frames(9, faces=[a_face("center")])
        self.assertEqual([x["looking"] for x in self.shapes()], [None, "center"])
        self.run_frames(5, faces=[a_face("left")])          # held: now it is a look
        self.assertEqual(self.shapes()[-1]["looking"], "left")

    def test_a_blink_is_counted_and_never_reads_closed(self):
        self.run_frames(9, faces=[a_face("center")])
        self.run_frames(9, faces=[a_face("center", closed=True)])     # 300 ms: a blink
        self.run_frames(3, faces=[a_face("center")])
        self.assertNotIn("closed", [x["eyes"] for x in self.shapes()])
        self.run_frames(5, faces=[a_face("left")])                    # something else changes
        self.assertEqual(len(self.gate.given[-1]["gave"]["blinks"]["recent"]), 1)

    def test_eyes_closed_past_400_ms_read_closed(self):
        self.run_frames(9, faces=[a_face("center")])
        self.run_frames(15, faces=[a_face("center", closed=True)])    # 500 ms
        self.assertEqual(self.shapes()[-1]["eyes"], "closed")
        closed_at = self.when[-1]
        self.assertGreater(closed_at - (T0 + 9 * FRAME_MS), eye.CLOSED_PAST_MS)

    def test_a_face_that_leaves_is_gone_only_after_500_ms(self):
        self.run_frames(30, faces=[a_face("center")])
        last_seen = T0 + 29 * FRAME_MS
        self.run_frames(30)
        self.assertEqual(self.shapes()[-1]["faces"], 0)
        self.assertEqual((self.shapes()[-1]["looking"], self.shapes()[-1]["eyes"]), (None, None))
        self.assertGreater(self.when[-1] - last_seen, eye.GONE_AFTER_MS)

    def test_a_dropped_frame_does_not_end_a_face(self):
        self.run_frames(10, faces=[a_face("center")])
        given = len(self.gate.given)
        self.run_frames(3)                                            # 100 ms unseen
        self.run_frames(5, faces=[a_face("center")])
        self.assertEqual(len(self.gate.given), given)

    def test_hands_go_by_image_side(self):
        self.run_frames(5, hands=[a_hand(0.2, 0.6), a_hand(0.7, 0.6)])
        self.assertEqual(self.shapes()[-1]["hands"], ["image_left", "image_right"])
        self.run_frames(30, hands=[a_hand(0.7, 0.6)])
        self.assertEqual(self.shapes()[-1]["hands"], ["image_right"])

    def test_a_movement_that_repeats_is_given_by_its_part(self):
        for _ in range(150):                                          # 5 s at 1.4 a second
            t = T0 + self.i * FRAME_MS
            y = 0.6 + 0.08 * math.sin(2 * math.pi * 1.4 * (t - T0) / 1000)
            self.run_frames(1, hands=[a_hand(0.7, y)])
        self.assertIn(["hand_image_right"], [x["repeating"] for x in self.shapes()])
        events = self.gate.given[-1]["gave"]["rhythm"]["events"]
        self.assertEqual([e["part"] for e in events], ["hand_image_right"])
        self.assertIn("weekday", events[0]["start_local"])

    def test_the_shape_holds_no_measurement_and_what_was_given_does(self):
        f = a_face("center")
        r = [[math.cos(math.radians(20)), 0, math.sin(math.radians(20))], [0, 1, 0],
             [-math.sin(math.radians(20)), 0, math.cos(math.radians(20))]]
        f["matrix"] = [r[0][0], r[0][1], r[0][2], 0, r[1][0], r[1][1], r[1][2], 0,
                       r[2][0], r[2][1], r[2][2], -45, 0, 0, 0, 1]
        f["blendshapes"]["eyeBlinkLeft"] = 0.05
        self.run_frames(10, faces=[f])
        reading = self.gate.given[-1]
        self.assertEqual(set(reading["shape"]),
                         {"faces", "looking", "eyes", "hands", "body", "repeating"})
        face = reading["gave"]["faces"][0]
        self.assertAlmostEqual(face["pose"]["yaw_deg"], 20, delta=0.01)
        self.assertEqual(len(face["lips"]), 40)
        self.assertIn("minute_of_day", reading["gave"]["local"])
        self.assertTrue(reading["organ_clock"].startswith("the eye "))

    def test_no_feeling_and_no_meaning_in_anything_given(self):
        for _ in range(150):
            t = T0 + self.i * FRAME_MS
            y = 0.6 + 0.08 * math.sin(2 * math.pi * 1.4 * (t - T0) / 1000)
            self.run_frames(1, faces=[a_face("center")], hands=[a_hand(0.7, y)])
        text = json.dumps(self.gate.given).lower()
        for word in ("happy", "sad", "angry", "scared", "fear", "emotion", "feeling", "stim",
                     "stress", "hungry", "thirst", "means", "meaning"):
            self.assertNotIn('"' + word, text, word)
            self.assertNotIn(" " + word + " ", text, word)

    def test_a_frame_not_caught_is_refused_loudly(self):
        with self.assertRaisesRegex(ValueError, "not caught"):
            self.eye.see({"caught": False, "why": "mediapipe is not installed"}, T0)


class TheModelsAndTheCamera(unittest.TestCase):
    def test_no_models_where_they_were_looked_for_is_said(self):
        lm = Landmarks(model_dir=os.path.join(THIS_RUN, "nowhere"))
        self.assertFalse(lm.available)
        self.assertIn("not found", lm.why_not)

    def test_a_model_that_does_not_match_lucents_bytes_is_not_used(self):
        place = os.path.join(THIS_RUN, "wrong-models")
        os.makedirs(place, exist_ok=True)
        for name in eye.MODEL_SUMS:
            with open(os.path.join(place, name), "wb") as f:
                f.write(b"not the model")
        lm = Landmarks(model_dir=place)
        self.assertIn("does not match Lucent's SHA256SUMS", lm.why_not)
        self.assertEqual(lm.catch(None, T0), {"caught": False, "why": lm.why_not})

    def test_without_mediapipe_the_reason_is_given(self):
        place = next((p for p in eye.MODEL_PLACES if p and os.path.isdir(p)), None)
        if place is None:
            self.skipTest("Lucent's models are not on this machine")
        try:
            import mediapipe  # noqa: F401
            self.skipTest("mediapipe is installed in this Python")
        except ImportError:
            pass
        self.assertIn("mediapipe is not installed", Landmarks().why_not)

    def test_the_camera_is_not_pretended(self):
        the_eye = Eye(Gateway(Catches()))
        with self.assertRaisesRegex(RuntimeError, "cannot see"):
            the_eye.look()


class WithTheRealConch(unittest.TestCase):
    def test_what_the_eye_gives_reaches_the_conch_whole(self):
        path = os.path.join(THIS_RUN, "with-the-conch", "spiral.jsonl")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        conch = Conch("bench-being", path)
        gate = Gateway(conch)
        the_eye = Eye(gate)
        came = []
        for i in range(20):
            came += the_eye.see(frame(faces=[a_face("center")]), T0 + i * FRAME_MS)
        for i in range(20, 40):
            came += the_eye.see(frame(), T0 + i * FRAME_MS)
        gate.close()
        self.assertTrue(came)
        self.assertTrue(all(isinstance(c, (Turn, LipDrop)) for c in came))
        sights = [item.moment.senses["sight"]["shape"] for item in conch.hand_over()]
        self.assertIn(QUIET, sights)
        self.assertTrue(any(isinstance(s, dict) and s["looking"] == "center" for s in sights))


class StandsAlone(unittest.TestCase):
    def test_only_the_standard_library_at_the_top(self):
        allowed = {"__future__", "hashlib", "math", "os", "sys", "threading", "time",
                   "eye_reading", "conch_records"}
        with open(os.path.join(HERE, "eye.py"), encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.Import):
                for n in node.names:
                    self.assertIn(n.name.split(".")[0], allowed)
            if isinstance(node, ast.ImportFrom):
                self.assertIn(node.module.split(".")[0], allowed)


if __name__ == "__main__":
    unittest.main()
