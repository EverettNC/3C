"""patch_ear_adapts.py: the ear adapts to a steady sound and gives the room (C3, C4; 17 Nov 2026).

    python3 docs/tools/patch_ear_adapts.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once, or nothing is written.
"""
import sys

PATH = "ear.py"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""- The microphone is opened when this Python has a way to open it
  (sounddevice). If not, live listening refuses with the reason. On the bench
  the ear hears a WAV file.

LIMIT. A steady sound that never falls away (a fan) keeps one event open.
\"\"\"""",
     """- The microphone is opened when this Python has a way to open it
  (sounddevice). If not, live listening refuses with the reason. On the bench
  the ear hears a WAV file.
- It adapts, as carbon does (C3 in the notes). Carbon answers a sound held or
  repeated less and less and keeps answering one that is new (stimulus-specific
  adaptation: Ayala and Malmierca, 2013). So the ear's floor is the lowest level
  it has heard across the span carbon holds sound in the ear (echoic memory,
  about three to four seconds: Darwin, Turvey and Crowder, 1972). An event opens
  when the sound rises past the floor by Corti's onset and closes when it falls
  back to the floor by Corti's offset. A fan starting is heard; once it is the
  floor, it is no longer an event.
- The room still counts (C4). "Attention selects a target. Memory keeps the
  room." Between events the ear gives the room as it stands: quiet when the floor
  is silence; otherwise the floor itself, as "the room", voiced or not, with its
  note when YIN locks on it.

LIMIT. The ear hears one mixture. It does not yet separate one source from
another (Bregman's streams); picking among sources is attention, not the ear's.
\"\"\""""),

    ("""import array
import json
import math
import os
import statistics
import threading
import wave
""",
     """import array
import collections
import json
import math
import os
import statistics
import threading
import wave
"""),

    ("""HOP = 256               # samples between one measurement and the next
""",
     """HOP = 256               # samples between one measurement and the next
ECHOIC_MS = 4000        # the span the floor is taken over: echoic memory, three to four seconds
"""),

    ("""        self._open = None                     # the utterance being heard, or None
        self._stream = None
        gateway.connect(self.ORGAN, "sound")""",
     """        self._open = None                     # the utterance being heard, or None
        self._levels = collections.deque(maxlen=max(1, ECHOIC_MS * RATE // (1000 * HOP)))
        self._room = None                     # the shape the ear last gave for the room
        self._stream = None
        gateway.connect(self.ORGAN, "sound")"""),

    ("""    def _step(self, frame) -> list:
        level, crossings = rms(frame), zcr(frame)
        ms = 1000 * self._t / RATE
        if self._open is None:
            if level < ONSET:
                return []
            self._open = {""",
     """    def _floor(self) -> float:
        return min(self._levels) if self._levels else 0.0

    def _step(self, frame) -> list:
        level, crossings = rms(frame), zcr(frame)
        ms = 1000 * self._t / RATE
        self._levels.append(level)
        floor = self._floor()
        if self._open is None:
            if level < floor + ONSET:
                return self._the_room(frame, floor)
            self._open = {"""),

    ("""        if level < OFFSET and ms - u["start_ms"] >= MIN_MS:
            return self._close(ms)
        return []""",
     """        if level < floor + OFFSET and ms - u["start_ms"] >= MIN_MS:
            return self._close(ms, frame, floor)
        return []

    def _the_room(self, frame, floor: float) -> list:
        \"\"\"Between events: the room as it stands. Given only when it changes.\"\"\"
        if floor < OFFSET:
            shape, reading = "quiet", None
        else:
            locked = yin(frame)
            f0 = locked[0] if locked and locked[1] > LOCK else None
            shape = {"heard": "the room", "voiced": f0 is not None,
                     "note": note_of(f0) if f0 is not None else "no lock"}
            reading = {"floor_rms": round(floor, 5),
                       "f0_hz": None if f0 is None else round(f0, 2)}
        if shape == self._room:
            return []
        self._room = shape
        clock = "the ear " + now()
        given = quiet(clock) if reading is None else gave(reading, shape, clock)
        came = self._gateway.arrive(self.ORGAN, "sound", given)
        return [] if came is None else [came]"""),

    ("""    def _close(self, ms: float) -> list:""",
     """    def _close(self, ms: float, frame, floor: float) -> list:"""),

    ("""        clock = "the ear " + now()
        came = [self._gateway.arrive(self.ORGAN, "sound", gave(what, shape, clock)),
                self._gateway.arrive(self.ORGAN, "sound", quiet(clock))]
        return [c for c in came if c is not None]""",
     """        clock = "the ear " + now()
        came = [self._gateway.arrive(self.ORGAN, "sound", gave(what, shape, clock))]
        self._room = None                     # the room is given again after every event
        came.extend(self._the_room(frame, floor))
        return [c for c in came if c is not None]"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("the ear adapts and gives the room")
