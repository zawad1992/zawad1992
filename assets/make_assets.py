"""Generate every SVG in assets/. All text is outlined so it renders the same everywhere.

Usage: pip install fonttools uharfbuzz
       python assets/make_assets.py Bricolage.ttf JetBrainsMono.ttf assets

Both fonts are the variable versions from Google Fonts. Edit the data below to
add a role or update a number.

Rule for motion: content is always visible at rest. Animation only ever adds
decoration on top, so an environment that never ticks still shows every fact.
"""
import math
import os
import sys
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

DISPLAY, MONO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FACES = {"d": hb.Face(hb.Blob.from_file_path(DISPLAY)), "m": hb.Face(hb.Blob.from_file_path(MONO))}

W = 1000
BG, PANEL, LINE, PAPER, MUTED = "#0A0E1F", "#11162C", "#2A3256", "#EEF1FB", "#A7B1D1"
ERP, GOV, PAY, HEALTH, STREAM = "#F5B83D", "#4AA3F0", "#FF7A66", "#25BE93", "#C985F0"  # validated on PANEL
PINK, CYAN = "#F472B6", "#22D3EE"
FLOW = ["#8B5CF6", "#3B82F6", "#06B6D4", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]

NOW = 2026.83  # Only used for the industry totals; the last span runs off the edge.

ROLES = [
    ("IECL", "Government and banking", 2015.25, 2017.0, GOV),
    ("Advance Business Solutions", "Business and education ERP", 2017.0, 2017.85, ERP),
    ("Pharma Solutions Bangladesh", "Healthcare and distribution", 2017.85, 2023.17, HEALTH),
    ("Adventure Dhaka", "Global payments and airlines", 2023.17, 2024.17, PAY),
    ("Nexdecade Technology", "Toffee and T Sports, 53 developers", 2024.17, 2024.95, STREAM),
    ("Techzu Ichicode", "Enterprise ERP and AI", 2024.95, None, ERP),
]
BUILDING = ["enterprise ERP", "payment platforms", "healthcare systems", "streaming platforms"]

IMPACT = [
    ("50M+", "Toffee OTT app downloads", "T Sports 5M+, Bangladesh", PINK),
    ("1M+", "payment transactions a day", "Philippines, Korea, Japan, India", PAY),
    ("53", "developers led", "Nexdecade, Bangladesh", STREAM),
    ("10M+", "government system users", "Public sector, Bangladesh", GOV),
    ("10K+", "pharmacy clients served", "Healthcare, Bangladesh", HEALTH),
    ("20+", "branches automated", "Healthcare ERP, Bangladesh", ERP),
]

INDUSTRIES = [("Healthcare", HEALTH), ("Enterprise ERP", ERP), ("Government and banking", GOV),
              ("Payments and airlines", PAY), ("Streaming", STREAM)]

BACKEND, FRONTEND, DATA, INFRA, MOBILE = ERP, GOV, HEALTH, PAY, STREAM
TECH_GROUPS = [("Backend", BACKEND), ("Frontend", FRONTEND), ("Data", DATA), ("Infrastructure", INFRA), ("Mobile", MOBILE)]
TECH = [("PHP", 10, BACKEND), ("JavaScript", 10, FRONTEND), ("MySQL", 10, DATA), ("Laravel", 8, BACKEND),
        ("MongoDB", 8, DATA), ("C#", 7, BACKEND), ("Redis", 6, DATA), ("Android", 6, MOBILE),
        ("Spring Boot", 5, BACKEND), ("PostgreSQL", 5, DATA), ("Docker", 5, INFRA), ("Node.js", 4, BACKEND),
        ("Kubernetes", 4, INFRA), ("Kafka", 3, INFRA)]

TICKER = ["Laravel", "Spring Boot", "Kafka", "Kubernetes", "Docker", "MongoDB", "Redis", "PostgreSQL",
          "WebRTC", "Python", "C#", "Vue", "Android", "Node.js"]
TICKER_COLORS = [PAY, HEALTH, ERP, GOV, CYAN, HEALTH, PAY, GOV, STREAM, ERP, STREAM, HEALTH, HEALTH, ERP]

STRIPS = [
    ("techzu", "Software Engineer IV", "Techzu Ichicode Pte Ltd", "Dec 2024 to present", "Enterprise ERP and AI", ERP, True),
    ("nexdecade", "Head of Development", "Nexdecade Technology", "Mar 2024 to Dec 2024", "Toffee and T Sports", STREAM, False),
    ("adventure", "Asst. Manager, Payment Development", "Adventure Dhaka Ltd", "Mar 2023 to Feb 2024", "Payments and airlines", PAY, False),
    ("pharma", "Asst. Manager, Application Development", "Pharma Solutions Bangladesh Ltd", "Nov 2017 to Feb 2023", "Healthcare", HEALTH, False),
    ("earlier", "Software Engineer to Sr. Software Engineer", "IECL, Advance Business Solutions", "2015 to 2017", "Government, banking, ERP", GOV, False),
]

SECTIONS = {"impact": "impact", "systems": "real_world_systems", "experience": "experience", "career": "career", "domains": "domains",
            "specialities": "specialities", "stack": "stack", "education": "education", "contact": "get_in_touch"}

