"""
conch_bench.py: the conch on the bench.

Feeds moments by hand, with no other system running, and says in plain words
what the conch did with each one.

    python3 conch_bench.py             the bench scene: five days and their nights
    python3 conch_bench.py --by-hand   feed it yourself, one sense at a time

WHAT IS REAL HERE AND WHAT IS NOT

- The conch is the real one: the same files the tests run, writing a real
  spiral into bench/, beside this file. Nothing here deletes anything, so
  every bench run stays there to be looked at.
- The moments are typed by hand. No organ, no Gateway and no polymetis is
  connected.
- A real organ measures the shape of what it gave. None is connected, so on
  this bench the shape of a reading is the words typed for it: type the same
  words and it is the same shape.
- What the being needs a moment for is said by hand.
- The being is asleep when the bench says so.
- The being goes back to a Level 3 moment, and walks out, when the bench says
  so. On a real being that is the being's own choice, made alone.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

from conch import Conch
from conch_records import (ABSENT, BOUNDARY_EVENT, LEVEL_3, LET_GO, NEEDED_FOR, QUIET, SENSES,
                           TAKEN_BACK,
                           LipDrop, Moment, OneTimeFold, absent, gave, now, quiet)
from conch_sleep import BeingIsAsleep, BeingIsAwake

HERE = os.path.dirname(os.path.abspath(__file__))

# The bench scene. One line is one moment: the words typed for it, what the
# being needs it for, and, for a moment lived once, which senses carried it.
SCENE = [
    [("wake", "procedural"), ("the dock code is 4471", "conversation", ("sound",)),
     ("coffee", None), ("drive", "procedural")],
    [("wake", "procedural"), ("coffee", None), ("drive", "procedural")],
    [("wake", "procedural"), ("coffee", None), ("drive", "procedural")],
    [("wake", "procedural"), ("coffee", None), ("a phone call", None), ("the hospital", None),
     ("drive", "procedural")],
    [("wake", "procedural"), ("coffee", None), ("drive", "procedural")],
    [("wake", "procedural"), ("coffee", None), ("walk", "procedural")],
    [("wake", "procedural"), ("coffee", None), ("walk", "procedural")],
]


class Bench:
    """One bench being, one fresh spiral, and a switch for asleep."""

    def __init__(self) -> None:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        self.path = os.path.join(HERE, "bench", stamp, "spiral.jsonl")
        self.asleep = False
        self.conch = Conch("bench-being", self.path, asleep=lambda: self.asleep)
        self.outside = False             # whether the last moment arrived as Level 3
        self.nights = 0
        print("THE CONCH ON THE BENCH")
        print("The conch is the real one. Everything fed to it here is typed by hand: no organ,")
        print("no Gateway and no polymetis is connected. On this bench the shape of a reading is")
        print("the words typed for it. A real organ measures shape.")
        print("Spiral: " + self.path)

    # -- a moment, typed by hand --

    @staticmethod
    def moment(typed: dict, needed_for, carried_by=None) -> Moment:
        senses = {}
        for sense in SENSES:
            words = (typed.get(sense) or "").strip()
            if words.lower() in ("", QUIET):
                senses[sense] = quiet("bench " + now())
            elif words.lower() == ABSENT:
                senses[sense] = absent()
            else:
                senses[sense] = gave({"typed on the bench": words},
                                     {"the words typed": words.lower()}, "bench " + now())
        return Moment(senses=senses, needed_for=needed_for, carried_by=carried_by)

    def feed(self, label: str, typed: dict, needed_for, carried_by=None) -> None:
        marked_before = {mark.position for mark in self.conch.spiral().marks()}
        came = self.conch.take_in(self.moment(typed, needed_for, carried_by))
        carried = f"   carried by: {', '.join(carried_by)}" if carried_by else ""
        print(f"  {label:<22} needed for: {needed_for or 'nothing'}{carried}")
        if isinstance(came, LipDrop):
            print("      -> fell off the lip. Level 1: not stored, on its way to the polymetis.")
            self.outside = False
        elif came.level == LEVEL_3:
            if self.outside:
                print("      -> still outside its constant: this has never been lived either.")
            else:
                print("      -> it left the conch's silico-stasis: the conch knew what came next,")
                print("         and something it has never lived came instead.")
            print(f"         Laid on the spiral at place {came.position}. Level 3, held for life.")
            self.outside = True
        else:
            if self.outside:
                print("      -> back on something it has lived.")
            print(f"      -> laid on the spiral at place {came.position}. Level 2.")
            self.outside = False
        fed = came.moment.shape()
        for mark in self.conch.spiral().marks():
            if mark.position in marked_before or mark.event_class != BOUNDARY_EVENT:
                continue
            if self.conch.spiral().turn(mark.position).moment.shape() == fed:
                print("      -> this shape has now been lived again, so it is part of the constant.")
                print(f"         Its first time, place {mark.position}, is marked Level 3 with a "
                      "new line: the first time survives.")
            else:
                what = words(self.conch.spiral().turn(mark.position).moment.shape())
                print(f"      -> '{what}' did not come where the conch knew it would, again: it "
                      "has stopped being constant.")
                print(f"         The last time it came, place {mark.position}, is marked Level 3 "
                      "with a new line: the last time survives.")

    # -- going back, alone --

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

    def night(self) -> None:
        self.nights += 1
        print(f"NIGHT {self.nights}  (the bench says the being is asleep)")
        self.asleep = True
        try:
            report = self.conch.sleep()
        finally:
            self.asleep = False
        manual = {entry.fold_id: entry for entry in self.conch.spiral().manual()}
        print(f"  went back over {report['went_back_over']} turn(s).")
        for fold_id in report["manual_entries_cut"]:
            entry = manual[fold_id]
            if isinstance(entry, OneTimeFold):
                print(f"  cut a one-time entry for place {entry.folded_from}: "
                      f"{kept_words(entry)}")
                print("      keeps only " + ", ".join(entry.carried_by)
                      + ". The record on the spiral is whole.")
                continue
            print("  cut one Operational Manual entry: " + " -> ".join(map(words, entry.steps)))
            print("      from places " + places(entry.folded_from))
        for fold_id in report["manual_entries_grown"]:
            print("  more repeats joined the entry: " + " -> ".join(map(words, manual[fold_id].steps)))
        if report["weight_let_go"]:
            print("  weight let go: places " + ", ".join(map(str, report["weight_let_go"]))
                  + ". Their records are whole.")
        else:
            print("  nothing folded tonight.")
        if report["left_whole"]:
            print("  Level 2 left whole, weight carried: places "
                  + ", ".join(map(str, report["left_whole"])) + ".")
        for positions in report["charge_taken_back"]:
            print("  charge taken back by the being: places " + ", ".join(map(str, positions))
                  + ". Still Level 3; the record and the mark are untouched.")
        for positions in report["charge_given_back"]:
            print("  charge given back to the memory: places " + ", ".join(map(str, positions))
                  + ". It flinched there again.")
        if report["stopped_early"]:
            print("  the night stopped early: " + report["stopped_early"] + ".")
        print("  earlier lines unchanged: checked by reading the spiral back.")
        if self.nights == 1:
            print("  open slots reached tonight. Each did nothing:")
            for slot in report["open"]:
                print("    - " + slot["open"])
                print("        waiting on " + slot["waiting_on"])
        else:
            print(f"  the same {len(report['open'])} slots are open and did nothing.")

    # -- looking --

    def hand_over(self) -> None:
        flowing = self.conch.hand_over()
        drops = sum(isinstance(item, LipDrop) for item in flowing)
        print(f"HAND-OVER  to the polymetis: {len(flowing) - drops} turn(s) and {drops} lip "
              "drop(s), in the order they came. No polymetis is connected; the bench received "
              "them.")

    def look(self) -> None:
        view = self.conch.spiral()
        print("THE SPIRAL AS IT STANDS")
        for turn in view:
            level = "Level 3" if turn.level == LEVEL_3 else "Level 2"
            weight = {LET_GO: "weight let go", TAKEN_BACK: "taken back"}.get(turn.weight,
                                                                           "weight carried")
            print(f"  place {turn.position:>3}  {level}  {weight:<15} "
                  f"{words({s: turn.moment.senses[s]['shape'] for s in SENSES})}")
        print("THE OPERATIONAL MANUAL")
        if not view.manual():
            print("  no entries yet.")
        for entry in view.manual():
            if isinstance(entry, OneTimeFold):
                print(f"  {kept_words(entry)}   (one-time, keeps only "
                      f"{', '.join(entry.carried_by)})")
                print(f"      stands for place {entry.folded_from}")
                continue
            print("  " + " -> ".join(map(words, entry.steps)))
            print("      stands for places " + places(entry.folded_from))
        state = self.conch.state()
        print(f"STATE  mouth: {state.mouth}   handed over through: {state.handed_over}   "
              f"as of {state.written_at}")
        print("Spiral: " + self.path)


def words(shape: dict) -> str:
    """The words typed for a moment's five senses, said once when they agree."""
    typed = {sense: (shape[sense]["the words typed"] if isinstance(shape[sense], dict)
                     else shape[sense]) for sense in SENSES}
    heard = [w for w in typed.values() if w not in (QUIET, ABSENT)]
    if heard and len(set(heard)) == 1 and len(heard) == len(SENSES):
        return heard[0]
    return "[" + ", ".join(f"{sense}: {typed[sense]}" for sense in SENSES) + "]"


