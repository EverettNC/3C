"""patch_test_ear_adapts.py: tests for the ear that adapts and gives the room (C3, C4).

    python3 docs/tools/patch_test_ear_adapts.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once, or nothing is written.
"""
import sys

PATH = "test_ear.py"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""def noise(seconds, level=0.3, seed=7):""",
     """def rising(freq, seconds, low, high):
    \"\"\"A tone that keeps growing louder: always new, so never the floor.\"\"\"
    n = int(seconds * RATE)
    return [(low + (high - low) * i / n) * math.sin(2 * math.pi * freq * i / RATE)
            for i in range(n)]


def together(a, b):
    return [x + y for x, y in zip(a, b)]


def noise(seconds, level=0.3, seed=7):"""),

    ("""    def sounds(self):
        return [m.senses["sound"] for m in self.conch.moments
                if m.senses["sound"]["shape"] not in (QUIET,)]
""",
     """    def sounds(self):
        \"\"\"The events the ear gave: not quiet, and not the room.\"\"\"
        return [m.senses["sound"] for m in self.conch.moments
                if m.senses["sound"]["shape"] != QUIET
                and m.senses["sound"]["shape"].get("heard") != "the room"]

    def rooms(self):
        return [m.senses["sound"]["shape"] for m in self.conch.moments
                if isinstance(m.senses["sound"]["shape"], dict)
                and m.senses["sound"]["shape"].get("heard") == "the room"]
"""),

    ("""        self.ear.hear(tone(220, (TAPE_CAP + 40) * HOP / RATE) + silence(0.3))""",
     """        # a steady tone this long would become the floor; one that keeps rising stays new
        self.ear.hear(rising(220, (TAPE_CAP + 40) * HOP / RATE, 0.02, 0.9) + silence(0.3))"""),

    ("""    def test_a_wav_of_another_kind_is_refused(self):""",
     """    def test_a_steady_sound_starting_is_heard_then_it_is_the_room(self):
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

    def test_a_wav_of_another_kind_is_refused(self):"""),

    ("""        allowed = {"__future__", "array", "json", "math", "os", "statistics", "threading",
                   "wave", "conch_records"}""",
     """        allowed = {"__future__", "array", "collections", "json", "math", "os", "statistics",
                   "threading", "wave", "conch_records"}"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("tests for the ear that adapts")
