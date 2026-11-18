"""
test_eye_reading.py: Lucent's measuring, rewritten for the 3C, held to Lucent's own tests.

    python3 -m unittest test_eye_reading -v

The cases are Lucent's (EverettNC/LUCENT b582a1d: geometry.test.ts, rhythm.test.ts,
reader.test.ts), carried over one for one. The six rhythm series carry the answers
behavior_capture.py itself gave on Everett's Mac (2026-10-29), as Lucent's test
wrote them down. Landmarks are made here; no picture of anyone is used.
"""

import json
import math
import re
import time
import unittest

import eye_reading as er

# ---- head pose ---------------------------------------------------------------------


def rotation(yaw, pitch, roll):
    """R = Rz(roll) Ry(yaw) Rx(pitch), as rows."""
    y, x, z = map(math.radians, (yaw, pitch, roll))
    rx = [[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]]
    ry = [[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]]
    rz = [[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]]

    def mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mul(mul(rz, ry), rx)


def matrix(r, t, layout):
    m = [[r[0][0], r[0][1], r[0][2], t[0]], [r[1][0], r[1][1], r[1][2], t[1]],
         [r[2][0], r[2][1], r[2][2], t[2]], [0, 0, 0, 1]]
    return [m[a][b] if layout == "row-major" else m[b][a] for a in range(4) for b in range(4)]


class HeadPose(unittest.TestCase):
    CASES = [(0, 0, 0), (25, 0, 0), (0, -15, 0), (0, 0, 30), (-35, 12, -8), (60, -40, 20)]

    def test_every_pose_comes_back_in_both_layouts(self):
        for layout in ("column-major", "row-major"):
            for yaw, pitch, roll in self.CASES:
                got = er.pose_from_matrix(matrix(rotation(yaw, pitch, roll), (1.5, -2, -45), layout))
                self.assertIsNotNone(got)
                self.assertEqual(got["layout"], layout)
                self.assertAlmostEqual(got["yaw_deg"], yaw, delta=1e-6)
                self.assertAlmostEqual(got["pitch_deg"], pitch, delta=1e-6)
                self.assertAlmostEqual(got["roll_deg"], roll, delta=1e-6)

    def test_a_matrix_that_is_not_a_rigid_transform_gives_no_pose(self):
        bad = list(range(1, 17))
        self.assertIsNone(er.matrix_layout(bad))
        self.assertIsNone(er.pose_from_matrix(bad))
        self.assertIsNone(er.pose_from_matrix([1, 0, 0]))


class Gaze(unittest.TestCase):
    def test_all_zeros_is_center(self):
        g = er.gaze_from_blendshapes({})
        self.assertEqual((g["cell"], g["horizontal"], g["vertical"]), ("center", 0, 0))

    def test_left_eye_out_and_right_eye_in_is_the_persons_own_left(self):
        g = er.gaze_from_blendshapes({"eyeLookOutLeft": 0.6, "eyeLookInRight": 0.6})
        self.assertEqual(g["cell"], "left")
        self.assertAlmostEqual(g["horizontal"], -0.6, delta=1e-9)

    def test_left_eye_in_and_right_eye_out_is_the_persons_own_right(self):
        self.assertEqual(er.gaze_from_blendshapes(
            {"eyeLookInLeft": 0.5, "eyeLookOutRight": 0.5})["cell"], "right")

    def test_up_is_top_and_down_is_bottom(self):
        self.assertEqual(er.gaze_from_blendshapes(
            {"eyeLookUpLeft": 0.5, "eyeLookUpRight": 0.5})["cell"], "top")
        self.assertEqual(er.gaze_from_blendshapes(
            {"eyeLookDownLeft": 0.4, "eyeLookDownRight": 0.4})["cell"], "bottom")

    def test_up_and_to_the_persons_right_is_top_right(self):
        self.assertEqual(er.gaze_from_blendshapes(
            {"eyeLookUpLeft": 0.5, "eyeLookUpRight": 0.5, "eyeLookInLeft": 0.5,
             "eyeLookOutRight": 0.5})["cell"], "top_right")

    def test_opposite_scores_cancel(self):
        self.assertEqual(er.gaze_from_blendshapes(
            {"eyeLookUpLeft": 0.5, "eyeLookUpRight": 0.5, "eyeLookDownLeft": 0.5,
             "eyeLookDownRight": 0.5})["cell"], "center")

    def test_just_under_the_step_stays_center_at_the_step_moves(self):
        s = er.GAZE_SCORE_STEP
        self.assertEqual(er.gaze_from_blendshapes(
            {"eyeLookOutLeft": s - 0.001, "eyeLookInRight": s - 0.001})["cell"], "center")
        self.assertEqual(er.gaze_from_blendshapes(
            {"eyeLookOutLeft": s, "eyeLookInRight": s})["cell"], "left")

    def test_names_all_nine_of_alphavoxs_cells(self):
        s = er.GAZE_SCORE_STEP
        pairs = [(-s, s), (0, s), (s, s), (-s, 0), (0, 0), (s, 0), (-s, -s), (0, -s), (s, -s)]
        self.assertEqual([er.gaze_cell(h, v) for h, v in pairs], list(er.GAZE_CELLS))


