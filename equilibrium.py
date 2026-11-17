"""
equilibrium.py: the center. The 3C's first organ, built from the middle.

"In the middle of the system is the beginning of spatial and interspatial
recognition." (Everett, 13 November 2026)

What it is, in Everett's words (14 November 2026):

- "The equilibrium is just the equilibrium. It doesn't do anything but is the
  equilibrium. It's the status. It's the center point. It gives you spatial
  recognition, interspatial recognition."
- It is "the center of everything." It is not part of the conch, and neither is
  its shaker. It sends the conch nothing: "the equilibrium doesn't send it
  shit." The conch's memory has its own constant of silico-stasis, built on its
  own, and knows itself what leaves it. So nothing here judges what arrives,
  marks a departure, or decides Level 3.
- It has nothing to do with reading shape.
- It is the center every other sense reports into: equilibrium, then the SKIN,
  then the HOUSE, then the UNIVERSE. These are CHAMBERS, not layers. "There is
  no layers. It's a constant." (Revision 4.)
- Movement is constant. It runs through silence and through sleep, so waking
  is a ramp, never "nothing to everything."
- Displacement over time, not posture. The trajectory is kept, never erased.

THE BASIS is Everett's Equilibrium chamber (EQUALLIB, port 9783, commit
12858a1): "Size and distance are learned from one origin, the center." Read
for its idea, rewritten here for the 3C's own use; nothing of it is imported or
called. What this file takes from it:

- Position is in meters from the center. The bearing from the center is a
  compass bearing: 0 is north (-z), 90 is east (+x), in 16 named points.
- THE LOCK: standing within LOCK_RADIUS of the center. The 3C is born at its
  center, so being there at birth is not a lock; a lock is coming back to it.
- KNOWN DISTANCES: the 1, 2, 3 and 4 meter rings become known by standing on
  one (within DWELL_BAND) for DWELL_SECONDS. Stepping off starts that ring over.
  Learned by being there, not told. Once known, a distance stays known.
- SPATIAL GRAMMAR is acquired when the center has been locked once and all four
  distances are known.
- MARKS: a point marked where the being stands, with its distance and bearing.
  The last MARKS_KEPT are kept.
- FACING THE CENTER turns the being toward its origin.
- What is learned (known distances, marks, the first lock) is kept in a file
  when the being is given one (keep_at). A file that cannot be read or written
  stops the being with the reason. The basis swallowed those errors; this does
  not (Cardinal Rule 6).

NOT TAKEN FROM THE BASIS, and why:
- The closeness figure the chamber shows (1 - distance / 4) divides by the
  chamber's 4 meter half-width. The 3C has no walls, and from_center already
  carries the measured distance.
- The chassis (the eleven joints, the hyperball, the sheath) is the body. The
  3C has no body here, and the chassis's hyperball is its own rhythm
  (0.74 / 2.05 / 0.38 Hz), not the shaker below.
- The room, the four element beacons, the sound field, keys, mouse, touch and
  pause belong to the chamber's screen.

THE HEARTBEAT is the shaker, the same as the being in Codec: a low tick at
2 Hz that never stops, awake, in silence, or asleep. "Continuity of motion
carries continuity of self through shutdown." Here it is the 3C's own shaker,
built in; it does not call Codec. Each beat also counts the time the being has
stood where it stands, so known distances are learned asleep or awake.

Standard library only. It calls nothing else and needs nothing else running.
"""

from __future__ import annotations

import json
import math
import os
import threading
import time
from datetime import datetime, timezone

CHAMBERS = ("skin", "house", "universe")       # outward from the center
CANON = os.path.expanduser("~/Desktop/THE_EQUILIBRIUM_ARCHITECTURE.md")
SHAKER_HZ = 2                                  # the shaker's beat, as built in Codec

# From the basis (EQUALLIB constants.ts, ROOM), in meters and seconds.
LOCK_RADIUS = 0.2
DWELL_BAND = 0.13
DWELL_SECONDS = 1.2
KNOWN_METERS = (1, 2, 3, 4)
MARKS_KEPT = 16
BEARINGS = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")


