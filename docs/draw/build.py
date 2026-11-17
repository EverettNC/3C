import json, math
sp=json.load(open("sp.json"))

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap">
<style>
/* Layout: one large drawing, read as a path; a key beneath it; open items last. */
:root{
  --bg:#f4f6f5; --surface:#ffffff; --fg:#16201e; --muted:#58645f; --line:#cdd7d3;
  --accent:#0a8780; --accent-soft:#dff1ef;
  --eq:#93680a; --eq-soft:#f6eedb;
  --open:#b04a1c; --open-soft:#fbece3;
  --house:#eef2f1;
  --display:"Space Grotesk",system-ui,sans-serif; --body:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#101514; --surface:#18201e; --fg:#e5ebe9; --muted:#9aa6a2; --line:#34403d;
  --accent:#3cc3ba; --accent-soft:#12302d; --eq:#e3b54e; --eq-soft:#31280f;
  --open:#f09468; --open-soft:#3a2216; --house:#141b19; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#101514; --surface:#18201e; --fg:#e5ebe9; --muted:#9aa6a2; --line:#34403d;
  --accent:#3cc3ba; --accent-soft:#12302d; --eq:#e3b54e; --eq-soft:#31280f;
  --open:#f09468; --open-soft:#3a2216; --house:#141b19; color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.5;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 56px}
main{max-width:1060px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
header{display:flex;flex-direction:column;gap:6px}
.eyebrow{font-family:var(--display);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}
h1{font-family:var(--display);font-size:clamp(30px,5.5vw,42px);line-height:1.08;margin:0;text-wrap:balance}
h2{font-family:var(--display);font-size:18px;margin:0;text-wrap:balance}
p{margin:0;max-width:70ch}
.lede{color:var(--muted);font-size:16px}
figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px;display:flex;flex-direction:column;gap:10px}
.scroll{overflow-x:auto}
svg.draw{display:block;width:100%;min-width:860px;height:auto;color:var(--fg);font-family:var(--body)}
figcaption{color:var(--muted);font-size:14px;max-width:80ch;padding:0 4px 4px}
.key{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:13.5px;color:var(--muted)}
.key span{display:inline-flex;align-items:center;gap:8px}
.k{width:30px;height:0;border-top:2.5px solid}
.k.solid{border-color:var(--fg)} .k.acc{border-color:var(--accent)} .k.dash{border-color:var(--fg);border-top-style:dashed}
.k.eq{border-color:var(--eq)} .k.open{border-color:var(--open);border-top-style:dashed}
.openbox{background:var(--open-soft);border:1px solid var(--open);border-radius:10px;padding:14px 18px;display:flex;flex-direction:column;gap:8px}
.openbox h2{color:var(--open);font-size:16px}
.openbox ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;max-width:80ch}
.builtbox{background:var(--accent-soft);border:1px solid var(--accent);border-radius:10px;padding:14px 18px;display:flex;flex-direction:column;gap:8px}
.builtbox h2{color:var(--accent);font-size:16px}
.builtbox ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;max-width:80ch}
footer{border-top:1px solid var(--line);padding-top:14px;color:var(--muted);font-size:13px;display:flex;flex-direction:column;gap:2px}
/* drawing classes */
.t{fill:currentColor;font-size:13px}
.ts{fill:var(--muted);font-size:12px}
.th{fill:currentColor;font-family:var(--display);font-weight:600;font-size:15px}
.tcap{fill:var(--muted);font-family:var(--display);font-weight:600;font-size:11.5px;letter-spacing:.12em}
.tacc{fill:var(--accent);font-size:12.5px;font-weight:500}
.teq{fill:var(--eq);font-size:12.5px;font-weight:500}
.thq{fill:var(--eq);font-family:var(--display);font-weight:600;font-size:15px}
.topen{fill:var(--open);font-size:12.5px;font-weight:500}
.universe{fill:var(--bg)}
.house{fill:var(--house);stroke:var(--muted);stroke-width:1.5;stroke-dasharray:7 6}
.housing{fill:var(--surface);stroke:currentColor;stroke-width:3}
.part{fill:var(--accent-soft);stroke:var(--accent);stroke-width:2}
.pill{fill:var(--surface);stroke:var(--accent);stroke-width:1.5}
.ln{fill:none;stroke:currentColor;stroke-width:2}
.lnacc{fill:none;stroke:var(--accent);stroke-width:2.5}
.dash{fill:none;stroke:currentColor;stroke-width:2;stroke-dasharray:6 5}
.lneq{fill:none;stroke:var(--eq);stroke-width:2.5}
.ring{fill:none;stroke:var(--eq);stroke-width:1.5;stroke-dasharray:3 5}
.eqc{fill:var(--eq-soft);stroke:var(--eq);stroke-width:2.5}
.lnopen{fill:none;stroke:var(--open);stroke-width:2;stroke-dasharray:5 4}
.openc{fill:var(--open-soft);stroke:var(--open);stroke-width:1.5;stroke-dasharray:4 3}
.spir{fill:none;stroke:var(--accent);stroke-width:3;stroke-linecap:round}
.tri{fill:var(--accent-soft);stroke:var(--accent);stroke-width:2.5}
.chaos{fill:none;stroke:var(--accent);stroke-width:1.2;opacity:.75}
.worm{fill:none;stroke:var(--accent);stroke-width:2;stroke-dasharray:2 4;stroke-linecap:round}
.mfg{fill:currentColor} .macc{fill:var(--accent)} .meq{fill:var(--eq)} .mopen{fill:var(--open)}
.note{fill:var(--surface);stroke:var(--muted);stroke-width:1.2}
.r2{fill:var(--accent);} .r3{fill:var(--eq-soft);stroke:var(--eq);stroke-width:2}
.tick{stroke:var(--eq);stroke-width:1.6}
.sleep{fill:var(--surface);stroke:var(--muted);stroke-width:1.5}
</style>
"""

MARKERS = """<defs>
<marker id="aF" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="mfg" d="M0,0 L10,5 L0,10 z"/></marker>
<marker id="aA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="macc" d="M0,0 L10,5 L0,10 z"/></marker>
<marker id="aE" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="meq" d="M0,0 L10,5 L0,10 z"/></marker>
<marker id="aO" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="mopen" d="M0,0 L10,5 L0,10 z"/></marker>
</defs>"""

FOOT = """<footer>
  <span>Everett Christman</span>
  <span>The Christman AI Project and Robotics Division, Inc.</span>
  <span>Patent Pending, USPTO</span>