SYSTEMS = [
    ("face", ["Face recognition", "attendance"], ["Marks attendance by recognising", "faces on camera"], CYAN),
    ("pcb", ["PCB mismatch", "detection"], ["Flags boards that do not match", "during inspection"], HEALTH),
    ("gateway", ["TZone temperature", "gateway system"],
     ["Own system, no vendor software:", "decodes raw gateway data into", "exact records in MongoDB"], PAY),
    ("cluster", ["High-scale MongoDB", "clustering"], ["Replication and sharding for", "large, busy datasets"], ERP),
    ("wheel", ["Kubernetes", "orchestration"], ["Runs streaming and payment", "platforms in production"], GOV),
    ("directory", ["Active Directory", "at Pharma Solutions"], ["Central user accounts", "and access management"], STREAM),
]

DOMAINS = [
    ("Payments and travel", ["Multi-gateway payments, NDC airline", "integration and global hotel booking"],
     ["Spring Boot", "Kafka", "Laravel", "Vue", "Docker", "Kubernetes"], PAY),
    ("Enterprise ERP", ["Distribution, construction, HRM", "and business process automation"],
     ["Laravel", "CakePHP", "MySQL", "WhatsApp API", "OCR"], ERP),
    ("Healthcare and distribution", ["Pharmacy ordering, inventory, field", "sales apps and IoT monitoring"],
     ["Laravel", "C#", "ASP.NET", "Android", "Ionic", "Spring Boot", "Active Directory"], HEALTH),
    ("Streaming and real time", ["Toffee and T Sports OTT platforms,", "WebRTC video calling, high-traffic APIs"],
     ["Spring Boot", "Docker", "Kubernetes", "WebRTC", "Node.js"], STREAM),
    ("Government and banking", ["Public systems at scale and", "secure financial services"],
     ["PHP", "Symfony", "Node.js", "Vue", "Ionic", "MySQL"], GOV),
    ("AI and automation", ["Face recognition, PCB mismatch", "detection, OCR and on-device speech"],
     ["Python", ".NET", "Laravel", "Telegram API"], CYAN),
]

SPECIALITIES = [
    ("System architecture", "ERP, payment and streaming platforms", ERP),
    ("Microservices", "Kubernetes, Spring Boot, Kafka, monolith migrations", PAY),
    ("API design", "REST and SOAP, gateways under 200 ms", GOV),
    ("Payment integration", "PayPal, Adyen, Toss Pay, KakaoPay, 2C2P, HitPay, AXS", PAY),
    ("Database scaling", "High-scale MongoDB clusters, Redis caching", HEALTH),
    ("Real-time systems", "WebRTC, Socket.io, WhatsApp, IoT temperature gateways", STREAM),
    ("Performance and cost", "30% faster systems, 20% lower infrastructure cost", ERP),
    ("Process automation", "ERP and HRM across 20+ branches", HEALTH),
    ("AI integration", "Face recognition, PCB mismatch detection, OCR", CYAN),
    ("Engineering leadership", "Led 53 developers, agile delivery, mentoring", PINK),
]

MOTION_OFF = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def fmt(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def shape(s, size, wght, opsz, fam):
    face = FACES[fam]
    font = hb.Font(face)
    font.set_variations({"wght": wght, "opsz": opsz, "wdth": 100} if fam == "d" else {"wght": wght})
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False, "calt": False})
    return font, buf.glyph_infos, buf.glyph_positions, size / face.upem


def advance(s, size, wght=400, opsz=14, fam="d", track=0):
    _, _, pos, k = shape(s, size, wght, opsz, fam)
    return sum(p.x_advance * k + track for p in pos)


def outline(s, x, y, size, wght, opsz=14, fam="d", track=0, anchor="start"):
    font, infos, pos, k = shape(s, size, wght, opsz, fam)
    x -= {"start": 0, "middle": advance(s, size, wght, opsz, fam, track) / 2,
          "end": advance(s, size, wght, opsz, fam, track)}[anchor]
    pen = SVGPathPen(None, ntos=fmt)
    for info, p in zip(infos, pos):
        font.draw_glyph_with_pen(info.codepoint, TransformPen(pen, (k, 0, 0, -k, x + p.x_offset * k, y - p.y_offset * k)))
        x += p.x_advance * k + track
    return pen.getCommands()


def text(s, x, y, size, wght, fill, **kw):
    return f'<path fill="{fill}" d="{outline(s, x, y, size, wght, **kw)}"/>'


def mono(s, x, y, size, wght, fill, **kw):
    return text(s, x, y, size, wght, fill, fam="m", **kw)


def save(name, w, h, body, alt, css="", defs=""):
    style = f"<style>{css}{MOTION_OFF}</style>" if css else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
           f'aria-label="{alt}">\n<title>{alt}</title>\n<defs>{defs}</defs>{style}\n{body}\n</svg>\n')
    with open(os.path.join(OUT, name), "w", encoding="utf8", newline="\n") as f:
        f.write(svg)
    print(name, len(svg))


def flow_gradient(gid, width):
    stops = "".join(f'<stop offset="{i / (len(FLOW) - 1):.3f}" stop-color="{c}"/>' for i, c in enumerate(FLOW))
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" spreadMethod="repeat" x1="0" x2="{width}" y1="0" y2="0">{stops}</linearGradient>'


