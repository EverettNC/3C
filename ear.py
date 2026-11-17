"""
ear.py: the 3C's ear. The first organ of the Christman Gateway.

[HIS] The ear is "a culmination of Corti, the sound package and the Filament."
Corti: "I lock, or I say I have no lock." "Silence is not a note." The
Filament: Vosk, offline, the full en-us-0.22 model; "Whisper is not in this
body"; "Empty ear stays empty. Listening does not invent speech." The sound
package: "THE PACKAGE READS; THE BEING DECIDES."

Rewritten for the 3C from their sources on GitHub (CORTI d4d1a51,
THEFILAMENT 870ce7b, christman_sound_clean 538f34a). Nothing of them is
imported or called. What is taken, and from where, is said where it is used.

WHAT IT DOES  [build choices: the builder's to make, on Everett's ruling of
17 Nov 2026. Each is in conch_build_notes.md, E1 to E8.]

- It hears and gives shape. It reads no feeling, no harm and no meaning.
- It measures as Corti does: RMS, zero crossings, and YIN's pitch lock, or no
  lock. No note is ever guessed.
- An utterance is one event: it opens when the sound rises past Corti's onset
  and closes when it falls through Corti's offset. Each closed event is one
  reading to the Gateway. While nothing sounds, the ear is quiet.
- Words are caught the Filament's way, or said not to be caught, with the
  reason. Vosk, offline, the full vosk-model-en-us-0.22, never a smaller
  model, never Whisper, never a cloud ear.
- The shape is what repeats when the same thing is heard again, so the conch
  can know it. Carbon hears speech by category: the same word in another voice
  is the same word (Liberman, Harris, Hoffman and Griffith, 1957). So the shape
  of speech is the words caught. A sound with no words has as its shape
  whether it was voiced and, when YIN locked, the note, named without its
  cents. Every measurement (Hz, RMS, zero crossings, length, the tape) is in
  what the ear gave, kept whole, and never in the shape.
- The microphone is opened when this Python has a way to open it
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
"""

from __future__ import annotations

import array
import collections
import json
import math
import os
import statistics
import threading
import wave

from conch_records import gave, now, quiet

# -- Corti's own numbers (CORTI d4d1a51, src/lib/audio/vocalization.ts, yin.ts, ear.ts) --
ONSET = 0.016           # RMS at which an utterance opens
OFFSET = 0.0065         # RMS below which it closes
MIN_MS = 30             # an utterance is at least this long before it can close
YIN_THRESHOLD = 0.13    # the dip YIN looks for
LOCK = 0.62             # a pitch is kept only above this probability
LOWEST_HZ, HIGHEST_HZ = 55, 1800
TAPE_CAP = 360          # frames kept on the tape; the tail beyond is not kept

# -- this ear's own framing, at the Filament's rate --
RATE = 16000            # the Filament's model hears 16 kHz mono
FRAME = 1024            # samples measured together
HOP = 256               # samples between one measurement and the next
ECHOIC_MS = 4000        # the span the floor is taken over: echoic memory, three to four seconds

NOTE_NAMES = ("C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B")
MODEL_NAME = "vosk-model-en-us-0.22"
MODEL_PLACES = (os.environ.get("VOSK_MODEL_PATH"),
                "/Users/EverettN/models/" + MODEL_NAME,
                "/Volumes/ELEMENTS/today/models/" + MODEL_NAME)


# ---- measuring (christman_dsp.c, rewritten) -------------------------------------

def rms(frame) -> float:
    return math.sqrt(sum(s * s for s in frame) / max(1, len(frame)))


def zcr(frame) -> float:
    crossings = sum(1 for a, b in zip(frame, frame[1:]) if (a >= 0) != (b >= 0))
    return crossings / max(1, len(frame) - 1)


