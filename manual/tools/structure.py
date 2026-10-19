"""Book structure: parts, part divider text, and front-matter page builders."""
import html as htmlmod

PARTS = [
    {"num": "I", "title": "Foundations of Space Engineering", "photo": "part1",
     "chapters": ["01", "02", "03", "04", "05", "06", "07"],
     "desc": "Every space system — a weather balloon, a GPS satellite or a Mars rover — obeys the same physics "
             "and is built with the same engineering discipline. Part I explains the ecosystem, the environment "
             "a spacecraft must survive, how orbits work, how missions are engineered, the subsystems inside "
             "every spacecraft, and how data travels between space and the ground."},
    {"num": "II", "title": "Near-Space and Suborbital Flight", "photo": "part2",
     "chapters": ["08", "09", "10"],
     "desc": "Between the airliner cruise altitude and the lowest stable orbit lies a busy frontier: stratospheric "
             "balloons and solar aircraft that hover for months, sounding rockets that give minutes of microgravity, "
             "suborbital tourist vehicles, and winged spaceplanes that return from orbit like gliders."},
    {"num": "III", "title": "Satellites in Earth Orbit", "photo": "part3",
     "chapters": ["11", "12"],
     "desc": "About sixteen thousand active satellites now circle the Earth. This Part explains where they fly "
             "(LEO, MEO, GEO and special orbits), how constellations are designed, how a satellite bus is built, "
             "and the families of payload instruments they carry."},
    {"num": "IV", "title": "Earth Observation and Remote Sensing", "photo": "part4",
     "chapters": ["13", "14", "15", "16"],
     "desc": "Satellites that look down at our planet measure crops, cities, ice, oceans, storms and greenhouse "
             "gases. Part IV covers the physics of remote sensing, high-resolution optical and thermal imagers, "
             "synthetic aperture radar, and the weather and environmental satellites behind every forecast."},
    {"num": "V", "title": "Communication and Navigation Satellites", "photo": "part5",
     "chapters": ["17", "18"],
     "desc": "Satellites carry television, internet, phone calls and the timing signals that keep banks, power "
             "grids and phones synchronised. Part V explains communication payloads, broadband mega-constellations, "
             "direct-to-device service and the four global navigation systems: GPS, GLONASS, Galileo and BeiDou."},
    {"num": "VI", "title": "Military, Intelligence and Space Security", "photo": "part6",
     "chapters": ["19", "20", "21"],
     "desc": "Space is a strategic domain. This Part describes, using openly published information, how signals "
             "intelligence and missile-warning satellites work, and how radars and telescopes track tens of "
             "thousands of objects to keep orbits safe from collisions and debris."},
    {"num": "VII", "title": "Space Environmental Science", "photo": "part7",
     "chapters": ["22", "23"],
     "desc": "The Sun drives a violent 'weather' system that reaches every satellite and power grid on Earth. "
             "Part VII explains solar activity, geomagnetic storms, the magnetosphere, radiation belts and the "
             "ionosphere — and the missions and instruments that study them."},
    {"num": "VIII", "title": "Deep Space Exploration", "photo": "part8",
     "chapters": ["24", "25", "26", "27", "28", "29"],
     "desc": "From the Moon to interstellar space, robotic explorers have visited every planet. Part VIII covers "
             "interplanetary mission design, orbiters, flyby probes, landers and entry systems, rovers and "
             "helicopters, and missions that bring samples of other worlds back to Earth."},
    {"num": "IX", "title": "Human Spaceflight and Habitation", "photo": "part9",
     "chapters": ["30", "31", "32", "33"],
     "desc": "Keeping people alive and productive in space is the hardest engineering problem of all. Part IX "
             "explains the human body in space, life support, crewed spacecraft, space stations and the spacesuits "
             "that let astronauts work outside."},
    {"num": "X", "title": "Launch Systems and Infrastructure", "photo": "part10",
     "chapters": ["34", "35", "36", "37"],
     "desc": "Everything in space started on a launch pad. Part X explains launch vehicle engineering and rocket "
             "propulsion, surveys the world's launch vehicles including the new generation of reusable rockets, "
             "and describes spaceports and the ground systems that support them."},
    {"num": "XI", "title": "Space Observatories", "photo": "part11",
     "chapters": ["38", "39"],
     "desc": "Above the atmosphere, telescopes see the whole electromagnetic spectrum without blur. Part XI covers "
             "the engineering of space telescopes and the great observatories, from Hubble and Webb to the "
             "X-ray, gamma-ray, gravitational-wave and survey missions of today and tomorrow."},
    {"num": "XII", "title": "Emerging Frontiers", "photo": "part12",
     "chapters": ["40", "41", "42"],
     "desc": "The next era of spaceflight will service, refuel and build things in orbit, use resources from the "
             "Moon and asteroids, and move with new kinds of propulsion. Part XII explains the engineering and "
             "the economics behind these frontiers."},
    {"num": "XIII", "title": "Artificial Intelligence in the Space Ecosystem", "photo": "part13",
     "chapters": ["43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53"],
     "desc": "Artificial intelligence now runs on satellites, plans rover drives, forecasts the weather, screens "
             "collision warnings and designs rocket parts. Part XIII is an in-depth guide in eleven chapters: the "
             "foundations of machine learning and deep learning, the data and hardware that make AI work in orbit, "
             "its applications in Earth observation, weather, autonomy, operations, security, science, exploration, "
             "design and business — and the assurance and governance needed to trust it."},
    {"num": "XIV", "title": "Appendices and Reference Data", "photo": "part14",
     "chapters": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
     "desc": "Constants, equations, planetary data, frequency bands, mission databases, a timeline, acronyms, "
             "a glossary, standards and sources, and image credits — the quick-reference tools an engineer keeps "
             "within reach."},
]


