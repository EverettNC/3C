"""
eye.py: the 3C's eye. It sees and gives shape. It names no feeling and never
says what a movement means.

Rewritten for the 3C from Lucent (EverettNC/LUCENT b582a1d, read line by line
on 17 Nov 2026). Lucent is the eye of the house; its reader is the face reading.
Nothing of Lucent is imported or called: its measuring is rewritten in
eye_reading.py, and the landmarks come from the same models Lucent uses.

WHAT IT DOES  [build choices, the builder's to make on Everett's ruling of
17 Nov 2026; each is in conch_build_notes.md, V1 to V9]

- Landmarks come from Google's MediaPipe face, hand and pose landmarkers, the very
  files Lucent vendors (Apache 2.0), pulled from GitHub at Lucent b582a1d by
  install_lucent_models.sh into organs/lucent, checked byte for byte against
  Lucent's SHA256SUMS, and run offline. Never taken from a copy on a drive. If
  mediapipe or a model is not there, the landmarks are not caught and the reason
  is given. Nothing is made up.
- The camera is the eye's device, opened through opencv when this Python has it.
  If not, the eye says it cannot open the camera, with the reason.
- The shape is only Lucent's own categories: how many faces, where the first face
  is looking (one of AlphaVox's nine cells), its eyes open or closed, which image
  sides have a hand, whether a body is in view, and which parts are repeating.
  Every measurement goes in what the eye gave, never in the shape.
- A look counts once it holds 80 ms: shorter is too short to be a look at
  anything (Nuthmann, Smith, Engbert and Henderson, Psychological Review, 2010).
- Eyes are "closed" only past 400 ms; shorter is a blink (Rodriguez et al.,
  Clinical Ophthalmology, 2013). Blinks are kept in what the eye gave and do not
  end a moment.
- A face, hand or body counts as gone only after 500 ms unseen (Lucent's own
  rule for when a part has left). It counts as there when it is seen.
- The eye gives a reading only when its shape changes.

LIMIT. Lucent reads people. When no one is in view the eye says so and says
nothing of the room's light: AlphaVox's behavior_capture.py measured the whole
picture, and it has not been read yet.

Standard library at the top. mediapipe and opencv are imported only inside the
two places that need them, and only if this Python has them.
"""

from __future__ import annotations

import hashlib
import math
import os
import sys
import threading
import time

import eye_reading as er
from conch_records import gave, now

# -- Lucent's models, pinned to Lucent b582a1d public/mediapipe/SHA256SUMS ----------
MODEL_SUMS = {
    "face_landmarker.task": "64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff",
    "hand_landmarker.task": "fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1",
    "pose_landmarker_lite.task": "59929e1d1ee95287735ddd833b19cf4ac46d29bc7afddbbf6753c459690d574a",
}
# One place only: the 3C's own, filled from GitHub by install_lucent_models.sh at
# Lucent b582a1d. Never a copy on a drive, and no way to point it at one (Everett,
# 17 Nov 2026: "You only pull from GitHub when you're installing something.").
MODEL_PLACES = (os.path.join(os.path.dirname(os.path.abspath(__file__)), "organs", "lucent"),)

# -- the hold rules (V6, V7, V8) ------------------------------------------------------
LOOK_HOLD_MS = 80
CLOSED_PAST_MS = 400
GONE_AFTER_MS = er.MAX_GAP_MS

HAND_SIDES = ("image_left", "image_right")


def _r(v, places=4):
    return None if v is None or not math.isfinite(v) else round(v, places)


