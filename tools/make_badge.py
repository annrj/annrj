#!/usr/bin/env python3
"""Generate pastel skill badges as self-hosted SVG files (no dependencies).

Usage (run from the repository root):
  python tools/make_badge.py "Kubernetes" mint        # one badge
  python tools/make_badge.py --all                    # rebuild every badge in tools/badges.json

Colours: blue | lavender | mint | peach
Output : assets/badges/badge-<label-as-slug>.svg   (e.g. "REST APIs" -> badge-rest-apis.svg)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "badges"
INK = "#2E3250"
FONT = "'Avenir Next','Nunito','Segoe UI','Helvetica Neue',Arial,sans-serif"
# light fill, border, accent dot
COLOURS = {
    "blue":     ("#E3EFFF", "#B7D4FA", "#8FB8F0"),
    "lavender": ("#EEE9FC", "#CFC2F2", "#AE9BE6"),
    "mint":     ("#E1F6EC", "#B8E8D2", "#8DD6B7"),
    "peach":    ("#FFEBDF", "#FFD0BA", "#FFB594"),
}

def slug(label):
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")

def text_width(text, size=13):
    """Rough, slightly generous width estimate so text never clips."""
    narrow, wide = set("iljtfI.,:;'|/!- "), set("mwMW")
    total = 0.0
    for ch in text:
        if ch in narrow: total += 0.30
        elif ch in wide: total += 0.85
        elif ch.isupper(): total += 0.68
        elif ch.isdigit(): total += 0.57
        else: total += 0.54
    return total * size * 1.06

def make_badge(label, colour):
    light, border, dot = COLOURS[colour]
    width = round(text_width(label) + 44)
    label = label.replace("&", "&amp;")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 30" width="{width}" height="30" role="img" aria-label="{label}">'
        f'<title>{label}</title>'
        f'<rect x="0.75" y="0.75" width="{width-1.5}" height="28.5" rx="14.25" fill="{light}" stroke="{border}" stroke-width="1.5"/>'
        f'<circle cx="16" cy="15" r="4" fill="{dot}"/>'
        f'<text x="28" y="19.5" font-family="{FONT}" font-size="13" font-weight="600" fill="{INK}">{label}</text>'
        f'</svg>'
    )

def write(label, colour):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"badge-{slug(label)}.svg"
    path.write_text(make_badge(label, colour), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        for item in json.loads((ROOT / "tools" / "badges.json").read_text(encoding="utf-8")):
            write(item["label"], item["colour"])
    elif len(args) == 2 and args[1] in COLOURS:
        write(args[0], args[1])
    else:
        sys.exit(__doc__)
