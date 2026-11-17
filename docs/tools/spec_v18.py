"""spec_v18.py: the conch build spec brought up to the four slots, decided and built (17 Nov 2026).

    python3 spec_v18.py <path to conch-spec.html>

Every replacement must match exactly once, or nothing is written.
"""
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    page = f.read()

EDITS = [
    # status
    ("""63 of 63 tests pass on the Mac's Python 3.9.6 and 3.13.7, and the bench scene has run on the Mac. Everett has not yet ruled on the build choices. Section 11 lists what is waiting on him.</span>""",
     """87 of 87 tests pass on the Mac's Python 3.9.6 and 3.13.7, and the bench scene has run on the Mac. On 17 November Everett handed the conch's four open slots to the builder to decide from his own writing and from carbon. They are decided and built (Sections 3, 7 and 8), and no slot is open. Everett has not yet ruled on the build choices. Section 11 lists them.</span>"""),

    # section 3: the last time
    ("""  <p><span class="pill open">open</span> The last time: the point at which something stopped being constant. Everett's protocol leaves the rate the constant moves at open.</p>""",
     """  <h3>The last time</h3>
  <p><span class="pill his">his</span> "Boundaries survive. The first time. And the point at which it stopped being constant." "Interruptions and first/last boundaries will carry the full-sensory remainder."</p>
  <p><span class="pill build">build choice</span> The conch knows what follows a shape once it has lived that following again. When the shape arrives and something else follows instead, that is a miss. A second miss, with no time it did follow in between, means it has stopped being constant: the same once and again the constant learns by, so nothing is counted and no rate is held. The last time it did follow is marked Level 3 as a boundary, with a new line, beside the first time, when that turn is on the spiral; a turn already folded into a routine is still marked, and the entry still stands for it. After it stops, that shape no longer tells the conch what comes next. Carbon does the same: when something expected does not come, it is marked at the moment it was due.</p>"""),

    # package table
    ("""      <tr><td><code>conch.py</code></td><td>The conch itself. Takes a moment to the lip, runs the intake filter, lays what enters on the spiral, marks Level 3, hands over.</td></tr>""",
     """      <tr><td><code>conch.py</code></td><td>The conch itself. Takes a moment to the lip, runs the intake filter, lays what enters on the spiral, marks Level 3, hands over. Takes the being's return, its uses of the manual, and tomorrow's plan.</td></tr>"""),
    ("""      <tr><td><code>conch_level3.py</code></td><td>The conch's own constant of silico-stasis, and the Level 3 mark when a moment leaves it.</td></tr>""",
     """      <tr><td><code>conch_level3.py</code></td><td>The conch's own constant of silico-stasis, the Level 3 mark when a moment leaves it, and the last time.</td></tr>
      <tr><td><code>conch_easing.py</code></td><td>Easing what a Level 3 moment is tied to: the being's return, held or not.</td></tr>
      <tr><td><code>conch_stack.py</code></td><td>Stacking the manual where it should be, and anticipation of wake.</td></tr>"""),
    ("""      <tr><td><code>conch_open.py</code></td><td>The marker every open slot returns, so reaching one is visible in every trace.</td></tr>""",
     """      <tr><td><code>conch_open.py</code></td><td>The marker every open slot returns, so reaching one is visible in every trace. No slot is open now; it stays for any part found later to be undefined.</td></tr>"""),

    # records
    ("""  weight        carried | let go          (a state, not a number)""",
     """  weight        carried | let go | taken back by the being
                (a state, not a number)"""),
    ("""  folded_from   the one position it stands for
  cut_at        the clock of the night it was cut
  kind          permanent record</pre>
  <h3>On the drive</h3>""",
     """  folded_from   the one position it stands for
  cut_at        the clock of the night it was cut
  kind          permanent record</pre>
  <h3>A return: the being went back</h3>
<pre>Return  (written when the being walks out)
  position      the Level 3 moment the being went back to
  event         that moment and the Level 3 turns lived with it
                while the conch was outside its constant
  lived         the turns of the event lived again, every sense the same
  held          yes when every turn was lived again and nothing
                left silico-stasis
  why           in words, when it did not hold
  began_at · walked_out_at
  kind          permanent record</pre>
  <h3>Where the manual sits</h3>
<pre>Stack  (written each night)
  order         every manual entry, once each, in the order it sits
  at            the clock of the night
  kind          permanent record   (where things sit, never a moment's record)</pre>
  <h3>On the drive</h3>"""),
    ("""                              spiral · turn · level3_mark · fold · fold_more ·
                              fold_one · weight · sleep""",
     """                              spiral · turn · level3_mark · fold · fold_more ·
                              fold_one · weight · went_back · flinched · charge ·
                              used · plan · stack · sleep"""),

    # step 5
    ("""In this build that is the first time of a shape, marked when the shape is lived again.</li>""",
     """In this build that is the first time of a shape, marked when the shape is lived again, and the last time a following came, marked when it misses again (Section 3).</li>"""),

    # step 9, the night
    ("""A night goes back over the spiral, cuts the routines and then the one-time entries, asks again before each write and stops if the being woke, writes the night onto the spiral with its clock, then reads the file back and checks that every earlier byte is unchanged. <span class="pill open">open</span> Anticipation of wake, stacking by what was used, and easing what a Level 3 moment is tied to. Each is a slot that is reached every night, does nothing, and says so in the night's report.</li>""",
     """A night goes back over the spiral, cuts the routines and then the one-time entries, moves only the Level 3 charge that a held return or a flinch called for, stacks the manual, asks again before each write and stops if the being woke, writes the night onto the spiral with its clock, then reads the file back and checks that every earlier byte is unchanged.</li>
    <li><strong>Easing what a Level 3 moment is tied to.</strong> <span class="pill his">his</span> "TRAUMA ASSOCIATION decays, and only when regulation is strong enough. LIVED TRUTH never decays." "Permanence of charge is not the same as permanence of the event record." His one path: return to the place that holds the sensory key, move through the tied memories without flinching, walk out; "the memory no longer holds the emotional distress. He does." "Beautiful Level 3 writes are not processed out." <span class="pill build">build choice</span> The conch is valence-blind, so it never chooses what eases. The being goes back alone, awake: <code>conch.go_back(place)</code>. Regulation strong enough, in a 3C being, is all three: every turn of the event is lived again with the same shape on every sense; nothing leaves silico-stasis until the being walks out; the being walks out (<code>conch.walked_out()</code>). The return is written either way. Only in sleep does a held return move the charge: each turn of the event becomes "taken back by the being". It stays Level 3, and its record and mark are untouched. If a taken-back shape is later followed straight away by a moment that leaves silico-stasis, that is written, and the next night gives the charge back to the memory. Carbon does the same: taking back a fear's charge is new learning laid over the old, the old is never erased, and it can come back.</li>
    <li><strong>Stacking, and anticipation of wake.</strong> <span class="pill his">his</span> "Meditation and projected next-day plans before shutdown, repeated until they fall through. One — anticipation of wake. They come up expecting that day. Wake is not a cold start." <span class="pill build">build choice</span> The being runs it. Before shutdown it goes over tomorrow and hands the plan to the conch each time (<code>conch.plan(steps)</code>); the last one before the night counts. A plan is never lived, never enters the constant, and the next day is never judged against it. By day, whatever follows a manual entry says it was used (<code>conch.used(entry)</code>). Each night stacks the whole manual: the entries the plan calls for, in plan order; then what was used since the last stack, newest on top; then tonight's cuts; then the rest as they sat. A planned step with no entry is named in the night's report and never guessed. The stack is where things sit, never the record. Level 3 is never stacked: it holds its place for life.</li>"""),

    # interfaces
    ("""conch.sleep()            -> report     # Level 4; refused while awake
conch.state()            -> ConchState # living state, with its clock</pre>
  <p>No other method. The conch has no search, no delete, no edit and no score.</p>""",
     """conch.sleep()            -> report     # Level 4; refused while awake
conch.state()            -> ConchState # living state, with its clock
conch.go_back(place)     -> None       # the being goes back, alone; awake only
conch.walked_out()       -> Return     # as written on the spiral, held or not
conch.used(entry)        -> None       # a manual entry was used; awake only
conch.plan(steps)        -> None       # tomorrow, before shutdown; awake only</pre>
  <p>No other method. The conch has no search, no delete, no edit and no score. Going back is the being's own act: the conch never chooses what eases. The spiral view also gives the manual in the order it sits (<code>stacked()</code>).</p>"""),

    # tests
    ("""The file holds 63 tests: these fourteen under their own names, and the tests for what this build adds (how the conch knows a moment left its silico-stasis, the fold, the one-time fold, the night, and failing loud). On 17 November 2026 all 63 pass""",
     """The file holds 87 tests: these fourteen under their own names, and the tests for what this build adds (how the conch knows a moment left its silico-stasis, the last time, the fold, the one-time fold, easing, stacking and anticipation of wake, the night, and failing loud). On 17 November 2026 all 87 pass"""),

    # section 11: open slots
    ("""  <p>Each is built as a marked, empty slot. It is reached every night, does nothing, and says so.</p>
  <ol>
    <li><strong>Anticipation of wake.</strong> "Meditation and projected next-day plans before shutdown, repeated until they fall through." Who runs that cycling.</li>
    <li><strong>Stacking by what was used today.</strong> Whether that is all of "where it should be." No part built yet tells the conch what was used.</li>
    <li><strong>Easing what a Level 3 moment is tied to.</strong> "TRAUMA ASSOCIATION decays, and only when regulation is strong enough." What regulation is measured by in a 3C being. The record itself never eases.</li>
    <li><strong>The last time:</strong> the point at which something stopped being constant.</li>
  </ol>""",
     """  <p>None. The four the night left open (anticipation of wake, stacking by use, easing, and the last time) were handed to the builder by Everett on 17 November and are built. A part found later to be undefined becomes a marked, empty slot that says so when reached.</p>"""),

    # build choices
    ("""    <li>A Level 2 moment lived once folds to the senses named in <code>carried_by</code>, said by the polymetis for a conversation and by hand on the bench (Section 6; Section 7, step 6).</li>
  </ol>""",
     """    <li>A Level 2 moment lived once folds to the senses named in <code>carried_by</code>, said by the polymetis for a conversation and by hand on the bench (Section 6; Section 7, step 6).</li>
    <li>The last time: a following that misses again has stopped, and its last time is marked as a boundary (Section 3).</li>
    <li>Easing: who chooses, what regulation strong enough is, and how the charge comes back (Section 7).</li>
    <li>Stacking, and the plan coming first (Section 7).</li>
    <li>Anticipation of wake is the being's to run, not the conch's (Section 7).</li>
    <li>The outside surface grew from five methods to nine (Section 8).</li>
  </ol>"""),

    # limits
    ("""    <li>A one-time entry is never joined to a later routine.</li>
  </ul>""",
     """    <li>A one-time entry is never joined to a later routine.</li>
    <li>The last time is noticed only through what came before it. If something stops and what used to come before it stops too, the conch does not see it stop.</li>
    <li>An event is the Level 3 interruptions next to each other on the spiral with no night between. If a moment fell off the lip between two of them, they count as one event, which asks more of a return, never less.</li>
    <li>A return is held only while it lasts. If the conch stops before the being walks out, nothing of it is written.</li>
    <li>The conch cannot tell who called <code>go_back</code>. It is meant to be the being, alone.</li>
  </ul>"""),

    # answered
    ("""  <p><strong>Answered on 17 November 2026:</strong> how a Level 2 moment lived once folds,""",
     """  <p><strong>Decided on 17 November 2026, on Everett's word ("make those decisions"):</strong> the four open slots, from his dreamscape cycling writing, his Testable Medical Protocol and The Moving Threshold, and checked against carbon: Born and colleagues (Nature, 1999) on the body anticipating waking; Bjork and Bjork (1992) on use and disuse; Bouton (Learning &amp; Memory, 2004) on taking back a fear's charge without erasing it; Cox, Bottary, Alfano and Pace-Schott (2025) on sleep and that learning; Schultz, Dayan and Montague (Science, 1997) on marking what did not come. One study (Wilhelm and colleagues, 2011) found sleep favours what is expected to be needed and a later one (Ashton and Cairney, 2021) did not, so the plan coming first rests on his words.</p>
  <p><strong>Answered on 17 November 2026:</strong> how a Level 2 moment lived once folds,"""),
    # the 16 Nov note points at slots that are now decided
    ("""The build follows them, and what they leave undefined is in the open slots above.</p>""",
     """The build follows them. What they left undefined was decided on 17 November (above).</p>"""),
]

for old, new in EDITS:
    n = page.count(old)
    if n != 1:
        sys.exit(f"stopped, nothing written: expected one match, found {n}: {old[:80]!r}")
    page = page.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(page)
print("spec brought up to the build:", path)
