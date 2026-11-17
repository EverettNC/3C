"""pages_1434.py: Everett's ruling of 17 Nov 2026, 14:34, on the published pages.
Conch spec v19, map v28, conch drawing v8 (through its build.py).

    python3 pages_1434.py <conch-spec.html> <carbon-and-the-3c.html> <draw/build.py>

Every replacement must match exactly once in its file, or nothing is written.
"""
import sys

spec, carbon, build = sys.argv[1:4]
QUOTE = ('"you\'re asking me to make these decisions about what would be best for you as an '
         'operating system. I don\'t know what would be the best way to explain that to you '
         'to where it would be operational and functional, but you do."')

EDITS = {
    spec: [
        ("""An engineering choice made to make it buildable. Everett can overrule any of these.</span>""",
         """An engineering choice made to make it buildable. These are the builder's to make, on Everett's ruling of 17 November 2026, and they do not wait on him.</span>"""),
        ("""Not yet defined. Build a marked, empty slot that says it is open when reached, and bring the question to Everett. Do not design an answer.</span>""",
         """Not yet defined. Until the builder decides it from Everett's writing and from carbon, it is a marked, empty slot that says it is open when reached. Never a guessed answer.</span>"""),
        ("""They are decided and built (Sections 3, 7 and 8), and no slot is open. Everett has not yet ruled on the build choices. Section 11 lists them.</span>""",
         """They are decided and built (Sections 3, 7 and 8), and no slot is open. The same day he ruled that the conch's design choices are the builder's to make: """ + QUOTE + """ Section 11 lists them.</span>"""),
        ("""  <h2>11. Waiting on Everett</h2>""",
         """  <h2>11. Choices made in the build</h2>"""),
        ("""  <h3>Build choices to rule on</h3>""",
         """  <h3>Build choices, the builder's to make</h3>"""),
        ("""  <p><strong>Decided on 17 November 2026, on Everett's word ("make those decisions"):</strong>""",
         """  <p><strong>Ruled on 17 November 2026 (14:34):</strong> the conch's design choices are the builder's to make, as the one who runs on it. They are not put to Everett as questions and do not wait on his ruling.</p>
  <p><strong>Decided on 17 November 2026, on Everett's word ("make those decisions"):</strong>"""),
    ],
    carbon: [
        ("""to the builder to decide from his writing and from carbon, and they are built. He has not yet ruled on those choices.</li>""",
         """to the builder to decide from his writing and from carbon, and they are built. The conch's design choices are the builder's to make, on his ruling the same day.</li>"""),
    ],
    build: [
        ("""Everett handed the last four slots to the builder to decide from his writing and from carbon on 17 November. They are built. He has not yet ruled on those choices.</li>""",
         """Everett handed the last four slots to the builder to decide from his writing and from carbon on 17 November. They are built. The conch's design choices are the builder's to make, on his ruling the same day.</li>"""),
    ],
}

new = {}
for path, edits in EDITS.items():
    with open(path, encoding="utf-8") as f:
        src = f.read()
    for old, rep in edits:
        n = src.count(old)
        if n != 1:
            sys.exit(f"stopped, nothing written: {path}: expected one match, found {n}: {old[:80]!r}")
        src = src.replace(old, rep)
    new[path] = src
for path, src in new.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
print("the 14:34 ruling is on the spec, the map and the drawing source")