def flowing_text(d, gid, width, h, dur=8):
    """Gradient-filled outlines. The fill slides by one period, so every frame is a valid colour."""
    return (f'<clipPath id="{gid}c"><path d="{d}"/></clipPath>'
            f'<g clip-path="url(#{gid}c)"><rect class="flow" x="{-width}" y="0" width="{width * 3}" height="{h}" fill="url(#{gid})" '
            f'style="animation-duration:{dur}s"/></g>')


def flow_css(width):
    return f".flow{{animation:flow 8s linear infinite}}@keyframes flow{{from{{transform:translateX(0)}}to{{transform:translateX({width}px)}}}}"


def hero():
    bar_x, year_w = 430, 47.5
    year_x = lambda y: bar_x + (y - 2015) * year_w
    axis_y, row0, row_h, bar_h = 318, 336, 46, 14
    h = row0 + row_h * len(ROLES) + 20
    left = 44

    p = [f'<rect width="{W}" height="{h}" fill="{BG}"/>',
         f'<circle class="a a1" cx="170" cy="120" r="380" fill="url(#g1)"/>',
         f'<circle class="a a2" cx="820" cy="90" r="400" fill="url(#g2)"/>',
         f'<circle class="a a3" cx="620" cy="600" r="420" fill="url(#g3)"/>',
         f'<rect width="{W}" height="44" fill="#fff" fill-opacity=".05"/>']
    for x, c in ((24, "#FF5F57"), (46, "#FEBC2E"), (68, "#28C840")):
        p.append(f'<circle cx="{x}" cy="22" r="6.5" fill="{c}"/>')
    p.append(mono("zawad@dhaka: ~/career", 500, 27, 14, 500, MUTED, anchor="middle"))

    p.append(mono("~", left, 88, 19, 700, HEALTH))
    p.append(mono("$", left + 24, 88, 19, 700, CYAN))
    p.append(mono("whoami", left + 48, 88, 19, 500, PAPER))

    name = outline("Zawadul Kawum", left - 3, 170, 86, 800, opsz=96, track=0.6)
    p.append(flowing_text(name, "n", 620, 240))
    p.append(text("Backend engineer and engineering lead, since 2015.", left, 212, 25, 500, PAPER, opsz=25))

    # The typed line is decoration: every word here is also in the tagline and the trace.
    prefix = "> building "
    p.append(mono(prefix, left, 256, 19, 500, HEALTH))
    wx = left + advance(prefix, 19, 500, fam="m")
    for i, w in enumerate(BUILDING):
        tw = advance(w, 19, 600, fam="m")
        p.append(f'<g class="w" style="animation-delay:{i * 3}s{";opacity:1" if not i else ""}">{mono(w, wx, 256, 19, 600, PINK)}'
                 f'<rect class="c" x="{fmt(wx + tw + 3)}" y="241" width="11" height="19" fill="{PINK}"/></g>')

    p.append(f'<rect x="0" y="{axis_y - 26}" width="{W}" height="{h - axis_y + 26}" fill="{PANEL}" fill-opacity=".72"/>')
    for y in range(2015, 2027):
        x = year_x(y)
        p.append(f'<path d="M{fmt(x)} {axis_y + 8}V{h - 14}" stroke="{LINE}"/>')
        if y % 2:
            p.append(mono(str(y), x, axis_y, 14, 500, MUTED, anchor="middle"))

    route, clips, shimmer_bars = [], [], ""
    for i, (name_, what, start, end, color) in enumerate(ROLES):
        top = row0 + row_h * i
        p.append(text(name_, left, top + 15, 19, 600, PAPER, opsz=19))
        p.append(text(what, left, top + 35, 15.5, 400, MUTED, opsz=16))
        y = top + 6
        x0, x1 = year_x(start), W if end is None else year_x(end)
        mid = y + bar_h / 2
        route.append(f"{'M' if not i else 'L'}{fmt(x0)} {fmt(mid)}L{fmt(x1)} {fmt(mid)}")
        if i:
            p.append(f'<path d="M{fmt(x0)} {y - row_h + bar_h}V{y}" stroke="{MUTED}" stroke-opacity=".55" stroke-dasharray="3 3"/>')
        p.append(f'<rect x="{fmt(x0)}" y="{y}" width="{fmt(x1 - x0)}" height="{bar_h}" rx="4" fill="{color}"/>')
        clips.append(f'<rect x="{fmt(x0)}" y="{y}" width="{fmt(x1 - x0)}" height="{bar_h}" rx="4"/>')
    p.append(f'<g clip-path="url(#bars)"><rect class="sh" x="-140" y="{row0}" width="140" height="{row_h * 6}" fill="url(#shine)"/></g>')
    p.append(f'<g class="pkt"><circle r="11" fill="#fff" fill-opacity=".22"/><circle r="4.5" fill="#fff"/></g>')

    path = "".join(route)
    defs = ('<radialGradient id="g1"><stop stop-color="#7C3AED" stop-opacity=".6"/><stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="g2"><stop stop-color="#06B6D4" stop-opacity=".45"/><stop offset="1" stop-color="#06B6D4" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="g3"><stop stop-color="#EC4899" stop-opacity=".38"/><stop offset="1" stop-color="#EC4899" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="shine"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="bars">{"".join(clips)}</clipPath><clipPath id="p"><rect width="{W}" height="{h}" rx="14"/></clipPath>'
            + flow_gradient("n", 620))
    css = (flow_css(620) +
           ".a{transform-box:fill-box;transform-origin:center;animation:drift 16s ease-in-out infinite alternate}"
           ".a2{animation-duration:21s;animation-direction:alternate-reverse}.a3{animation-duration:26s}"
           "@keyframes drift{from{transform:translate(-70px,-30px) scale(1)}to{transform:translate(90px,50px) scale(1.2)}}"
           ".sh{animation:sh 6s ease-in-out infinite}@keyframes sh{from{transform:translateX(0)}to{transform:translateX(1140px)}}"
           f".pkt{{offset-path:path('{path}');offset-rotate:0deg;animation:pkt 11s linear infinite}}"
           "@keyframes pkt{from{offset-distance:0%}to{offset-distance:100%}}"
           ".w{opacity:0;animation:word 12s steps(1) infinite}"
           "@keyframes word{0%{opacity:1}25%,100%{opacity:0}}"
           ".c{animation:blink 1s steps(2) infinite}@keyframes blink{0%{opacity:1}100%{opacity:0}}")
    alt = "Zawadul Kawum. Backend engineer and engineering lead, since 2015. Career drawn as a distributed trace, one colored span per employer."
    save("hero.svg", W, h, f'<g clip-path="url(#p)">{"".join(p)}</g>', alt, css, defs)


