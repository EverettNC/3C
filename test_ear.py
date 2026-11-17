"""
test_ear.py: the 3C's ear, tested forward.

    python3 -m unittest test_ear -v

Tones are made here with the standard library, so what the ear should lock on
is known. No recording of any being is used here. A test that needs vosk or a
microphone this Python
does not have is skipped with the reason; it never counts as a pass. Files
written here go into test_spirals/, beside this file, and nothing is deleted.
"""

import array
import ast
import math
import os
import random
import unittest
import wave
from datetime import datetime, timezone

import ear
from conch import Conch
from conch_records import QUIET, LipDrop, Turn
from ear import (FRAME, HOP, MODEL_NAME, RATE, TAPE_CAP, Ear, Words, note_of, rms, yin,
                 zcr)
from gateway import Gateway

HERE = os.path.dirname(os.path.abspath(__file__))
THIS_RUN = os.path.join(HERE, "test_spirals", "ear-"
                        + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
                        + "-" + str(os.getpid()))


def tone(freq, seconds, level=0.3):
    return [level * math.sin(2 * math.pi * freq * n / RATE) for n in range(int(seconds * RATE))]


def silence(seconds):
    return [0.0] * int(seconds * RATE)


def rising(freq, seconds, low, high):
    """A tone that keeps growing louder: always new, so never the floor."""
    n = int(seconds * RATE)
    return [(low + (high - low) * i / n) * math.sin(2 * math.pi * freq * i / RATE)
            for i in range(n)]


def together(a, b):
    return [x + y for x, y in zip(a, b)]


def noise(seconds, level=0.3, seed=7):
    r = random.Random(seed)
    return [level * (2 * r.random() - 1) for _ in range(int(seconds * RATE))]


def vosk_here():
    try:
        import vosk  # noqa: F401
        return True
    except ImportError:
        return False


class NoWords(Words):
    """Words that are not caught, with a reason, so a test does not depend on vosk."""

    def __init__(self):
        self.model, self.why_not = None, "not caught in this test"


class Catches:
    def __init__(self):
        self.moments = []

    def take_in(self, moment):
        self.moments.append(moment)
        return "taken"


class Measuring(unittest.TestCase):
    def test_yin_locks_on_a_tone_or_says_no_lock(self):
        freq, sure = yin(tone(220, FRAME / RATE))
        self.assertAlmostEqual(freq, 220, delta=2)
        self.assertGreater(sure, ear.LOCK)
        self.assertIsNone(yin(silence(FRAME / RATE)))         # silence is not a note
        self.assertIsNone(yin(noise(FRAME / RATE)))           # noise is no lock, never a guess

    def test_a_note_is_named_without_its_cents(self):
        self.assertEqual(note_of(440), "A4")
        self.assertEqual(note_of(445), "A4")
        self.assertEqual(note_of(220), "A3")
        self.assertEqual(note_of(261.63), "C4")

    def test_rms_and_zero_crossings(self):
        self.assertEqual(rms(silence(0.01)), 0)
        self.assertAlmostEqual(rms(tone(220, 0.1, level=0.3)), 0.3 / math.sqrt(2), places=2)
        self.assertGreater(zcr(noise(0.05)), zcr(tone(220, 0.05)))


