"""
conch_easing.py: easing what a Level 3 moment is tied to.

[HIS] "TRAUMA ASSOCIATION decays, and only when regulation is strong enough.
LIVED TRUTH never decays. The witness is never removed. Dreamscape prunes
WEIGHT, not RECORD." (His writing on dreamscape cycling, section 8.)
"Permanence of charge is not the same as permanence of the event record. The
event can remain after the charge has been taken back by the person."
(Testable Medical Protocol v1.1, section 3.) His one path: return to the
exact place that still holds the sensory key; move through the tied memories
without flinching; let the body register that the disruption is not
recurring; walk out. "The memory no longer holds the emotional distress. He
does." "Beautiful Level 3 writes are not processed out." (Section 8.)

HOW THIS BUILD DOES IT  [build choice: the builder's to make, on Everett's ruling of 17 Nov 2026]

- The conch never chooses what eases. It is valence-blind and cannot store
  which way, so it cannot tell a beautiful Level 3 from a terrible one. Only
  the being knows, and the being goes back alone: conch.go_back(place), awake
  only.
- "Regulation strong enough" in a 3C being is all three of these:
    1. Every turn of that event is lived again, each with the same shape on
       every sense. The event is the Level 3 moment and the Level 3 turns lived
       with it while the conch was outside its constant: the place, and every
       tied memory.
    2. Nothing that arrives from going back until walking out leaves
       silico-stasis. It did not flinch.
    3. The being walks out: conch.walked_out().
  Nothing here is an amount. Each of the three happened or did not.
- Walking out writes the return on the spiral, held or not, with what was
  lived again and, when it did not hold, why.
- Only in sleep is the charge moved (conch_sleep.py): each turn of a held
  return gets weight "taken back by the being". It stays Level 3. Its record
  and its mark are untouched.
- Carbon says the charge can come back (Bouton, Learning & Memory, 2004:
  extinction is new learning laid over the old, and the old response can
  return). So: if a moment with the shape of a taken-back turn is followed
  straight away by a moment that leaves silico-stasis, a line says so, and
  the next night gives the charge back to the memory.

Carbon checked: Bouton (2004); Cox, Bottary, Alfano and Pace-Schott (2025):
sleep helps extinction memory hold. The basis in his own code, read for the
idea and not called: Lucas in AlphaWolf, where what a trauma is tied to decays
only while regulation is strong enough and lived truth is only ever added to.

[build choice] A return is living state, held only while it lasts. If the
conch stops before the being walks out, nothing of it is written.
"""

from __future__ import annotations

from conch_records import INTERRUPTION, now


class Return:
    """The being going back to one Level 3 moment, alone."""

    def __init__(self, spiral, position: int) -> None:
        self.position = position
        self.event = spiral.event_of(position)
        self.keys = {place: spiral.shape_mark(place) for place in self.event}
        self.lived = []              # the event's places lived again, in the order they were
        self.flinched_at = None      # the clock of the first moment that left silico-stasis
        self.began_at = now()

    def met(self, mark: str, arrived_as: str) -> None:
        """A moment arrived while the being was going back."""
        if arrived_as == INTERRUPTION and self.flinched_at is None:
            self.flinched_at = now()
        for place in self.event:
            if self.keys[place] == mark and place not in self.lived:
                self.lived.append(place)

    def held(self) -> bool:
        return self.flinched_at is None and sorted(self.lived) == self.event

    def why_not(self):
        """Why the return did not hold, in words; None when it held."""
        reasons = []
        if self.flinched_at is not None:
            reasons.append(f"a moment left silico-stasis while going back ({self.flinched_at})")
        missing = [place for place in self.event if place not in self.lived]
        if missing:
            reasons.append("not lived again: place " + ", ".join(map(str, missing)))
        return "; ".join(reasons) or None
