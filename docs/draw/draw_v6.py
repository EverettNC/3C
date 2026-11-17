"""draw_v6.py: the one-time Level 2 fold is built (17 Nov 2026).

    python3 draw_v6.py      (run in the folder that holds build.py, then run build.py)

Every replacement must match exactly once, or nothing is written.
"""
import sys

with open("build.py", encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ('<text class="ts" x="716" y="244">Built: folds each routine into one entry.</text>',
     '<text class="ts" x="716" y="244">Built: folds routines and one-time moments.</text>'),
    ("Stored, and folded at night: each routine lived more than once becomes one entry.</span>",
     "Stored, and folded at night: each routine lived more than once becomes one entry, and a moment lived once keeps only the senses that carried it.</span>"),
    ("Level 3 is never folded.</li>\n",
     "Level 3 is never folded.</li>\n"
     "    <li><strong>A Level 2 moment lived once folds too.</strong> It keeps only the senses that carried what it is needed for: sound for speech, sight or touch for a gesture or a board. For a conversation the polymetis says which senses carried it; nothing is guessed. A moment that says nothing is left whole. If it comes again, its first time is still held as Level 3.</li>\n"),
    ("    <li><strong>How a Level 2 moment that never repeats folds.</strong></li>\n", ""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(src)
print("drawing source brought up to the build")
