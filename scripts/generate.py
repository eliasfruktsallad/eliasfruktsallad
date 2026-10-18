"""Generates the self-hosted SVG for the GitHub profile README."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(text="#e6edf3", muted="#7d8590", faint="#484f58", rule="#262c36", live="#3fb950"),
    "light": dict(text="#1f2328", muted="#656d76", faint="#8c959f", rule="#e5e8eb", live="#1a7f37"),
}

W, COL = 1000, 230

ROWS = [
    ("About", [
        [("I build interfaces and the systems behind them.", "text")],
        [("Focused on clarity, performance and details that hold up.", "muted")],
    ]),
    ("Stack", [
        [("Languages", "faint"), ("TypeScript, JavaScript, Python, PHP", "text")],
        [("Frontend", "faint"), ("React, Next.js, Vue, Tailwind, Sass", "text")],
        [("Backend", "faint"), ("Node.js, PostgreSQL, MySQL, Docker, Linux", "text")],
    ]),
    ("Projects", [
        [("vk-studio", "text"), ("In progress", "status")],
    ]),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def page(t):
    out = []
    out.append(f'<text x="0" y="52" font-size="40" font-weight="600" letter-spacing="-1.2" fill="{t["text"]}">Elias</text>')
    out.append(f'<text x="0" y="92" font-size="19" fill="{t["muted"]}">Developer, building for the web.</text>')
    out.append(f'<text x="{W}" y="52" text-anchor="end" font-size="15" fill="{t["muted"]}">On GitHub since 2021</text>')

    y = 140
    for label, lines in ROWS:
        out.append(f'<rect x="0" y="{y}" width="{W}" height="1" fill="{t["rule"]}"/>')
        ly = y + 42
        out.append(f'<text x="0" y="{ly}" font-size="15" fill="{t["muted"]}">{label}</text>')
        for line in lines:
            if len(line) == 1:
                txt, tone = line[0]
                out.append(f'<text x="{COL}" y="{ly}" font-size="17" fill="{t[tone]}">{esc(txt)}</text>')
            else:
                (a, a_tone), (b, b_tone) = line
                if b_tone == "status":
                    out.append(f'<text x="{COL}" y="{ly}" font-size="17" fill="{t[a_tone]}">{esc(a)}</text>')
                    out.append(f'<text x="{W}" y="{ly}" text-anchor="end" font-size="15" fill="{t["muted"]}">{esc(b)}</text>')
                    out.append(f'<circle cx="{W - 92}" cy="{ly - 5}" r="3.5" fill="{t["live"]}"/>')
                else:
                    out.append(f'<text x="{COL}" y="{ly}" font-size="15" fill="{t[a_tone]}">{esc(a)}</text>')
                    out.append(f'<text x="{COL + 140}" y="{ly}" font-size="17" fill="{t[b_tone]}">{esc(b)}</text>')
            ly += 30
        y = ly + 6
    out.append(f'<rect x="0" y="{y}" width="{W}" height="1" fill="{t["rule"]}"/>')
    h = y + 1

    body = "\n  ".join(out)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" fill="none" role="img" aria-label="Elias. Developer, building for the web.">
  <style>text {{ font-family: {SANS}; }}</style>
  {body}
</svg>
"""


for mode, t in THEMES.items():
    (OUT / f"profile-{mode}.svg").write_text(page(t), encoding="utf-8")
print("ok")