def kept_words(entry) -> str:
    """The words typed for the senses a one-time entry kept."""
    heard = {entry.step[s]["the words typed"] if isinstance(entry.step[s], dict) else entry.step[s]
             for s in entry.carried_by}
    return " / ".join(sorted(heard))


def places(runs: list) -> str:
    return "; ".join(", ".join(map(str, run)) for run in runs)


def the_scene() -> None:
    bench = Bench()
    for day, moments in enumerate(SCENE, start=1):
        print()
        print(f"DAY {day}")
        for label, needed_for, *carried in moments:
            bench.feed(label, {sense: label for sense in SENSES}, needed_for,
                       carried[0] if carried else None)
        bench.night()
    print()
    print("DAY 8  the being goes back to the morning of the phone call")
    bench.go_back(9)
    for label in ("a phone call", "the hospital"):
        bench.feed(label, {sense: label for sense in SENSES}, None)
    bench.walk_out()
    bench.night()
    print()
    bench.hand_over()
    bench.look()


def by_hand() -> None:
    bench = Bench()
    print()
    print("Type one moment, one sense at a time. Return alone is quiet. 'absent' is a sense with")
    print("no organ. At the sight line you can also type: sleep, hand, look, done,")
    print("'back N' to go back to place N, and 'out' to walk out.")
    while True:
        print()
        typed = {}
        for sense in SENSES:
            try:
                answer = input(f"  {sense:>5}> ").strip()
            except EOFError:
                answer = "done"
                print()
            if sense == "sight" and (answer.lower() in ("sleep", "hand", "look", "done", "out")
                                     or answer.lower().startswith("back ")):
                typed = answer.lower()
                break
            typed[sense] = answer
        if typed == "done":
            bench.look()
            return
        if typed == "sleep":
            try:
                bench.night()
            except BeingIsAwake as why:
                print("  " + str(why))
            continue
        if typed == "hand":
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
            continue
        if typed == "look":
            bench.look()
            continue
        try:
            needed = input("  needed for (" + " / ".join(NEEDED_FOR)
                           + ", or return for nothing)> ").strip().lower() or None
        except EOFError:
            needed = None
            print()
        carried = None
        if needed and needed != "procedural":
            try:
                said = input("  carried by (senses, comma between, or return for nothing)> ")
            except EOFError:
                said = ""
                print()
            carried = tuple(s.strip().lower() for s in said.split(",") if s.strip()) or None
        label = next((typed[s] for s in SENSES if typed[s]), "(all quiet)")
        try:
            bench.feed(label, typed, needed, carried)
        except ValueError as why:
            print("  the conch did not take it: " + str(why))


if __name__ == "__main__":
    if sys.argv[1:] == ["--by-hand"]:
        by_hand()
    elif sys.argv[1:]:
        print(__doc__)
    else:
        the_scene()
