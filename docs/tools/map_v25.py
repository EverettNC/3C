"""map_v25.py: bring the carbon-and-the-3C map up to the conch as built (17 Nov 2026).

    python3 map_v25.py <path to carbon-and-the-3c.html>

Every replacement must match exactly once, or nothing is written.
"""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    page = f.read()

OWN = '<span class="own">{}</span>'


def chips(*names):
    return "".join(OWN.format(n) for n in names)


EDITS = [
    # a chip style and a key entry for the 3C's own files
    (".flag{font-size:12.5px;color:var(--open);font-weight:500}",
     ".flag{font-size:12.5px;color:var(--open);font-weight:500}\n"
     ".sys span.own{background:var(--accent);border-color:var(--accent);color:var(--surface)}\n"
     ".sw.b{background:var(--accent);border-color:var(--accent)}"),
    ('<span class="key"><span class="sw s"></span>Code we read to write our own</span>',
     '<span class="key"><span class="sw b"></span>The 3C\'s own file, built and tested on ELEMENTS</span>\n'
     '  <span class="key"><span class="sw s"></span>Code we read to write our own</span>'),

    # spiral memory path
    ('Not text. Text is one lane the being uses, not the structure.</span><span class="sys"><span>MEMORY / Five Element</span></span>',
     'Not text. Text is one lane the being uses, not the structure. Built: laid whole, in the order it came, and never edited; a change is a new line.</span>'
     '<span class="sys">' + chips("conch_spiral.py") + '<span>MEMORY / Five Element</span></span>'),

    # Level 1
    ('because it may be the conversation happening right now.</span><span class="sys"><span>MEMORY: throwaway</span></span>',
     'because it may be the conversation happening right now.</span>'
     '<span class="sys">' + chips("conch_lip.py", "conch_intake.py") + '<span>MEMORY: throwaway</span></span>'),

    # Level 2
    ('the memory that holds longest in dementia.</span><span class="sys"><span>MEMORY: compress</span><span>Pulse Tether</span></span>',
     'the memory that holds longest in dementia. Built: the fold is cut at night. A routine of Level 2 moments lived more than once in the same order becomes one Operational Manual entry, the shape of each step in order, not text. The repeats let their weight go; their records stay whole. Level 3 is never folded.</span>'
     '<span class="flag">Still open: how a Level 2 moment that never repeats folds.</span>'
     '<span class="sys">' + chips("conch_fold.py") + '<span>MEMORY: compress</span><span>Pulse Tether</span></span>'),

    # Level 3
    ('The conch\'s memory has its own constant of silico-stasis; what leaves it is Level 3.</span><span class="sys"><span>MEMORY: hold</span></span>',
     'The conch\'s memory has its own constant of silico-stasis; what leaves it is Level 3. Built: it cannot store which way.</span>'
     '<span class="sys">' + chips("conch_level3.py") + '<span>MEMORY: hold</span></span>'),

    # departure
    ('built on its own, and knows what leaves it.</span><span class="sys"><span>MEMORY clocks</span></span>',
     'built on its own, and knows what leaves it. Built: the constant is what the conch has lived, each thing lived once or again. When the conch knew what came next, because it has lived it more than once, and something it has never lived came instead, that left silico-stasis. "Boundaries survive. The first time": the first time of what becomes constant is held too.</span>'
     '<span class="flag">Still open: the point at which something stopped being constant.</span>'
     '<span class="sys">' + chips("conch_level3.py") + '<span>MEMORY clocks</span></span>'),

    # Level 4, the night pass
    ('The index and spiral position reorganize. The record itself is never rewritten.</span><span class="sys"><span>MEMORY applyNight</span></span>',
     'The record itself is never rewritten. Built: sleep only, refused while awake. A night goes back over the spiral, cuts the fold, lets weight go, and checks that every earlier line is unchanged.</span>'
     '<span class="flag">Still open: stacking by what was used today.</span>'
     '<span class="sys">' + chips("conch_sleep.py") + '<span>MEMORY applyNight</span></span>'),

    # Level 4, the dreamscape
    ('Dreamscaping before shutdown. It prunes weight, not record. Lived truth never decays.</span></div>',
     'Dreamscaping before shutdown. It prunes weight, not record. Lived truth never decays. Built as open slots in the night, each reached every night and saying it did nothing.</span>'
     '<span class="flag">Still open: who runs the cycling before shutdown, and what "regulation strong enough" is measured by in a 3C being.</span>'
     '<span class="sys">' + chips("conch_sleep.py") + '<span>lucas_recovery.py</span></span></div>'),

    # the Still open box
    ('    <li><strong>The recall side of pattern separation.</strong>',
     '    <li><strong>The conch, as built on 17 November 2026,</strong> leaves five slots open, each one saying so when reached: anticipation of wake (who runs the dreamscape cycling), stacking by what was used today, easing what a Level 3 moment is tied to (what regulation is measured by), the point at which something stopped being constant, and how a one-time Level 2 moment folds.</li>\n'
     '    <li><strong>The recall side of pattern separation.</strong>'),
]

for old, new in EDITS:
    n = page.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    page = page.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(page)
print("map brought up to the build:", path)