def placed(points):
    """A landmark list with only the named indices placed; the rest None."""
    out = [None] * (max(points) + 1)
    for i, (x, y) in points.items():
        out[i] = [x, y, 0.0]
    return out


def eyes(iris_at, lid_gap):
    pts = {}
    for name, x0 in (("image_left", 0.3), ("image_right", 0.6)):
        e = er.EYE_INDICES[name]
        pts[e["corners"][0]] = (x0, 0.4)
        pts[e["corners"][1]] = (x0 + 0.1, 0.4)
        pts[e["lids"][0]] = (x0 + 0.05, 0.4 - lid_gap / 2)
        pts[e["lids"][1]] = (x0 + 0.05, 0.4 + lid_gap / 2)
        pts[e["iris"]] = (x0 + 0.1 * iris_at, 0.4)
    return placed(pts)


class Iris(unittest.TestCase):
    def test_iris_in_the_middle_of_an_open_eye_is_center_and_open(self):
        r = er.iris_from_landmarks(eyes(0.5, 0.04), 1000, 1000)
        self.assertAlmostEqual(r["iris_ratio"], 0.5, delta=1e-9)
        self.assertEqual((r["horizontal"], r["closed"]), ("center", False))

    def test_iris_toward_the_images_right_is_the_persons_own_left(self):
        self.assertEqual(er.iris_from_landmarks(eyes(0.8, 0.04), 1000, 1000)["horizontal"], "left")
        self.assertEqual(er.iris_from_landmarks(eyes(0.2, 0.04), 1000, 1000)["horizontal"], "right")

    def test_a_lid_gap_under_a_fifth_of_eye_width_reads_closed(self):
        self.assertIs(er.iris_from_landmarks(eyes(0.5, 0.015), 1000, 1000)["closed"], True)

    def test_with_no_eye_landmarks_nothing_is_guessed(self):
        r = er.iris_from_landmarks([], 1000, 1000)
        self.assertEqual((r["iris_ratio"], r["horizontal"], r["closed"]), (None, None, None))


class Mouth(unittest.TestCase):
    def test_lip_gap_and_width_over_face_height(self):
        m = er.MOUTH_INDICES
        lm = placed({m["forehead_top"]: (0.5, 0.2), m["chin"]: (0.5, 0.8),
                     m["upper_inner"]: (0.5, 0.65), m["lower_inner"]: (0.5, 0.71),
                     m["corner_a"]: (0.44, 0.68), m["corner_b"]: (0.56, 0.68)})
        r = er.mouth_from_landmarks(lm, 640, 640)
        self.assertAlmostEqual(r["open"], 0.1, delta=1e-9)
        self.assertAlmostEqual(r["width"], 0.2, delta=1e-9)

    def test_nothing_without_a_face_height(self):
        self.assertEqual(er.mouth_from_landmarks([], 640, 480), {"open": None, "width": None})


class Blinks(unittest.TestCase):
    def test_a_blink_is_the_closed_to_open_edge_and_the_rate_is_counted(self):
        b = er.BlinkLog(60_000)
        self.assertIsNone(b.update(0, False))
        self.assertIsNone(b.update(100, True))
        self.assertIsNone(b.update(150, True))
        self.assertEqual(b.update(220, False), {"start": 100, "end": 220, "duration_ms": 120})
        b.update(1000, True)
        b.update(1100, False)
        self.assertEqual(len(b.recent()), 2)
        self.assertEqual(b.per_minute(), 2)
        b.update(70_000, False)
        self.assertEqual(len(b.recent()), 0)

    def test_a_frame_with_no_eyes_read_neither_starts_nor_ends_a_blink(self):
        b = er.BlinkLog()
        b.update(0, True)
        b.update(50, None)
        self.assertIsNone(b.update(100, False))


# ---- rhythm --------------------------------------------------------------------------

FRAME_MS = 1000 / 30


def even_times(n):
    return [i * FRAME_MS for i in range(n)]


