"""
conch_intake.py: the intake filter, at the lip.

"Information comes in, filters through the conch and flows over it."

The filter sorts a moment as it arrives, by Everett's definitions. It is not a
gate that scores, and nothing here weighs one moment against another.

  Level 3  It left the conch's own silico-stasis. The conch knows that itself
           (conch_level3.py) and tells the filter. Nothing else reaches Level 3.
  Level 2  It did not leave silico-stasis, and it is what the being needs in
           order to function: education, operational and procedural
           information, structure, and the important parts of a conversation.
           "It's the sustain. It's the operating software... and that's learned
           through repetition."
  Level 1  Everything else: the bullshit of the day that doesn't require
           remembering, like the cup of coffee. "The lip is level one." It
           falls off.

Coming around again does not turn Level 1 into Level 2. The cup of coffee comes
every morning and is still the cup of coffee.

[build choice] What the being needs a moment for arrives with the moment
(Moment.needed_for). The part of the 3C that reads it off a moment has not been
built, so on the bench a person says it. A word the filter does not know stops
the moment with the reason. It is never guessed, because a guess would drop
something the being needs.
"""

from __future__ import annotations

from conch_records import LEVEL_1, LEVEL_2, LEVEL_3, NEEDED_FOR


def sort_at_the_lip(left_silico_stasis: bool, needed_for) -> str:
    """Where one moment goes: level_3, level_2, or level_1 (off the lip)."""
    if not isinstance(left_silico_stasis, bool):
        raise TypeError("whether a moment left silico-stasis is yes or no, and only the conch's "
                        "own constant says it")
    if left_silico_stasis:
        return LEVEL_3
    if needed_for is None:
        return LEVEL_1
    if needed_for in NEEDED_FOR:
        return LEVEL_2
    raise ValueError(f"needed_for is one of {', '.join(NEEDED_FOR)}, or nothing at all; "
                     f"not {needed_for!r}")