def chapter_part(key):
    for p in PARTS:
        if key in p["chapters"]:
            return p
    return None


def _cover(page_html, root):
    return page_html("Cover", """
<style>@page { margin: 0 } body { margin: 0 }
.cv { width: 210mm; height: 297mm; position: relative; overflow: hidden; color: #fff; font-family: Inter, sans-serif; }
.cv .bg { position: absolute; inset: 0; background: url(figures/photos/cover.jpg) center/cover; }
.cv .sh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(4,14,30,0.92) 0%, rgba(4,14,30,0.55) 34%, rgba(4,14,30,0.15) 58%, rgba(4,14,30,0.85) 100%); }
.cv .top { position: absolute; top: 24mm; left: 20mm; right: 20mm; }
.cv .kick { font-size: 10pt; letter-spacing: 0.32em; text-transform: uppercase; color: #F2A65A; font-weight: 700; }
.cv h1 { color: #fff; font-size: 40pt; line-height: 1.04; font-weight: 800; margin: 6mm 0 5mm; letter-spacing: -0.01em; }
.cv .sub { font-size: 13pt; line-height: 1.45; color: #DCE6F0; max-width: 165mm; font-weight: 400; }
.cv .bar { width: 36mm; height: 3pt; background: #D9772B; margin-top: 8mm; }
.cv .bot { position: absolute; bottom: 18mm; left: 20mm; right: 20mm; display: flex; justify-content: space-between; align-items: flex-end; }
.cv .ed { font-size: 10pt; color: #E7EEF5; line-height: 1.5; }
.cv .ed b { color: #F2A65A; }
.cv .cr { font-size: 6.5pt; color: #b8c4d0; max-width: 70mm; text-align: right; }
</style>
<div class="cv"><div class="bg"></div><div class="sh"></div>
<div class="top"><div class="kick">Engineering Reference Manual</div>
<h1>Space Exploration &amp;<br>Aerospace Engineering</h1>
<div class="sub">Near-space platforms · Sounding rockets · Spaceplanes · Satellites in LEO, MEO and GEO ·
Earth observation · SAR · Weather · Communications · GNSS · Space security and SSA · Space weather ·
Deep-space orbiters, probes, landers, rovers and sample return · Human spaceflight · Launch systems ·
Space telescopes · In-space manufacturing · Asteroid mining · Advanced propulsion · Artificial intelligence</div>
<div class="bar"></div></div>
<div class="bot"><div class="ed"><b>First Edition</b> · Current to October 2026<br>Written in plain language with deep technical detail</div>
<div class="cr">Cover: Earth limb and the International Space Station's solar arrays. Image: NASA.</div></div></div>""")


