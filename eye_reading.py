"""
eye_reading.py: Lucent's measuring, rewritten for the 3C.

Source: EverettNC/LUCENT b582a1d (2026-11-06), src/lib/reader/geometry.ts,
rhythm.ts and time.ts, read line by line on 17 Nov 2026. Every number here is
Lucent's, named where Lucent says it came from. None is fitted to anyone; each is
held until client data replaces it.

Numbers and directions only. Nothing in this file names a feeling, and nothing
here says what a movement means. A meaning is learned for one client by the
being that serves them; none is built in.

Landmarks are [x, y, z] normalized to the frame, as MediaPipe gives them. A
landmark list may hold None where a point was not given. The frame is raw (not
mirrored), as in Lucent.

Standard library only.
"""

from __future__ import annotations

import math
import os
import time

# ---- head pose from the facial transformation matrix (geometry.ts) ---------------


def matrix_layout(data):
    """MediaPipe gives the 4x4 pose of its canonical face as 16 numbers without
    saying the order. A rigid transform's bottom row is 0 0 0 1, so the layout is
    read from where the zeros sit. If neither holds, it is not a rigid transform."""
    if len(data) != 16:
        return None
    near0 = lambda v: abs(v) < 1e-6
    if abs(data[15] - 1) >= 1e-6:
        return None
    if near0(data[3]) and near0(data[7]) and near0(data[11]):
        return "column-major"
    if near0(data[12]) and near0(data[13]) and near0(data[14]):
        return "row-major"
    return None


def rotation_rows(data, layout):
    def at(row, col):
        return data[col * 4 + row] if layout == "column-major" else data[row * 4 + col]
    return [[at(r, c) for c in range(3)] for r in range(3)]


def pose_from_matrix(data):
    """Yaw, pitch and roll in degrees, taken in the order R = Rz(roll) Ry(yaw) Rx(pitch),
    on MediaPipe's camera axes (x right, y up, z toward the camera). None when the
    matrix is not a rigid transform."""
    layout = matrix_layout(data)
    if layout is None:
        return None
    r = rotation_rows(data, layout)
    s = max(-1.0, min(1.0, -r[2][0]))
    deg = 180 / math.pi
    return {"yaw_deg": math.asin(s) * deg,
            "pitch_deg": math.atan2(r[2][1], r[2][2]) * deg,
            "roll_deg": math.atan2(r[1][0], r[0][0]) * deg,
            "layout": layout}


# ---- gaze (geometry.ts; AlphaVox's nine regions, real_eye_tracking.py) -----------

GAZE_CELLS = ("top_left", "top", "top_right", "left", "center", "right",
              "bottom_left", "bottom", "bottom_right")

# A net eye-look score at or above this moves the cell off center. Lucent's chosen
# starting value: a fifth of the 0 to 1 range, so small drift stays "center".
GAZE_SCORE_STEP = 0.2


def gaze_cell(horizontal, vertical, step=GAZE_SCORE_STEP):
    h = "right" if horizontal >= step else "left" if horizontal <= -step else ""
    v = "top" if vertical >= step else "bottom" if vertical <= -step else ""
    if not h and not v:
        return "center"
    if not v:
        return h
    if not h:
        return v
    return v + "_" + h


def gaze_from_blendshapes(b, step=GAZE_SCORE_STEP):
    """Gaze from the eye-look blendshapes. The names follow ARKit: Left/Right are the
    person's own sides. Horizontal is positive toward the person's own right, vertical
    positive up. Lucent's own note: not yet checked against a live face turning to one
    known side."""
    def g(name):
        v = b.get(name)
        return v if isinstance(v, (int, float)) and math.isfinite(v) else 0.0
    toward_own_left = (g("eyeLookOutLeft") + g("eyeLookInRight")) / 2
    toward_own_right = (g("eyeLookInLeft") + g("eyeLookOutRight")) / 2
    up = (g("eyeLookUpLeft") + g("eyeLookUpRight")) / 2
    down = (g("eyeLookDownLeft") + g("eyeLookDownRight")) / 2
    horizontal = toward_own_right - toward_own_left
    vertical = up - down
    return {"horizontal": horizontal, "vertical": vertical,
            "cell": gaze_cell(horizontal, vertical, step)}