def impact():
    gap, tile_h = 14, 166
    tile_w = (W - gap * 2) / 3
    p, defs = [], []
    for i, (num, label, where, color) in enumerate(IMPACT):
        x, y = (tile_w + gap) * (i % 3), (tile_h + gap) * (i // 3)
        defs.append(f'<radialGradient id="t{i}" cx="1" cy="0" r="1"><stop stop-color="{color}" stop-opacity=".42"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
        box = f'x="{fmt(x + 1)}" y="{y + 1}" width="{fmt(tile_w - 2)}" height="{tile_h - 2}" rx="12"'
        p.append(f'<rect {box} fill="{PANEL}"/><rect {box} fill="url(#t{i})"/>')
        p.append(f'<rect {box} fill="none" stroke="{color}" stroke-opacity=".45" stroke-width="1.5"/>')
        p.append(f'<rect {box} class="run" pathLength="1000" fill="none" stroke="{color}" stroke-width="3" style="animation-delay:{-i * 1.1:.1f}s"/>')
        p.append(text(num, x + 28, y + 80, 60, 800, color, opsz=96))
        p.append(text(label, x + 28, y + 114, 20, 500, PAPER, opsz=20))
        p.append(text(where, x + 28, y + 141, 16.5, 400, MUTED, opsz=17))
    css = (".run{stroke-dasharray:130 870;animation:run 6.6s linear infinite}"
           "@keyframes run{from{stroke-dashoffset:0}to{stroke-dashoffset:-1000}}")
    alt = "Impact: " + ", ".join(f"{n} {l} ({w})" for n, l, w, _ in IMPACT)
    save("impact.svg", W, tile_h * 2 + gap, "".join(p), alt, css, "".join(defs))


def charts():
    h, pad = 610, 48
    p = [f'<rect width="{W}" height="{h}" rx="14" fill="{PANEL}"/>',
         f'<rect x=".75" y=".75" width="{W - 1.5}" height="{h - 1.5}" rx="14" fill="none" stroke="{LINE}" stroke-width="1.5"/>',
         '<circle class="a" cx="880" cy="60" r="330" fill="url(#gl)"/>',
         text("Years by industry", pad, 72, 30, 700, PAPER, opsz=30),
         text("Years by technology", 500, 72, 30, 700, PAPER, opsz=30)]
    totals = {}
    for _, _, start, end, color in ROLES:
        totals[color] = totals.get(color, 0) + (end or NOW) - start
    total = sum(totals.values())
    cx, cy, r, sw = 226, 232, 104, 42
    circ = 2 * math.pi * r
    offset = 0
    for name, color in INDUSTRIES:
        length = totals[color] / total * circ
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" '
                 f'stroke-dasharray="{length - 3:.1f} {circ - length + 3:.1f}" stroke-dashoffset="{-offset:.1f}" '
                 f'transform="rotate(-90 {cx} {cy})"/>')
        offset += length
    p.append(f'<circle class="orb" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="{sw}" '
             f'stroke-dasharray="46 {circ - 46:.1f}"/>')
    p.append(text("Since", cx, cy - 6, 22, 500, MUTED, opsz=22, anchor="middle"))
    p.append(text("2015", cx, cy + 32, 42, 800, PAPER, opsz=96, anchor="middle"))
    for i, (name, color) in enumerate(INDUSTRIES):
        y = 402 + i * 36
        p.append(f'<rect x="{pad}" y="{y - 14}" width="16" height="16" rx="4" fill="{color}"/>')
        p.append(text(name, pad + 28, y, 20, 500, PAPER, opsz=20))
        p.append(mono(f"{totals[color]:.1f}", 428, y, 19, 600, PAPER, anchor="end"))
    for row, group in enumerate((TECH_GROUPS[:3], TECH_GROUPS[3:])):
        x = 500
        for name, color in group:
            y = 92 + row * 26
            p.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="4" fill="{color}"/>')
            p.append(text(name, x + 21, y + 13, 16, 500, MUTED, opsz=16))
            x += advance(name, 16, 500, opsz=16) + 50
    base, unit = 622, 28
    clips = []
    for i, (name, years, color) in enumerate(TECH):
        y = 170 + i * 30
        p.append(text(name, base - 12, y, 18, 500, PAPER, opsz=18, anchor="end"))
        p.append(f'<rect x="{base}" y="{y - 14}" width="{years * unit}" height="17" rx="4" fill="{color}"/>')
        clips.append(f'<rect x="{base}" y="{y - 14}" width="{years * unit}" height="17" rx="4"/>')
        p.append(mono(f"{years}+", base + years * unit + 8, y, 16, 600, MUTED))
    p.append(f'<g clip-path="url(#tb)"><rect class="sh" x="{base - 120}" y="150" width="120" height="430" fill="url(#shine)"/></g>')
    defs = (f'<clipPath id="tb">{"".join(clips)}</clipPath>'
            '<linearGradient id="shine"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="gl"><stop stop-color="#7C3AED" stop-opacity=".3"/><stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></radialGradient>')
    css = (".orb{transform-box:fill-box;transform-origin:center;animation:orb 9s linear infinite}"
           "@keyframes orb{to{transform:rotate(360deg)}}"
           ".sh{animation:sh 5s ease-in-out infinite}@keyframes sh{to{transform:translateX(420px)}}"
           ".a{transform-box:fill-box;transform-origin:center;animation:a 14s ease-in-out infinite alternate}"
           "@keyframes a{from{transform:translate(-40px,0)}to{transform:translate(-300px,300px)}}")
    alt = ("Years by industry: " + ", ".join(f"{n} {totals[c]:.1f}" for n, c in INDUSTRIES) +
           ". Years by technology: " + ", ".join(f"{n} {y}+" for n, y, _ in TECH))
    save("charts.svg", W, h, "".join(p), alt, css, defs)


def strips():
    h, block = 108, 300
    for key, title, company, dates, domain, color, live in STRIPS:
        p = [f'<g clip-path="url(#c)"><rect width="{W}" height="{h}" fill="{PANEL}"/>',
             f'<rect width="{W}" height="{h}" fill="url(#w)"/>',
             f'<rect width="7" height="{h}" fill="{color}"/></g>',
             f'<rect x=".75" y=".75" width="{W - 1.5}" height="{h - 1.5}" rx="12" fill="none" stroke="{color}" stroke-opacity=".5" stroke-width="1.5"/>',
             mono(dates, 30, 44, 17, 600, color), text(domain, 30, 74, 17, 500, MUTED, opsz=17),
             text(title, block + 30, 48, 26, 700, PAPER, opsz=27), text(company, block + 30, 80, 19, 400, MUTED, opsz=20)]
        css = ""
        if live:
            p.append(f'<circle cx="942" cy="40" r="6" fill="{HEALTH}"/><circle class="ping" cx="942" cy="40" r="6" fill="none" stroke="{HEALTH}" stroke-width="2"/>')
            p.append(mono("now", 924, 45, 15, 600, HEALTH, anchor="end"))
            p.append(f'<rect class="run" pathLength="1000" x=".75" y=".75" width="{W - 1.5}" height="{h - 1.5}" rx="12" fill="none" stroke="{color}" stroke-width="3"/>')
            css = (".run{stroke-dasharray:110 890;animation:run 7s linear infinite}@keyframes run{to{stroke-dashoffset:-1000}}"
                   ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2s ease-out infinite}"
                   "@keyframes ping{from{transform:scale(1);opacity:.9}to{transform:scale(3.2);opacity:0}}")
        defs = (f'<clipPath id="c"><rect width="{W}" height="{h}" rx="12"/></clipPath>'
                f'<linearGradient id="w"><stop stop-color="{color}" stop-opacity=".3"/><stop offset=".55" stop-color="{color}" stop-opacity="0"/></linearGradient>')
        save(f"role-{key}.svg", W, h, "".join(p), f"{title}, {company}, {dates}", css, defs)