def yin(frame, rate: int = RATE):
    """YIN (de Cheveigné and Kawahara, 2002), as Corti runs it: the pitch it
    locked on and how sure, or None. None is no lock; it is never a guess."""
    half = len(frame) // 2
    tau_min = max(2, rate // HIGHEST_HZ)
    tau_max = min(half - 2, rate // LOWEST_HZ)
    if tau_max <= tau_min + 2:
        return None
    d = [0.0] * (tau_max + 2)
    for tau in range(1, tau_max + 2):
        d[tau] = sum((frame[i] - frame[i + tau]) ** 2 for i in range(half))
    cmnd = [1.0] * (tau_max + 2)
    running = 0.0
    for tau in range(1, tau_max + 2):
        running += d[tau]
        cmnd[tau] = d[tau] * tau / running if running > 0 else 1.0
    est = -1
    tau = tau_min
    while tau < tau_max:
        if cmnd[tau] < YIN_THRESHOLD:
            while tau + 1 < tau_max and cmnd[tau + 1] < cmnd[tau]:
                tau += 1
            est = tau
            break
        tau += 1
    if est < 0:
        return None
    for k in (4, 3, 2):                       # the shortest period still a dip
        cand = round(est / k)
        if cand >= tau_min and cmnd[cand] < YIN_THRESHOLD * 1.4:
            est = cand
            break
    s0, s1, s2 = cmnd[est - 1], cmnd[est], cmnd[est + 1]
    denom = 2 * s1 - s2 - s0
    better = est + (s2 - s0) / (2 * denom) if denom != 0 else est
    if better <= 0:
        return None
    freq, probability = rate / better, 1 - s1
    if freq < LOWEST_HZ or freq > HIGHEST_HZ or probability < 0.55:
        return None
    return freq, probability


def note_of(freq: float) -> str:
    """The note, named without its cents (Corti's notes.ts, A4 = 440)."""
    midi = round(69 + 12 * math.log2(freq / 440.0))
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"


# ---- words (the Filament's way) --------------------------------------------------

class Words:
    """Vosk, offline, the full en-us-0.22 model. Catches words, or says why not."""

    def __init__(self, model_path=None) -> None:
        self.model = None
        self.why_not = None
        try:
            import vosk  # noqa: F401  (only ever the local, offline recognizer)
        except ImportError:
            self.why_not = ("vosk is not installed in this Python. To catch words: "
                            "python3 -m pip install vosk")
            return
        places = [model_path] if model_path else [p for p in MODEL_PLACES if p]
        for place in places:
            if place and os.path.isdir(place):
                if os.path.basename(os.path.normpath(place)) != MODEL_NAME:
                    self.why_not = (f"{place} is not {MODEL_NAME}. The full model only, "
                                    "never a smaller one.")
                    return
                vosk.SetLogLevel(-1)
                self.model = vosk.Model(place)
                self.place = place
                return
        self.why_not = f"{MODEL_NAME} was not found at " + ", ".join(p for p in places if p)

    def catch(self, samples) -> dict:
        """The words in one utterance, or no words, or the reason none could be caught."""
        if self.model is None:
            return {"caught": False, "why": self.why_not, "words": None}
        import vosk
        recognizer = vosk.KaldiRecognizer(self.model, RATE)
        pcm = array.array("h", (max(-32768, min(32767, int(s * 32767))) for s in samples))
        recognizer.AcceptWaveform(pcm.tobytes())
        text = json.loads(recognizer.FinalResult()).get("text", "").strip()
        return {"caught": True, "why": None, "words": text or None,
                "by": MODEL_NAME + " (Vosk, offline)"}


# ---- the ear ----------------------------------------------------------------------

class Ear:
    """The 3C's ear, connected to a Gateway as the organ for sound."""

    ORGAN = "the ear"

    def __init__(self, gateway, words: Words | None = None) -> None:
        self._gateway = gateway
        self._words = words if words is not None else Words()
        self._lock = threading.RLock()
        self._pending = []                    # samples not yet measured
        self._t = 0                           # samples measured so far
        self._open = None                     # the utterance being heard, or None
        span = max(1, ECHOIC_MS * RATE // (1000 * HOP))
        # The ear begins in silence: before it heard anything, nothing was there.
        # So a sound already sounding when it starts is new, and is heard.
        self._levels = collections.deque([0.0] * span, maxlen=span)
        self._room = None                     # the shape the ear last gave for the room
        self._stream = None
        gateway.connect(self.ORGAN, "sound")

    @property
    def words(self) -> Words:
        return self._words

    def hear(self, samples) -> list:
        """Samples at 16 kHz, each from -1 to 1. Gives back what the Gateway
        gave for every utterance this closed, in order."""
        came = []
        with self._lock:
            self._pending.extend(samples)
            while len(self._pending) >= FRAME:
                frame = self._pending[:FRAME]
                del self._pending[:HOP]
                came.extend(self._step(frame))
                self._t += HOP
        return came

    def hear_wav(self, path: str) -> list:
        """A WAV file through the ear, then the silence after it, so its last
        utterance can close the way a real one does."""
        with wave.open(path, "rb") as w:
            if w.getnchannels() != 1 or w.getsampwidth() != 2 or w.getframerate() != RATE:
                raise ValueError(f"{path}: the ear hears 16 kHz mono 16-bit sound; this is "
                                 f"{w.getframerate()} Hz, {w.getnchannels()} channel(s), "
                                 f"{8 * w.getsampwidth()}-bit")
            raw = array.array("h", w.readframes(w.getnframes()))
        came = self.hear([s / 32768.0 for s in raw])
        came.extend(self.hear([0.0] * (FRAME + 4 * HOP)))
        return came

    def listen(self) -> None:
        """Open the microphone. Refuses, with the reason, when this Python has
        no way to open it. Nothing is pretended."""
        try:
            import sounddevice
        except ImportError:
            raise RuntimeError("this Python has no way to open the microphone "
                               "(sounddevice is not installed). The ear is not listening.")
        with self._lock:
            if self._stream is not None:
                return

            def arrived(indata, frames, time, status):
                self.hear([row[0] for row in indata.tolist()])

            self._stream = sounddevice.InputStream(samplerate=RATE, channels=1,
                                                   dtype="float32", callback=arrived)
            self._stream.start()

    def stop(self) -> None:
        with self._lock:
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
                self._stream = None

    # -- inside --

    def _floor(self) -> float:
        return min(self._levels) if self._levels else 0.0

    def _step(self, frame) -> list:
        level, crossings = rms(frame), zcr(frame)
        ms = 1000 * self._t / RATE
        self._levels.append(level)
        floor = self._floor()
        if self._open is None:
            if level < floor + ONSET:
                return self._the_room(frame, floor)
            self._open = {"start_ms": ms, "peak": level, "peak_ms": ms, "samples": [],
                          "f0s": [], "zcrs": [], "tape": []}
        u = self._open
        locked = yin(frame) if len(u["tape"]) % 2 == 0 else None
        f0 = locked[0] if locked and locked[1] > LOCK else None
        if f0 is not None:
            u["f0s"].append(f0)
        u["zcrs"].append(crossings)
        u["samples"].extend(frame[:HOP])
        if level > u["peak"]:
            u["peak"], u["peak_ms"] = level, ms
        if len(u["tape"]) < TAPE_CAP:
            u["tape"].append({"t_ms": round(ms - u["start_ms"], 1), "rms": round(level, 5),
                              "zcr": round(crossings, 4),
                              "f0": None if f0 is None else round(f0, 2)})
        if level < floor + OFFSET and ms - u["start_ms"] >= MIN_MS:
            return self._close(ms, frame, floor)
        return []

    def _the_room(self, frame, floor: float) -> list:
        """Between events: the room as it stands. Given only when it changes."""
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
        return [] if came is None else [came]

    def _close(self, ms: float, frame, floor: float) -> list:
        u, self._open = self._open, None
        voiced = len(u["f0s"]) >= 2
        f0 = statistics.median(u["f0s"]) if voiced else None
        words = self._words.catch(u["samples"])
        if words["words"]:
            shape = {"heard": "words", "words": words["words"]}
        else:
            shape = {"heard": "a sound", "voiced": voiced,
                     "note": note_of(f0) if f0 is not None else "no lock"}
        what = {"duration_ms": round(ms - u["start_ms"], 1), "peak_rms": round(u["peak"], 5),
                "attack_ms": round(u["peak_ms"] - u["start_ms"], 1),
                "f0_hz": None if f0 is None else round(f0, 2),
                "zcr_mean": round(sum(u["zcrs"]) / len(u["zcrs"]), 4),
                "voiced": voiced, "words": words, "tape": u["tape"]}
        clock = "the ear " + now()
        came = [self._gateway.arrive(self.ORGAN, "sound", gave(what, shape, clock))]
        self._room = None                     # the room is given again after every event
        came.extend(self._the_room(frame, floor))
        return [c for c in came if c is not None]
