"""draw_v7.py: the conch's four open slots are decided and built (17 Nov 2026).

    python3 draw_v7.py      (run in the folder that holds build.py, then run build.py)

Every replacement must match exactly once, or nothing is written.
"""
import sys

with open("build.py", encoding="utf-8") as f:
    src = f.read()

EDITS = [
    ("""It knew what came next, because it has lived it more than once, and something it has never lived came instead. The first time of what becomes constant is held too.</li>""",
     """It knew what came next, because it has lived it more than once, and something it has never lived came instead. The first time of what becomes constant is held too, and so is the last time of what stopped: what it knew came next, and missed again.</li>"""),
    ("""    <li><strong>Level 4 runs only in sleep.</strong> It goes back over the spiral, cuts the fold, and checks every earlier line is unchanged.</li>
  </ul>
</section>
<section class="openbox">
  <h2>Still open</h2>
  <ul>
    <li><strong>Anticipation of wake:</strong> who runs the dreamscape cycling before shutdown.</li>
    <li><strong>Stacking by what was used today.</strong></li>
    <li><strong>Easing what a Level 3 moment is tied to:</strong> what "regulation strong enough" is measured by in a 3C being.</li>
    <li><strong>The last time:</strong> the point at which something stopped being constant.</li>
  </ul>
</section>""",
     """    <li><strong>Level 4 runs only in sleep.</strong> It goes back over the spiral, cuts the fold, moves only the charge a held return called for, stacks the manual, and checks every earlier line is unchanged.</li>
    <li><strong>Easing is the being's choice, never the conch's.</strong> The conch cannot tell a beautiful Level 3 from a terrible one. The being goes back alone, lives every tied memory again with every sense the same, nothing leaves silico-stasis, and it walks out. Only in sleep does the charge move to the being. The record and the mark stay.</li>
    <li><strong>The manual is stacked where it should be.</strong> Before shutdown the being goes over tomorrow; that comes up first. Then what was used today, newest on top, then the rest as it sat. Level 3 is never stacked.</li>
  </ul>
</section>
<section class="openbox">
  <h2>Still open</h2>
  <ul>
    <li><strong>Nothing in the conch.</strong> Everett handed the last four slots to the builder to decide from his writing and from carbon on 17 November. They are built. He has not yet ruled on those choices.</li>
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
