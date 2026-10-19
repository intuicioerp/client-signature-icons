#!/usr/bin/env python3
"""Generate the Outlook mobile version of the Moving Life signatures.

Outlook for iPhone/Android breaks the desktop signature (about ten linked images in nested tables),
so the mobile version keeps the same look with ONE header image per person (logo, photo, name,
title, seals) and puts every link in plain text underneath.

Usage: python3 build_mobile.py --base-url https://intuicioerp.github.io/client-signature-icons/moving-life/
Reads src/*.htm (name, title, email, mobile). Needs Pillow and the Segoe UI fonts (Windows).
Output: images/cabecera-<slug>.png, dist/movil/<slug>.html and dist/movil/index.html. Never hand-edit them.
"""
import argparse
import html
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = Path("C:/Windows/Fonts")
S = 2                      # images are drawn at 2x for sharp phones
W = 340                    # display width in px, fits every phone screen
NAME, TITLE, LINE, BLUE, TEXT, MUTED = "#4A5560", "#1B75BC", "#DDE6EE", "#1B75BC", "#24282E", "#6B6459"
FB, IG, X = "https://www.facebook.com/MovingLifeVe", "https://www.instagram.com/movinglifeve/", "https://x.com/MovingLifeVe"

PAGE = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{title}</title>\n</head>\n'
        '<body style="margin:0;padding:12px;background-color:#FFFFFF;">\n{body}\n</body>\n</html>\n')


def person(src):
    text = src.read_text(encoding="utf-8")
    name = re.search(r'font-size:18px;[^>]*>([^<]+)</div>', text).group(1)
    title = re.search(r'font-size:13px;[^>]*>([^<]+)</div>', text).group(1)
    email = re.search(r'mailto:([^"]+)"', text).group(1)
    mobile = re.search(r'>Mobile</td>\s*<td[^>]*>([^<]+)</td>', text).group(1).strip()
    return {"slug": src.stem, "name": html.unescape(name), "title": html.unescape(title), "email": email, "mobile": mobile}


def fit(draw, text, font_file, size, max_w):
    while True:
        font = ImageFont.truetype(str(FONTS / font_file), size * S)
        if draw.textlength(text, font=font) <= max_w or size <= 10:
            return font
        size -= 1