def _lm(p):
    return [_r(p[0]), _r(p[1]), _r(p[2])]


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ---- landmarks (Lucent's models, through mediapipe) ---------------------------------

class Landmarks:
    """Lucent's three landmarkers, run offline in VIDEO mode. Catches landmarks, or
    says why not. Written to the mediapipe Tasks API (0.10); not yet run on this Mac,
    because mediapipe is not installed in either Python there."""

    def __init__(self, model_dir=None) -> None:
        self.why_not = None
        self.parts = {"face": None, "hands": None, "pose": None}
        self._tasks = {}
        self._last_ts = 0
        here = os.path.dirname(os.path.abspath(__file__))
        if model_dir is not None and not os.path.realpath(model_dir).startswith(
                os.path.realpath(here) + os.sep):
            self.why_not = (f"{model_dir} is outside the 3C. The eye's models come only from "
                            "GitHub, through ./install_lucent_models.sh, never from a copy")
            return
        places = [model_dir] if model_dir else [p for p in MODEL_PLACES if p]
        place = next((p for p in places if p and os.path.isdir(p)), None)
        if place is None:
            self.why_not = ("Lucent's models were not found at " + ", ".join(p for p in places if p)
                            + ". They are pulled from GitHub: ./install_lucent_models.sh")
            return
        for name, want in MODEL_SUMS.items():
            path = os.path.join(place, name)
            if not os.path.isfile(path):
                self.why_not = f"{path} is missing"
                return
            if _sha256(path) != want:
                self.why_not = f"{path} does not match Lucent's SHA256SUMS; it is not used"
                return
        self.place = place
        try:
            import mediapipe as mp
        except ImportError:
            self.why_not = ("mediapipe is not installed in this Python. On this Mac pip offers "
                            "mediapipe 0.10.21 for Python 3.9: python3 -m pip install mediapipe")
            return
        vision = mp.tasks.vision
        base = mp.tasks.BaseOptions
        mode = vision.RunningMode.VIDEO
        makers = {
            "face": lambda: vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
                base_options=base(model_asset_path=os.path.join(place, "face_landmarker.task")),
                running_mode=mode, num_faces=2, output_face_blendshapes=True,
                output_facial_transformation_matrixes=True)),
            "hands": lambda: vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
                base_options=base(model_asset_path=os.path.join(place, "hand_landmarker.task")),
                running_mode=mode, num_hands=2)),
            "pose": lambda: vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
                base_options=base(model_asset_path=os.path.join(place, "pose_landmarker_lite.task")),
                running_mode=mode, num_poses=1)),
        }
        for part, make in makers.items():
            try:
                self._tasks[part] = make()
                self.parts[part] = {"available": True, "reason": None}
            except Exception as err:                       # said, never swallowed
                self.parts[part] = {"available": False, "reason": f"{type(err).__name__}: {err}"}
        if not self._tasks:
            self.why_not = "no landmarker started: " + "; ".join(
                f"{k}: {v['reason']}" for k, v in self.parts.items())
            return
        self._mp = mp

    @property
    def available(self) -> bool:
        return self.why_not is None

    def catch(self, rgb, t_ms) -> dict:
        """One frame (an RGB array, height x width x 3) through the landmarkers."""
        if not self.available:
            return {"caught": False, "why": self.why_not}
        mp = self._mp
        ts = int(t_ms)
        if ts <= self._last_ts:                            # VIDEO mode needs rising times
            ts = self._last_ts + 1
        self._last_ts = ts
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        h, w = rgb.shape[0], rgb.shape[1]
        out = {"caught": True, "why": None, "frame_w": w, "frame_h": h,
               "faces": [], "hands": [], "bodies": [], "parts": self.parts}
        if "face" in self._tasks:
            fr = self._tasks["face"].detect_for_video(image, ts)
            for i, pts in enumerate(fr.face_landmarks):
                shapes = fr.face_blendshapes[i] if i < len(fr.face_blendshapes) else []
                mats = fr.facial_transformation_matrixes
                out["faces"].append({
                    "landmarks": [[p.x, p.y, p.z] for p in pts],
                    "blendshapes": {c.category_name: c.score for c in shapes},
                    "matrix": [float(v) for v in mats[i].flatten()] if i < len(mats) else None,
                })
        if "hands" in self._tasks:
            hr = self._tasks["hands"].detect_for_video(image, ts)
            for i, pts in enumerate(hr.hand_landmarks):
                side = hr.handedness[i][0] if i < len(hr.handedness) and hr.handedness[i] else None
                out["hands"].append({"landmarks": [[p.x, p.y, p.z] for p in pts],
                                     "model_handedness": side.category_name if side else None,
                                     "handedness_score": side.score if side else None})
        if "pose" in self._tasks:
            pr = self._tasks["pose"].detect_for_video(image, ts)
            for pts in pr.pose_landmarks:
                out["bodies"].append({"landmarks": [[p.x, p.y, p.z] for p in pts],
                                      "visibility": [p.visibility or 0.0 for p in pts]})
        return out

    def close(self) -> None:
        for task in self._tasks.values():
            task.close()
        self._tasks = {}


# ---- the eye ------------------------------------------------------------------------

