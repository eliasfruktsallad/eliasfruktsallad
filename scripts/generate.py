"""Generates the stat cards for the GitHub profile README.

Usage: python generate.py <octicons-dir> <assets-dir> <commit-dates.json>
The numbers are filled in by hand from the GitHub API (private repositories included).
"""
import datetime as dt
import json
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
    ("git-commit-16", "Commits in 2026:", "598"),
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


GRID, AXIS = "#44475a", "#6272a4"


def activity(dates):
    days = [dt.date.fromisoformat(d) for d in dates]
    start = min(days) - dt.timedelta(days=min(days).weekday())
    weeks = (max(days) - start).days // 7 + 1
    counts = [0] * weeks
    for d in days:
        counts[(d - start).days // 7] += 1
    w, h = 1000, 300
    x0, x1, y0, y1 = 30, 970, 250, 110
    top = max(10, math.ceil(max(counts) / 10) * 10)
    step = (x1 - x0) / weeks
    bw = step - 2
    b = [f'<rect width="{w}" height="{h}" rx="6" fill="{BG}"/>',
         f'<text x="30" y="46" font-size="22" fill="{TITLE}">Commit Activity</text>',
         f'<text x="30" y="72" font-size="14" fill="{AXIS}">Commits per week, private repositories included</text>',
         f'<text x="970" y="52" text-anchor="end" font-size="34" font-weight="600" fill="{VALUE}">{len(days)}</text>',
         f'<text x="970" y="74" text-anchor="end" font-size="14" fill="{AXIS}">commits in 2026</text>']
    for v in (top // 2, top):
        y = y0 - (y0 - y1) * v / top
        b.append(f'<rect x="{x0}" y="{y:.1f}" width="{x1 - x0}" height="1" fill="{GRID}" opacity=".6"/>')
        b.append(f'<text x="{x0}" y="{y - 5:.1f}" font-size="11" fill="{AXIS}">{v}</text>')
    peak = counts.index(max(counts))
    for i, c in enumerate(counts):
        if not c:
            continue
        bh = max(2, (y0 - y1) * c / top)
        x, y = x0 + i * step + 1, y0 - bh
        r = min(4, bw / 2, bh)
        b.append(f'<path d="M{x:.1f},{y0} V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} H{x + bw - r:.1f} '
                 f'Q{x + bw:.1f},{y:.1f} {x + bw:.1f},{y + r:.1f} V{y0} Z" fill="{TITLE}"/>')
        if i == peak:
            b.append(f'<text x="{x + bw / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="12" font-weight="600" fill="{VALUE}">{c}</text>')
    b.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="1" fill="{GRID}"/>')
    month = None
    for i in range(weeks):
        d = start + dt.timedelta(days=7 * i)
        if d.month != month:
            month = d.month
            b.append(f'<text x="{x0 + i * step + 1:.1f}" y="{y0 + 22}" font-size="12" fill="{AXIS}">{d.strftime("%b")}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="Commit activity: {len(days)} commits in 2026, peak week {max(counts)} commits.">
  <style>text {{ font-family: {SANS}; }}</style>
  {"\n  ".join(b)}
</svg>
"""


(OUT / "card-activity.svg").write_text(activity(json.load(open(sys.argv[3]))), encoding="utf-8")
(OUT / "card-stats.svg").write_text(stats(), encoding="utf-8")
(OUT / "card-languages.svg").write_text(languages(), encoding="utf-8")
print("ok")
