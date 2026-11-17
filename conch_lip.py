"""
conch_lip.py: the lip.

Level 1 falls off here, outside. It never enters the conch and is never
absorbed as space. It is not thrown away: it goes straight to the polymetis,
because it may be the conversation the being is having right now.

So this file touches no file and holds nothing. It turns a moment that fell
off into a LipDrop, and the conch hands the drop to the polymetis at the next
hand-over. A drop that has not been handed over when the conch stops is gone.
That is what never stored means.
"""

from __future__ import annotations

from conch_records import LipDrop, Moment, now


def fall_off(moment: Moment) -> LipDrop:
    """The moment fell off the lip. It is whole, it has its clock, and it is
    living state: on its way to the polymetis, never on the spiral."""
    return LipDrop(moment=moment, fell_at=now())
