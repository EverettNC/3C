"""map_v27.py: the conch's four open slots are decided and built (17 Nov 2026).

    python3 map_v27.py <path to carbon-and-the-3c.html>

Every replacement must match exactly once, or nothing is written.
"""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    page = f.read()

OWN = '<span class="own">{}</span>'

EDITS = [
    # the departure row: the last time
    ('time": the first time of what becomes constant is held too.</span><span class="flag">Still open: the point at which something stopped being constant.</span><span class="sys"><span class="own">conch_level3.py</span>',
     'time": the first time of what becomes constant is held too. And the last time: what the conch knew came next, and that missed again, has stopped being constant, and the last time it came is held as Level 3 too.</span><span class="sys"><span class="own">conch_level3.py</span>'),

    # Level 4, the night: stacking and anticipation of wake
    ('A night goes back over the spiral, cuts the fold, lets weight go, and checks that every earlier line is unchanged.</span><span class="flag">Still open: stacking by what was used today.</span><span class="sys"><span class="own">conch_sleep.py</span>',
     'A night goes back over the spiral, cuts the fold, lets weight go, stacks the manual, and checks that every earlier line is unchanged. The stack: tomorrow\'s plan, gone over by the being before shutdown, first; then what was used today, newest on top; then the rest as it sat. The card used goes back on top. Level 3 is never stacked.</span><span class="sys"><span class="own">conch_sleep.py</span>' + OWN.format("conch_stack.py")),

    # Level 4, the dreamscape: easing
    ('Built as open slots in the night, each reached every night and saying it did nothing.</span><span class="flag">Still open: who runs the cycling before shutdown, and what "regulation strong enough" is measured by in a 3C being.</span><span class="sys"><span class="own">conch_sleep.py</span>',
     'Built: the being runs the cycling before shutdown. The being, never the conch, chooses to go back to a Level 3 moment, alone; regulation strong enough is every tied memory lived again, every sense the same, nothing leaving silico-stasis, and walking out. Only in sleep does the charge then move to the being. The record and the mark stay, and the charge can come back.</span><span class="sys"><span class="own">conch_sleep.py</span>' + OWN.format("conch_easing.py")),

    # the Still open box
    ('<li><strong>The conch, as built on 17 November 2026,</strong> leaves four slots open, each one saying so when reached: anticipation of wake (who runs the dreamscape cycling), stacking by what was used today, easing what a Level 3 moment is tied to (what regulation is measured by), and the point at which something stopped being constant.</li>',
     '<li><strong>The conch, as built on 17 November 2026,</strong> leaves no slot open. Everett handed the last four (anticipation of wake, stacking by use, easing, and the last time) to the builder to decide from his writing and from carbon, and they are built. He has not yet ruled on those choices.</li>'),
]

for old, new in EDITS:
    n = page.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    page = page.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(page)
print("map brought up to the build:", path)