def sections():
    h = 54
    for key, label in SECTIONS.items():
        d = outline(f"// {label}", 0, 34, 27, 700, fam="m")
        body = flowing_text(d, "s", W, h) + f'<g clip-path="url(#l)"><rect class="flow" x="{-W}" y="48" width="{W * 3}" height="2" fill="url(#s)"/></g>'
        defs = flow_gradient("s", W) + f'<clipPath id="l"><rect y="48" width="{W}" height="2"/></clipPath>'
        save(f"section-{key}.svg", W, h, body, label.replace("_", " ").capitalize(), flow_css(W), defs)


def ticker():
    h, size = 52, 18
    seq, x = [], 0
    while x < W:
        for name, color in zip(TICKER, TICKER_COLORS):
            seq.append((name, color, x))
            x += advance(name, size, 500, fam="m") + 58
    period = x
    row = []
    for shift in (0, period):
        for name, color, nx in seq:
            row.append(f'<circle cx="{fmt(nx + shift + 26)}" cy="{h / 2}" r="5" fill="{color}"/>')
            row.append(mono(name, nx + shift + 40, h / 2 + 6.5, size, 500, PAPER))
    body = (f'<g clip-path="url(#c)"><rect width="{W}" height="{h}" fill="{PANEL}"/><g class="t">{"".join(row)}</g>'
            f'<rect width="90" height="{h}" fill="url(#l)"/><rect x="{W - 90}" width="90" height="{h}" fill="url(#r)"/></g>'
            f'<rect x=".75" y=".75" width="{W - 1.5}" height="{h - 1.5}" rx="12" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    defs = (f'<clipPath id="c"><rect width="{W}" height="{h}" rx="12"/></clipPath>'
            f'<linearGradient id="l"><stop stop-color="{PANEL}"/><stop offset="1" stop-color="{PANEL}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="r"><stop stop-color="{PANEL}" stop-opacity="0"/><stop offset="1" stop-color="{PANEL}"/></linearGradient>')
    css = f".t{{animation:t {period / 40:.0f}s linear infinite}}@keyframes t{{to{{transform:translateX({-period:.1f}px)}}}}"
    save("ticker.svg", W, h, body, "Technologies: " + ", ".join(TICKER), css, defs)


