"""Generates the self-hosted SVGs for the GitHub profile README.

Usage: python generate.py <screenshots-dir> <assets-dir>
Screenshots are 1440x900 PNGs named after the project slugs below.
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image

SHOTS = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(text="#e6edf3", muted="#8b949e", faint="#5a636e", rule="#262c36",
                 panel="#11161d", panel2="#161b22", live="#3fb950"),
    "light": dict(text="#1f2328", muted="#59636e", faint="#8c959f", rule="#e1e4e8",
                  panel="#f6f8fa", panel2="#eef1f4", live="#1a7f37"),
}

PROJECTS = [
    ("sainabou", "Sainabou Secka", "Makeup artist portfolio, Stockholm", "sainabousecka.se"),
    ("akbar", "Akbar Abdul Rasul", "Author and speaker website", "akbarabdulrasul.com"),
    ("mteknik", "M-Teknik", "Industrial products, Karlstad", "m-teknik.se"),
    ("crdator", "CR Datorservice", "Computer repair and custom builds", "crdatorservice.se"),
    ("expertdack", "Expert Däck", "Tyres and car service, Göteborg", "expert-dack.vercel.app"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def svg(w, h, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{esc(label)}">
  <style>text {{ font-family: {SANS}; }}</style>
  {body}
</svg>
"""


def hero(t):
    b = [
        f'<text x="0" y="24" font-size="17" font-weight="600" fill="{t["text"]}">Elias</text>',
        f'<text x="1000" y="24" text-anchor="end" font-size="15" fill="{t["muted"]}">Web developer, Sweden</text>',
        f'<rect x="0" y="48" width="1000" height="1" fill="{t["rule"]}"/>',
        f'<text x="0" y="138" font-size="50" font-weight="600" letter-spacing="-1.6" fill="{t["text"]}">I design and build websites</text>',
        f'<text x="0" y="198" font-size="50" font-weight="600" letter-spacing="-1.6" fill="{t["faint"]}">for brands that care about detail.</text>',
    ]
    meta = [("Focus", "Web design and development"), ("Built with", "Next.js, TypeScript, Tailwind"),
            ("Also", "FiveM server development")]
    for i, (k, v) in enumerate(meta):
        x = i * 340
        b.append(f'<text x="{x}" y="262" font-size="14" fill="{t["faint"]}">{k}</text>')
        b.append(f'<text x="{x}" y="286" font-size="16" fill="{t["text"]}">{esc(v)}</text>')
    return svg(1000, 300, "\n  ".join(b), "Elias. Web developer, Sweden. I design and build websites for brands that care about detail.")


def heading(t, title, right):
    b = [
        f'<text x="0" y="30" font-size="22" font-weight="600" letter-spacing="-.4" fill="{t["text"]}">{esc(title)}</text>',
        f'<text x="1000" y="30" text-anchor="end" font-size="15" fill="{t["muted"]}">{esc(right)}</text>',
        f'<rect x="0" y="52" width="1000" height="1" fill="{t["rule"]}"/>',
    ]
    return svg(1000, 54, "\n  ".join(b), title)


CW, IH, CH = 600, 375, 452


def caption(t, name, kind, domain, dot=False):
    y = IH + 40
    b = [
        f'<text x="2" y="{y}" font-size="19" font-weight="600" letter-spacing="-.2" fill="{t["text"]}">{esc(name)}</text>',
        f'<text x="2" y="{y + 28}" font-size="16" fill="{t["muted"]}">{esc(kind)}</text>',
        f'<text x="{CW - 2}" y="{y}" text-anchor="end" font-size="15" fill="{t["muted"]}">{esc(domain)} ↗</text>',
    ]
    if dot:
        b.append(f'<circle cx="{CW - 8}" cy="{y + 23}" r="4" fill="{t["live"]}"/>')
        b.append(f'<text x="{CW - 20}" y="{y + 28}" text-anchor="end" font-size="15" fill="{t["muted"]}">Live</text>')
    return b


