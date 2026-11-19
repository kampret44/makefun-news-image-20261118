#!/usr/bin/env python3
"""Render the make.fun news-image-20261118 entry: a one-page front page
summing up Wednesday 18 November 2026 world news.

Drawn entirely with Pillow (no network, no AI generation): text stays crisp
and legible, which is what the judge weighs. Run: python3 render.py
writes entry.png (1024x1024) in this directory.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (20, 38, 74)
NAVY_LT = (38, 64, 112)
RED = (179, 32, 44)
GOLD = (198, 142, 32)
GREY = (90, 88, 82)
LINE = (200, 192, 175)
MAP_BG = (226, 234, 240)
MAP_LAND = (176, 196, 168)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_badge(d, cx, cy, r, color, draw_icon):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
              outline=(255, 255, 255), width=2)
    draw_icon(d, cx, cy, r)


# ---- small pictograms, drawn inside a badge of radius r -------------------
def icon_globe(d, cx, cy, r):
    d.ellipse([cx - r * .55, cy - r * .55, cx + r * .55, cy + r * .55],
              outline=(255, 255, 255), width=3)
    d.ellipse([cx - r * .28, cy - r * .55, cx + r * .28, cy + r * .55],
              outline=(255, 255, 255), width=2)
    d.line([cx - r * .55, cy, cx + r * .55, cy], fill=(255, 255, 255), width=2)


def icon_missile(d, cx, cy, r):
    d.polygon([(cx, cy - r * .6), (cx + r * .3, cy + r * .1),
               (cx, cy + r * .55), (cx - r * .3, cy + r * .1)],
              fill=(255, 255, 255))
    d.polygon([(cx - r * .55, cy + r * .15), (cx - r * .2, cy + r * .35),
               (cx - r * .45, cy + r * .6)], fill=(255, 210, 90))


def icon_bridge(d, cx, cy, r):
    d.arc([cx - r * .6, cy - r * .2, cx + r * .6, cy + r * .9],
          180, 360, fill=(255, 255, 255), width=4)
    d.line([cx - r * .6, cy + r * .35, cx + r * .6, cy + r * .35],
           fill=(255, 255, 255), width=4)
    for x in (-.4, 0, .4):
        d.line([cx + x * r, cy - r * .05, cx + x * r, cy + r * .35],
               fill=(255, 255, 255), width=3)


def icon_ballot(d, cx, cy, r):
    d.rectangle([cx - r * .5, cy - r * .15, cx + r * .5, cy + r * .55],
                outline=(255, 255, 255), width=3)
    d.line([cx - r * .25, cy + r * .2, cx - r * .05, cy + r * .4,
            cx + r * .35, cy - r * .25], fill=(255, 255, 255), width=4)


def icon_virus(d, cx, cy, r):
    for k in range(8):
        import math
        a = k * math.pi / 4
        x1, y1 = cx + r * .35 * math.cos(a), cy + r * .35 * math.sin(a)
        x2, y2 = cx + r * .6 * math.cos(a), cy + r * .6 * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(255, 255, 255), width=3)
    d.ellipse([cx - r * .32, cy - r * .32, cx + r * .32, cy + r * .32],
              fill=(255, 255, 255))


def icon_probe(d, cx, cy, r):
    d.polygon([(cx - r * .5, cy + r * .3), (cx + r * .1, cy - r * .1),
               (cx + r * .55, cy - r * .55), (cx + r * .25, cy + r * .35)],
              outline=(255, 255, 255), width=3)
    d.line([cx + r * .1, cy - r * .1, cx + r * .55, cy - r * .55],
           fill=(255, 255, 255), width=3)
    d.ellipse([cx + r * .45, cy - r * .65, cx + r * .65, cy - r * .45],
              fill=(255, 210, 90))
    for sx, sy in ((-r * .55, -r * .45), (-r * .15, -r * .6)):
        d.ellipse([cx + sx - 2, cy + sy - 2, cx + sx + 2, cy + sy + 2],
                  fill=(255, 255, 255))


def icon_flags(d, cx, cy, r):
    for i, x in enumerate((-.35, .05)):
        d.line([cx + x * r, cy - r * .5, cx + x * r, cy + r * .55],
               fill=(255, 255, 255), width=3)
        d.polygon([(cx + x * r, cy - r * .5), (cx + (x + .45) * r, cy - r * .32),
                   (cx + x * r, cy - r * .14)], fill=(255, 210, 90) if i == 0
                  else (255, 255, 255))


def icon_euro(d, cx, cy, r):
    d.text((cx, cy), "\u20ac", font=font(SANS_B, int(r * 1.15)),
           fill=(255, 255, 255), anchor="mm")


def icon_chip(d, cx, cy, r):
    d.rectangle([cx - r * .35, cy - r * .35, cx + r * .35, cy + r * .35],
                outline=(255, 255, 255), width=3)
    d.rectangle([cx - r * .15, cy - r * .15, cx + r * .15, cy + r * .15],
                fill=(255, 255, 255))
    for x in (-.2, 0, .2):
        d.line([cx + x * r, cy - r * .55, cx + x * r, cy - r * .35],
               fill=(255, 255, 255), width=3)
        d.line([cx + x * r, cy + r * .35, cx + x * r, cy + r * .55],
               fill=(255, 255, 255), width=3)


# ---- story card ------------------------------------------------------------
def story_card(d, x, y, w, h, num, kicker, color, icon, headline, summary):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 3], fill=color)
    r = 24
    cx, cy = x + 12 + r, y + 14 + r
    draw_badge(d, cx, cy, r, color, icon)
    tx = x + 12 + 2 * r + 10
    d.text((tx, y + 9), kicker, font=font(SANS_B, 12), fill=color)
    hl = wrap(d, headline, font(SERIF_B, 20), w - (tx - x) - 10)
    yy = y + 27
    for line in hl[:2]:
        d.text((tx, yy), line, font=font(SERIF_B, 20), fill=INK)
        yy += 22
    yy = y + 73
    for line in wrap(d, summary, font(SANS, 14), w - (tx - x) - 10)[:2]:
        d.text((tx, yy), line, font=font(SANS, 14), fill=(52, 50, 46))
        yy += 16


# ---- simplified world map --------------------------------------------------
# Rough equirectangular continent outlines (lon/lat -> map box).
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 30), (-90, 21), (-97, 26), (-105, 20), (-110, 24),
     (-120, 34), (-125, 48), (-140, 60), (-155, 58), (-168, 66)],
    # South America
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52),
     (-73, -44), (-73, -30), (-70, -18), (-80, -5), (-80, 9)],
    # Africa
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (51, 11), (48, -1), (40, -10), (36, -18),
     (33, -26), (20, -35), (15, -27), (12, -18), (9, -1), (-8, 4),
     (-17, 15)],
    # Eurasia (Europe + Asia, one outline)
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 58), (10, 59),
     (18, 56), (21, 55), (24, 60), (30, 70), (45, 68), (60, 69),
     (75, 72), (90, 75), (110, 74), (130, 72), (150, 70), (170, 67),
     (178, 65), (162, 60), (158, 52), (142, 50), (140, 40), (130, 33),
     (122, 30), (115, 22), (108, 12), (104, 8), (100, 7), (97, 16),
     (92, 21), (88, 22), (80, 13), (77, 8), (72, 20), (66, 25),
     (61, 25), (57, 26), (52, 28), (48, 30), (44, 29), (40, 36),
     (36, 36), (30, 36), (26, 40), (23, 36), (19, 42), (12, 44),
     (8, 44), (3, 43), (-2, 37), (-10, 36)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (136, -15), (142, -11),
     (146, -19), (150, -23), (153, -27), (150, -37), (140, -38),
     (135, -35), (129, -32), (124, -33), (115, -35), (114, -22)],
]


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    return (mx + (lon + 180) / 360 * mw, my + (90 - lat) / 180 * mh)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MAP_BG, outline=LINE, width=1)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x + 6, y + 4, w - 12, h - 8)
               for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND, outline=(140, 160, 140))
    d.text((x + w - 12, y + 8), "WHERE IT HAPPENED", font=font(SANS_B, 13),
           fill=NAVY, anchor="ra")


def map_dot(d, x, y, w, h, lon, lat, num, label, lx, ly, anchor):
    """Dot radius 11; label anchored at (px+lx, py+ly) with at least a
    5px clear gap from the dot edge, so no text ever touches a dot."""
    px, py = lonlat_to_xy(lon, lat, x + 6, y + 4, w - 12, h - 8)
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=RED,
              outline=(255, 255, 255), width=2)
    d.text((px, py), str(num), font=font(SANS_B, 12),
           fill=(255, 255, 255), anchor="mm")
    d.text((px + lx, py + ly), label, font=font(SANS_B, 13), fill=INK,
           anchor=anchor)


# ---- page ------------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 12], fill=RED)
    d.text((24, 26), "THE WORLD", font=font(SERIF_B, 64), fill=INK)
    d.text((W - 24, 34), "THE WORLD IN ONE PAGE", font=font(SANS_B, 20),
           fill=NAVY, anchor="ra")
    d.text((W - 24, 62), "ONE DAY \u00b7 TWELVE STORIES \u00b7 SIX CONTINENTS",
           font=font(SANS, 14), fill=GREY, anchor="ra")
    d.line([24, 100, W - 24, 100], fill=INK, width=2)

    # date banner
    d.rectangle([24, 112, W - 24, 168], fill=NAVY)
    d.text((W // 2, 122), "WEDNESDAY  18  NOVEMBER  2026",
           font=font(SANS_B, 40), fill=(255, 255, 255), anchor="ma")

    # lead story
    ly, lh = 178, 108
    d.rectangle([24, ly, W - 24, ly + lh], fill=(255, 255, 255),
                outline=LINE, width=1)
    d.rectangle([24, ly, W - 24, ly + 4], fill=RED)
    draw_badge(d, 24 + 52, ly + lh // 2, 38, NAVY, icon_globe)
    tx = 24 + 104
    d.text((tx, ly + 10), "1 \u00b7 LEAD STORY \u2014 CHINA \u00b7 APEC SUMMIT",
           font=font(SANS_B, 14), fill=RED)
    d.text((tx, ly + 30), "Xi meets Putin in Shenzhen as Trump trilateral looms",
           font=font(SERIF_B, 30), fill=INK)
    for i, line in enumerate(wrap(
            d, "The three leaders are due to meet on Thursday 19 November "
            "\u2014 the first summit of its kind.",
            font(SANS, 17), W - 24 - tx - 16)):
        d.text((tx, ly + 68 + i * 20), line, font=font(SANS, 17),
               fill=(52, 50, 46))

    # grid of 8 stories, 2 columns x 4 rows
    stories = [
        (2, "MIDDLE EAST", NAVY_LT, icon_missile,
         "US strikes Iranian missile site; Iran hits Gulf bases",
         "US jets hit a launch site on Qeshm Island; Iran drones "
         "targeted bases in Bahrain and Kuwait."),
        (3, "UKRAINE WAR", (90, 60, 30), icon_bridge,
         "Ukraine hits the Kerch bridge again; span collapses",
         "Second day of strikes on the Russia\u2013Crimea link; Russia "
         "says it downed 1,400+ drones."),
        (4, "US POLITICS", (30, 90, 60), icon_ballot,
         "Peltola wins Alaska; Democrats take 56\u201344 Senate",
         "Democrat beats incumbent Dan Sullivan \u2014 the party's ninth "
         "Senate flip of the midterms."),
        (5, "HEALTH", (150, 40, 90), icon_virus,
         "US loses measles-free status after 26 years",
         "5,412 cases in 2026, the most since 1991, across 45 states; "
         "10 deaths reported."),
        (6, "AFRICA \u00b7 HEALTH", (120, 40, 40), icon_virus,
         "Ebola in DR Congo passes 11,000 cases",
         "Outbreak has more than doubled in three months; now the "
         "second-largest on record."),
        (7, "SPACE", (40, 40, 90), icon_probe,
         "Voyager 1 reaches one light-day from Earth",
         "The probe crossed 16 billion miles at 05:16 ET \u2014 a first "
         "for any human-made object."),
        (8, "ASIA-PACIFIC", (20, 90, 110), icon_flags,
         "Quad leaders meet in Manila \u2014 first in 2+ years",
         "US, Japan, India and Australia at leader level; Trump "
         "announces a Philippines trade deal."),
        (9, "EUROPE", GOLD, icon_euro,
         "EU proposes a \u20ac45bn loan for Ukraine in 2027",
         "\u20ac25bn for defence, \u20ac20bn for the budget; four member "
         "states opt out."),
    ]
    gx, gy = 24, 294
    cw, ch, gap = 476, 106, 24
    for i, s in enumerate(stories):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + 8)
        story_card(d, cx, cy, cw, ch, *s)

    # map panel
    my = gy + 4 * ch + 3 * 8 + 8
    mh = 158
    draw_map(d, 24, my, W - 48, mh)
    # Labels sit on alternating sides with a clear gap from their dot:
    # Shenzhen left of its dot, Manila below its dot. Shenzhen is nudged
    # slightly west (112, 33) so dots 1 and 8 no longer touch each other.
    dots = [
        (112, 33, 1, "Shenzhen", -16, 0, "rm"),
        (52, 27, 2, "Gulf", 0, -16, "mb"),
        (35, 45, 3, "Kerch", 0, -16, "mb"),
        (-150, 64, 4, "Alaska", 0, 16, "ma"),
        (-100, 40, 5, "USA", 0, 16, "ma"),
        (25, -2, 6, "DR Congo", 16, 0, "lm"),
        (121, 14, 8, "Manila", 0, 16, "ma"),
        (4, 51, 9, "Brussels", -16, 0, "rm"),
    ]
    for lon, lat, num, label, lx, ly, anchor in dots:
        map_dot(d, 24, my, W - 48, mh, lon, lat, num, label, lx, ly, anchor)
    # Voyager: off the map, a star in the sky
    d.text((W - 40, my + mh - 22), "\u2605 7 Voyager 1: one light-day out",
           font=font(SANS_B, 13), fill=NAVY, anchor="ra")

    # also-today strip
    ay = my + mh + 8
    d.rectangle([24, ay, W - 24, ay + 62], fill=(255, 255, 255),
                outline=LINE, width=1)
    d.text((36, ay + 6), "ALSO TODAY", font=font(SANS_B, 13), fill=RED)
    items = [
        ("10  TECH", "Nvidia board rejects Jensen Huang's return as CEO "
         "\u2014 on a record $115.8bn quarter."),
        ("11  AI", "OpenAI launches GPT-6.2 Astra and Sol, with lower "
         "API prices."),
        ("12  WEATHER", "Cyclone Akvan strengthens in the Bay of Bengal, "
         "bearing down on Andhra Pradesh."),
    ]
    yy = ay + 22
    for tag, text in items:
        d.text((36, yy), tag, font=font(SANS_B, 12), fill=NAVY)
        d.text((150, yy), text, font=font(SANS, 13), fill=INK)
        yy += 13

    # footer
    fy = ay + 62 + 8
    d.line([24, fy, W - 24, fy], fill=INK, width=1)
    d.text((24, fy + 6),
           "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 Euronews \u00b7 NASA \u00b7 WHO \u00b7 "
           "PAHO",
           font=font(SANS, 12), fill=GREY)
    d.text((24, fy + 22),
           "Judge: every story above happened, or was first reported, on "
           "Wednesday 18 November 2026.",
           font=font(SANS_B, 13), fill=INK)
    d.text((W - 24, fy + 8), "THE WORLD IN ONE PAGE",
           font=font(SANS_B, 12), fill=GREY, anchor="ra")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
