#!/usr/bin/env python3
"""Build Outlook-safe HTML email signatures for Orchid MoveMex.

Reads config/signatures.json and writes, for every person, two files:
  signatures/<id>.html            -> with the privacy notice
  signatures/<id>-sin-aviso.html  -> without the privacy notice
plus preview.html (all signatures on one page, images loaded relatively).

Usage:
  python3 build.py --base-url https://intuicioerp.github.io/client-signature-icons/orchid/images/
"""
import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_BASE_URL = "https://intuicioerp.github.io/client-signature-icons/orchid/images/"
FONT = "Arial, Helvetica, sans-serif"
TEXT = "#1F1F2E"
MUTED = "#6A6A78"
LINE = "#E6E2EE"
NOTICE = "#5E5E6B"


def e(value):
    return escape(value, quote=True)


def img(base, file, width, height, alt, extra=""):
    return (f'<img src="{e(base + file)}" width="{width}" height="{height}" alt="{e(alt)}" '
            f'style="display:block;border:0;outline:none;width:{width}px;height:{height}px;{extra}">')


def link(url, inner, style=""):
    return f'<a href="{e(url)}" target="_blank" style="text-decoration:none;{style}">{inner}</a>'


def contact_row(base, icon, inner_html, url, valign="middle"):
    return (
        '<tr>'
        f'<td width="24" valign="{valign}" style="padding:3px 0;width:24px">{img(base, icon, 16, 16, "")}</td>'
        f'<td valign="{valign}" style="padding:3px 0;font-family:{FONT};font-size:13px;line-height:18px;color:{TEXT}">'
        f'{link(url, inner_html, f"color:{TEXT}")}</td>'
        '</tr>'
    )