def frame(t, inner):
    return [
        '<defs><clipPath id="r"><rect width="600" height="375" rx="14"/></clipPath></defs>',
        f'<g clip-path="url(#r)">{inner}</g>',
        f'<rect x=".5" y=".5" width="599" height="374" rx="13.5" stroke="{t["rule"]}"/>',
    ]


def shot_b64(slug):
    im = Image.open(SHOTS / f"{slug}.png").convert("RGB").resize((1200, 750), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode()


def card(t, slug, name, kind, domain, data):
    img = f'<image width="600" height="375" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{data}"/>'
    b = frame(t, img) + caption(t, name, kind, domain, dot=True)
    return svg(CW, CH, "\n  ".join(b), f"{name}, {kind}")


def horisonten(t):
    lines = [("Resources", "Qbox, ox_lib, custom scripts"), ("Infrastructure", "Migrations, tooling, docs"),
             ("Assets", "Vehicles, MLOs, clothing, maps")]
    inner = [f'<rect width="600" height="375" fill="{t["panel"]}"/>',
             f'<text x="40" y="64" font-size="13" font-weight="600" letter-spacing="2" fill="{t["faint"]}">FIVEM ROLEPLAY SERVER</text>',
             f'<text x="38" y="128" font-size="46" font-weight="600" letter-spacing="-1.4" fill="{t["text"]}">Horisonten RP</text>',
             f'<text x="40" y="164" font-size="17" fill="{t["muted"]}">Full server build, from framework to streamed assets.</text>',
             f'<rect x="40" y="206" width="520" height="1" fill="{t["rule"]}"/>']
    for i, (k, v) in enumerate(lines):
        y = 246 + i * 38
        inner.append(f'<text x="40" y="{y}" font-size="15" fill="{t["faint"]}">{k}</text>')
        inner.append(f'<text x="190" y="{y}" font-size="16" fill="{t["text"]}">{esc(v)}</text>')
    b = frame(t, "".join(inner)) + caption(t, "Horisonten RP", "Game server development", "github.com/Horisonten-RP")
    return svg(CW, CH, "\n  ".join(b), "Horisonten RP, FiveM roleplay server")


def stack(t):
    rows = [("Web", "Next.js, React, TypeScript, Tailwind CSS"), ("Backend", "Node.js, PostgreSQL, Vercel"),
            ("Game", "Lua, FiveM, Qbox, ox_lib"), ("Also", "Python, PHP, Figma, Docker, Git")]
    b = []
    for i, (k, v) in enumerate(rows):
        y = 34 + i * 40
        b.append(f'<text x="0" y="{y}" font-size="15" fill="{t["faint"]}">{k}</text>')
        b.append(f'<text x="230" y="{y}" font-size="17" fill="{t["text"]}">{esc(v)}</text>')
    y = 34 + len(rows) * 40 - 6
    b.append(f'<rect x="0" y="{y}" width="1000" height="1" fill="{t["rule"]}"/>')
    b.append(f'<text x="0" y="{y + 40}" font-size="15" fill="{t["muted"]}">Open to new projects.</text>')
    b.append(f'<text x="1000" y="{y + 40}" text-anchor="end" font-size="15" fill="{t["faint"]}">On GitHub since 2021</text>')
    return svg(1000, y + 52, "\n  ".join(b), "Stack: Next.js, React, TypeScript, Tailwind CSS, Node.js, PostgreSQL, Vercel, Lua, FiveM.")


shots = {slug: shot_b64(slug) for slug, *_ in PROJECTS}
for mode, t in THEMES.items():
    files = {
        "hero": hero(t),
        "work": heading(t, "Selected work", "Websites and servers"),
        "stack-title": heading(t, "Stack", "Tools I reach for"),
        "stack": stack(t),
        "horisonten": horisonten(t),
    }
    for slug, name, kind, domain in PROJECTS:
        files[slug] = card(t, slug, name, kind, domain, shots[slug])
    for name, content in files.items():
        (OUT / f"{name}-{mode}.svg").write_text(content, encoding="utf-8")
print("ok")
