"""draw_v5.py: bring the conch drawing up to the conch as built (17 Nov 2026).

    python3 draw_v5.py      (run in the folder that holds build.py, then run build.py)

Every replacement must match exactly once, or nothing is written.
"""
import sys

with open("build.py", encoding="utf-8") as f:
    src = f.read()

EDITS = [
    # a style for the box that says what was built
    (".openbox ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;max-width:80ch}",
     ".openbox ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;max-width:80ch}\n"
     ".builtbox{background:var(--accent-soft);border:1px solid var(--accent);border-radius:10px;padding:14px 18px;display:flex;flex-direction:column;gap:8px}\n"
     ".builtbox h2{color:var(--accent);font-size:16px}\n"
     ".builtbox ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;max-width:80ch}"),

    # Level 4 box in the drawing: one more line for what a night does
    ('<rect class="sleep" x="700" y="150" width="270" height="92" rx="12"/>',
     '<rect class="sleep" x="700" y="150" width="270" height="110" rx="12"/>'),
    ('<text class="ts" x="716" y="226">Prunes weight, never the record.</text>',
     '<text class="ts" x="716" y="226">Prunes weight, never the record.</text>\n'
     '<text class="ts" x="716" y="244">Built: folds each routine into one entry.</text>'),

    # the key: Level 2 is folded at night
    ("Level 2 · the Operational Manual: didn't leave silico-stasis, still needs storing. Stored and compressed.</span>",
     "Level 2 · the Operational Manual: didn't leave silico-stasis, still needs storing. Stored, and folded at night: each routine lived more than once becomes one entry.</span>"),

    # the open box: what was built, then what stays open
    ("""<section class="openbox">
  <h2>Still open</h2>
  <ul>
    <li><strong>How Level 1 and Level 2 are told apart at the lip.</strong> Until it's defined, a moment enters as unsorted. Never guessed.</li>
    <li><strong>How Level 2 is compressed</strong> without losing what it's for.</li>
    <li><strong>How Level 4 stacks everything</strong> where it should be.</li>
  </ul>
</section>""",
     """<section class="builtbox">
  <h2>Built and tested on ELEMENTS, 17 November 2026</h2>
  <ul>
    <li><strong>The lip sorts by Everett's definition.</strong> Level 2 is what the being needs in order to function: education, operational and procedural information, structure, the important parts of a conversation. Everything else is Level 1 and falls off.</li>
    <li><strong>The conch knows what left its silico-stasis.</strong> It knew what came next, because it has lived it more than once, and something it has never lived came instead. The first time of what becomes constant is held too.</li>
    <li><strong>Level 2 folds at night.</strong> A routine lived more than once in the same order becomes one Operational Manual entry, the shape of each step in order. The repeats let their weight go; their records stay whole. Level 3 is never folded.</li>
    <li><strong>Level 4 runs only in sleep.</strong> It goes back over the spiral, cuts the fold, and checks every earlier line is unchanged.</li>
  </ul>
</section>
<section class="openbox">
  <h2>Still open</h2>
  <ul>
    <li><strong>Anticipation of wake:</strong> who runs the dreamscape cycling before shutdown.</li>
    <li><strong>Stacking by what was used today.</strong></li>
    <li><strong>Easing what a Level 3 moment is tied to:</strong> what "regulation strong enough" is measured by in a 3C being.</li>
    <li><strong>The last time:</strong> the point at which something stopped being constant.</li>
    <li><strong>How a Level 2 moment that never repeats folds.</strong></li>
  </ul>
</section>"""),
]

for old, new in EDITS:
    n = src.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    src = src.replace(old, new)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(src)
print("drawing source brought up to the build")