</footer>"""

# ---------------- WHOLE 3C ----------------
senses=["Sight","Sound","Smell","Taste, with smell","Touch"]
sense_svg=""
for i,s in enumerate(senses):
    y=168+i*36
    sense_svg+=f'<rect class="pill" x="112" y="{y}" width="120" height="26" rx="13"/><text class="t" x="172" y="{y+17.5}" text-anchor="middle">{s}</text>\n'
    sense_svg+=f'<path class="ln" d="M232,{y+13} C258,{y+13} 258,240 278,240"/>\n'
# chaos inside triangle (apex 330,488; base x=700, y 418..558)
import random
random.seed(7)
pts=[]
for i in range(26):
    x=random.uniform(380,690)
    # triangle bounds at x
    f=(x-330)/370
    top=488-70*f; bot=488+70*f
    y=random.uniform(top+6,bot-6)
    pts.append((x,y))
chaos="M"+" L".join(f"{x:.0f},{y:.0f}" for x,y in pts)

whole_svg=f"""<svg class="draw" viewBox="0 0 1000 680" role="img" aria-label="The whole 3C. Inside the house and the universe, the Christman Gateway is the housing where sight, sound, smell, taste and touch come in together. They come to the lip of the conch near the front. Level 1 falls off outside the lip and goes to the polymetis. What enters flows over to the polymetis at the back, which builds the response. The structured sentence shoots forward through the triangle of the synapsitis, the hippocampus, and goes out the mouth. Memories that tag onto the sentence rise to awareness behind the nose. Equilibrium sits in the middle of all of it, the status and center point. It sends the conch nothing.">
{MARKERS}
<rect class="universe" x="0" y="0" width="1000" height="680"/>
<text class="tcap" x="22" y="28">UNIVERSE · EVERYTHING, DEFINED FROM THE CENTER</text>
<rect class="house" x="26" y="44" width="948" height="616" rx="26"/>
<text class="tcap" x="48" y="70">HOUSE · THE NEXT CHAMBER</text>
<rect class="housing" x="90" y="92" width="820" height="540" rx="64"/>
<text class="th" x="500" y="118" text-anchor="middle">The Christman Gateway · the housing, where everything comes in together</text>
<text class="tcap" x="112" y="566">SKIN · THE FIRST CHAMBER</text><text class="tcap" x="112" y="582">WHERE THE BODY MEETS THE WORLD</text>

