#!/usr/bin/env python3
"""Generate the phone version of the Orchid MoveMex signatures (Outlook for iPhone/Android).

Outlook on the phone breaks the desktop signature (a dozen linked images in nested tables), so the
phone version keeps the same look with ONE header image per person (logo, name, title, company,
badges) and puts every link in plain text underneath. Same two variants as the desktop signature:
with and without the privacy notice.

Usage: python3 build_mobile.py --base-url https://intuicioerp.github.io/client-signature-icons/orchid/images/
Reads config/signatures.json. Needs Pillow and the Arial fonts (Windows).
Output: images/cabecera-<id>.png, signatures/movil/<id>.html, signatures/movil/<id>-sin-aviso.html
and signatures/movil/index.html. Never hand-edit them.
"""
import argparse
import json
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = Path("C:/Windows/Fonts")
S = 2                      # images are drawn at 2x for sharp phones
W = 340                    # display width in px, fits every phone screen
TEXT, MUTED, LINE, NOTICE = "#1F1F2E", "#6A6A78", "#E6E2EE", "#5E5E6B"
FONT = "font-family:Arial,Helvetica,sans-serif;"

PAGE = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{title}</title>\n</head>\n'
        '<body style="margin:0;padding:12px;background-color:#FFFFFF;">\n{body}\n</body>\n</html>\n')


def e(value):
    return escape(value, quote=True)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size * S)


def fit(draw, text, name, size, max_w):
    while size > 9 and draw.textlength(text, font=font(name, size)) > max_w:
        size -= 1
    return font(name, size)


def load(file, height):
    im = Image.open(ROOT / "images" / file).convert("RGBA")
    return im.resize((round(im.width * height * S / im.height), height * S), Image.LANCZOS)


