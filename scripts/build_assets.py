#!/usr/bin/env python3
"""Generates every SVG used by the profile README, in a light and a dark variant.

    python scripts/build_assets.py

Edit the CARDS list or the copy below, rerun, commit the assets/ folder.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

MONO = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', "
        "'Nirmala UI', 'Kohinoor Devanagari', 'Noto Sans Devanagari', monospace")
SANS = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, "
        "'Nirmala UI', 'Kohinoor Devanagari', 'Noto Sans Devanagari', sans-serif")

# GitHub's own palette, with Jaipur pink as the accent.
THEMES = {
    "dark": dict(card="#151b23", bar="#10151c", inset="#0d1117", border="#2a313c",
                 text="#e6edf3", muted="#9198a1", dim="#656c76", accent="#ff9b85",
                 green="#56d364", red="#ff7b72", yellow="#e3b341", blue="#79c0ff",
                 purple="#d2a8ff"),
    "light": dict(card="#ffffff", bar="#f6f8fa", inset="#f6f8fa", border="#d1d9e0",
                  text="#1f2328", muted="#59636e", dim="#818b98", accent="#b8442b",
                  green="#1a7f37", red="#cf222e", yellow="#9a6700", blue="#0969da",
                  purple="#8250df"),
}


def x(s):
    return escape(s, quote=False)


def spans(t, line):
    """A line is a plain string or a list of (text, color[, bold]) segments."""
    if isinstance(line, str):
        line = [(line, "text")]
    out = []
    for seg in line:
        text, color = seg[0], seg[1]
        bold = ' font-weight="700"' if len(seg) > 2 and seg[2] else ""
        out.append(f'<tspan fill="{t[color]}"{bold}>{x(text)}</tspan>')
    return "".join(out)


def svg(w, h, label, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">\n'
            f'<style>.m{{font-family:{MONO};white-space:pre}}.s{{font-family:{SANS}}}{style}</style>\n'
            f'{body}\n</svg>\n')


# --------------------------------------------------------------------------- header

def hawa_mahal(t, cx, base):
    """Hawa Mahal, Jaipur: stepped tiers of domed jharokhas."""
    tiers = [(204, 40), (176, 34), (148, 32), (118, 30), (86, 26), (52, 22)]
    parts, y = [], base
    for i, (w, h) in enumerate(tiers):
        top = y - h
        left = cx - w / 2
        g = [f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="2" '
             f'fill="{t["accent"]}" fill-opacity=".12" stroke="{t["accent"]}" stroke-width="1.2"/>']
        n = int((w - 10) // 14)
        start = cx - (n - 1) * 14 / 2
        for k in range(n):
            wx = start + k * 14
            r, wh = 3.5, h - 14
            if i == 0 and abs(wx - cx) < 8:
                continue  # leave room for the gate
            g.append(f'<path d="M{wx - r} {top + 7 + wh} V{top + 7 + r} A{r} {r} 0 0 1 {wx + r} {top + 7 + r} '
                     f'V{top + 7 + wh} Z" fill="{t["accent"]}" fill-opacity=".55"/>')
            g.append(f'<path d="M{wx - 4.5} {top} A4.5 4.5 0 0 1 {wx + 4.5} {top} Z" '
                     f'fill="{t["accent"]}" fill-opacity=".45"/>')
        if i == 0:
            g.append(f'<path d="M{cx - 9} {y} V{top + 18} A9 9 0 0 1 {cx + 9} {top + 18} V{y} Z" '
                     f'fill="{t["accent"]}" fill-opacity=".7"/>')
        parts.append(f'<g class="a" style="animation-delay:{0.35 + i * 0.12:.2f}s">{"".join(g)}</g>')
        y = top
    crown = [f'<path d="M{cx + dx - r} {y} A{r} {r} 0 0 1 {cx + dx + r} {y} Z" fill="{t["accent"]}" fill-opacity=".8"/>'
             f'<line x1="{cx + dx}" y1="{y - r}" x2="{cx + dx}" y2="{y - r - 6}" stroke="{t["accent"]}" stroke-width="1.2"/>'
             for dx, r in ((-16, 6), (0, 9), (16, 6))]
    parts.append(f'<g class="a" style="animation-delay:1.1s">{"".join(crown)}</g>')
    parts.append(f'<line x1="{cx - 120}" y1="{base + .5}" x2="{cx + 120}" y2="{base + .5}" stroke="{t["border"]}"/>')
    parts.append(f'<text x="{cx}" y="{base + 20}" class="m a" style="animation-delay:1.2s" font-size="11" '
                 f'text-anchor="middle" fill="{t["dim"]}">26.92°N 75.82°E · the pink city</text>')
    return "".join(parts)


def header(t):
    W, H = 900, 300
    body = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>',
        f'<path d="M.5 38 V12.5 A12 12 0 0 1 12.5 .5 H{W - 12.5} A12 12 0 0 1 {W - .5} 12.5 V38 Z" fill="{t["bar"]}"/>',
        f'<line x1=".5" y1="38.5" x2="{W - .5}" y2="38.5" stroke="{t["border"]}"/>',
        *[f'<circle cx="{22 + i * 20}" cy="19.5" r="6" fill="{c}"/>'
          for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))],
        f'<text x="{W / 2}" y="24" class="s" font-size="13" text-anchor="middle" fill="{t["dim"]}">ujjwal@jaipur: ~</text>',
    ]

    def prompt():
        return f'<tspan fill="{t["blue"]}">~</tspan><tspan fill="{t["dim"]}"> $ </tspan>'

    def typed(cmd, start, step=0.07):
        chars = "".join(f'<tspan class="k" style="animation-delay:{start + i * step:.2f}s">{x(c)}</tspan>'
                        for i, c in enumerate(cmd))
        return f'<tspan fill="{t["text"]}">{chars}</tspan>', start + len(cmd) * step

    def line(y, inner, delay=None):
        cls = "m a" if delay is not None else "m"
        style = f' style="animation-delay:{delay:.2f}s"' if delay is not None else ""
        return f'<text x="32" y="{y}" class="{cls}" font-size="16"{style}>{inner}</text>'

    cmd, end = typed("whoami", 0.3)
    body.append(line(84, prompt() + cmd))
    body.append(line(113, spans(t, [("Ujjwal Dadhich", "text", True), ("  ·  Jaipur, Rajasthan, India", "muted")]), end + .2))
    body.append(line(139, spans(t, [("नमस्ते! ", "accent", True), ("I turn ideas into products people actually use.", "muted")]), end + .35))

    cmd, end = typed("ls ~/projects", end + .8)
    body.append(line(181, prompt() + cmd))
    rows = [["chapterchase", "darshan-player", "hindicode", "commit-roast"],
            ["todo-tomb", "env-triage", "indian-number", "hinglishify", "slug-wizard"]]
    d = end + .2
    for y, names in zip((209, 235), rows):
        inner = []
        for n in names:
            inner.append(f'<tspan class="t" style="animation-delay:{d:.2f}s" fill="{t["blue"]}" font-weight="700">{n}</tspan>'
                         f'<tspan class="t" style="animation-delay:{d:.2f}s" fill="{t["dim"]}">/  </tspan>')
            d += .06
        body.append(line(y, "".join(inner)))

    body.append(f'<g class="a" style="animation-delay:{d + .3:.2f}s">'
                + line(277, prompt() + f'<tspan class="cur" fill="{t["accent"]}" style="animation-delay:{d + .3:.2f}s">█</tspan>')
                + "</g>")
    body.append(hawa_mahal(t, 770, 248))

    # tspans ignore `opacity` in some browsers, so text runs fade with fill-opacity
    style = ("@keyframes f{from{opacity:0}to{opacity:1}}"
             "@keyframes ft{from{fill-opacity:0}to{fill-opacity:1}}"
             "@keyframes b{0%{fill-opacity:1}50%{fill-opacity:0}}"
             ".a{animation:f .3s ease-out both}"
             ".t{animation:ft .3s ease-out both}"
             ".k{animation:ft .05s linear both}"
             ".cur{animation:b 1.1s steps(1) infinite}"
             "@media (prefers-reduced-motion:reduce){.a,.t,.k,.cur{animation:none}}")
    label = ("Terminal: whoami prints Ujjwal Dadhich, Jaipur, Rajasthan, India. "
             "ls ~/projects lists chapterchase, darshan-player, hindicode, commit-roast, todo-tomb, "
             "env-triage, indian-number, hinglishify and slug-wizard. Beside it, a drawing of Hawa Mahal.")
    return svg(W, H, label, "\n".join(body), style)


# --------------------------------------------------------------------------- banner

def chapterchase(t):
    W, H = 900, 176
    body = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>',
        f'<text x="32" y="42" class="m" font-size="12" letter-spacing="2" fill="{t["accent"]}" font-weight="700">NOW BUILDING</text>',
        f'<text x="32" y="80" class="s" font-size="30" font-weight="700" fill="{t["text"]}">ChapterChase</text>',
        f'<text x="32" y="108" class="s" font-size="15" fill="{t["muted"]}">Read and publish novels and comics, with forums for readers</text>',
        f'<text x="32" y="128" class="s" font-size="15" fill="{t["muted"]}">and a way for authors to get paid.</text>',
        f'<text x="32" y="156" class="m" font-size="12">'
        + spans(t, [("chapterchase.com ↗", "accent", True), ("   Qwik · Bun · Expo · Cloudflare", "dim")]) + '</text>',
    ]
    # a shelf of books
    shelf_y, bx = 146, 622
    books = [(20, 86, "accent", .9), (16, 70, "blue", .75), (24, 98, "purple", .7), (18, 78, "yellow", .75),
             (22, 92, "accent", .55), (15, 66, "green", .7), (26, 104, "blue", .5), (19, 82, "purple", .5)]
    for i, (w, h, c, o) in enumerate(books):
        y = shelf_y - h
        g = (f'<rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="2.5" fill="{t[c]}" fill-opacity="{o}"/>'
             f'<rect x="{bx + 3}" y="{y + 10}" width="{w - 6}" height="2" rx="1" fill="{t["card"]}" fill-opacity=".55"/>'
             f'<rect x="{bx + 3}" y="{y + h - 14}" width="{w - 6}" height="2" rx="1" fill="{t["card"]}" fill-opacity=".55"/>')
        body.append(g)
        bx += w + 4
    # one book leaning on the last
    lw, lh = 20, 88
    body.append(f'<g transform="rotate(-16 {bx + lw} {shelf_y})"><rect x="{bx + 6}" y="{shelf_y - lh}" width="{lw}" height="{lh}" '
                f'rx="2.5" fill="{t["accent"]}" fill-opacity=".8"/>'
                f'<rect x="{bx + 9}" y="{shelf_y - lh + 10}" width="{lw - 6}" height="2" rx="1" fill="{t["card"]}" fill-opacity=".55"/></g>')
    body.append(f'<line x1="606" y1="{shelf_y + .5}" x2="{W - 32}" y2="{shelf_y + .5}" stroke="{t["border"]}" stroke-width="2"/>')
    label = ("Now building ChapterChase: read and publish novels and comics, with forums for readers "
             "and a way for authors to get paid. chapterchase.com")
    return svg(W, H, label, "\n".join(body))


# --------------------------------------------------------------------------- cards

def card(t, title, tag, desc, lines, extra=""):
    W, H = 400, 214
    body = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>',
        f'<text x="20" y="35" class="s" font-size="16" font-weight="600" fill="{t["text"]}">{x(title)}</text>',
        f'<text x="{W - 20}" y="34" class="m" font-size="11" text-anchor="end" fill="{t["dim"]}">{x(tag)}</text>',
        f'<text x="20" y="57" class="s" font-size="12.5" fill="{t["muted"]}">{x(desc)}</text>',
        f'<rect x="12" y="72" width="{W - 24}" height="{H - 84}" rx="7" fill="{t["inset"]}" stroke="{t["border"]}" stroke-opacity=".7"/>',
    ]
    for i, ln in enumerate(lines):
        body.append(f'<text x="26" y="{95 + i * 19}" class="m" font-size="12">{spans(t, ln)}</text>')
    body.append(extra)
    return svg(W, H, f"{title}: {desc}", "\n".join(body))


def P(cmd):  # shell prompt line
    return [("$ ", "dim"), (cmd, "text", True)]


def darshan_extra(t):
    y = 158
    track_l, track_r = 50, 300
    fill = track_l + (track_r - track_l) * .46
    a, b = track_l + (track_r - track_l) * .3, track_l + (track_r - track_l) * .63
    return "".join([
        f'<path d="M28 {y - 7} L40 {y} L28 {y + 7} Z" fill="{t["accent"]}"/>',
        f'<rect x="{track_l}" y="{y - 2}" width="{track_r - track_l}" height="4" rx="2" fill="{t["border"]}"/>',
        f'<rect x="{track_l}" y="{y - 2}" width="{fill - track_l}" height="4" rx="2" fill="{t["accent"]}"/>',
        f'<circle cx="{fill}" cy="{y}" r="6" fill="{t["card"]}" stroke="{t["accent"]}" stroke-width="2"/>',
        *[f'<line x1="{p}" y1="{y - 9}" x2="{p}" y2="{y + 9}" stroke="{t["yellow"]}" stroke-width="1.5"/>'
          f'<text x="{p}" y="{y - 12}" class="m" font-size="9" text-anchor="middle" fill="{t["yellow"]}">{lbl}</text>'
          for p, lbl in ((a, "A"), (b, "B"))],
        f'<text x="312" y="{y + 4}" class="m" font-size="11" fill="{t["muted"]}">1:12:08</text>',
        f'<text x="26" y="190" class="m" font-size="11" fill="{t["dim"]}">MP4 MKV AVI MOV MP3 FLAC · subtitles · PiP</text>',
    ])


CARDS = [
    ("darshan-player", "Darshan Player", "C# · WPF", "Free, open-source media player for Windows.",
     [[("PS> ", "dim"), ("winget install UjjwalDadhich.Darshan", "text", True)],
      [("Successfully installed", "green")]],
     darshan_extra),
    ("hindicode", "hindicode", "npm", "Write JavaScript in Hindi. 100% keyword coverage.",
     [[("स्थिर ", "purple"), ("नाम = ", "text"), ('"अर्जुन"', "blue"), (";", "text")],
      [("कार्य ", "purple"), ("स्वागत", "accent"), ("(व्यक्ति) {", "text")],
      [("  लौटाओ ", "purple"), ("`नमस्ते ${व्यक्ति}`", "blue"), (";", "text")],
      [("}", "text")],
      [("दिखाओ", "accent"), ("(स्वागत(नाम));", "text"), ("  // नमस्ते अर्जुन", "dim")]],
     None),
    ("hinglishify", "hinglishify", "npx", "Hinglish to Devanagari and back. Hindi URL slugs.",
     [P('npx hinglishify "kaise ho"'), [("कैसे हो", "green")],
      P('npx hinglishify --latin "नमस्ते दुनिया"'), [("namaste duniya", "green")],
      P('npx hinglishify --slug "मेरा Blog पोस्ट #1"'), [("mera-blog-post-1", "green")]],
     None),
    ("indian-number", "indian-number", "npx", "Lakh, crore and rupees in words, in English and Hindi.",
     [P("npx indian-number 12345678.9"),
      [("grouped     ", "dim"), ("1,23,45,678.90", "text")],
      [("currency    ", "dim"), ("₹1,23,45,678.90", "green")],
      [("short       ", "dim"), ("1.23 crore", "text")],
      [("devanagari  ", "dim"), ("१,२३,४५,६७८.९०", "text")],
      [("words hi    ", "dim"), ("एक करोड़ तेईस लाख पैंतालीस हज़ार …", "text")]],
     None),
    ("commit-roast", "commit-roast", "npx", "Roasts your git commit messages. Offline, no AI.",
     [P("npx commit-roast"),
      [("✖ ", "red"), ("4 subjects run past 72 characters — that is", "text")],
      [("  not a subject, that is the body wearing a", "text")],
      [("  subject's coat.", "text")],
      [("score 85/100 ", "muted"), ("[█████████████████", "accent"), ("░░░]", "dim"), (" grade A", "green", True)]],
     None),
    ("todo-tomb", "todo-tomb", "npx", "Every TODO in your repo, aged with git blame.",
     [P("npx todo-tomb"),
      [("🍂 ", "text"), ("BUG ", "red", True), ("src/services/chapter-admin.service.ts:21", "muted")],
      [("   buried 1 month ago by Ujjwal Dadhich", "dim")],
      [("🌱 ", "text"), ("DEPRECATED ", "yellow", True), ("src/components/Link.tsx:13", "muted")],
      [("   buried 19 days ago by Ujjwal Dadhich", "dim")],
      [("12 markers in 9 files · oldest 3m", "text")]],
     None),
    ("env-triage", "env-triage", "npx", "The .env checkup that never prints your secrets.",
     [P("npx env-triage"),
      [("✗ ", "red"), ("SENTRY_DSN      ", "text", True), ("missing from .env", "muted")],
      [("✗ ", "red"), ("SESSION_SECRET  ", "text", True), ("is still a placeholder value", "muted")],
      [("⚠ ", "yellow"), ("API_PORT        ", "text", True), ("defined more than once", "muted")],
      [("⚠ ", "yellow"), ("STRIPE_SECRET_KEY ", "text", True), ("looks like a real secret", "muted")],
      [("5 errors, 12 warnings, 6 info", "text")]],
     None),
    ("slug-wizard", "slug-wizard", "npm", "URL slugs with collision handling. No dependencies.",
     [P("npm i slug-wizard"),
      [("> ", "dim"), ("createSlug", "accent"), ('("Straße in Łódź")', "text")],
      [("'strasse-in-lodz'", "green")],
      [("> ", "dim"), ("generateUniqueSlug", "accent"), ('("My Post", {existingSlugs})', "text")],
      [("'my-post-2'", "green"), ("  // my-post, my-post-1 taken", "dim")]],
     None),
]


def main():
    (OUT / "cards").mkdir(parents=True, exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
        (OUT / f"chapterchase-{name}.svg").write_text(chapterchase(t), encoding="utf-8")
        for slug, title, tag, desc, lines, extra in CARDS:
            svg_text = card(t, title, tag, desc, lines, extra(t) if extra else "")
            (OUT / "cards" / f"{slug}-{name}.svg").write_text(svg_text, encoding="utf-8")
    print(f"wrote {2 + len(CARDS)} x {len(THEMES)} svgs to {OUT}")


if __name__ == "__main__":
    main()