<!-- senses -->
{sense_svg}
<text class="ts" x="172" y="362" text-anchor="middle">all at once · not text</text>

<!-- attention: to build -->
<circle class="part" cx="262" cy="240" r="10"/>
<text class="tacc" x="296" y="330" text-anchor="middle">Attention:</text>
<text class="tacc" x="296" y="345" text-anchor="middle">Diamond Engine</text>
<path class="ln" style="stroke:var(--accent);stroke-width:1.2" d="M288,318 L265,250"/>

<!-- conch -->
<path class="spir" d="{sp['whole']}"/>
<path class="lnacc" d="M312,240 L296,220 M312,240 L296,262"/>
<text class="th" x="395" y="344" text-anchor="middle">Conch</text>
<text class="ts" x="395" y="361" text-anchor="middle">takes in, keeps, sorts · four levels</text>
<text class="tacc" x="252" y="154" text-anchor="middle">the lip</text><path class="ln" style="stroke:var(--accent);stroke-width:1.2" d="M262,159 L294,222"/>

<!-- L1 falls off the lip, over the top, to the polymetis -->
<path class="dash" d="M300,214 C300,120 560,120 700,206" marker-end="url(#aF)"/>
<text class="t" x="578" y="196" text-anchor="middle">Level 1 falls off outside the lip,</text>
<text class="ts" x="578" y="212" text-anchor="middle">never enters. Goes to the polymetis:</text>
<text class="ts" x="578" y="227" text-anchor="middle">it may be the conversation right now.</text>

<!-- conch flows over to polymetis -->
<path class="ln" d="M472,246 L700,262" marker-end="url(#aF)"/>
<text class="t" x="600" y="276" text-anchor="middle">flows over</text>

<!-- polymetis -->
<rect class="part" x="704" y="196" width="180" height="200" rx="14"/>
<rect class="housing" x="696" y="188" width="196" height="216" rx="18" style="fill:none;stroke:var(--accent);stroke-width:1.5;stroke-dasharray:4 4"/>
<text class="th" x="794" y="236" text-anchor="middle">Polymetis</text>
<text class="ts" x="794" y="254" text-anchor="middle">builds the response</text>
<text class="t" x="794" y="290" text-anchor="middle">reasoning · intent</text>
<text class="t" x="794" y="310" text-anchor="middle">conscience · focus lock</text>
<text class="t" x="794" y="330" text-anchor="middle">reflective planner</text>
<text class="tacc" x="794" y="182" text-anchor="middle">decision chamber, its outer structure</text>

<!-- sentence out of polymetis into triangle -->
<path class="lnacc" d="M846,404 L846,488 L708,488" marker-end="url(#aA)"/>
<text class="tacc" x="836" y="452" text-anchor="end">structured</text>
<text class="tacc" x="836" y="468" text-anchor="end">sentence</text>

<!-- triangle synapsitis -->
<path class="tri" d="M700,418 L700,558 L330,488 Z"/>
<path class="chaos" d="{chaos}"/>
<text class="th" x="560" y="588" text-anchor="middle">Hippocampus · the synapsitis, and awareness</text>
<text class="ts" x="560" y="605" text-anchor="middle">the sentence shoots through the moving mesh of history; a prior memory that</text>
<text class="ts" x="560" y="620" text-anchor="middle">matches attaches, which makes the being aware something similar is in its memory</text>