# ---- iris and eye opening (geometry.ts; AlphaVox facial_gesture_service.py) -------

# "image_left" is the eye that appears on the left of the raw camera image.
EYE_INDICES = {
    "image_left": {"corners": (33, 133), "lids": (159, 145), "iris": 468},
    "image_right": {"corners": (362, 263), "lids": (386, 374), "iris": 473},
}
# The middle sixth reads as center, so small iris jitter does not flip the side.
IRIS_CENTER_LOW = 0.42
IRIS_CENTER_HIGH = 0.58
# Lid gap over eye width below which an eye reads as closed (Soukupova and Cech 2016,
# two-point form, as AlphaVox chose it).
EYE_CLOSED_RATIO = 0.2


def _point(lm, i):
    return lm[i] if 0 <= i < len(lm) else None


def iris_from_landmarks(lm, frame_w, frame_h):
    def px(i):
        p = _point(lm, i)
        return None if p is None else (p[0] * frame_w, p[1] * frame_h)
    per_eye = {}
    for name in ("image_left", "image_right"):
        idx = EYE_INDICES[name]
        a, b = px(idx["corners"][0]), px(idx["corners"][1])
        top, bottom = px(idx["lids"][0]), px(idx["lids"][1])
        iris = px(idx["iris"])
        if None in (a, b, top, bottom, iris):
            per_eye[name] = {"iris_ratio": None, "openness": None}
            continue
        width = math.hypot(b[0] - a[0], b[1] - a[1])
        left_x = min(a[0], b[0])
        span = max(a[0], b[0]) - left_x
        per_eye[name] = {
            "iris_ratio": (iris[0] - left_x) / span if span > 0 else None,
            "openness": (math.hypot(bottom[0] - top[0], bottom[1] - top[1]) / width
                         if width > 0 else None),
        }
    ratios = [e["iris_ratio"] for e in per_eye.values() if e["iris_ratio"] is not None]
    opens = [e["openness"] for e in per_eye.values() if e["openness"] is not None]
    ratio = sum(ratios) / len(ratios) if ratios else None
    return {"iris_ratio": ratio, "per_eye": per_eye,
            "horizontal": iris_horizontal(ratio),
            "closed": (max(opens) < EYE_CLOSED_RATIO) if opens else None}


def iris_horizontal(ratio):
    """The frame is raw, so an iris toward the image's right is the person looking to
    their own left (AlphaVox's rule)."""
    if ratio is None:
        return None
    if ratio > IRIS_CENTER_HIGH:
        return "left"
    if ratio < IRIS_CENTER_LOW:
        return "right"
    return "center"


# ---- mouth (geometry.ts; chin 152 as the bottom of the face: PhotoTruth) ---------

MOUTH_INDICES = {"upper_inner": 13, "lower_inner": 14, "corner_a": 61, "corner_b": 291,
                 "forehead_top": 10, "chin": 152}
# The 40 lip landmarks of Face Mesh (outer then inner contour), kept for a lip reader.
LIP_INDICES = (61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0,
               37, 39, 40, 185, 78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415,
               310, 311, 312, 13, 82, 81, 80, 191)


def mouth_from_landmarks(lm, frame_w, frame_h):
    """Inner lip gap and corner-to-corner width, each over face height (forehead 10 to
    chin 152). No open-or-closed rule: Lucent has none."""
    def d(i, j):
        a, b = _point(lm, i), _point(lm, j)
        if a is None or b is None:
            return None
        return math.hypot((a[0] - b[0]) * frame_w, (a[1] - b[1]) * frame_h)
    m = MOUTH_INDICES
    face = d(m["forehead_top"], m["chin"])
    if not face or face <= 0:
        return {"open": None, "width": None}
    gap = d(m["upper_inner"], m["lower_inner"])
    width = d(m["corner_a"], m["corner_b"])
    return {"open": None if gap is None else gap / face,
            "width": None if width is None else width / face}