def _title(page_html, root):
    return page_html("Title", """
<style>.tp { height: 250mm; display: flex; flex-direction: column; justify-content: space-between; font-family: Inter, sans-serif; }
.tp .k { font-size: 9pt; letter-spacing: 0.3em; text-transform: uppercase; color: #D9772B; font-weight: 700; margin-top: 30mm; }
.tp h1 { font-size: 32pt; color: #0B2E4F; line-height: 1.08; margin: 5mm 0; font-weight: 800; }
.tp .s { font-size: 12.5pt; color: #33414e; max-width: 150mm; line-height: 1.5; font-family: 'SrcSerif', serif; }
.tp .rule { width: 40mm; height: 3pt; background: #D9772B; margin: 8mm 0; }
.tp .meta { font-size: 9.5pt; color: #5B6670; line-height: 1.6; }
.cp { font-size: 8.4pt; color: #3e4851; line-height: 1.5; }
.cp p { text-align: left; margin-bottom: 0.7em; }
.cp h4 { font-size: 9pt; margin: 1em 0 0.2em; }
</style>
<div class="tp"><div><div class="k">Engineering Reference Manual</div>
<h1>Space Exploration &amp; Aerospace Engineering</h1>
<div class="s">A complete, illustrated guide to the space ecosystem — from stratospheric balloons to interstellar
probes — explaining how every major class of space system works, how it is engineered, and where artificial
intelligence is changing it.</div><div class="rule"></div>
<div class="meta">First Edition · Information current to October 2026<br>
A4 format · Fourteen Parts · Forty-seven chapters · Ten appendices</div></div></div>
<div class="pagebreak"></div>
<div class="cp">
<h4>About this edition</h4>
<p>This manual was written to be read by students, engineers, analysts, managers and curious readers. Each topic
starts with plain-language explanations and builds up to the equations, numbers and design trade-offs that
practising engineers use. Facts, mission status and programme milestones are current to October 2026; space
programmes change quickly, so dates of future events should be read as plans, not certainties.</p>
<h4>Figures, photographs and data</h4>
<p>Diagrams, charts and graphs were drawn specifically for this manual from published physical relationships
and public data. Photographs are from the NASA Image and Video Library and are used under NASA's media usage
guidelines (NASA material is generally not subject to copyright in the United States); individual credits appear
with each image and in Appendix J. NASA does not endorse this publication. Numerical values (masses, power levels,
performance) are representative published figures and may differ slightly between sources and mission phases.</p>
<h4>Safety and responsibility</h4>
<p>This is an educational reference. It is not a design standard, a flight rule, or a substitute for the
requirements, analyses and verification processes of a qualified engineering organisation. Chapters dealing with
military and intelligence systems use only openly published information and describe principles, not
operational or classified details.</p>
<h4>How numbers are written</h4>
<p>SI units are used throughout, with common aerospace units (nautical miles, feet, pounds-force) shown where the
industry uses them. Large numbers use thin spacing (e.g., 35 786 km). "≈" means approximately, "~" means
order-of-magnitude. Dates follow the ISO format (YYYY-MM-DD) in tables.</p>
<h4>Typography and production</h4>
<p>Set in Source Serif 4, Inter and JetBrains Mono. Equations typeset with MathJax. Produced from Markdown
sources with an automated pipeline (pandoc, Chromium, pypdf); the sources and build scripts accompany the PDF.</p>
</div>""")