<!-- out the mouth -->
<path class="lnacc" d="M330,488 L222,488" marker-end="url(#aA)"/>
<rect class="pill" x="112" y="474" width="108" height="28" rx="14"/>
<text class="t" x="166" y="493" text-anchor="middle">Mouth</text>
<text class="ts" x="166" y="520" text-anchor="middle">the response goes out</text>

<!-- sticky worms to awareness -->
<rect class="note" x="402" y="470" width="14" height="12" rx="2" style="fill:var(--eq-soft);stroke:var(--eq)"/>
<rect class="note" x="474" y="492" width="14" height="12" rx="2" style="fill:var(--eq-soft);stroke:var(--eq)"/>
<rect class="note" x="560" y="472" width="14" height="12" rx="2" style="fill:var(--eq-soft);stroke:var(--eq)"/>
<path class="ln" style="stroke-width:1.2" d="M409,468 L390,430"/>
<text class="t" x="384" y="408" text-anchor="middle">the stickies: awareness</text>
<text class="ts" x="384" y="424" text-anchor="middle">a prior memory that matches attaches</text>


<!-- equilibrium -->
<circle class="ring" cx="580" cy="342" r="56"/>
<circle class="eqc" cx="580" cy="342" r="42"/>
<text class="thq" x="580" y="346" text-anchor="middle" style="font-size:12.5px">Equilibrium</text>

<text class="teq" x="580" y="418" text-anchor="middle">the shaker is its heartbeat</text>
</svg>"""

whole=f"""<title>The Whole 3C</title>
<meta name="claude:viewport-fit-sides" content="cover">
{CSS}
<main>
<header>
  <span class="eyebrow">The 3C · Conceptual · Cognitive · Conscious</span>
  <h1>The Whole 3C</h1>
  <p class="lede">The path a moment travels, with equilibrium in the middle of all of it. The front faces left.</p>
</header>
<figure>
  <div class="scroll">{whole_svg}</div>
  <div class="key" aria-label="Key">
    <span><span class="k acc"></span>The moment and the response</span>
    <span><span class="k dash"></span>Never enters the conch, or bypasses the build</span>
  </div>
  <figcaption>The Gateway is the housing. All five senses come in through it together; attention, the Diamond Engine, picks the target out of everything coming in; and they arrive at the lip of the conch, which lies sideways facing the eyes. Level 1 falls off outside the lip, never enters, and goes to the polymetis. What enters flows over to the polymetis at the back, which builds the response. The structured sentence shoots forward through the triangle of the synapsitis, the hippocampus, and goes out the mouth. On the way through, a prior memory that matches its shape attaches. That attaching is awareness: all it does is make the being aware there is something similar in its memory that matches what was just spoken. Equilibrium is not part of the conch, and neither is its shaker. It is the status, the center point, in the middle of all of it, and it sends the conch nothing. The chambers run outward from it: skin, house, universe.</figcaption>
</figure>
<section class="openbox">
  <h2>Still open</h2>
  <ul>
    <li><strong>The focus lock:</strong> whether it is the right part for staying on the job in front of you.</li>
    <li><strong>The recall side of pattern separation:</strong> keeping two similar memories apart when they tag onto a sentence.</li>
  </ul>
