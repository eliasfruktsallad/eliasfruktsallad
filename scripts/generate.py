"""Generates the self-hosted SVGs for the GitHub profile README.

Usage: python generate.py <assets-dir>
"""
import math
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(panel="#11161d", line="#e6edf3", text="#f0f6fc", muted="#8b949e", faint="#5a636e",
                 rule="#262c36", accent="#ff5a36"),
    "light": dict(panel="#f6f8fa", line="#1f2328", text="#1f2328", muted="#59636e", faint="#8c959f",
                  rule="#e1e4e8", accent="#e5482a"),
}

W, H = 1000, 420


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def svg(h, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" fill="none" role="img" aria-label="{esc(label)}">
  <style>text {{ font-family: {SANS}; }}</style>
  {body}
</svg>
"""


def ridges():
    """Rows of noisy peaks, strongest in the middle, as point lists from back to front."""
    rnd = random.Random(7)
    rows, n, x0, x1, cx = [], 34, 572, 936, 754
    for i in range(n):
        base = 112 + i * 7.6
        bumps = [(rnd.gauss(cx, 34), rnd.uniform(12, 24), rnd.uniform(0.25, 1.0)) for _ in range(rnd.randint(3, 5))]
        phase = rnd.uniform(0, 100)
        pts = []
        for x in range(x0, x1 + 1, 3):
            env = math.exp(-((x - cx) / 105) ** 4)
            peak = sum(a * math.exp(-((x - c) / w) ** 2) for c, w, a in bumps)
            noise = 0.5 + 0.5 * math.sin(x * 0.13 + phase) * math.sin(x * 0.051 + phase * 1.7)
            y = base - env * (math.tanh(peak / 1.3) * 52 + noise * 6) - rnd.uniform(0, 1.2) * env
            pts.append((x, y))
        rows.append((base, pts))
    return rows


RIDGES = ridges()
ACCENT_ROW = 21

ROWS = [("Focus", "Interfaces and the systems behind them"),
        ("Stack", "TypeScript, React, Next.js, Tailwind CSS"),
        ("Also", "Node.js, PostgreSQL, Lua, Python")]


def hero(t):
    b = ['<defs><clipPath id="r"><rect width="1000" height="420" rx="18"/></clipPath></defs>',
         f'<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="{t["panel"]}"/>']
    for i, (base, pts) in enumerate(RIDGES):
        d = "M" + " L".join(f"{x},{y:.1f}" for x, y in pts)
        fill = d + f" L{pts[-1][0]},{base + 30:.0f} L{pts[0][0]},{base + 30:.0f} Z"
        accent = i == ACCENT_ROW
        b.append(f'<path d="{fill}" fill="{t["panel"]}"/>')
        b.append(f'<path d="{d}" stroke="{t["accent"] if accent else t["line"]}" stroke-width="{1.5 if accent else 1}" '
                 f'stroke-linejoin="round"{"" if accent else " stroke-opacity=\".85\""}/>')
    b.append('</g>')
    b += [
        f'<rect x=".5" y=".5" width="999" height="419" rx="17.5" stroke="{t["rule"]}"/>',
        f'<text x="48" y="78" font-size="13" font-weight="600" letter-spacing="2" fill="{t["faint"]}">DEVELOPER · SWEDEN</text>',
        f'<text x="44" y="158" font-size="76" font-weight="600" letter-spacing="-2.6" fill="{t["text"]}">Elias</text>',
        f'<text x="48" y="200" font-size="18" fill="{t["muted"]}">Building calm, well-made software for the web.</text>',
        f'<rect x="48" y="244" width="452" height="1" fill="{t["rule"]}"/>',
    ]
    for i, (k, v) in enumerate(ROWS):
        y = 288 + i * 40
        b.append(f'<text x="48" y="{y}" font-size="15" fill="{t["faint"]}">{k}</text>')
        b.append(f'<text x="160" y="{y}" font-size="16" fill="{t["text"]}">{esc(v)}</text>')
    b.append(f'<text x="952" y="384" text-anchor="end" font-size="13" letter-spacing="2" fill="{t["faint"]}">EST. 2021</text>')
    return svg(H, "\n  ".join(b), "Elias. Developer, Sweden. Building calm, well-made software for the web. Stack: TypeScript, React, Next.js, Tailwind CSS, Node.js, PostgreSQL, Lua, Python.")


def footer(t):
    b = [f'<circle cx="52" cy="22" r="4" fill="{t["accent"]}"/>',
         f'<text x="66" y="27" font-size="15" fill="{t["muted"]}">Thanks for stopping by.</text>',
         f'<text x="952" y="27" text-anchor="end" font-size="15" fill="{t["faint"]}">github.com/eliasfruktsallad</text>']
    return svg(44, "\n  ".join(b), "Thanks for stopping by.")


for mode, t in THEMES.items():
    (OUT / f"hero-{mode}.svg").write_text(hero(t), encoding="utf-8")
    (OUT / f"footer-{mode}.svg").write_text(footer(t), encoding="utf-8")
print("ok")
