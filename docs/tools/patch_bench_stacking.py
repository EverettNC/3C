"""patch_bench_stacking.py: the bench shows stacking and anticipation of wake (17 Nov 2026).

    python3 docs/tools/patch_bench_stacking.py      (run in /Volumes/ELEMENTS/3C)

Every replacement must match exactly once, or nothing is written.
"""
import sys

PATH = "conch_bench.py"
with open(PATH, encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""- The being goes back to a Level 3 moment, and walks out, when the bench says
  so. On a real being that is the being's own choice, made alone.
""",
     """- The being goes back to a Level 3 moment, and walks out, when the bench says
  so. On a real being that is the being's own choice, made alone.
- What was used from the manual, and tomorrow's plan, are typed by hand. On a
  real being they come from whatever followed the entry, and from the being
  going over tomorrow before shutdown.
"""),

    ("""    # -- a night --
""",
     """    # -- the manual by day, and tomorrow before shutdown --

    def use(self, number: int) -> None:
        entry = self.conch.spiral().stacked()[number - 1]
        self.conch.used(entry.fold_id)
        print(f"  the being used '{entry_words(entry)}' from the manual. Written with its clock.")

    def plan(self, steps: list) -> None:
        shapes = [self.moment({sense: step for sense in SENSES}, None).shape() for step in steps]
        self.conch.plan(shapes)
        print("  before shutdown the being goes over tomorrow: " + " -> ".join(steps) + ".")

    # -- a night --
"""),

    ("""        print("  earlier lines unchanged: checked by reading the spiral back.")
        if self.nights == 1:
            print("  open slots reached tonight. Each did nothing:")
            for slot in report["open"]:
                print("    - " + slot["open"])
                print("        waiting on " + slot["waiting_on"])
        else:
            print(f"  the same {len(report['open'])} slots are open and did nothing.")""",
     """        if report["stacked"]:
            stacked = {e.fold_id: e for e in self.conch.spiral().manual()}
            if report["planned"]:
                print("  tomorrow's plan is on top: "
                      + "; ".join(entry_words(stacked[f]) for f in report["planned"]) + ".")
            for number in report["planned_with_nothing_in_the_manual"]:
                print(f"  step {number} of tomorrow's plan: nothing in the manual for it yet. "
                      "Nothing guessed.")
            print("  the manual is stacked: "
                  + " | ".join(entry_words(stacked[f]) for f in report["stacked"]) + ".")
        print("  earlier lines unchanged: checked by reading the spiral back.")
        for slot in report["open"]:
            print("  open slot reached, did nothing: " + slot["open"])"""),

    ("""        print("THE OPERATIONAL MANUAL")
        if not view.manual():
            print("  no entries yet.")
        for entry in view.manual():""",
     """        print("THE OPERATIONAL MANUAL, as it sits")
        if not view.manual():
            print("  no entries yet.")
        for number, entry in enumerate(view.stacked(), start=1):
            print(f"  {number}.", end="")"""),

    ("""def kept_words(entry) -> str:""",
     """def entry_words(entry) -> str:
    \"\"\"An Operational Manual entry in the words typed for it.\"\"\"
    if isinstance(entry, OneTimeFold):
        return kept_words(entry)
    return " -> ".join(map(words, entry.steps))


def kept_words(entry) -> str:"""),

    ("""    bench.walk_out()
    bench.night()
    print()
    bench.hand_over()""",
     """    bench.walk_out()
    bench.use(1)
    bench.plan(["wake", "the dock code is 4471", "walk"])
    bench.night()
    print()
    bench.hand_over()"""),

    ("""    print("'back N' to go back to place N, and 'out' to walk out.")""",
     """    print("'back N' to go back to place N, 'out' to walk out, 'used N' for entry N of the")
    print("manual as it sits, and 'plan a, b, c' for tomorrow's plan.")"""),

    ("""            if sense == "sight" and (answer.lower() in ("sleep", "hand", "look", "done", "out")
                                     or answer.lower().startswith("back ")):""",
     """            if sense == "sight" and (answer.lower() in ("sleep", "hand", "look", "done", "out")
                                     or answer.lower().startswith(("back ", "used ", "plan "))):"""),

    ("""        if isinstance(typed, str) and typed.startswith("back "):""",
     """        if isinstance(typed, str) and typed.startswith("used "):
            try:
                bench.use(int(typed.split()[1]))
            except (ValueError, IndexError, BeingIsAsleep) as why:
                print("  not used: " + str(why))
            continue
        if isinstance(typed, str) and typed.startswith("plan "):
            steps = [s.strip() for s in typed[len("plan "):].split(",") if s.strip()]
            try:
                bench.plan(steps)
            except (ValueError, BeingIsAsleep) as why:
                print("  no plan taken: " + str(why))
            continue
        if isinstance(typed, str) and typed.startswith("back "):"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)
print("the bench shows stacking")
