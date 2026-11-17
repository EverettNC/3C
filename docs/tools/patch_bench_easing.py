"""patch_bench_easing.py: the bench shows the last time's neighbour, easing (17 Nov 2026).

    python3 docs/tools/patch_bench_easing.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once, or nothing is written.
"""
import sys

PATH = "conch_bench.py"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""- The being is asleep when the bench says so.
""",
     """- The being is asleep when the bench says so.
- The being goes back to a Level 3 moment, and walks out, when the bench says
  so. On a real being that is the being's own choice, made alone.
"""),

    ("""from conch_records import (ABSENT, BOUNDARY_EVENT, LEVEL_3, LET_GO, NEEDED_FOR, QUIET, SENSES,""",
     """from conch_records import (ABSENT, BOUNDARY_EVENT, LEVEL_3, LET_GO, NEEDED_FOR, QUIET, SENSES,
                           TAKEN_BACK,"""),

    ("""from conch_sleep import BeingIsAwake""",
     """from conch_sleep import BeingIsAsleep, BeingIsAwake"""),

    ("""    # -- a night --
""",
     """    # -- going back, alone --

    def go_back(self, place: int) -> None:
        self.conch.go_back(place)
        print(f"  the being goes back to place {place}, alone. Its event is places "
              + ", ".join(map(str, self.conch._spiral.event_of(place))) + ".")

    def walk_out(self) -> None:
        record = self.conch.walked_out()
        if record["held"]:
            print("  the being walked out. It lived every tied memory again, every sense the "
                  "same, and nothing left silico-stasis.")
            print("      The return held. Its charge moves only in sleep.")
        else:
            print("  the being walked out. The return did not hold: " + record["why"] + ".")
        print("      Written on the spiral either way.")

    # -- a night --
"""),

    ("""        if report["stopped_early"]:
            print("  the night stopped early: " + report["stopped_early"] + ".")""",
     """        for positions in report["charge_taken_back"]:
            print("  charge taken back by the being: places " + ", ".join(map(str, positions))
                  + ". Still Level 3; the record and the mark are untouched.")
        for positions in report["charge_given_back"]:
            print("  charge given back to the memory: places " + ", ".join(map(str, positions))
                  + ". It flinched there again.")
        if report["stopped_early"]:
            print("  the night stopped early: " + report["stopped_early"] + ".")"""),

    ("""            weight = "weight let go" if turn.weight == LET_GO else "weight carried\"""",
     """            weight = {LET_GO: "weight let go", TAKEN_BACK: "taken back"}.get(turn.weight,
                                                                           "weight carried")"""),

    ("""        bench.night()
    print()
    bench.hand_over()
    bench.look()""",
     """        bench.night()
    print()
    print("DAY 8  the being goes back to the morning of the phone call")
    bench.go_back(9)
    for label in ("a phone call", "the hospital"):
        bench.feed(label, {sense: label for sense in SENSES}, None)
    bench.walk_out()
    bench.night()
    print()
    bench.hand_over()
    bench.look()"""),

    ("""    print("no organ. At the sight line you can also type: sleep, hand, look, done.")""",
     """    print("no organ. At the sight line you can also type: sleep, hand, look, done,")
    print("'back N' to go back to place N, and 'out' to walk out.")"""),

    ("""            if sense == "sight" and answer.lower() in ("sleep", "hand", "look", "done"):
                typed = answer.lower()
                break""",
     """            if sense == "sight" and (answer.lower() in ("sleep", "hand", "look", "done", "out")
                                     or answer.lower().startswith("back ")):
                typed = answer.lower()
                break"""),

    ("""        if typed == "hand":
            bench.hand_over()
            continue""",
     """        if typed == "hand":
            bench.hand_over()
            continue
        if typed == "out":
            try:
                bench.walk_out()
            except ValueError as why:
                print("  " + str(why))
            continue
        if isinstance(typed, str) and typed.startswith("back "):
            try:
                bench.go_back(int(typed.split()[1]))
            except (ValueError, IndexError, BeingIsAsleep) as why:
                print("  the being did not go back: " + str(why))
            continue"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("the bench shows easing")