def spikes(n, at, height=0.2):
    v = [0.0] * n
    for i in at:
        v[i] = height
    return v


# The answers behavior_capture.py's _find_repetitive_patterns gave, copied unchanged and
# run with numpy 2.4.6 and fps 30 on Everett's Mac (2026-10-29), as Lucent wrote them.
ORIGINAL = {
    "triangle_period_15": (2.0, 1.0, 7),
    "steady_spikes": (1.9626168224299065, 0.9326065182156263, 8),
    "irregular_spikes": None, "too_short": None, "two_peaks": None, "flat": None,
}
SERIES = {
    "triangle_period_15": [0.01 * (i % 15) for i in range(120)],
    "steady_spikes": spikes(120, [10, 25, 41, 55, 72, 86, 101, 117]),
    "irregular_spikes": spikes(120, [5, 9, 30, 33, 70, 100]),
    "too_short": [0.01 * (i % 15) for i in range(59)],
    "two_peaks": spikes(120, [20, 80]),
    "flat": [0.01] * 120,
}


class TheBehaviorCaptureMath(unittest.TestCase):
    def test_gives_the_originals_answer_on_all_six_series(self):
        for name, values in SERIES.items():
            got = er.find_repetition(values, even_times(len(values)))
            want = ORIGINAL[name]
            if want is None:
                self.assertIsNone(got, name)
                continue
            frequency, consistency, count = want
            self.assertIsNotNone(got, name)
            self.assertEqual(got["peaks"], count, name)
            self.assertAlmostEqual(got["peaks_per_second"], frequency, delta=1e-9, msg=name)
            self.assertAlmostEqual(got["steadiness"], consistency, delta=1e-9, msg=name)

    def test_gaps_are_measured_by_each_frames_own_time(self):
        values = [0.3 if i % 10 == 5 else 0.0 for i in range(100)]
        r = er.find_repetition(values, [i * 20 for i in range(100)])
        self.assertEqual((r["mean_interval_ms"], r["peaks_per_second"],
                          r["mean_interval_samples"]), (200, 5, 10))

    def test_values_and_times_of_different_lengths_are_refused_loudly(self):
        with self.assertRaisesRegex(ValueError, "2 values but 1 times"):
            er.find_repetition([0, 1], [0])


W, H = 640, 480


def face(dx=0.0, dy=0.0, jaw=0.0):
    pts = [[0.5 + dx, 0.5 + dy, 0.0] for _ in range(478)]
    pts[10] = [0.5 + dx, 0.3 + dy, 0.0]
    pts[1] = [0.5 + dx, 0.5 + dy, 0.0]
    pts[152] = [0.5 + dx, 0.65 + dy + jaw, 0.0]
    pts[234] = [0.4 + dx, 0.5 + dy, 0.0]
    pts[454] = [0.6 + dx, 0.5 + dy, 0.0]
    return pts