def _preface(page_html, root):
    return page_html("Preface", """
<div class="front-title">Preface and How to Use This Manual</div>
<p>Space is no longer a niche. In 2025 the world made about 330 orbital launch attempts — more than in any previous
year — and by late 2026 about sixteen thousand active satellites were in orbit, two-thirds of them Starlinks. A single company now lands and re-flies orbital
boosters every few days, governments are building lunar landers with private partners, and the same smartphone
that streams a video can receive a signal from four navigation constellations and, increasingly, from satellites
directly. Behind all of this is a large, interconnected <em>ecosystem</em> of vehicles, instruments, ground systems,
science, regulation and business.</p>
<p>This manual describes that ecosystem from end to end. It is organised in fourteen Parts that follow the journey
of space systems from the edge of space to the edge of the Solar System:</p>
<ul>
<li><b>Part I — Foundations</b> gives the physics and engineering every other Part relies on: the space environment,
orbital mechanics, systems engineering, spacecraft subsystems and communications.</li>
<li><b>Parts II–III</b> climb from near-space balloons, sounding rockets and spaceplanes to satellites in Earth orbit.</li>
<li><b>Parts IV–VII</b> cover what satellites <em>do</em>: observe the Earth, carry communications and navigation signals,
support national security and space situational awareness, and study space weather.</li>
<li><b>Parts VIII–IX</b> leave Earth orbit: robotic deep-space exploration and human spaceflight.</li>
<li><b>Parts X–XII</b> cover how we get to space (launch systems and spaceports), how we look at the universe
(space telescopes), and the emerging frontiers of in-space manufacturing, space resources and advanced propulsion.</li>
<li><b>Part XIII</b> is an in-depth, eleven-chapter treatment of <b>artificial intelligence</b> across the whole space ecosystem: foundations (Chapters 43–45), applications (Chapters 46–52) and trustworthy AI (Chapter 53).</li>
<li><b>Part XIV</b> contains reference data: constants, equations, planetary data, frequency bands, mission
databases, a timeline, acronyms, a glossary, sources and image credits.</li>
</ul>
<h3>Reading paths</h3>
<p>The manual can be read cover to cover, but it is designed as a reference. Each chapter opens with a short summary
and a list of its sections, and cross-references (shown as <span style="color:#1F6FB2">blue links</span> in the PDF)
connect related figures, tables and sections. Suggested paths:</p>
<table><thead><tr><th>If you are…</th><th>Start with</th><th>Then read</th></tr></thead><tbody>
<tr><td>New to space engineering</td><td>Chapters 1, 2, 3</td><td>Any application chapter; return to Chapters 4–7 as needed</td></tr>
<tr><td>A satellite or payload engineer</td><td>Chapters 4–7, 11–12</td><td>Part IV (EO), Part V (comms/nav), Chapter 45 (edge AI in orbit)</td></tr>
<tr><td>Working in Earth observation or climate</td><td>Chapters 13–16</td><td>Chapters 46–47 (AI for EO, weather and climate)</td></tr>
<tr><td>Working in defence or space security</td><td>Chapters 19–21</td><td>Chapters 22 (space weather), 50 (AI for SSA and defence)</td></tr>
<tr><td>A planetary or deep-space engineer</td><td>Chapters 3, 24</td><td>Chapters 25–29, 42 (propulsion), 48 (autonomy)</td></tr>
<tr><td>Interested in human spaceflight</td><td>Chapters 30–33</td><td>Chapters 10 (reentry), 31 (crewed spacecraft), 36 (launchers)</td></tr>
<tr><td>A launch or propulsion engineer</td><td>Chapters 34–37</td><td>Chapters 9–10, 42</td></tr>
<tr><td>An AI or data scientist entering space</td><td>Chapter 1, Chapters 43–45</td><td>Chapters 13, 21, 24 for domain context, then Chapters 46–53</td></tr>
</tbody></table>
<h3>Special boxes</h3>
<div class="key"><p><strong>Key concept</strong></p><p>The one idea in a section you should remember.</p></div>
<div class="example"><p><strong>Worked example</strong></p><p>A calculation with real numbers, step by step.</p></div>
<div class="note"><p><strong>Engineering note</strong></p><p>Practical detail, rule of thumb, or design lesson.</p></div>
<div class="warning"><p><strong>Failure lesson</strong></p><p>What went wrong in a real mission and what engineers learned.</p></div>
<div class="data"><p><strong>Data box</strong></p><p>Key numbers for a system or mission.</p></div>
<div class="ai"><p><strong>AI in practice</strong></p><p>How artificial intelligence is used for the topic at hand.</p></div>
<h3>A note on accuracy and currency</h3>
<p>Space programmes evolve weekly: launch dates slip, missions end, and new vehicles fly. The information here reflects
publicly available sources as of October 2026. Where a programme's future was uncertain at that date (for example,
proposed cancellations in government budgets), the manual says so. Performance figures are representative values
from official fact sheets, peer-reviewed literature and agency documentation; readers designing real systems
should always go to the primary source listed in Appendix I.</p>
""")


FRONT = [("cover", _cover), ("title", _title), ("preface", _preface)]
