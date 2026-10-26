#!/usr/bin/env python3
"""Generate the Outlook mobile version of the A2Z signatures.

Outlook for iPhone/Android breaks the desktop signature (a dozen linked images in nested tables),
so the mobile version keeps the same look with ONE header image per person (photo, name, title,
tagline, logo, membership badges) and puts every link in plain text underneath.

Usage: python3 build_mobile.py --base-url https://intuicioerp.github.io/client-signature-icons/a2z/
Reads config/signatures.json. Needs Pillow and the Arial fonts (Windows).
Output: images/header-<slug>.png, dist/mobile/<slug>.html and dist/mobile/index.html. Never hand-edit them.
"""
import argparse
import html
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = Path("C:/Windows/Fonts")
S = 2                      # images are drawn at 2x for sharp phones
W = 340                    # display width in px, fits every phone screen

PAGE = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{title}</title>\n</head>\n'
        '<body style="margin:0;padding:12px;background-color:#FFFFFF;">\n{body}\n</body>\n</html>\n')


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size * S)


def fit(draw, text, name, size, max_w):
    while size > 9 and draw.textlength(text, font=font(name, size)) > max_w:
        size -= 1
    return font(name, size)


def load(file, width):
    im = Image.open(ROOT / "images" / file).convert("RGBA")
    return im.resize((width * S, round(im.height * width * S / im.width)), Image.LANCZOS)


def badge_rows(badges):
    """Split the badges into two centred rows (one row is too small to read on a phone)."""
    half = (len(badges) + 1) // 2
    return [badges[:half], badges[half:]]