def hand(cx, cy):
    return [[cx + (i % 5) * 0.01, cy - (i // 5) * 0.02, 0.0] for i in range(21)]


class Parts(unittest.TestCase):
    def test_the_head_is_measured_in_face_heights(self):
        a, b = er.head_shape(face(), W, H), er.head_shape(face(0.05, 0), W, H)
        self.assertAlmostEqual(er.part_movement(a, b), 32 / 168, delta=1e-12)

    def test_a_still_jaw_is_not_moving_when_the_whole_head_moves(self):
        a = er.jaw_shape(face(), W, H)
        self.assertLess(er.part_movement(a, er.jaw_shape(face(0.1, 0.05), W, H)), 1e-12)
        self.assertGreater(er.part_movement(a, er.jaw_shape(face(0, 0, 0.02), W, H)), 0)

    def test_a_hand_is_measured_in_hand_lengths(self):
        a, b = er.hand_shape(hand(0.3, 0.6), W, H), er.hand_shape(hand(0.3, 0.62), W, H)
        self.assertGreater(er.part_movement(a, b), 0)
        self.assertIsNone(er.hand_shape(hand(0.3, 0.6)[:20], W, H))

    def test_shoulders_only_when_both_are_seen_above_half(self):
        pose = [[0.5, 0.5, 0.0] for _ in range(33)]
        pose[11], pose[12] = [0.4, 0.7, 0.0], [0.6, 0.7, 0.0]
        vis = [0.9] * 33
        self.assertIsNotNone(er.shoulder_shape(pose, vis, W, H))
        vis[12] = 0.4
        self.assertIsNone(er.shoulder_shape(pose, vis, W, H))

    def test_which_side_a_hand_is_on(self):
        s = er.hand_sides([hand(0.7, 0.6), hand(0.2, 0.6)], 0.5)
        self.assertEqual((s["left"][0][0], s["right"][0][0]), (0.2, 0.7))
        self.assertIsNone(er.hand_sides([hand(0.3, 0.6)], 0.5)["right"])
        self.assertIsNone(er.hand_sides([hand(0.3, 0.6)], 0.2)["left"])
        self.assertEqual(er.hand_sides([], 0.5), {"left": None, "right": None})


def frames(seconds, hz, start=0.0):
    out = []
    for i in range(int(seconds * 30)):
        t = start + i * FRAME_MS
        y = 0.6 + 0.08 * math.sin(2 * math.pi * hz * (t / 1000))
        out.append((t, {"head": er.head_shape(face(), W, H), "jaw": er.jaw_shape(face(), W, H),
                        "hand_image_right": er.hand_shape(hand(0.3, y), W, H)}))
    return out


class RhythmPerPart(unittest.TestCase):
    def test_names_the_part_that_repeats_and_only_that_part(self):
        r = er.RhythmTracker()
        began = []
        for t, parts in frames(5, 1.4):
            began += [e["part"] for e in r.update(t, parts)["began"]]
        self.assertEqual(began, ["hand_image_right"])
        p = {x["part"]: x for x in r.parts()}
        rep = p["hand_image_right"]["repetition"]
        self.assertAlmostEqual(rep["peaks_per_second"], 2.8, delta=0.3)
        self.assertGreater(rep["steadiness"], 0.7)
        self.assertIsNone(p["head"]["repetition"])
        self.assertIsNone(p["jaw"]["repetition"])
        self.assertEqual((p["hand_image_left"]["samples"], p["shoulders"]["samples"]), (0, 0))
        self.assertEqual(r.repeating(), ["hand_image_right"])

    def test_a_rhythm_carries_its_local_time_and_closes_when_the_part_leaves(self):
        r = er.RhythmTracker()
        t0 = time.mktime((2026, 10, 27, 14, 30, 0, 0, 0, -1)) * 1000   # a Tuesday, 2:30 pm here
        for t, parts in frames(5, 1.4, t0):
            r.update(t, parts)
        opened = [e for e in r.recent() if e["part"] == "hand_image_right"][0]
        self.assertIsNone(opened["end"])
        self.assertEqual(opened["start_local"]["weekday"], "Tuesday")
        self.assertEqual(opened["start_local"]["date"], "2026-10-27")
        self.assertTrue(opened["start_local"]["time"].startswith("14:30:0"))
        self.assertEqual(opened["start_local"]["minute_of_day"], 14 * 60 + 30)
        gone = t0 + 5000 + er.MAX_GAP_MS + 100
        ended = r.update(gone, {"head": er.head_shape(face(), W, H)})["ended"]
        self.assertEqual([e["part"] for e in ended], ["hand_image_right"])
        self.assertEqual(ended[0]["end"], gone)
        self.assertEqual({x["part"]: x["samples"] for x in r.parts()}["hand_image_right"], 0)
        self.assertEqual(r.repeating(), [])

    def test_says_nothing_about_what_a_movement_means(self):
        r = er.RhythmTracker()
        for t, parts in frames(5, 1.4):
            r.update(t, parts)
        text = json.dumps({"parts": r.parts(), "events": r.recent()}).lower()
        for word in ("tic", "stim", "stress", "happy", "sad", "angry", "fear", "thirst",
                     "hungry", "sugar", "means", "meaning"):
            self.assertIsNone(re.search(r"\b%s\b" % word, text), word)


class LocalTime(unittest.TestCase):
    def test_reads_this_machines_own_clock(self):
        t = time.mktime((2026, 1, 4, 6, 5, 9, 0, 0, -1)) * 1000
        s = er.local_stamp(t)
        self.assertEqual((s["date"], s["time"], s["weekday"], s["minute_of_day"]),
                         ("2026-01-04", "06:05:09", "Sunday", 365))
        self.assertEqual(s["utc_offset_min"], time.localtime(t / 1000).tm_gmtoff // 60)


class StandsAlone(unittest.TestCase):
    def test_only_the_standard_library(self):
        import ast
        import os
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "eye_reading.py"),
                  encoding="utf-8") as f:
            tree = ast.parse(f.read())
        names = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                names |= {n.name.split(".")[0] for n in node.names}
            if isinstance(node, ast.ImportFrom):
                names.add(node.module.split(".")[0])
        self.assertTrue(names <= {"__future__", "math", "os", "time"}, names)


if __name__ == "__main__":
    unittest.main()