def build_signature(company, person, base, with_notice):
    accent = company["accent"]
    logo = company["logo"]

    social = list(company["social"])
    if person.get("whatsapp_url"):
        social.append({"icon": "icon-whatsapp.png", "alt": "WhatsApp", "url": person["whatsapp_url"]})
    social_cells = "".join(
        f'<td style="padding:0 4px">{link(s["url"], img(base, s["icon"], 32, 32, s["alt"]))}</td>' for s in social
    )

    rows = []
    if person.get("mobile"):
        m = person["mobile"]
        rows.append(contact_row(base, "icon-mobile.png",
                                f'<span style="color:{MUTED}">{e(m["label"])}</span> {e(m["display"])}', m["url"]))
    if person.get("phone"):
        p = person["phone"]
        rows.append(contact_row(base, "icon-phone.png",
                                f'<span style="color:{MUTED}">{e(p["label"])}</span> {e(p["display"])}', p["url"]))
    rows.append(contact_row(base, "icon-email.png", e(person["email"]), f'mailto:{person["email"]}'))
    rows.append(contact_row(base, "icon-web.png", f'<b>{e(company["website_label"])}</b>', company["website"]))
    rows.append(contact_row(base, "icon-location.png", "<br>".join(e(l) for l in company["address_lines"]),
                            company["address_url"], valign="top"))

    badges = []
    for b in company["badges"]:
        tag = img(base, b["file"], b["width"], b["height"], b["alt"])
        if b.get("url"):
            tag = link(b["url"], tag)
        badges.append(f'<td valign="middle" style="padding-right:22px">{tag}</td>')

    pb = company["powered_by"]
    powered = (
        f'<td valign="middle" style="border-left:1px solid {LINE};padding-left:18px" align="center">'
        f'<div style="font-family:{FONT};font-size:9px;line-height:12px;font-weight:bold;letter-spacing:1.5px;color:#5C5C5C;padding-bottom:4px">POWERED BY</div>'
        f'{link(pb["url"], img(base, pb["file"], pb["width"], pb["height"], pb["alt"]))}'
        '</td>'
    )

    notice_html = ""
    if with_notice:
        n = company["privacy_notice"]
        p_style = f"margin:0 0 8px 0;font-family:{FONT};font-size:10px;line-height:15px;color:{NOTICE}"
        a_style = f"color:{accent};text-decoration:underline"
        notice_html = (
            '<tr><td style="padding-top:16px">'
            f'<p style="margin:0 0 8px 0;font-family:{FONT};font-size:10px;line-height:14px;font-weight:bold;letter-spacing:1.2px;text-transform:uppercase;color:#3E3E4C">{e(n["title"])}</p>'
            f'<p style="{p_style}">{e(n["es"])} <a href="{e(n["es_link"]["url"])}" target="_blank" style="{a_style}">{e(n["es_link"]["label"])}</a></p>'
            f'<p style="{p_style}">{e(n["en"])} <a href="{e(n["en_link"]["url"])}" target="_blank" style="{a_style}">{e(n["en_link"]["label"])}</a></p>'
            '</td></tr>'
        )

    return (
        f'<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="600" '
        f'style="width:600px;border-collapse:collapse;font-family:{FONT};color:{TEXT};background:#FFFFFF">'
        # Header: logo + social | accent bar | details
        '<tr><td style="padding-bottom:20px">'
        '<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse"><tr>'
        '<td width="200" valign="middle" align="center" style="width:200px">'
        f'{link(company["website"], img(base, logo["file"], logo["width"], logo["height"], logo["alt"]))}'
        '<table cellpadding="0" cellspacing="0" border="0" role="presentation" align="center" style="margin-top:14px"><tr>'
        f'{social_cells}</tr></table>'
        '</td>'
        '<td width="24" style="width:24px;font-size:0;line-height:0">&nbsp;</td>'
        f'<td width="3" bgcolor="{accent}" style="width:3px;background:{accent};font-size:0;line-height:0">&nbsp;</td>'
        '<td width="24" style="width:24px;font-size:0;line-height:0">&nbsp;</td>'
        '<td valign="top">'
        f'<div style="font-family:{FONT};font-size:21px;line-height:26px;font-weight:bold;color:{TEXT}">{e(person["name"])}</div>'
        f'<div style="font-family:{FONT};font-size:14px;line-height:20px;font-weight:bold;color:{accent};padding-bottom:10px">'
        f'{e(person["title"])} &middot; {e(company["name"])}</div>'
        f'<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse">{"".join(rows)}</table>'
        '</td>'
        '</tr></table>'
        '</td></tr>'
        # Badges + powered by
        f'<tr><td style="border-top:1px solid {LINE};border-bottom:1px solid {LINE};padding:14px 0">'
        '<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="100%" style="border-collapse:collapse"><tr>'
        f'{"".join(badges)}<td width="100%">&nbsp;</td>{powered}'
        '</tr></table>'
        '</td></tr>'
        f'{notice_html}'
        '</table>'
    )


def page(title, body):
    return (f'<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<title>{e(title)}</title>\n</head>\n'
            f'<body style="margin:0;padding:24px;background:#FFFFFF">\n{body}\n</body>\n</html>\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Public URL of the images/ folder (trailing slash)")
    args = parser.parse_args()
    base = args.base_url if args.base_url.endswith("/") else args.base_url + "/"

    config = json.loads((ROOT / "config" / "signatures.json").read_text(encoding="utf-8"))
    company = config["company"]
    out = ROOT / "signatures"
    out.mkdir(exist_ok=True)

    preview = []
    for person in config["people"]:
        for with_notice, suffix, label in ((True, "", "con aviso de privacidad"), (False, "-sin-aviso", "sin aviso de privacidad")):
            sig = build_signature(company, person, base, with_notice)
            (out / f'{person["id"]}{suffix}.html').write_text(page(f'{person["name"]} - {label}', sig), encoding="utf-8")
            preview.append(
                f'<h2 style="font-family:{FONT};font-size:14px;color:#6A6A78;margin:32px 0 12px">{e(person["name"])} - {label}</h2>'
                + build_signature(company, person, "images/", with_notice)
            )
            print(f'signatures/{person["id"]}{suffix}.html')

    (ROOT / "preview.html").write_text(page("Orchid MoveMex - signatures preview", "\n".join(preview)), encoding="utf-8")
    print("preview.html")


if __name__ == "__main__":
    main()