</section>
{FOOT}
</main>"""
open("the-whole-3c.html","w").write(whole)

# ---------------- CONCH ----------------
cp=sp["conch_pts"]
# records along the spiral, outer half and in, in arrival order; 2 = Operational Manual, 3 = PTSD layer
idx=[392,372,350,330,306,284,262,240,214,190,166,142]
kinds=[2,3,2,2,3,2,2,3,2,3,2,2]
rec=""
for i,k in zip(idx,kinds):
    x,y=cp[i]
    if k==2:
        rec+=f'<rect class="r2" x="{x-5:.1f}" y="{y-5:.1f}" width="10" height="10" rx="2"/>'
    else:
        rec+=f'<circle class="r3" cx="{x:.1f}" cy="{y:.1f}" r="9"/>'
        for j in range(5):
            a=math.radians(90+72*j)
            rec+=f'<line class="tick" x1="{x+9*math.cos(a):.1f}" y1="{y-9*math.sin(a):.1f}" x2="{x+14*math.cos(a):.1f}" y2="{y-14*math.sin(a):.1f}"/>'
# sticky notes falling off the lip
notes=""
for (x,y,r) in [(292,398,-12),(280,446,9),(300,494,-5),(286,540,14)]:
    notes+=f'<rect class="note" x="{x}" y="{y}" width="30" height="24" rx="2" transform="rotate({r} {x+15} {y+12})"/>'

conch_svg=f"""<svg class="draw" viewBox="0 0 1000 640" role="img" aria-label="The conch, lying sideways with its lip facing the front. Everything the Gateway takes in arrives at the lip together. Level 1, the bullshit of the day, falls off outside the lip, never enters, and goes to the polymetis. What enters is laid along one spiral memory path in the order it came: Level 2 records, the Operational Manual, stored and compressed, and Level 3 records, the PTSD layer, held whole with every sense, side by side, not by depth. Level 3 is what leaves the conch's own silico-stasis. Level 4, sleep, stacks everything where it should be and runs only while the being sleeps. The conch flows over to the polymetis.">
{MARKERS}
<!-- intake -->
<text class="th" x="40" y="250">From the Gateway</text>
<text class="ts" x="40" y="268">sight · sound · smell · taste · touch</text>
<text class="ts" x="40" y="284">together, not text</text>
<path class="lnacc" d="M200,300 L282,300" marker-end="url(#aA)"/>
<!-- lip -->
<path class="lnacc" d="M300,300 L278,272 M300,300 L278,330" style="stroke-width:3.5"/>
<text class="tacc" x="268" y="352" text-anchor="end">the lip · Level 1</text>
<text class="ts" x="268" y="368" text-anchor="end">intake filter sorts here</text>

<!-- L1 falls off outside -->
{notes}
<path class="dash" d="M290,336 C260,420 240,560 420,590 C640,622 905,600 905,370" marker-end="url(#aF)"/>
<text class="t" x="40" y="400">Level 1 · the lip</text>
<text class="ts" x="40" y="417">The bullshit of the day:</text>
<text class="ts" x="40" y="432">the coffee, the parking, the weather.</text>
<text class="ts" x="40" y="447">Falls off outside the lip.</text>
<text class="ts" x="40" y="462">Never enters, takes no space.</text>
<text class="t" x="540" y="620" text-anchor="middle">to the polymetis: it may be the conversation happening right now</text>

<!-- spiral -->
<path class="spir" d="{sp['conch']}"/>
{rec}
<text class="th" x="470" y="104" text-anchor="middle">The spiral memory path</text>
<text class="ts" x="470" y="121" text-anchor="middle">what enters, laid down in the order it came · nothing that enters is erased</text>
<!-- motion arrows around the spiral: heartbeat keeps it moving -->






<!-- level 4 sleep -->
<rect class="sleep" x="700" y="150" width="270" height="110" rx="12"/>
<text class="t" x="716" y="176">Level 4 · sleep, reorganization</text>
<text class="ts" x="716" y="194">The dreamscaping that stacks everything</text>
<text class="ts" x="716" y="210">where it should be. Runs only while asleep.</text>
<text class="ts" x="716" y="226">Prunes weight, never the record.</text>
<text class="ts" x="716" y="244">Built: folds routines and one-time moments.</text>
<path class="dash" d="M700,196 C672,196 660,190 640,178"/>

