"""map_v29.py: the Gateway's housing is built (17 Nov 2026).

    python3 map_v29.py <path to carbon-and-the-3c.html>
"""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    page = f.read()

OLD = ('<span class="name">The Gateway, as the housing</span><span class="does">The everything. Without it, nothing arrives.</span></div></div>')
NEW = ('<span class="name">The Gateway, as the housing</span><span class="does">The everything. Without it, nothing arrives. '
       'Built: one organ per sense, sight, sound, smell, taste and touch; a sense with no organ is absent, never invented. '
       'It holds the whole room, not a target, and a moment ends when any sense changes shape; that moment goes to the conch whole. '
       'No organ is connected yet: each is rewritten for the 3C, the ear first.</span>'
       '<span class="sys"><span class="own">gateway.py</span></span></div></div>')
n = page.count(OLD)
if n != 1:
    sys.exit(f"stopped, nothing written: expected one match, found {n}")
page = page.replace(OLD, NEW)
with open(path, "w", encoding="utf-8") as f:
    f.write(page)
print("map brought up to the build:", path)