class Hearing(unittest.TestCase):
    def setUp(self):
        self.conch = Catches()
        self.gate = Gateway(self.conch)
        self.ear = Ear(self.gate, NoWords())

    def sounds(self):
        """The events the ear gave: not quiet, and not the room."""
        return [m.senses["sound"] for m in self.conch.moments
                if m.senses["sound"]["shape"] != QUIET
                and m.senses["sound"]["shape"].get("heard") != "the room"]

    def rooms(self):
        return [m.senses["sound"]["shape"] for m in self.conch.moments
                if isinstance(m.senses["sound"]["shape"], dict)
                and m.senses["sound"]["shape"].get("heard") == "the room"]

    def test_an_utterance_is_one_event_and_one_reading(self):
        self.ear.hear(silence(0.3) + tone(220, 0.4))
        self.assertEqual(self.sounds(), [])                   # still sounding: nothing closed it
        self.ear.hear(silence(0.3))                           # it fell away: closed, and quiet after
        heard = self.sounds()
        self.assertEqual(len(heard), 1)
        self.assertEqual(heard[0]["shape"], {"heard": "a sound", "voiced": True, "note": "A3"})
        self.assertAlmostEqual(heard[0]["gave"]["f0_hz"], 220, delta=2)
        self.assertGreater(heard[0]["gave"]["duration_ms"], 300)
        self.assertEqual(self.gate.room()["sound"]["shape"], QUIET)   # quiet after it

    def test_two_utterances_are_two_events(self):
        self.ear.hear(tone(220, 0.3) + silence(0.3) + tone(330, 0.3) + silence(0.3))
        self.gate.close()
        notes = [s["shape"]["note"] for s in self.sounds()]
        self.assertEqual(notes, ["A3", "E4"])

    def test_an_unvoiced_sound_has_no_note(self):
        self.ear.hear(noise(0.3) + silence(0.3))
        self.gate.close()
        shape = self.sounds()[0]["shape"]
        self.assertEqual(shape, {"heard": "a sound", "voiced": False, "note": "no lock"})

    def test_silence_alone_is_quiet_and_never_an_event(self):
        self.ear.hear(silence(2))
        self.gate.close()
        self.assertEqual(self.sounds(), [])

    def test_the_shape_holds_no_measurement(self):
        self.ear.hear(tone(220, 0.3) + silence(0.3))
        reading = self.sounds()[0]
        self.assertEqual(set(reading["shape"]), {"heard", "voiced", "note"})
        for name in ("f0_hz", "peak_rms", "zcr_mean", "duration_ms", "tape"):
            self.assertIn(name, reading["gave"])
        self.assertTrue(reading["organ_clock"].startswith("the ear "))

    def test_words_not_caught_are_said_not_caught_never_made_up(self):
        self.ear.hear(tone(220, 0.3) + silence(0.3))
        words = self.sounds()[0]["gave"]["words"]
        self.assertEqual(words, {"caught": False, "why": "not caught in this test",
                                 "words": None})

    def test_the_tape_keeps_its_head_and_drops_its_tail(self):
        # a steady tone this long would become the floor; one that keeps rising stays new
        self.ear.hear(rising(220, (TAPE_CAP + 40) * HOP / RATE, 0.02, 0.9) + silence(0.3))
        self.assertEqual(len(self.sounds()[0]["gave"]["tape"]), TAPE_CAP)

    def test_a_steady_sound_starting_is_heard_then_it_is_the_room(self):
        self.ear.hear(silence(0.5) + tone(110, 6))
        heard = self.sounds()
        self.assertEqual(len(heard), 1)                       # one event, and it closed
        self.assertEqual(heard[0]["shape"]["note"], "A2")
        self.assertGreater(heard[0]["gave"]["duration_ms"], 3000)
        self.assertLess(heard[0]["gave"]["duration_ms"], 4600)
        self.assertEqual(self.gate.room()["sound"]["shape"],
                         {"heard": "the room", "voiced": True, "note": "A2"})
        self.assertIn("floor_rms", self.gate.room()["sound"]["gave"])

    def test_the_room_is_given_only_when_it_changes(self):
        self.ear.hear(silence(0.5) + tone(110, 8))
        self.assertEqual(self.rooms(), [{"heard": "the room", "voiced": True, "note": "A2"}])

    def test_an_utterance_over_a_hum_is_still_an_event_and_the_hum_is_the_room_after(self):
        hum = tone(110, 7.4, level=0.05)
        voice = silence(6) + tone(233, 0.4) + silence(1)
        self.ear.hear(silence(0.5) + together(hum, voice))
        heard = self.sounds()
        self.assertEqual(len(heard), 2)                       # the hum starting, then the voice
        self.assertGreater(heard[1]["gave"]["duration_ms"], 300)
        self.assertLess(heard[1]["gave"]["duration_ms"], 600)
        self.assertEqual(self.gate.room()["sound"]["shape"],
                         {"heard": "the room", "voiced": True, "note": "A2"})

    def test_when_the_hum_stops_the_room_is_quiet_again(self):
        self.ear.hear(silence(0.5) + tone(110, 6) + silence(0.5))
        self.assertEqual(self.gate.room()["sound"]["shape"], QUIET)

    def test_a_wav_of_another_kind_is_refused(self):
        os.makedirs(THIS_RUN, exist_ok=True)
        path = os.path.join(THIS_RUN, "cd-quality.wav")
        with wave.open(path, "wb") as w:
            w.setnchannels(1), w.setsampwidth(2), w.setframerate(44100)
            w.writeframes(array.array("h", [0] * 4410).tobytes())
        with self.assertRaises(ValueError):
            self.ear.hear_wav(path)