def lips(lm):
    return [list(lm[i]) for i in LIP_INDICES if _point(lm, i) is not None]


# ---- blinks (time.ts; AlphaVox's eye-opening rule) --------------------------------

class BlinkLog:
    """Closed-to-open edges of the eyes, from a per-frame "closed" reading. Keeps the
    blinks of the last window and the rate over it."""

    def __init__(self, window_ms=60_000):
        self.window_ms = window_ms
        self._closed_since = None
        self._events = []

    def update(self, t, closed):
        ended = None
        if closed is True and self._closed_since is None:
            self._closed_since = t
        if closed is False and self._closed_since is not None:
            ended = {"start": self._closed_since, "end": t, "duration_ms": t - self._closed_since}
            self._events.append(ended)
            self._closed_since = None
        if closed is None:
            self._closed_since = None
        cutoff = t - self.window_ms
        self._events = [e for e in self._events if e["end"] >= cutoff]
        return ended

    def recent(self, n=10):
        return [dict(e) for e in self._events[-n:]]

    def per_minute(self):
        return len(self._events) * 60_000 / self.window_ms

    def clear(self):
        self._closed_since = None
        self._events = []


# ---- rhythm (rhythm.ts; AlphaVox behavior_capture.py, from Everett's notebooks) ---

RHYTHM_WINDOW = 120         # samples kept per part: "4 seconds at 30fps"
RHYTHM_MIN_SAMPLES = 60     # judged only from two seconds on
PEAK_ABOVE_MEAN = 0.02      # MOVEMENT_THRESHOLD, here in the part's own size per frame
MIN_PEAKS = 3               # two peaks give one gap; one gap cannot show steadiness
MAX_INTERVAL_SPREAD = 0.3   # gaps steady when std over mean is under this
MAX_GAP_MS = 500            # a part unseen this long starts over (Lucent's own rule)
POSE_VISIBILITY_MIN = 0.5   # shoulders count only above this (PhotoTruth V9.3)
RHYTHM_EVENTS_KEPT = 20


def find_repetition(values, times):
    """Peaks and their steadiness in a run of movement samples, the steps of
    behavior_capture.py's _find_repetitive_patterns; gaps measured in milliseconds
    from each frame's own time, as Lucent does."""
    n = len(values)
    if len(times) != n:
        raise ValueError("find_repetition: %d values but %d times" % (n, len(times)))
    if n < RHYTHM_MIN_SAMPLES:
        return None
    threshold = sum(values) / n + PEAK_ABOVE_MEAN
    peaks = [i for i in range(1, n - 1)
             if values[i] > threshold and values[i] > values[i - 1] and values[i] > values[i + 1]]
    if len(peaks) < MIN_PEAKS:
        return None
    gaps_ms = [times[peaks[i + 1]] - times[peaks[i]] for i in range(len(peaks) - 1)]
    gap_samples = sum(peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1))
    mean_ms = sum(gaps_ms) / len(gaps_ms)
    if not mean_ms > 0:
        return None
    variance = sum((g - mean_ms) ** 2 for g in gaps_ms) / len(gaps_ms)
    spread = math.sqrt(variance) / mean_ms
    if not spread < MAX_INTERVAL_SPREAD:
        return None
    return {"peaks": len(peaks), "mean_interval_samples": gap_samples / len(gaps_ms),
            "mean_interval_ms": mean_ms, "peaks_per_second": 1000 / mean_ms,
            "spread": spread, "steadiness": 1 - spread}


WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def machine_time_zone():
    """The IANA zone this machine is set to, from where /etc/localtime points, or None
    when it does not point into a zone folder."""
    try:
        target = os.path.realpath("/etc/localtime")
    except OSError:
        return None
    marker = "zoneinfo/"
    i = target.find(marker)
    return target[i + len(marker):] if i >= 0 else None


def local_stamp(t_ms):
    """The time on this machine's own clock, for finding the same time on other days."""
    lt = time.localtime(t_ms / 1000)
    return {"date": time.strftime("%Y-%m-%d", lt), "time": time.strftime("%H:%M:%S", lt),
            "weekday": WEEKDAYS[lt.tm_wday], "minute_of_day": lt.tm_hour * 60 + lt.tm_min,
            "utc_offset_min": lt.tm_gmtoff // 60, "time_zone": machine_time_zone()}


PART_IDS = ("head", "jaw", "hand_image_left", "hand_image_right", "shoulders")
HEAD_POINTS = (1, 10, 152, 234, 454)    # nose tip, forehead top, chin, the two sides
HEAD_SCALE = (10, 152)                  # forehead top to chin: the head's size
JAW_POINTS = {"nose_tip": 1, "chin": 152, "forehead_top": 10}
HAND_SCALE = (0, 9)                     # wrist to the middle finger's knuckle
SHOULDER_POINTS = (11, 12)


def _px(p, w, h):
    return None if p is None else (p[0] * w, p[1] * h)


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def head_shape(face, w, h):
    points = [_px(_point(face, i), w, h) for i in HEAD_POINTS]
    a, b = _px(_point(face, HEAD_SCALE[0]), w, h), _px(_point(face, HEAD_SCALE[1]), w, h)
    if None in points or a is None or b is None:
        return None
    size = _dist(a, b)
    return {"points": points, "size": size} if size > 0 else None


def jaw_shape(face, w, h):
    nose = _px(_point(face, JAW_POINTS["nose_tip"]), w, h)
    chin = _px(_point(face, JAW_POINTS["chin"]), w, h)
    top = _px(_point(face, JAW_POINTS["forehead_top"]), w, h)
    if None in (nose, chin, top):
        return None
    upper = _dist(top, nose)
    if not upper > 0:
        return None
    return {"points": [chin], "size": upper, "jaw_drop": _dist(nose, chin) / upper}


def hand_shape(hand, w, h):
    if len(hand) < 21:
        return None
    points = [_px(p, w, h) for p in hand]
    size = _dist(points[HAND_SCALE[0]], points[HAND_SCALE[1]])
    return {"points": points, "size": size} if size > 0 else None


def shoulder_shape(pose, visibility, w, h):
    for i in SHOULDER_POINTS:
        if _point(pose, i) is None or (visibility[i] if i < len(visibility) else 0) <= POSE_VISIBILITY_MIN:
            return None
    points = [_px(pose[i], w, h) for i in SHOULDER_POINTS]
    size = _dist(points[0], points[1])
    return {"points": points, "size": size} if size > 0 else None


def part_movement(prev, curr):
    """How much a part moved between two frames, in the part's own size. For the jaw,
    how much its drop changed; for the others, the mean distance each point travelled."""
    if "jaw_drop" in curr and "jaw_drop" in prev:
        return abs(curr["jaw_drop"] - prev["jaw_drop"])
    n = min(len(prev["points"]), len(curr["points"]))
    if not n:
        return 0.0
    return sum(_dist(prev["points"][i], curr["points"][i]) for i in range(n)) / n / curr["size"]


def hand_sides(hands, midline_x):
    """Which side of the image each hand is on, by its wrist. Two hands: the wrist
    nearer the image's left edge is image_left. One hand: the side of the midline."""
    with_wrist = [(hd, hd[0][0]) for hd in hands if hd and hd[0] is not None]
    if not with_wrist:
        return {"left": None, "right": None}
    if len(with_wrist) == 1:
        pts, x = with_wrist[0]
        return {"left": pts, "right": None} if x < midline_x else {"left": None, "right": pts}
    a, b = sorted(with_wrist[:2], key=lambda p: p[1])
    return {"left": a[0], "right": b[0]}


def parts_from(faces, hands, bodies, w, h):
    """The parts one frame shows. faces and hands are landmark lists; bodies are
    (landmarks, visibility) pairs. The first face gives the head and jaw, the first
    body the shoulders, and the hands go by image side."""
    face = faces[0] if faces else None
    body = bodies[0] if bodies else None
    shoulders = shoulder_shape(body[0], body[1], w, h) if body else None
    if face is not None and _point(face, JAW_POINTS["nose_tip"]) is not None:
        midline = face[JAW_POINTS["nose_tip"]][0]
    elif body and shoulders:
        midline = (body[0][11][0] + body[0][12][0]) / 2
    else:
        midline = 0.5
    sides = hand_sides(hands, midline)
    return {"head": head_shape(face, w, h) if face is not None else None,
            "jaw": jaw_shape(face, w, h) if face is not None else None,
            "hand_image_left": hand_shape(sides["left"], w, h) if sides["left"] else None,
            "hand_image_right": hand_shape(sides["right"], w, h) if sides["right"] else None,
            "shoulders": shoulders}


class _Track:
    def __init__(self):
        self.last_t = -math.inf
        self.open = None
        self.reset()

    def reset(self):
        self.values, self.times = [], []
        self.prev = None
        self.movement = None
        self.repetition = None


class RhythmTracker:
    """Follows each part over time: which part repeats a movement, how fast and how
    steadily, and when. It never says what a movement means."""

    def __init__(self):
        self._tracks = {p: _Track() for p in PART_IDS}
        self._events = []

    def update(self, t, parts):
        began, ended = [], []
        for part in PART_IDS:
            track = self._tracks[part]
            shape = parts.get(part)
            if shape is None:
                track.prev = None
                track.movement = None
                if t - track.last_t > MAX_GAP_MS:
                    track.reset()
                    self._close(track, t, ended)
                continue
            if t - track.last_t > MAX_GAP_MS:
                track.reset()
                self._close(track, t, ended)
            if track.prev is not None:
                m = part_movement(track.prev, shape)
                track.values.append(m)
                track.times.append(t)
                if len(track.values) > RHYTHM_WINDOW:
                    track.values.pop(0)
                    track.times.pop(0)
                track.movement = m
            track.prev = shape
            track.last_t = t
            track.repetition = find_repetition(track.values, track.times)
            r = track.repetition
            if r:
                if track.open is None:
                    track.open = {"part": part, "start": t, "start_local": local_stamp(t),
                                  "last_seen": t, "end": None, "end_local": None,
                                  "duration_ms": 0, "peaks_per_second": r["peaks_per_second"],
                                  "steadiness": r["steadiness"], "peaks": r["peaks"]}
                    self._events.append(track.open)
                    if len(self._events) > RHYTHM_EVENTS_KEPT:
                        self._events.pop(0)
                    began.append(track.open)
                else:
                    o = track.open
                    o["last_seen"], o["duration_ms"] = t, t - o["start"]
                    o["peaks_per_second"], o["steadiness"], o["peaks"] = (
                        r["peaks_per_second"], r["steadiness"], r["peaks"])
            else:
                self._close(track, t, ended)
        return {"began": began, "ended": ended}

    def _close(self, track, t, ended):
        if track.open is None:
            return
        track.open["end"] = t
        track.open["end_local"] = local_stamp(t)
        ended.append(track.open)
        track.open = None

    def parts(self):
        return [{"part": p, "samples": len(self._tracks[p].values),
                 "movement": self._tracks[p].movement,
                 "repetition": self._tracks[p].repetition} for p in PART_IDS]

    def repeating(self):
        """The parts with a repeat open now, in Lucent's part order."""
        return [p for p in PART_IDS if self._tracks[p].open is not None]

    def recent(self):
        return [dict(e) for e in self._events]
