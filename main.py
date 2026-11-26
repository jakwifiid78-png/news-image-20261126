#!/usr/bin/env python3
"""news-image-20261126 — one image that sums up the world news of
Thursday 26 November 2026, drawn as a newspaper front page.

The program draws the front page with Pillow (stdlib + PIL) and writes it
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png outside the
grader). The drawing is fully deterministic: fixed text, fixed layout,
no clocks and no randomness, so two runs write the same bytes. If PIL is
unavailable at run time, the bundled entry.png beside this file — drawn
by this very program — is copied to the output instead.

News of 26 November 2026 summed up here (as reported that day):
- Washington: President Trump announces new tariffs on 14 trading
  partners after an excess-capacity probe; China, the EU and India among
  those targeted; Jakarta coordinates a reply to a proposed 18% rate.
- Cairo: a fuel tanker overturns and burns on the Ring Road in Giza,
  killing at least 31 people and injuring about 21.
- Jakarta: President Prabowo watches police destroy 601.7 tons of seized
  narcotics worth Rp61.68 trillion.
- Bogor: 13 miners die in the illegal Pongkor gold mine.
- Markets: the rupiah slides past Rp18,380 per US dollar.
- In brief: Russian missiles wound seven in Kyiv; Israeli strikes kill
  nine in Gaza; EU leaders haggle over a two-trillion-euro budget; the
  FCC clears SpaceX's million-satellite plan; North Korea signals
  further nuclear expansion.
"""

import os
import shutil
import sys

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (22, 19, 14)
MUTED = (90, 83, 72)
ACCENT = (140, 43, 29)
RULE = (22, 19, 14)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

DATE_LINE = "26 NOVEMBER 2026"
DAY_LINE = "THURSDAY"