def header(p, out):
    img_dir = ROOT / "images"
    logo = Image.open(img_dir / "logo.png")
    photo = Image.open(img_dir / f"foto-{p['slug']}.png")
    seals = Image.open(img_dir / "sellos.png")
    w = W * S
    logo_w = 170 * S
    logo = logo.resize((logo_w, round(logo.height * logo_w / logo.width)), Image.LANCZOS)
    photo = photo.resize((76 * S, 76 * S), Image.LANCZOS)
    seals_w = 320 * S
    seals = seals.resize((seals_w, round(seals.height * seals_w / seals.width)), Image.LANCZOS)

    split = logo_w + 8 * S
    col_x, col_w = split + 8 * S, w - split - 8 * S
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    name_f = fit(probe, p["name"], "segoeuib.ttf", 16, col_w)
    title_f = fit(probe, p["title"], "segoeuib.ttf", 12, col_w)
    # text boxes are taller than the font size (descenders), so measure with textbbox
    name_h = probe.textbbox((0, 0), p["name"], font=name_f)[3]
    title_h = probe.textbbox((0, 0), p["title"], font=title_f)[3]
    block_h = photo.height + 6 * S + name_h + 2 * S + title_h

    top_h = max(logo.height, block_h + 4 * S)
    pad = 12 * S
    h = top_h + pad + 1 * S + pad + seals.height
    canvas = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(logo, (0, (top_h - logo.height) // 2), logo)
    draw.rectangle([split, 6 * S, split, top_h - 6 * S], fill=LINE)
    y = (top_h - block_h) // 2
    canvas.paste(photo, (col_x + (col_w - photo.width) // 2, y), photo)
    y += photo.height + 6 * S
    for text, font, color, th in ((p["name"], name_f, NAME, name_h), (p["title"], title_f, TITLE, title_h)):
        tw = draw.textlength(text, font=font)
        draw.text((col_x + (col_w - tw) / 2, y), text, font=font, fill=color)
        y += th + 2 * S

    y = top_h + pad
    draw.rectangle([0, y, w, y + 1 * S - 1], fill=LINE)
    canvas.paste(seals, ((w - seals.width) // 2, y + 1 * S + pad), seals)
    canvas.save(out, optimize=True)
    return h // S


def body(p, img_url, img_h):
    tel = "+" + re.sub(r"\D", "", p["mobile"])
    f = "font-family:'Segoe UI',Arial,Helvetica,sans-serif;"
    a = f"color:{BLUE};text-decoration:none;"
    label = f'style="padding:0 10px 4px 0;{f}font-size:14px;line-height:20px;font-weight:bold;color:{NAME};"'
    value = f'style="padding:0 0 4px 0;{f}font-size:14px;line-height:20px;color:{TEXT};"'
    return f"""<table cellpadding="0" cellspacing="0" border="0" width="{W}" style="width:{W}px;max-width:100%;border-collapse:collapse;background-color:#ffffff;">
  <tr><td style="padding:0 0 10px 0;"><img src="{img_url}" width="{W}" height="{img_h}" alt="{html.escape(p['name'])} · {html.escape(p['title'])} · Moving Life" style="display:block;border:0;width:{W}px;max-width:100%;height:auto;"></td></tr>
  <tr><td style="padding:10px 0 6px 0;border-top:1px solid {LINE};">
    <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
      <tr><td valign="top" {label}>Email</td><td valign="top" {value}><a href="mailto:{p['email']}" style="{a}">{p['email']}</a></td></tr>
      <tr><td valign="top" {label}>Mobile</td><td valign="top" {value}><a href="tel:{tel}" style="{a}">{html.escape(p['mobile'])}</a></td></tr>
      <tr><td valign="top" {label}>Web</td><td valign="top" {value}><a href="https://www.movinglife.com.ve" style="{a}">www.movinglife.com.ve</a></td></tr>
    </table>
  </td></tr>
  <tr><td style="padding:2px 0 10px 0;{f}font-size:13px;line-height:18px;color:{TEXT};">Caracas, Venezuela &nbsp;·&nbsp; <a href="{FB}" style="{a}">Facebook</a> &nbsp;·&nbsp; <a href="{IG}" style="{a}">Instagram</a> &nbsp;·&nbsp; <a href="{X}" style="{a}">X</a></td></tr>
  <tr><td style="padding:8px 0 0 0;border-top:1px solid #EFEBE5;{f}font-size:10px;line-height:14px;color:{MUTED};">
    <p style="margin:0 0 5px 0;"><b style="color:{NAME};">Aviso de contacto:</b> Nuestro canal de comunicación principal es el correo electrónico. De manera alternativa, habilitamos la recepción de mensajes exclusivamente vía WhatsApp a través del número provisto en esta firma.</p>
    <p style="margin:0 0 5px 0;"><b style="color:{NAME};">Contact Notice:</b> Please be advised that our primary communication channel is email. Alternatively, we accept messages exclusively via WhatsApp at the number provided in this signature.</p>
    <p style="margin:0;color:#8A8177;">Powered by <a href="https://intuicioerp.com" style="color:#8A8177;text-decoration:none;font-weight:bold;">intuiCIO</a></p>
  </td></tr>
</table>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    base = ap.parse_args().base_url.rstrip("/") + "/"
    out = ROOT / "dist" / "movil"
    out.mkdir(parents=True, exist_ok=True)
    gallery = []
    for src in sorted((ROOT / "src").glob("*.htm")):
        p = person(src)
        png = f"cabecera-{p['slug']}.png"
        img_h = header(p, ROOT / "images" / png)
        sig = body(p, f"{base}images/{png}", img_h)
        title = f"Firma móvil {p['name']} · Moving Life"
        (out / f"{p['slug']}.html").write_text(PAGE.format(title=title, body=sig), encoding="utf-8")
        gallery.append(f'<h2 style="font-family:Arial;font-size:16px;margin:28px 0 8px 0;">{html.escape(p["name"])} &mdash; '
                       f'<a href="{p["slug"]}.html">solo la firma</a> &middot; <a href="../../images/{png}">imagen</a></h2>{sig}')
        print("wrote dist/movil/%s.html and images/%s" % (p["slug"], png))
    (out / "index.html").write_text(PAGE.format(title="Firmas móvil Moving Life", body="".join(gallery)), encoding="utf-8")


if __name__ == "__main__":
    main()
