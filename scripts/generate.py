"""Generates the stat cards for the GitHub profile README.

Usage: python generate.py <octicons-dir> <assets-dir>
The numbers are filled in by hand from the GitHub API (private repositories included).
"""
import math
import re
import sys
from pathlib import Path

ICONS = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

# Dracula
BG, TITLE, LABEL, VALUE, MARK = "#282a36", "#ff79c6", "#ffb86c", "#f8f8f2", "#6272a4"
PALETTE = ["#ff79c6", "#8be9fd", "#ffb86c", "#f1fa8c", "#bd93f9", "#50fa7b"]

STATS = [
    ("git-commit-16", "Commits in 2026:", "595"),
    ("flame-16", "Active repos in 2026:", "25"),
    ("repo-16", "Total repos:", "37"),
    ("organization-16", "Organizations:", "4"),
    ("calendar-16", "On GitHub since:", "2021"),
]

LANGS = [("Lua", 42.2), ("TypeScript", 33.0), ("Python", 10.6), ("JavaScript", 6.7), ("Other", 7.5)]

W, H = 500, 220


def icon(name):
    return re.search(r'<path d="([^"]+)"', (ICONS / f"{name}.svg").read_text(encoding="utf-8")).group(1)


def card(title, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="{label}">
  <style>text {{ font-family: {SANS}; }}</style>
  <rect width="{W}" height="{H}" rx="6" fill="{BG}"/>
  <text x="30" y="46" font-size="22" fill="{TITLE}">{title}</text>
  {body}
</svg>
"""


def stats():
    b = []
    for i, (ic, k, v) in enumerate(STATS):
        y = 84 + i * 27
        b.append(f'<path transform="translate(30 {y - 13})" d="{icon(ic)}" fill="{LABEL}"/>')
        b.append(f'<text x="54" y="{y}" font-size="15" fill="{LABEL}">{k}</text>')
        b.append(f'<text x="230" y="{y}" font-size="15" font-weight="600" fill="{VALUE}">{v}</text>')
    b.append(f'<path transform="translate(330 60) scale(7)" d="{icon("mark-github-16")}" fill="{MARK}"/>')
    label = ", ".join(f"{k} {v}" for _, k, v in STATS)
    return card("Stats", "\n  ".join(b), label)


def arc(cx, cy, r0, r1, a0, a1):
    def p(r, a):
        return cx + r * math.cos(a), cy + r * math.sin(a)
    large = 1 if a1 - a0 > math.pi else 0
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p(r1, a0), p(r1, a1), p(r0, a1), p(r0, a0)
    return (f"M{x0:.2f},{y0:.2f} A{r1},{r1} 0 {large} 1 {x1:.2f},{y1:.2f} "
            f"L{x2:.2f},{y2:.2f} A{r0},{r0} 0 {large} 0 {x3:.2f},{y3:.2f} Z")


def languages():
    b, total = [], sum(p for _, p in LANGS)
    a = -math.pi / 2
    for i, (name, pct) in enumerate(LANGS):
        y = 84 + i * 27
        col = PALETTE[i]
        b.append(f'<rect x="30" y="{y - 12}" width="13" height="13" rx="2" fill="{col}"/>')
        b.append(f'<text x="52" y="{y}" font-size="15" fill="{VALUE}">{name}</text>')
        b.append(f'<text x="200" y="{y}" font-size="15" fill="{LABEL}">{pct:.1f}%</text>')
        sweep = 2 * math.pi * pct / total
        b.append(f'<path d="{arc(390, 128, 34, 62, a, a + sweep - 0.03)}" fill="{col}"/>')
        a += sweep
    label = "Top languages: " + ", ".join(f"{n} {p}%" for n, p in LANGS)
    return card("Top Languages", "\n  ".join(b), label)


(OUT / "stats.svg").write_text(stats(), encoding="utf-8")
(OUT / "languages.svg").write_text(languages(), encoding="utf-8")
print("ok")