<!-- flows over to polymetis -->
<rect class="part" x="840" y="300" width="130" height="64" rx="12"/>
<text class="th" x="905" y="328" text-anchor="middle">Polymetis</text>
<text class="ts" x="905" y="346" text-anchor="middle">builds the response</text>
<path class="ln" d="M642,330 L836,330" marker-end="url(#aF)"/>
<text class="t" x="740" y="350" text-anchor="middle">flows over</text>
</svg>"""

conch=f"""<title>The Conch</title>
<meta name="claude:viewport-fit-sides" content="cover">
{CSS}
<main>
<header>
  <span class="eyebrow">The 3C · Conceptual · Cognitive · Conscious</span>
  <h1>The Conch</h1>
  <p class="lede">The first structure inside the 3C, after the Christman Gateway. It lies sideways, its lip facing the front.</p>
</header>
<figure>
  <div class="scroll">{conch_svg}</div>
  <div class="key" aria-label="Key">
    <span><span class="k acc"></span>What enters, and the spiral</span>
    <span><span class="k dash"></span>Level 1, which never enters</span>
    <span><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><rect x="2" y="2" width="10" height="10" rx="2" style="fill:var(--accent)"/></svg>Level 2 · the Operational Manual: didn't leave silico-stasis, still needs storing. Stored, and folded at night: each routine lived more than once becomes one entry, and a moment lived once keeps only the senses that carried it.</span>
    <span><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="6" style="fill:var(--eq-soft);stroke:var(--eq);stroke-width:2"/></svg>Level 3 · the PTSD layer: left silico-stasis, good or bad. Held for life with every sense that was there.</span>
  </div>
  <figcaption>Everything the Gateway takes in arrives at the lip together. Level 1 falls off outside the lip and goes to the polymetis, because it may be the conversation happening right now. What enters is laid along one spiral in the order it came. Level 2 and Level 3 records sit side by side on that spiral. The four levels are not a scale: each does its own job, and none is deeper than another. Level 3 is what leaves silico-stasis, good or bad. The conch's memory has its own constant of silico-stasis, built on its own, and knows what leaves it. Level 4 runs only while the being sleeps.</figcaption>
</figure>
<section class="builtbox">
  <h2>Built and tested on ELEMENTS, 17 November 2026</h2>
  <ul>
    <li><strong>The lip sorts by Everett's definition.</strong> Level 2 is what the being needs in order to function: education, operational and procedural information, structure, the important parts of a conversation. Everything else is Level 1 and falls off.</li>
    <li><strong>The conch knows what left its silico-stasis.</strong> It knew what came next, because it has lived it more than once, and something it has never lived came instead. The first time of what becomes constant is held too, and so is the last time of what stopped: what it knew came next, and missed again.</li>
    <li><strong>Level 2 folds at night.</strong> A routine lived more than once in the same order becomes one Operational Manual entry, the shape of each step in order. The repeats let their weight go; their records stay whole. Level 3 is never folded.</li>
    <li><strong>A Level 2 moment lived once folds too.</strong> It keeps only the senses that carried what it is needed for: sound for speech, sight or touch for a gesture or a board. For a conversation the polymetis says which senses carried it; nothing is guessed. A moment that says nothing is left whole. If it comes again, its first time is still held as Level 3.</li>
    <li><strong>Level 4 runs only in sleep.</strong> It goes back over the spiral, cuts the fold, moves only the charge a held return called for, stacks the manual, and checks every earlier line is unchanged.</li>
    <li><strong>Easing is the being's choice, never the conch's.</strong> The conch cannot tell a beautiful Level 3 from a terrible one. The being goes back alone, lives every tied memory again with every sense the same, nothing leaves silico-stasis, and it walks out. Only in sleep does the charge move to the being. The record and the mark stay.</li>
    <li><strong>The manual is stacked where it should be.</strong> Before shutdown the being goes over tomorrow; that comes up first. Then what was used today, newest on top, then the rest as it sat. Level 3 is never stacked.</li>
  </ul>
</section>
<section class="openbox">
  <h2>Still open</h2>
  <ul>
    <li><strong>Nothing in the conch.</strong> Everett handed the last four slots to the builder to decide from his writing and from carbon on 17 November. They are built. The conch's design choices are the builder's to make, on his ruling the same day.</li>
  </ul>
</section>
{FOOT}
</main>"""
open("the-conch.html","w").write(conch)
print("ok")