def load_fonts(ImageFont):
    def f(path, size):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()

    return {
        "dateline": f(SERIF_BOLD, 30),
        "dateline_side": f(SANS_BOLD, 24),
        "meta": f(SANS, 16),
        "kicker": f(SANS_BOLD, 20),
        "headline": f(SERIF_BOLD, 58),
        "deck": f(SERIF, 24),
        "byline": f(SANS, 15),
        "body": f(SERIF, 20),
        "body_small": f(SERIF, 16),
        "rail_head": f(SERIF_BOLD, 23),
        "caption": f(SANS, 14),
        "section": f(SANS_BOLD, 21),
        "id_head": f(SERIF_BOLD, 20),
        "id_body": f(SERIF, 16),
        "ticker": f(SANS_BOLD, 13),
    }


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, font, width, lh, fill=INK, max_lines=None):
    lines = wrap(draw, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def centered(draw, cx, y, text, font, fill=INK):
    w_ = draw.textlength(text, font=font)
    draw.text((cx - w_ / 2, y), text, font=font, fill=fill)


def fit_font(ImageFont, path, text, start, width, draw):
    size = start
    while size > 10:
        fnt = ImageFont.truetype(path, size)
        if draw.textlength(text, font=fnt) <= width:
            return fnt
        size -= 2
    return ImageFont.truetype(path, size)


def draw_ship(draw, box):
    """A container ship under a harbour crane, in flat shapes."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(220, 231, 236))
    # sun and clouds
    draw.ellipse([x0 + 24, y0 + 12, x0 + 56, y0 + 44], fill=(233, 197, 92))
    for cx, cy, cw in ((140, 18, 84), (520, 12, 100), (320, 24, 64)):
        draw.ellipse([x0 + cx, y0 + cy, x0 + cx + cw, y0 + cy + 18], fill=(244, 247, 248))
    # sea
    sea_y = y1 - 30
    draw.rectangle([x0, sea_y, x1, y1], fill=(47, 85, 104))
    for i in range(5):
        wx = x0 + 18 + i * 62
        draw.arc([wx, sea_y + 6, wx + 32, sea_y + 20], 180, 360, fill=(214, 230, 236), width=2)
    # hull
    hull_top = sea_y - 20
    draw.polygon([(x0 + 28, hull_top), (x1 - 84, hull_top),
                  (x1 - 112, sea_y + 6), (x0 + 64, sea_y + 6)], fill=(38, 48, 58))
    draw.rectangle([x0 + 28, hull_top, x1 - 84, hull_top + 4], fill=(140, 43, 29))
    # containers: two stacked rows on deck
    cols = [(164, 74, 63), (63, 97, 140), (193, 154, 63), (93, 122, 82), (140, 90, 70)]
    cw_, ch_, gap = 58, 15, 3
    base = hull_top - 2
    for row in range(2):
        for col in range(5):
            cx = x0 + 44 + col * (cw_ + gap)
            cy = base - (row + 1) * (ch_ + gap)
            draw.rectangle([cx, cy, cx + cw_, cy + ch_], fill=cols[(row + col) % 5],
                           outline=(30, 30, 30), width=1)
    # superstructure
    sx = x1 - 142
    draw.rectangle([sx, base - 46, sx + 40, base], fill=(240, 238, 230), outline=(30, 30, 30))
    for r in range(2):
        for c in range(3):
            draw.rectangle([sx + 6 + c * 11, base - 38 + r * 14,
                            sx + 12 + c * 11, base - 31 + r * 14], fill=(70, 90, 105))
    # crane on the right
    gx = x1 - 42
    draw.line([gx, y0 + 6, gx, sea_y], fill=(38, 48, 58), width=6)
    draw.line([x0 + 190, y0 + 6, gx, y0 + 6], fill=(38, 48, 58), width=6)
    draw.line([x0 + 300, y0 + 6, x0 + 300, y0 + 34], fill=(38, 48, 58), width=3)
    draw.rectangle([x0 + 274, y0 + 34, x0 + 326, y0 + 50], fill=(193, 154, 63),
                   outline=(30, 30, 30))
    draw.rectangle(box, outline=INK, width=2)


def draw_page():
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    F = load_fonts(ImageFont)
    M = 36                      # margin
    R = W - M                   # right edge of content (988)
    CW = R - M                  # content width (952)

    # --- meta strip ---------------------------------------------------
    d.text((M, 20), "Vol. I — No. 26", font=F["meta"], fill=MUTED)
    centered(d, W // 2, 20, "JAKARTA · LONDON · NEW YORK · CAIRO", F["meta"], MUTED)
    t = "EST. 2026"
    d.text((R - d.textlength(t, font=F["meta"]), 20), t, font=F["meta"], fill=MUTED)
    d.line([M, 46, R, 46], fill=RULE, width=2)

    # --- masthead ------------------------------------------------------
    mast = fit_font(ImageFont, SERIF_BOLD, "THE WORLD TODAY", 96, CW, d)
    centered(d, W // 2, 54, "THE WORLD TODAY", mast)
    d.line([M, 150, R, 150], fill=RULE, width=5)
    d.line([M, 158, R, 158], fill=RULE, width=1)

    # --- dateline band -------------------------------------------------
    d.text((M, 168), DAY_LINE, font=F["dateline_side"], fill=INK)
    centered(d, W // 2, 164, DATE_LINE, F["dateline"], INK)
    t = "LATE FINAL"
    d.text((R - d.textlength(t, font=F["dateline_side"]), 168), t,
           font=F["dateline_side"], fill=INK)
    d.line([M, 202, R, 202], fill=RULE, width=1)

    # --- main headline -------------------------------------------------
    d.text((M, 214), "GLOBAL ECONOMY — WASHINGTON", font=F["kicker"], fill=ACCENT)
    y = text_block(d, M, 242,
                   "TRUMP UNLEASHES NEW TARIFFS ON 14 TRADING PARTNERS",
                   F["headline"], CW, 64)
    y = text_block(d, M, y + 6,
                   "Washington strikes after an excess-capacity probe — China, "
                   "the EU and India in its sights, and Jakarta weighing a reply "
                   "to a proposed 18% rate.",
                   F["deck"], CW, 29)
    d.text((M, y + 8), "By THE WORLD DESK · Thursday, 26 November 2026 · "
                       "Washington / Jakarta / Cairo",
           font=F["byline"], fill=MUTED)
    d.line([M, y + 34, R, y + 34], fill=RULE, width=2)
    mid_top = y + 48

    # --- middle zone: main story (left) + rail (right) ------------------
    rail_x = 636
    body = ("President Donald Trump announced a new round of tariffs on 14 major "
            "trading partners, accusing them of flooding world markets with excess "
            "factory output after a US probe into industrial overcapacity. China, "
            "the European Union and India are among those in Washington's sights. "
            "In Jakarta, officials stepped up coordination with Washington over a "
            "proposed 18% import tariff. Markets shrugged the plan off: shares "
            "rebounded across Europe and Asia.")
    text_block(d, M, mid_top, body, F["body"], rail_x - M - 24, 26)

    draw_ship(d, (rail_x, mid_top, R, mid_top + 116))
    d.text((rail_x, mid_top + 124), "Cargo for US ports faces new duties.",
           font=F["caption"], fill=MUTED)
    cy = mid_top + 148
    d.line([rail_x, cy, R, cy], fill=RULE, width=1)
    d.text((rail_x, cy + 8), "EGYPT — CAIRO", font=F["kicker"], fill=ACCENT)
    cy = text_block(d, rail_x, cy + 38,
                    "Tanker fire kills 31 on Cairo ring road",
                    F["rail_head"], R - rail_x, 26)
    text_block(d, rail_x, cy + 4,
               "Fuel tanker overturns and burns on the Ring Road; "
               "21 injured.",
               F["body_small"], R - rail_x, 20)

    # --- Indonesia band --------------------------------------------------
    id_top = 832
    d.line([M, id_top, R, id_top], fill=RULE, width=2)
    d.text((M, id_top + 10), "INDONESIA", font=F["section"], fill=ACCENT)
    t = "THURSDAY, 26 NOVEMBER 2026"
    d.text((R - d.textlength(t, font=F["section"]), id_top + 10), t,
           font=F["section"], fill=INK)
    col_w = (CW - 48) // 3
    cols = [
        ("Prabowo watches 601.7 tons of drugs burn",
         "Police burn seized narcotics worth Rp61.68 trillion."),
        ("13 miners die at Pongkor gold mine",
         "Dozens trapped in the illegal Bogor dig; backers hunted."),
        ("Rupiah slides past Rp18,380 a dollar",
         "A record low on domestic risks; stocks close at 5,242."),
    ]
    for i, (head, txt) in enumerate(cols):
        cx = M + i * (col_w + 24)
        hy = text_block(d, cx, id_top + 42, head, F["id_head"], col_w, 23)
        text_block(d, cx, hy + 4, txt, F["id_body"], col_w, 19)
        if i:
            d.line([cx - 12, id_top + 44, cx - 12, id_top + 124], fill=MUTED, width=1)

    # --- ticker band -------------------------------------------------------
    band_y = 968
    d.rectangle([M, band_y, R, band_y + 48], fill=INK)
    centered(d, W // 2, band_y + 7,
             "KYIV: RUSSIAN MISSILES WOUND 7 · GAZA: ISRAELI STRIKES KILL 9 · "
             "BRUSSELS: EU HAGGLES OVER €2 TRILLION BUDGET",
             F["ticker"], PAPER)
    centered(d, W // 2, band_y + 28,
             "SPACE: FCC CLEARS SPACEX MILLION-SATELLITE PLAN · PYONGYANG: "
             "NORTH KOREA SIGNALS NUCLEAR EXPANSION",
             F["ticker"], PAPER)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    try:
        img = draw_page()
    except ImportError:
        # No PIL in this environment: ship the image this program drew.
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
        shutil.copyfile(src, out_path)
        return 0
    img.save(out_path, format="PNG", optimize=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
