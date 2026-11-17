"""
conch_open.py: the marker every open slot returns.

Open means open. An undefined part is a marked, empty slot that says so when
it is reached. It never pretends to work, and it never designs an answer.
Reaching one is kept on the slot, so it shows in every trace.
"""

from __future__ import annotations

from conch_records import now


class Open:
    """An open slot. It does nothing, and it says so."""

    is_open = True

    def __init__(self, slot: str, waiting_on: str) -> None:
        self.slot = slot
        self.waiting_on = waiting_on
        self.reached = []            # the clock of every time it was reached

    def reach(self) -> dict:
        at = now()
        self.reached.append(at)
        return {"open": self.slot, "waiting_on": self.waiting_on, "reached_at": at,
                "did": "nothing"}

    def __repr__(self) -> str:
        return f"OPEN: {self.slot}. Waiting on: {self.waiting_on}."
