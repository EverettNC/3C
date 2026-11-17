"""spec_v17.py: bring the conch build spec up to the one-time Level 2 fold (17 Nov 2026).

    python3 spec_v17.py <path to conch-spec.html>

Every replacement must match exactly once, or nothing is written.
"""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    page = f.read()

EDITS = [
    # status line
    ("55 of 55 tests pass on the Mac's Python 3.9.6 and 3.13.7",
     "63 of 63 tests pass on the Mac's Python 3.9.6 and 3.13.7"),

    # the moment record
    ("""  needed_for    education | operational | procedural | structure |
                conversation, or nothing at all</pre>""",
     """  needed_for    education | operational | procedural | structure |
                conversation, or nothing at all
  carried_by    the senses that carried what it is needed for, or nothing
                (never on a procedural moment; never a quiet or absent sense)</pre>"""),
    ("No organ is built and no part that reads need is built, so on the bench a person says both.</p>",
     "No organ is built and no part that reads need is built, so on the bench a person says both.</p>\n"
     "  <p><span class=\"pill build\">build choice</span> <code>carried_by</code> says which senses carried what the moment is needed for: sound for speech, sight or touch for a gesture or a board. For a conversation the polymetis says it, because the polymetis took the conversation in; on the bench a person says it. The conch never guesses it. A moment that names a sense it does not have, a quiet or absent sense, or the same sense twice, is refused with the reason.</p>"),

    # the one-time entry record
    ("""  cut_at        the clock of the night it was cut
  kind          permanent record</pre>
  <h3>On the drive</h3>""",
     """  cut_at        the clock of the night it was cut
  kind          permanent record

OneTimeFold
  fold_id       its own id
  carried_by    the senses it keeps
  step          the shapes of only those senses
  folded_from   the one position it stands for
  cut_at        the clock of the night it was cut
  kind          permanent record</pre>
  <h3>On the drive</h3>"""),
    ("spiral · turn · level3_mark · fold · fold_more ·\n                              weight · sleep",
     "spiral · turn · level3_mark · fold · fold_more ·\n                              fold_one · weight · sleep"),

    # step 3: Level 1 is the polymetis's to hold
    ("It is handed straight to the polymetis as a <code>LipDrop</code>. <span class=\"pill build\">build choice</span>",
     "It is handed straight to the polymetis as a <code>LipDrop</code>. <span class=\"pill his\">his</span> It is \"only held long enough to continue the conversation… during sleep, it's shifted out.\" Holding it and emptying it at sleep is the polymetis's job, not the conch's. <span class=\"pill build\">build choice</span>"),

    # step 6: the one-time fold
    ("a missing or extra step stops the fold. <span class=\"pill open\">open</span> How a Level 2 moment that never repeats folds. The full record stays either way.</li>",
     "a missing or extra step stops the fold. <span class=\"pill his\">his</span> Procedure is learned through repetition; the important parts of a conversation are Level 2 the first time, and Level 2 is folded \"so they do not occupy full-sensory volume.\" <span class=\"pill build\">build choice</span> After the routines, each Level 2 turn still carried whole that has <code>carried_by</code> folds to a one-time entry holding only those senses' shapes. Before it is written, the entry is held against the turn; a sense lost or added stops it. A procedural moment never folds one-time: it waits until it repeats. A moment with no <code>carried_by</code> is left whole and the night says so. If the moment turns out later to be the first time of something lived again, it is marked Level 3 and carries its weight again. The full record stays either way.</li>"),

    # step 9: night does both folds
    ("A night goes back over the spiral, cuts the fold, asks again",
     "A night goes back over the spiral, cuts the routines and then the one-time entries, asks again"),

    # tests section
    ("The file holds 55 tests: these fourteen under their own names, and the tests for what this build adds (how the conch knows a moment left its silico-stasis, the fold, the night, and failing loud). On 17 November 2026 all 55 pass",
     "The file holds 63 tests: these fourteen under their own names, and the tests for what this build adds (how the conch knows a moment left its silico-stasis, the fold, the one-time fold, the night, and failing loud). On 17 November 2026 all 63 pass"),

    # open slots: the one-time slot is closed
    ("    <li><strong>How a Level 2 moment that never repeats folds.</strong> One time gives the fold nothing to hold it against, so this build leaves it whole.</li>\n",
     ""),

    # build choices
    ("    <li>The constant learns from what falls off the lip, and keeps only a one-way mark of it (Section 3).</li>\n  </ol>",
     "    <li>The constant learns from what falls off the lip, and keeps only a one-way mark of it (Section 3).</li>\n"
     "    <li>A Level 2 moment lived once folds to the senses named in <code>carried_by</code>, said by the polymetis for a conversation and by hand on the bench (Section 6; Section 7, step 6).</li>\n  </ol>"),

    # known limits
    ("    <li>Shapes match exactly, on all five senses, or not at all.</li>\n  </ul>",
     "    <li>Shapes match exactly, on all five senses, or not at all.</li>\n"
     "    <li>A Level 2 moment between the steps of a routine splits that day's routine, and the night can cut it as separate pieces instead of one entry.</li>\n"
     "    <li>A one-time entry is never joined to a later routine.</li>\n  </ul>"),

    # answered
    ("<p><strong>Answered on 14 November 2026:</strong> Level 1 does reach the polymetis.",
     "<p><strong>Answered on 17 November 2026:</strong> how a Level 2 moment lived once folds, from Everett's word that the important parts of a conversation are Level 2 and still compress, and that conversation goes through the polymetis. Level 1 is held by the polymetis only long enough to continue the conversation and is emptied at sleep.</p>\n"
     "  <p><strong>Answered on 14 November 2026:</strong> Level 1 does reach the polymetis."),
]

for old, new in EDITS:
    n = page.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    page = page.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(page)
print("spec brought up to the build:", path)