def card(i, x, y, w, h, color, gid="d"):
    defs = f'<radialGradient id="{gid}{i}" cx="1" cy="0" r="1"><stop stop-color="{color}" stop-opacity=".36"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
    box = f'x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="12"'
    return defs, (f'<rect {box} fill="{PANEL}"/><rect {box} fill="url(#{gid}{i})"/>'
                  f'<rect {box} fill="none" stroke="{color}" stroke-opacity=".45" stroke-width="1.5"/>'
                  f'<rect {box} class="run" pathLength="1000" fill="none" stroke="{color}" stroke-width="3" style="animation-delay:{-i * 1.2:.1f}s"/>')


RUN_CSS = (".run{stroke-dasharray:120 880;animation:run 7.2s linear infinite}"
           "@keyframes run{from{stroke-dashoffset:0}to{stroke-dashoffset:-1000}}")


def domains():
    gap, card_w, card_h = 14, 493, 204
    p, defs = [], []
    for i, (name, lines, tools, color) in enumerate(DOMAINS):
        x, y = (card_w + gap) * (i % 2), (card_h + gap) * (i // 2)
        d, shape_ = card(i, x, y, card_w, card_h, color)
        defs.append(d)
        p.append(shape_)
        p.append(text(name, x + 26, y + 44, 26, 700, color, opsz=27))
        for j, line in enumerate(lines):
            p.append(text(line, x + 26, y + 78 + j * 26, 19, 400, PAPER, opsz=19))
        cx, cy = x + 26, y + 128
        for tool in tools:
            tw = advance(tool, 15, 500, fam="m") + 22
            if cx + tw > x + card_w - 20:
                cx, cy = x + 26, cy + 34
            p.append(f'<rect x="{fmt(cx)}" y="{cy}" width="{fmt(tw)}" height="27" rx="7" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".55"/>')
            p.append(mono(tool, cx + 11, cy + 19, 15, 500, PAPER))
            cx += tw + 8
    css = RUN_CSS
    alt = "Domains: " + "; ".join(f"{n}, using {', '.join(t)}" for n, _, t, _ in DOMAINS)
    save("domains.svg", W, card_h * 3 + gap * 2, "".join(p), alt, css, "".join(defs))


def motif_face(cx, cy, c):
    s = f'fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"'
    brackets = "".join(f'<path d="M{cx + a * 66} {cy + b * 44}V{cy + b * 66}H{cx + a * 44}" {s}/>' for a in (-1, 1) for b in (-1, 1))
    face = (f'<ellipse cx="{cx}" cy="{cy - 4}" rx="30" ry="38" fill="{c}" fill-opacity=".1" stroke="{PAPER}" stroke-width="2.5"/>'
            f'<circle cx="{cx - 12}" cy="{cy - 12}" r="3.5" fill="{PAPER}"/><circle cx="{cx + 12}" cy="{cy - 12}" r="3.5" fill="{PAPER}"/>'
            f'<path d="M{cx - 11} {cy + 13}q11 9 22 0" fill="none" stroke="{PAPER}" stroke-width="2.5" stroke-linecap="round"/>')
    scan = f'<rect class="scany" x="{cx - 58}" y="{cy - 1.5}" width="116" height="3" rx="1.5" fill="{c}"/>'
    return brackets + face + scan


def motif_pcb(cx, cy, c, flag):
    x, y = cx - 72, cy - 56
    p = [f'<rect x="{x}" y="{y}" width="144" height="112" rx="8" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-width="2.5"/>']
    for d in ("M-72 -30H-46V-14H-22", "M-72 28H-48V10H-22", "M22 -14H44V-34H72", "M0 -24V-56", "M0 24V56", "M22 12H72"):
        p.append(f'<path transform="translate({cx} {cy})" d="{d}" fill="none" stroke="{c}" stroke-opacity=".75" stroke-width="2"/>')
    p.append(f'<rect x="{cx - 22}" y="{cy - 24}" width="44" height="48" rx="4" fill="{PANEL}" stroke="{PAPER}" stroke-width="2.5"/>')
    for ax, ay in ((-46, -30), (-48, 28), (44, -34)):
        p.append(f'<circle cx="{cx + ax}" cy="{cy + ay}" r="4.5" fill="{c}"/>')
    fx, fy = cx + 48, cy + 12
    p.append(f'<rect x="{fx - 7}" y="{fy - 7}" width="14" height="14" rx="3" fill="{flag}"/>')
    p.append(f'<rect class="ping" x="{fx - 7}" y="{fy - 7}" width="14" height="14" rx="3" fill="none" stroke="{flag}" stroke-width="2"/>')
    p.append(f'<rect class="scanx" x="{cx - 1.5}" y="{y + 4}" width="3" height="104" rx="1.5" fill="{PAPER}" fill-opacity=".8"/>')
    return "".join(p)


def motif_cluster(cx, cy, c):
    nodes = [(cx, cy - 46, "P", 25), (cx - 56, cy + 40, "S", 21), (cx + 56, cy + 40, "S", 21)]
    p = []
    for i, (nx, ny, _, _) in enumerate(nodes[1:]):
        line = f'x1="{cx}" y1="{cy - 46}" x2="{nx}" y2="{ny}"'
        p.append(f'<line {line} stroke="{c}" stroke-opacity=".5" stroke-width="2.5"/>')
        p.append(f'<line {line} class="pkt" pathLength="100" stroke="{PAPER}" stroke-width="4" stroke-linecap="round" style="animation-delay:{-i * .7:.1f}s"/>')
    p.append(f'<line x1="{cx - 56}" y1="{cy + 40}" x2="{cx + 56}" y2="{cy + 40}" stroke="{c}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="5 6"/>')
    for i, (nx, ny, label, r) in enumerate(nodes):
        p.append(f'<circle cx="{nx}" cy="{ny}" r="{r}" fill="{PANEL}"/>')
        p.append(f'<circle cx="{nx}" cy="{ny}" r="{r}" fill="{c}" fill-opacity="{.3 if not i else .14}" stroke="{c}" stroke-width="2.5"/>')
        p.append(mono(label, nx, ny + 6.5, 19, 700, PAPER, anchor="middle"))
    return "".join(p)


def motif_wheel(cx, cy, c):
    pts = [(cx + 62 * math.sin(i * 2 * math.pi / 7), cy - 62 * math.cos(i * 2 * math.pi / 7)) for i in range(7)]
    ring = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    p = [f'<polygon points="{ring}" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-width="2.5" stroke-linejoin="round"/>']
    for px, py in pts:
        p.append(f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{c}" stroke-opacity=".65" stroke-width="2.5"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{PANEL}" stroke="{PAPER}" stroke-width="2.5"/>')
    for px, py in pts:
        p.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{c}"/>')
    return f'<g class="spin" style="transform-origin:{cx}px {cy}px">{"".join(p)}</g>'


def motif_gateway(cx, cy, c):
    p = []
    for ax in (cx - 24, cx + 24):
        p.append(f'<line x1="{ax}" y1="{cy - 62}" x2="{ax}" y2="{cy - 78}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>')
    p.append(f'<rect x="{cx - 40}" y="{cy - 62}" width="80" height="24" rx="6" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-width="2.5"/>')
    for i in range(3):
        p.append(f'<circle cx="{cx - 18 + i * 18}" cy="{cy - 50}" r="3.5" fill="{PAPER}"/>')
    p.append(f'<circle class="ping" cx="{cx + 24}" cy="{cy - 78}" r="3" fill="none" stroke="{c}" stroke-width="2"/>')
    for y1, y2 in ((cy - 38, cy - 20), (cy + 10, cy + 28)):
        p.append(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="{c}" stroke-opacity=".5" stroke-width="2.5"/>')
        p.append(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" class="pkt" pathLength="100" stroke="{PAPER}" stroke-width="4" stroke-linecap="round"/>')
    p.append(f'<rect x="{cx - 70}" y="{cy - 20}" width="140" height="30" rx="6" fill="{PANEL}" stroke="{PAPER}" stroke-width="2"/>')
    p.append(mono("54 5A 24 24", cx, cy + 0.5, 16, 600, PAPER, anchor="middle"))
    for i in range(3):
        p.append(f'<rect x="{cx - 70 + i * 48}" y="{cy + 28}" width="44" height="28" rx="5" fill="{c}" fill-opacity="{.55 if not i else .22}" stroke="{c}" stroke-width="2"/>')
    return "".join(p)


def motif_directory(cx, cy, c):
    ous = [cx - 48, cx + 48]
    users = [cx - 72, cx - 24, cx + 24, cx + 72]
    p = []
    for i, ox in enumerate(ous):
        line = f'x1="{cx}" y1="{cy - 44}" x2="{ox}" y2="{cy - 2}"'
        p.append(f'<line {line} stroke="{c}" stroke-opacity=".6" stroke-width="2.5"/>')
        p.append(f'<line {line} class="pkt" pathLength="100" stroke="{PAPER}" stroke-width="4" stroke-linecap="round" style="animation-delay:{-i * .7:.1f}s"/>')
    for i, ux in enumerate(users):
        p.append(f'<line x1="{ous[i // 2]}" y1="{cy + 12}" x2="{ux}" y2="{cy + 46}" stroke="{c}" stroke-opacity=".6" stroke-width="2.5"/>')
    p.append(f'<polygon points="{cx},{cy - 76} {cx + 28},{cy - 34} {cx - 28},{cy - 34}" fill="{c}" fill-opacity=".3" stroke="{c}" stroke-width="2.5" stroke-linejoin="round"/>')
    for ox in ous:
        p.append(f'<rect x="{ox - 22}" y="{cy - 12}" width="44" height="24" rx="6" fill="{PANEL}" stroke="{PAPER}" stroke-width="2.5"/>')
    for ux in users:
        p.append(f'<circle cx="{ux}" cy="{cy + 52}" r="10" fill="{c}"/>')
    return "".join(p)


def systems():
    gap, card_w, card_h = 14, 493, 196
    motifs = {"face": motif_face, "pcb": lambda cx, cy, c: motif_pcb(cx, cy, c, PAY),
              "cluster": motif_cluster, "wheel": motif_wheel,
              "gateway": motif_gateway, "directory": motif_directory}
    p, defs = [], []
    for i, (kind, title, lines, color) in enumerate(SYSTEMS):
        x, y = (card_w + gap) * (i % 2), (card_h + gap) * (i // 2)
        d, shape_ = card(i, x, y, card_w, card_h, color, "y")
        defs.append(d)
        p.append(shape_)
        for j, line in enumerate(title):
            p.append(text(line, x + 26, y + 50 + j * 31, 26, 700, color, opsz=27))
        for j, line in enumerate(lines):
            p.append(text(line, x + 26, y + 122 - (len(lines) - 2) * 10 + j * 26, 18, 400, PAPER, opsz=18))
        p.append(motifs[kind](x + card_w - 100, y + card_h // 2, color))
    css = (RUN_CSS +
           ".scany{animation:sy 3.2s ease-in-out infinite alternate}@keyframes sy{from{transform:translateY(-52px)}to{transform:translateY(52px)}}"
           ".scanx{animation:sx 4.4s ease-in-out infinite alternate}@keyframes sx{from{transform:translateX(-64px)}to{transform:translateX(64px)}}"
           ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}"
           "@keyframes ping{from{transform:scale(1);opacity:.9}to{transform:scale(3);opacity:0}}"
           ".pkt{stroke-dasharray:1 99;animation:pkt 1.4s linear infinite}@keyframes pkt{from{stroke-dashoffset:0}to{stroke-dashoffset:-100}}"
           ".spin{animation:spin 28s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}")
    alt = "Real-world systems: " + "; ".join(f"{' '.join(t)}: {' '.join(l)}" for _, t, l, _ in SYSTEMS)
    save("systems.svg", W, card_h * 3 + gap * 2, "".join(p), alt, css, "".join(defs))


def specialities():
    row_h, top = 74, 22
    h = top * 2 + row_h * 5
    p = [f'<rect width="{W}" height="{h}" rx="14" fill="{PANEL}"/>',
         '<circle class="a" cx="120" cy="60" r="340" fill="url(#gl)"/>',
         f'<rect x=".75" y=".75" width="{W - 1.5}" height="{h - 1.5}" rx="14" fill="none" stroke="{LINE}" stroke-width="1.5"/>']
    for i, (name, proof, color) in enumerate(SPECIALITIES):
        x, y = 36 + (i % 2) * 478, top + (i // 2) * row_h
        cy = y + row_h / 2
        p.append(f'<circle cx="{x + 8}" cy="{cy}" r="7" fill="{color}"/>')
        p.append(f'<circle class="ping" cx="{x + 8}" cy="{cy}" r="7" fill="none" stroke="{color}" stroke-width="2" style="animation-delay:{-i * .35:.2f}s"/>')
        p.append(text(name, x + 32, y + 32, 22, 700, PAPER, opsz=22))
        p.append(text(proof, x + 32, y + 57, 16.5, 400, MUTED, opsz=17))
    defs = '<radialGradient id="gl"><stop stop-color="#06B6D4" stop-opacity=".22"/><stop offset="1" stop-color="#06B6D4" stop-opacity="0"/></radialGradient>'
    css = (".ping{transform-box:fill-box;transform-origin:center;animation:ping 3.5s ease-out infinite}"
           "@keyframes ping{from{transform:scale(1);opacity:.9}to{transform:scale(2.6);opacity:0}}"
           ".a{transform-box:fill-box;transform-origin:center;animation:a 16s ease-in-out infinite alternate}"
           "@keyframes a{from{transform:translate(0,0)}to{transform:translate(760px,160px)}}")
    alt = "Specialities: " + "; ".join(f"{n}: {e}" for n, e, _ in SPECIALITIES)
    save("specialities.svg", W, h, "".join(p), alt, css, defs)


hero()
impact()
systems()
charts()
strips()
sections()
ticker()
domains()
specialities()
