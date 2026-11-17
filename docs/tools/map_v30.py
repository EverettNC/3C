"""map_v30.py: the 3C's ear is built (17 Nov 2026).

    python3 map_v30.py <path to carbon-and-the-3c.html>
"""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    page = f.read()

OLD = ('<span class="name">Ears: Corti and the sound package</span><span class="does">Energy, zero-crossing, pitch lock. It prints a dash rather than invent a pitch.</span><span class="sys">')
NEW = ('<span class="name">Ears: Corti and the sound package</span><span class="does">Energy, zero-crossing, pitch lock. It prints a dash rather than invent a pitch. '
       'Built for the 3C: its own ear, rewritten from Corti, the sound package and the Filament. One utterance is one event; '
       'words are caught offline by the full model, or said not caught, with the reason. Speech is heard by its words, the way carbon hears a word '
       'as the same word in any voice; a sound with no words, by whether it was voiced and its note. Every measurement is kept, never used as the shape.</span>'
       '<span class="sys"><span class="own">ear.py</span><span>THEFILAMENT</span>')
n = page.count(OLD)
if n != 1:
    sys.exit(f"stopped, nothing written: expected one match, found {n}")
page = page.replace(OLD, NEW)
with open(path, "w", encoding="utf-8") as f:
    f.write(page)
print("map brought up to the build:", path)