class Eye:
    """The 3C's eye, connected to a Gateway as the organ for sight."""

    ORGAN = "the eye"

    def __init__(self, gateway, landmarks: Landmarks | None = None) -> None:
        self._gateway = gateway
        self._landmarks = landmarks
        self._lock = threading.RLock()
        self._rhythm = er.RhythmTracker()
        self._blinks = er.BlinkLog()
        self._seen_faces = {}            # k -> last time at least k faces were seen
        self._seen_hand = {}             # image side -> last time a hand was seen there
        self._seen_body = -math.inf
        self._look = None                # the look held now
        self._look_try = None            # a cell not yet held, and since when
        self._closed_since = None
        self._eyes = None
        self._shape = None               # the shape last given
        self._camera = None
        self._thread = None
        self.error = None                # what stopped the camera, if anything did
        gateway.connect(self.ORGAN, "sight")

    def see(self, caught: dict, t_ms: float) -> list:
        """One frame's landmarks, as Landmarks.catch gives them, at time t_ms (epoch
        milliseconds). Gives back what the Gateway gave if the shape changed."""
        if not caught.get("caught"):
            raise ValueError("the eye was handed a frame whose landmarks were not caught: "
                             + str(caught.get("why")))
        with self._lock:
            return self._step(caught, t_ms)

    def look(self, camera: int = 0) -> None:
        """Open the camera and see until stop(). Refuses, with the reason, when this
        Python cannot open a camera or has no landmarks. Nothing is pretended."""
        if self._landmarks is None or not self._landmarks.available:
            why = "no landmarks were given" if self._landmarks is None else self._landmarks.why_not
            raise RuntimeError("the eye cannot see: " + why)
        try:
            import cv2
        except ImportError:
            raise RuntimeError("this Python has no way to open the camera "
                               "(opencv is not installed). The eye is not seeing.")
        with self._lock:
            if self._camera is not None:
                return
            cap = cv2.VideoCapture(camera)
            if not cap.isOpened():
                raise RuntimeError(f"camera {camera} did not open (on a Mac the terminal must "
                                   "be allowed the camera in System Settings)")
            self._camera = cap

        def seeing():
            while True:
                with self._lock:
                    cap = self._camera
                if cap is None:
                    return
                ok, bgr = cap.read()
                if not ok:
                    self.error = "the camera stopped giving frames"
                    print("the eye: " + self.error, file=sys.stderr)
                    self.stop()
                    return
                t = time.time() * 1000
                try:
                    caught = self._landmarks.catch(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), t)
                    self.see(caught, t)
                except Exception as err:
                    self.error = f"{type(err).__name__}: {err}"
                    print("the eye stopped: " + self.error, file=sys.stderr)
                    self.stop()
                    raise

        self._thread = threading.Thread(target=seeing, name="the eye", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        with self._lock:
            if self._camera is not None:
                self._camera.release()
                self._camera = None

    # -- inside --

    def _step(self, caught, t):
        w, h = caught["frame_w"], caught["frame_h"]
        faces = caught.get("faces", [])
        hands = caught.get("hands", [])
        bodies = caught.get("bodies", [])
        read = [self._face(f, w, h) for f in faces]
        parts = er.parts_from([f["landmarks"] for f in faces], [x["landmarks"] for x in hands],
                              [(b["landmarks"], b["visibility"]) for b in bodies], w, h)
        self._rhythm.update(t, parts)
        first = read[0] if read else None
        self._blinks.update(t, first["iris"]["closed"] if first else None)

        for k in (1, 2):
            if len(faces) >= k:
                self._seen_faces[k] = t
        held_faces = max([k for k in (1, 2)
                          if t - self._seen_faces.get(k, -math.inf) <= GONE_AFTER_MS] or [0])
        midline = (faces[0]["landmarks"][er.JAW_POINTS["nose_tip"]][0] if faces else
                   (bodies[0]["landmarks"][11][0] + bodies[0]["landmarks"][12][0]) / 2
                   if parts["shoulders"] else 0.5)
        sides = er.hand_sides([x["landmarks"] for x in hands], midline)
        for side, key in (("image_left", "left"), ("image_right", "right")):
            if sides[key] is not None:
                self._seen_hand[side] = t
        if bodies:
            self._seen_body = t

        if held_faces == 0:
            self._look, self._look_try = None, None
            self._closed_since, self._eyes = None, None
        elif first is not None:
            cell = first["gaze"]["cell"] if first["gaze"] else None
            if self._look_try is None or self._look_try[0] != cell:
                self._look_try = (cell, t)
            if t - self._look_try[1] >= LOOK_HOLD_MS:
                self._look = cell
            closed = first["iris"]["closed"]
            if closed is True:
                if self._closed_since is None:
                    self._closed_since = t
                if t - self._closed_since > CLOSED_PAST_MS:
                    self._eyes = "closed"
            elif closed is False:
                self._closed_since, self._eyes = None, "open"
        # a face still held but not read in this frame keeps its look and its eyes

        shape = {"faces": held_faces, "looking": self._look, "eyes": self._eyes,
                 "hands": [s for s in HAND_SIDES
                           if t - self._seen_hand.get(s, -math.inf) <= GONE_AFTER_MS],
                 "body": t - self._seen_body <= GONE_AFTER_MS,
                 "repeating": self._rhythm.repeating()}
        if shape == self._shape:
            return []
        self._shape = shape
        what = {
            "frame": [w, h],
            "local": er.local_stamp(t),
            "faces": [self._house_face(f) for f in read],
            "hands": [{"model_handedness": x.get("model_handedness"),
                       "landmarks": [_lm(p) for p in x["landmarks"]]} for x in hands],
            "bodies": [{"landmarks": [_lm(p) for p in b["landmarks"]],
                        "visibility": [_r(v, 3) for v in b["visibility"]]} for b in bodies],
            "blinks": {"per_minute": _r(self._blinks.per_minute(), 2),
                       "recent": self._blinks.recent()},
            "rhythm": {"parts": [self._house_part(p) for p in self._rhythm.parts()],
                       "events": [self._house_event(e) for e in self._rhythm.recent()]},
            "parts": caught.get("parts"),
        }
        came = self._gateway.arrive(self.ORGAN, "sight", gave(what, shape, "the eye " + now()))
        return [] if came is None else [came]

    @staticmethod
    def _face(f, w, h):
        lm = f["landmarks"]
        b = f.get("blendshapes") or {}
        pose = er.pose_from_matrix(f["matrix"]) if f.get("matrix") else None
        mouth = er.mouth_from_landmarks(lm, w, h)
        jaw = b.get("jawOpen")
        mouth["jaw_open"] = jaw if isinstance(jaw, (int, float)) and math.isfinite(jaw) else None
        return {"landmarks": lm, "blendshapes": b, "pose": pose,
                "gaze": er.gaze_from_blendshapes(b) if b else None,
                "iris": er.iris_from_landmarks(lm, w, h), "mouth": mouth}

    @staticmethod
    def _house_face(f):
        """One face as Lucent's house record carries it (reading.ts houseFace)."""
        p, g, i, m, b = f["pose"], f["gaze"], f["iris"], f["mouth"], f["blendshapes"]
        return {
            "pose": None if p is None else {"yaw_deg": _r(p["yaw_deg"], 2),
                                            "pitch_deg": _r(p["pitch_deg"], 2),
                                            "roll_deg": _r(p["roll_deg"], 2)},
            "gaze": {"direction": g["cell"] if g else None,
                     "horizontal": _r(g["horizontal"]) if g else None,
                     "vertical": _r(g["vertical"]) if g else None,
                     "iris_ratio": _r(i["iris_ratio"]) if i["iris_ratio"] is not None else None,
                     "iris_horizontal": i["horizontal"]},
            "eyes": {"image_left_openness": _r(i["per_eye"]["image_left"]["openness"])
                     if i["per_eye"]["image_left"]["openness"] is not None else None,
                     "image_right_openness": _r(i["per_eye"]["image_right"]["openness"])
                     if i["per_eye"]["image_right"]["openness"] is not None else None,
                     "closed": i["closed"],
                     "blink_left_score": _r(b["eyeBlinkLeft"]) if "eyeBlinkLeft" in b else None,
                     "blink_right_score": _r(b["eyeBlinkRight"]) if "eyeBlinkRight" in b else None},
            "mouth": {"open": _r(m["open"]) if m["open"] is not None else None,
                      "width": _r(m["width"]) if m["width"] is not None else None,
                      "jaw_open": _r(m["jaw_open"]) if m["jaw_open"] is not None else None},
            "lips": [_lm(p) for p in er.lips(f["landmarks"])],
            "blendshapes": {k: _r(v) for k, v in b.items()},
        }

    @staticmethod
    def _house_part(p):
        r = p["repetition"]
        return {"part": p["part"], "samples": p["samples"],
                "movement": _r(p["movement"]) if p["movement"] is not None else None,
                "repeating": r is not None,
                "peaks_per_second": _r(r["peaks_per_second"], 3) if r else None,
                "steadiness": _r(r["steadiness"], 3) if r else None,
                "peaks": r["peaks"] if r else None}

    @staticmethod
    def _house_event(e):
        out = dict(e)
        out["peaks_per_second"] = _r(e["peaks_per_second"], 3)
        out["steadiness"] = _r(e["steadiness"], 3)
        return out