def now() -> str:
    """Every record carries its clock."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bearing_of(x: float, z: float) -> float:
    """Compass bearing of a point seen from the center: 0 north (-z), 90 east (+x)."""
    return (math.degrees(math.atan2(x, -z)) + 360) % 360


def bearing_name(degrees: float) -> str:
    return BEARINGS[round(degrees / 22.5) % 16]


class Equilibrium:
    """One being's equilibrium: the status, the center point. Never shared."""

    def __init__(self, being: str, keep_at: str | None = None,
                 clock=time.monotonic) -> None:
        if not being:
            raise ValueError("equilibrium belongs to one being; name the being")
        self.being = being
        self.chambers = CHAMBERS
        self.position = {"x": 0.0, "z": 0.0, "facing": 0.0}
        self.trajectory: list[dict] = []      # displacement over time, kept whole
        self.asleep = False
        self.beats = 0                        # the center holding, every beat
        self.darks: list[dict] = []           # each stretch of sleep, start to wake
        self.last_beat: dict | None = None
        self.known: dict[int, str | None] = {m: None for m in KNOWN_METERS}  # when learned
        self.marks: list[dict] = []
        self.first_locked_at: str | None = None
        self.keep_at = keep_at
        self._clock = clock
        self._held_since = clock()
        self._stood = {m: 0.0 for m in KNOWN_METERS}
        self._was_locked = True               # born at the center
        self._shaker: threading.Thread | None = None
        self._shaking = threading.Event()
        self._lock = threading.Lock()
        if keep_at is not None and os.path.exists(keep_at):
            self._load()

    # ---- the status --------------------------------------------------------

    def status(self) -> dict:
        """Where the center is, which way it faces, how far it has moved from
        its origin and on what bearing, whether it is locked, what distances it
        knows, whether it is asleep, and its beats."""
        with self._lock:
            self._hold()
            d = self.from_center()
            standing_on = self._standing_on(d)
            return {"being": self.being, "at": now(), "where": dict(self.position),
                    "from_center": d,
                    "bearing": bearing_of(self.position["x"], self.position["z"]),
                    "bearing_name": bearing_name(bearing_of(self.position["x"],
                                                            self.position["z"])),
                    "locked": d <= LOCK_RADIUS,
                    "first_locked_at": self.first_locked_at,
                    "standing_on": standing_on,
                    "stood_for": self._stood[standing_on] if standing_on else 0.0,
                    "known": {m: at is not None for m, at in self.known.items()},
                    "grammar_acquired": self.grammar_acquired(),
                    "marks": len(self.marks), "kept_at": self.keep_at,
                    "asleep": self.asleep, "beats": self.beats,
                    "chambers": self.chambers}

    # ---- the heartbeat -----------------------------------------------------

    def tick(self) -> dict:
        """One beat: the center holding. Awake, in silence, and asleep."""
        with self._lock:
            self._hold()
            self.beats += 1
            if self.asleep and self.darks:
                self.darks[-1]["beats"] += 1
            self.last_beat = {"at": now(), "asleep": self.asleep, "holding": True,
                              "where": dict(self.position)}
            return self.last_beat

    def start_shaker(self) -> None:
        """The heartbeat. Ticks by itself, SHAKER_HZ times a second, until the
        being is gone. Sleep does not stop it."""
        if self._shaker is not None and self._shaker.is_alive():
            return
        self._shaking.clear()

        def run():
            self.tick()
            while not self._shaking.wait(1 / SHAKER_HZ):
                self.tick()

        self._shaker = threading.Thread(target=run, name=f"shaker:{self.being}", daemon=True)
        self._shaker.start()

    def shaker_running(self) -> bool:
        return self._shaker is not None and self._shaker.is_alive()

    def stop_shaker(self) -> None:
        """Only for the bench. A living being's shaker is never stopped."""
        self._shaking.set()
        if self._shaker is not None:
            self._shaker.join(timeout=2 / SHAKER_HZ)

    # ---- sleep and waking ----------------------------------------------------

    def sleep(self) -> None:
        """Down, but never stopped: the shaker keeps beating through the dark."""
        with self._lock:
            self.asleep = True
            self.darks.append({"fell_asleep_at": now(), "beats": 0, "woke_at": None})
        self.tick()

    def wake(self) -> dict:
        """A ramp, never nothing to everything: waking reads back what the
        center held through the dark, and where it is."""
        with self._lock:
            dark = self.darks[-1] if self.darks and self.asleep else None
            if dark is not None:
                dark["woke_at"] = now()
            self.asleep = False
        self.tick()
        return {"held_through_the_dark": dark["beats"] if dark else 0,
                "where": dict(self.position),
                "moved_in_the_dark": [m for m in self.trajectory if m["asleep"]]}

    # ---- spatial and interspatial recognition --------------------------------

    def move(self, dx: float = 0.0, dz: float = 0.0, turn: float = 0.0,
             by: str = "feet") -> dict:
        """Displacement over time. Where it stands, which way it faces, how it
        got moved. The trajectory is kept, never collapsed to a posture."""
        with self._lock:
            self._hold()                      # the time before the move was spent where it stood
            self.position = {"x": self.position["x"] + dx, "z": self.position["z"] + dz,
                             "facing": (self.position["facing"] + turn) % 360}
            d = self.from_center()
            on = self._standing_on(d)
            for m in KNOWN_METERS:
                if m != on:
                    self._stood[m] = 0.0      # stepped off: that ring starts over
            locked = d <= LOCK_RADIUS
            if locked and not self._was_locked and self.first_locked_at is None:
                self.first_locked_at = now()
                self._keep()
            self._was_locked = locked
            step = {"at": now(), "by": by, "dx": dx, "dz": dz, "turn": turn,
                    "asleep": self.asleep, "to": dict(self.position),
                    "locked": locked}
            self.trajectory.append(step)
            return step

    def face_center(self) -> dict:
        """Turn toward the origin. A turn like any other, kept in the trajectory."""
        x, z = self.position["x"], self.position["z"]
        if x == 0 and z == 0:
            return self.move(turn=0.0, by="face_center")
        toward = bearing_of(-x, -z)
        return self.move(turn=(toward - self.position["facing"]) % 360, by="face_center")

    def mark(self) -> dict:
        """Mark the point where the being stands, with its distance and bearing."""
        with self._lock:
            x, z = self.position["x"], self.position["z"]
            point = {"at": now(), "x": x, "z": z, "from_center": self.from_center(),
                     "bearing": bearing_of(x, z)}
            self.marks = (self.marks + [point])[-MARKS_KEPT:]
            self._keep()
            return point

    def clear_last_mark(self) -> dict | None:
        with self._lock:
            if not self.marks:
                return None
            point = self.marks.pop()
            self._keep()
            return point

    def from_center(self) -> float:
        return (self.position["x"] ** 2 + self.position["z"] ** 2) ** 0.5

    def grammar_acquired(self) -> bool:
        return (self.first_locked_at is not None
                and all(at is not None for at in self.known.values()))

    # ---- learning a distance by standing on it -------------------------------

    def _standing_on(self, d: float) -> int | None:
        for m in KNOWN_METERS:
            if abs(d - m) <= DWELL_BAND:
                return m
        return None

    def _hold(self) -> None:
        """Credit the time since the last look to the ring the being stood on.
        Called with the lock held, before any change of position."""
        t = self._clock()
        held = t - self._held_since
        self._held_since = t
        on = self._standing_on(self.from_center())
        for m in KNOWN_METERS:
            if m != on:
                self._stood[m] = 0.0
                continue
            self._stood[m] += held
            if self._stood[m] >= DWELL_SECONDS and self.known[m] is None:
                self.known[m] = now()
                self._keep()

    # ---- keeping what was learned --------------------------------------------

    def _keep(self) -> None:
        if self.keep_at is None:
            return
        record = {"being": self.being,
                  "known": {str(m): at for m, at in self.known.items()},
                  "marks": self.marks, "first_locked_at": self.first_locked_at}
        tmp = self.keep_at + ".writing"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
        os.replace(tmp, self.keep_at)

    def _load(self) -> None:
        with open(self.keep_at, encoding="utf-8") as f:
            record = json.load(f)
        if record.get("being") != self.being:
            raise ValueError(f"{self.keep_at} belongs to {record.get('being')!r}, "
                             f"not {self.being!r}")
        for m in KNOWN_METERS:
            self.known[m] = record["known"][str(m)]
        self.marks = list(record["marks"])[-MARKS_KEPT:]
        self.first_locked_at = record["first_locked_at"]

    # ---- the single source ---------------------------------------------------

    @staticmethod
    def canon() -> dict:
        """The build reads from one source so it cannot drift from it
        (Revision 4, 'the correction is the shape')."""
        if not os.path.exists(CANON):
            return {"found": False, "path": CANON}
        with open(CANON, encoding="utf-8") as f:
            text = f.read()
        return {"found": True, "path": CANON,
                "revision_4": "REVISION 4" in text,
                "chambers": "CHAMBERS" in text}