def header(company, person, out):
    """Logo | accent bar | name, title, company; divider; badges centred underneath."""
    w = W * S
    accent = company["accent"]
    logo = load(company["logo"]["file"], 34)                      # 130 px wide
    bar_x = logo.width + 10 * S
    x = bar_x + 3 * S + 12 * S
    col_w = w - x
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = [
        (person["name"], fit(probe, person["name"], "arialbd.ttf", 18, col_w), TEXT, 4),
        (person["title"], fit(probe, person["title"], "arialbd.ttf", 13, col_w), accent, 3),
        (company["name"], fit(probe, company["name"], "arial.ttf", 12, col_w), MUTED, 0),
    ]
    heights = [probe.textbbox((0, 0), t, font=f)[3] for t, f, _, _ in lines]
    block_h = sum(heights) + sum(g for *_, g in lines) * S
    top_h = max(logo.height, block_h) + 8 * S

    badge_h = {"badge-iamx.png": 30, "badge-movers.png": 21, "badge-iam.png": 34}
    badges = [load(b["file"], badge_h.get(b["file"], 28)) for b in company["badges"]]
    row_h = max(b.height for b in badges)
    pad = 12 * S
    h = top_h + pad + 1 * S + pad + row_h + 4 * S

    canvas = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(logo, (0, (top_h - logo.height) // 2), logo)
    draw.rectangle([bar_x, 4 * S, bar_x + 3 * S - 1, top_h - 4 * S], fill=accent)
    y = (top_h - block_h) // 2
    for (text, f, color, gap), th in zip(lines, heights):
        draw.text((x, y), text, font=f, fill=color)
        y += th + gap * S

    y = top_h + pad
    draw.rectangle([0, y, w, y + 1 * S - 1], fill=LINE)
    y += 1 * S + pad
    gap = 18 * S
    bx = (w - sum(b.width for b in badges) - gap * (len(badges) - 1)) // 2
    for b in badges:
        canvas.paste(b, (bx, y + (row_h - b.height) // 2), b)
        bx += b.width + gap
    canvas.save(out, optimize=True)
    return h // S


def body(company, person, img_url, img_h, with_notice):
    accent = company["accent"]
    a = f"color:{accent};text-decoration:none;"
    label = f'style="padding:0 10px 4px 0;{FONT}font-size:13px;line-height:19px;font-weight:bold;color:{TEXT};white-space:nowrap;"'
    value = f'style="padding:0 0 4px 0;{FONT}font-size:13px;line-height:19px;color:{TEXT};"'

    rows = []
    for key in ("mobile", "phone"):
        if person.get(key):
            p = person[key]
            rows.append((p["label"], f'<a href="{e(p["url"])}" style="{a}">{e(p["display"])}</a>'))
    rows.append(("Email", f'<a href="mailto:{e(person["email"])}" style="{a}">{e(person["email"])}</a>'))
    rows.append(("Web", f'<a href="{e(company["website"])}" style="{a}">{e(company["website_label"])}</a>'))
    rows.append(("Dirección", f'<a href="{e(company["address_url"])}" style="{a}">{"<br>".join(e(l) for l in company["address_lines"])}</a>'))
    social = " &nbsp;·&nbsp; ".join(f'<a href="{e(s["url"])}" style="{a}">{e(s["alt"])}</a>' for s in company["social"])
    rows.append(("Redes", social))
    iam = next((b["url"] for b in company["badges"] if b.get("url")), None)
    if iam:
        rows.append(("IAM", f'<a href="{e(iam)}" style="{a}">Ver nuestro registro</a>'))
    data = "\n".join(f'      <tr><td valign="top" {label}>{k}</td><td valign="top" {value}>{v}</td></tr>' for k, v in rows)

    small = f"{FONT}font-size:10px;line-height:14px;color:{NOTICE};"
    notice = ""
    if with_notice:
        n = company["privacy_notice"]
        link = f"color:{accent};text-decoration:underline;"
        notice = (f'    <p style="margin:0 0 6px 0;font-weight:bold;color:#3E3E4C;">{e(n["title"])}</p>\n'
                  f'    <p style="margin:0 0 6px 0;">{e(n["es"])} <a href="{e(n["es_link"]["url"])}" style="{link}">{e(n["es_link"]["label"])}</a></p>\n'
                  f'    <p style="margin:0 0 6px 0;">{e(n["en"])} <a href="{e(n["en_link"]["url"])}" style="{link}">{e(n["en_link"]["label"])}</a></p>\n')
    pb = company["powered_by"]
    alt = f'{person["name"]} · {person["title"]} · {company["name"]}'
    return f"""<table cellpadding="0" cellspacing="0" border="0" width="{W}" style="width:{W}px;max-width:100%;border-collapse:collapse;background-color:#ffffff;">
  <tr><td style="padding:0 0 10px 0;"><img src="{e(img_url)}" width="{W}" height="{img_h}" alt="{e(alt)}" style="display:block;border:0;width:{W}px;max-width:100%;height:auto;"></td></tr>
  <tr><td style="padding:10px 0 8px 0;border-top:1px solid {LINE};">
    <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
{data}
    </table>
  </td></tr>
  <tr><td style="padding:8px 0 0 0;border-top:1px solid {LINE};{small}">
{notice}    <p style="margin:0;color:{MUTED};">Powered by <a href="{e(pb["url"])}" style="color:{MUTED};text-decoration:none;font-weight:bold;">intuiCIO</a></p>
  </td></tr>
</table>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", required=True, help="Public URL of the images/ folder")
    base = ap.parse_args().base_url.rstrip("/") + "/"
    cfg = json.loads((ROOT / "config" / "signatures.json").read_text(encoding="utf-8"))
    company = cfg["company"]
    out = ROOT / "signatures" / "movil"
    out.mkdir(parents=True, exist_ok=True)
    gallery = []
    for person in cfg["people"]:
        png = f'cabecera-{person["id"]}.png'
        img_h = header(company, person, ROOT / "images" / png)
        for with_notice, suffix, label in ((True, "", "con aviso de privacidad"), (False, "-sin-aviso", "sin aviso de privacidad")):
            sig = body(company, person, base + png, img_h, with_notice)
            name = f'{person["id"]}{suffix}.html'
            (out / name).write_text(PAGE.format(title=f'Firma celular {person["name"]} - {label}', body=sig), encoding="utf-8")
            gallery.append(f'<h2 style="{FONT}font-size:15px;color:{MUTED};margin:28px 0 8px 0;">{e(person["name"])} &mdash; {label} &middot; '
                           f'<a href="{name}">solo la firma</a> &middot; <a href="../../images/{png}">imagen</a></h2>{sig}')
            print(f"wrote signatures/movil/{name}")
        print(f"wrote images/{png}")
    (out / "index.html").write_text(PAGE.format(title="Firmas celular Orchid MoveMex", body="\n".join(gallery)), encoding="utf-8")


if __name__ == "__main__":
    main()