class TheWordsAndTheMicrophone(unittest.TestCase):
    def test_without_vosk_or_the_model_the_reason_is_given(self):
        if vosk_here():
            words = Words(model_path=os.path.join(THIS_RUN, "nowhere", MODEL_NAME))
            self.assertIn("was not found", words.why_not)
        else:
            words = Words()
            self.assertIn("vosk is not installed", words.why_not)
        self.assertEqual(words.catch([0.0] * 100)["caught"], False)

    def test_never_a_smaller_model(self):
        if not vosk_here():
            self.skipTest("vosk is not installed in this Python, so no model is opened")
        small = os.path.join(THIS_RUN, "vosk-model-small-en-us-0.15")
        os.makedirs(small, exist_ok=True)
        self.assertIn("never a smaller one", Words(model_path=small).why_not)

    def test_the_microphone_is_not_pretended(self):
        try:
            import sounddevice  # noqa: F401
        except ImportError:
            with self.assertRaises(RuntimeError):
                Ear(Gateway(Catches()), NoWords()).listen()
            return
        self.skipTest("this Python can open the microphone; a test does not open it")


class WithTheRealConch(unittest.TestCase):
    def test_an_utterance_reaches_the_conch_through_the_gateway(self):
        path = os.path.join(THIS_RUN, "with-the-conch", "spiral.jsonl")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        conch = Conch("bench-being", path)
        gate = Gateway(conch)
        the_ear = Ear(gate, NoWords())
        came = the_ear.hear(tone(220, 0.3) + silence(0.3))
        self.assertTrue(came)
        self.assertTrue(all(isinstance(c, (Turn, LipDrop)) for c in came))
        handed = conch.hand_over()
        self.assertTrue(any(isinstance(item, LipDrop) and
                            item.moment.senses["sound"]["shape"]["note"] == "A3"
                            for item in handed if isinstance(item.moment.senses["sound"]["shape"],
                                                             dict)))


class StandsAlone(unittest.TestCase):
    def test_only_the_standard_library_at_the_top(self):
        allowed = {"__future__", "array", "collections", "json", "math", "os", "statistics",
                   "threading", "wave", "conch_records"}
        with open(os.path.join(HERE, "ear.py"), encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.Import):
                for n in node.names:
                    self.assertIn(n.name.split(".")[0], allowed)
            if isinstance(node, ast.ImportFrom):
                self.assertIn(node.module.split(".")[0], allowed)
        with open(os.path.join(HERE, "ear.py"), encoding="utf-8") as f:
            source = f.read()
        for outside in ("whisper", "openai", "google", "requests", "urllib", "http"):
            self.assertNotIn("import " + outside, source)


if __name__ == "__main__":
    unittest.main()
