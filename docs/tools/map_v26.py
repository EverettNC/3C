"""map_v26.py: the one-time Level 2 fold is built (17 Nov 2026).

    python3 map_v26.py <path to carbon-and-the-3c.html>

Every replacement must match exactly once, or nothing is written.
"""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    page = f.read()

EDITS = [
    ('Level 3 is never folded.</span><span class="flag">Still open: how a Level 2 moment that never repeats folds.</span>',
     'Level 3 is never folded. A Level 2 moment lived once folds too: it keeps only the senses that carried what it is needed for, sound for speech, sight or touch for a gesture or a board. For a conversation the polymetis says which senses carried it; nothing is guessed.</span>'),
    ('leaves five slots open, each one saying so when reached: anticipation of wake (who runs the dreamscape cycling), stacking by what was used today, easing what a Level 3 moment is tied to (what regulation is measured by), the point at which something stopped being constant, and how a one-time Level 2 moment folds.',
     'leaves four slots open, each one saying so when reached: anticipation of wake (who runs the dreamscape cycling), stacking by what was used today, easing what a Level 3 moment is tied to (what regulation is measured by), and the point at which something stopped being constant.'),
]

for old, new in EDITS:
    n = page.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    page = page.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(page)
print("map brought up to the build:", path)