def header(cfg, p, out):
    b = cfg["brand"]
    w = W * S
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    logo = load(b["logo"]["file"], 64)
    photo = load(p["photo"]["file"], 76) if p.get("photo") else None
    logo_left = p.get("logo_position") == "left"
    lead = photo or (logo if logo_left else None)       # image left of the accent bar

    x = 0
    if lead:
        x = lead.width + 8 * S + 3 * S + 10 * S         # image, gap, accent bar, gap
    text_w = w - x - (0 if logo_left else logo.width + 8 * S)
    name_f = fit(probe, p["name"], "arialbi.ttf", 20, text_w)
    title_f = fit(probe, p["title"], "arial.ttf", 13, text_w)
    company_f = fit(probe, b["company"], "arialbd.ttf", 13, text_w)
    tag_f = fit(probe, b["tagline"], "arialbi.ttf", 12, w)
    tag_h = probe.textbbox((0, 0), b["tagline"], font=tag_f)[3]
    lines = [(p["name"], name_f, b["text_dark"]), (p["title"], title_f, b["text_body"]),
             (b["company"], company_f, b["accent"])]
    heights = [probe.textbbox((0, 0), t, font=f)[3] for t, f, _ in lines]
    gaps = [5 * S, 2 * S]
    block_h = sum(heights) + sum(gaps)
    top_h = max(logo.height, photo.height if photo else 0, block_h) + 4 * S

    rows = badge_rows(cfg["logo_rows"][p.get("logo_row", "default")])
    row_imgs = [[load(i["file"], i["width"]) for i in row] for row in rows]
    row_h = [max(im.height for im in r) for r in row_imgs]
    pad = 12 * S
    h = top_h + 8 * S + tag_h + pad + 1 * S + pad + row_h[0] + 10 * S + row_h[1]

    canvas = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(canvas)
    if lead:
        canvas.paste(lead, (0, (top_h - lead.height) // 2), lead)
        bar_x = lead.width + 8 * S
        draw.rectangle([bar_x, 4 * S, bar_x + 3 * S - 1, top_h - 4 * S], fill=b["accent"])
    y = (top_h - block_h) // 2
    for (text, f, color), th, gap in zip(lines, heights, gaps + [0]):
        draw.text((x, y), text, font=f, fill=color)
        y += th + gap
    if not logo_left:
        canvas.paste(logo, (w - logo.width, (top_h - logo.height) // 2), logo)

    tw = draw.textlength(b["tagline"], font=tag_f)
    draw.text(((w - tw) / 2, top_h + 8 * S), b["tagline"], font=tag_f, fill=b["accent"])
    y = top_h + 8 * S + tag_h + pad
    draw.rectangle([0, y, w, y + 1 * S - 1], fill=b["divider"])
    y += 1 * S + pad
    for imgs, rh in zip(row_imgs, row_h):
        gap = 12 * S
        total = sum(im.width for im in imgs) + gap * (len(imgs) - 1)
        bx = (w - total) // 2
        for im in imgs:
            canvas.paste(im, (bx, y + (rh - im.height) // 2), im)
            bx += im.width + gap
        y += rh + 10 * S
    canvas.save(out, optimize=True)
    return h // S


def body(cfg, p, img_url, img_h):
    b, legal = cfg["brand"], cfg["legal"]
    f = "font-family:Arial,Helvetica,sans-serif;"
    a = f"color:{b['accent']};text-decoration:none;"
    label = f'style="padding:0 10px 4px 0;{f}font-size:13px;line-height:19px;font-weight:bold;color:{b["text_dark"]};"'
    value = f'style="padding:0 0 4px 0;{f}font-size:13px;line-height:19px;color:{b["text_body"]};"'
    rows = []
    if p.get("phone_display"):
        rows.append(("WhatsApp/Cell", f'<a href="tel:{p["phone_tel"]}" style="{a}">{html.escape(p["phone_display"])}</a>'))
    rows.append(("Email", f'<a href="mailto:{p["email"]}" style="{a}">{p["email"]}</a>'))
    rows.append(("Web", f'<a href="{b["website_url"]}" style="{a}">{b["website_label"]}</a>'))
    social = []
    if p.get("linkedin_url"):
        social.append(f'<a href="{p["linkedin_url"]}" style="{a}">LinkedIn</a>')
    social.append(f'<a href="{b["instagram_url"]}" style="{a}">Instagram</a>')
    rows.append(("Follow", " &nbsp;·&nbsp; ".join(social)))
    data = "\n".join(f'      <tr><td valign="top" {label}>{k}</td><td valign="top" {value}>{v}</td></tr>' for k, v in rows)
    links = " &nbsp;|&nbsp; ".join(f'<a href="{html.escape(l["url"])}" style="color:{b["accent"]};font-weight:bold;">{l["label"]}</a>'
                                   for l in legal["links"])
    small = f"{f}font-size:10px;line-height:14px;color:{b['text_muted']};"
    return f"""<table cellpadding="0" cellspacing="0" border="0" width="{W}" style="width:{W}px;max-width:100%;border-collapse:collapse;background-color:#ffffff;">
  <tr><td style="padding:0 0 10px 0;"><img src="{img_url}" width="{W}" height="{img_h}" alt="{html.escape(p['name'])} · {html.escape(p['title'])} · {b['company']}" style="display:block;border:0;width:{W}px;max-width:100%;height:auto;"></td></tr>
  <tr><td style="padding:10px 0 8px 0;border-top:1px solid {b['divider']};">
    <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
{data}
    </table>
  </td></tr>
  <tr><td style="padding:8px 0 0 0;border-top:1px solid {b['divider']};{small}">
    <p style="margin:0 0 6px 0;"><b style="color:{b['text_body']};">Confidentiality Notice:</b> {legal['confidentiality']}</p>
    <p style="margin:0 0 6px 0;"><b style="color:{b['accent']};">{legal['market_title']}</b><br>{legal['market_text']}</p>
    <p style="margin:0 0 6px 0;font-size:12px;line-height:16px;">{links}</p>
    <p style="margin:0;">Powered by <a href="{b['powered_by']['url']}" style="color:{b['text_muted']};text-decoration:none;font-weight:bold;">intuiCIO</a></p>
  </td></tr>
</table>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    base = ap.parse_args().base_url.rstrip("/") + "/"
    cfg = json.loads((ROOT / "config" / "signatures.json").read_text(encoding="utf-8"))
    out = ROOT / "dist" / "mobile"
    out.mkdir(parents=True, exist_ok=True)
    gallery = []
    for p in cfg["people"]:
        png = f"header-{p['slug']}.png"
        img_h = header(cfg, p, ROOT / "images" / png)
        sig = body(cfg, p, f"{base}images/{png}", img_h)
        (out / f"{p['slug']}.html").write_text(PAGE.format(title=f"Mobile signature - {p['name']}", body=sig), encoding="utf-8")
        gallery.append(f'<h2 style="font-family:Arial;font-size:16px;margin:28px 0 8px 0;">{html.escape(p["name"])} &mdash; '
                       f'<a href="{p["slug"]}.html">signature only</a> &middot; <a href="../../images/{png}">image</a></h2>{sig}')
        print("wrote dist/mobile/%s.html and images/%s" % (p["slug"], png))
    (out / "index.html").write_text(PAGE.format(title="A2Z mobile signatures", body="".join(gallery)), encoding="utf-8")


if __name__ == "__main__":
    main()
