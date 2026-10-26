#!/usr/bin/env python3
"""Generate Outlook-compatible HTML email signatures for A2Z Move Management.

Usage:
    python3 build.py --base-url https://<owner>.github.io/a2z-signature/images/
    python3 build.py --local            # relative image paths, for previewing on disk

Output: dist/<slug>.html (one signature per file) and dist/index.html (preview gallery).
Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config" / "signatures.json"
DIST = ROOT / "dist"
FONT = "Arial, Helvetica, sans-serif"


def attr(value: str) -> str:
    return escape(value, quote=True)


class Renderer:
    def __init__(self, cfg: dict, base_url: str) -> None:
        self.cfg = cfg
        self.brand = cfg["brand"]
        self.base = base_url if base_url.endswith("/") else base_url + "/"

    # ---------- helpers ----------
    def img(self, spec: dict, extra_style: str = "") -> str:
        return (
            f'<img src="{attr(self.base + spec["file"])}" width="{spec["width"]}" height="{spec["height"]}" '
            f'alt="{attr(spec["alt"])}" border="0" '
            f'style="display:block;border:0;outline:none;text-decoration:none;width:{spec["width"]}px;'
            f'height:{spec["height"]}px;{extra_style}">'
        )

    def link(self, url: str, label: str, style: str) -> str:
        return f'<a href="{attr(url)}" style="{style}">{escape(label)}</a>'

    # ---------- blocks ----------
    def info_cell(self, p: dict) -> str:
        b = self.brand
        accent, body, dark = b["accent"], b["text_body"], b["text_dark"]
        link_style = f"color:{body};text-decoration:none;"
        rows = [
            f'<tr><td style="font-family:{FONT};font-size:22px;line-height:26px;font-weight:bold;'
            f'font-style:italic;color:{dark};padding:0 0 4px 0;">{escape(p["name"])}</td></tr>',
            f'<tr><td style="font-family:{FONT};font-size:13px;line-height:18px;color:{body};padding:0 0 6px 0;">'
            f'{escape(p["title"])} at <strong style="color:{accent};">{escape(b["company"])}</strong></td></tr>',
        ]
        contact = []
        if p.get("phone_tel"):
            contact.append(
                f'<strong style="color:{dark};">{escape(p["phone_label"])}</strong> '
                + self.link(f'tel:{p["phone_tel"]}', p["phone_display"], link_style)
            )
        contact.append(self.link(f'mailto:{p["email"]}', p["email"], link_style))
        contact.append(self.link(b["website_url"], b["website_label"], link_style))
        rows.append(
            f'<tr><td style="font-family:{FONT};font-size:12px;line-height:18px;color:{body};padding:0 0 8px 0;">'
            + "<br>".join(contact)
            + "</td></tr>"
        )

        icons = []
        if p.get("linkedin_url"):
            icons.append(f'<a href="{attr(p["linkedin_url"])}" style="text-decoration:none;">{self.img(self.cfg["icons"]["linkedin"])}</a>')
        icons.append(f'<a href="{attr(b["instagram_url"])}" style="text-decoration:none;">{self.img(self.cfg["icons"]["instagram"])}</a>')
        icon_cells = "".join(f'<td style="padding:0 6px 0 0;" valign="middle">{i}</td>' for i in icons)
        rows.append(
            '<tr><td style="padding:0;"><table cellpadding="0" cellspacing="0" border="0" role="presentation"><tr>'
            + icon_cells
            + "</tr></table></td></tr>"
        )
        rows.append(
            f'<tr><td style="font-family:{FONT};font-size:13px;line-height:18px;font-weight:bold;'
            f'font-style:italic;color:{accent};padding:6px 0 0 0;">{escape(b["tagline"])}</td></tr>'
        )
        return (
            '<table cellpadding="0" cellspacing="0" border="0" role="presentation">' + "".join(rows) + "</table>"
        )

    def header_row(self, p: dict) -> str:
        b = self.brand
        logo_left = p.get("logo_position") == "left"
        cells = []
        if p.get("photo"):
            cells.append(f'<td width="{p["photo"]["width"]}" valign="middle" style="padding:0 16px 0 0;">{self.img(p["photo"])}</td>')
        elif logo_left:
            cells.append(f'<td width="{b["logo"]["width"]}" valign="middle" style="padding:0 16px 0 0;">{self.img(b["logo"])}</td>')
        cells.append(
            f'<td width="4" bgcolor="{b["accent"]}" style="width:4px;background-color:{b["accent"]};font-size:0;line-height:0;">&nbsp;</td>'
        )
        cells.append(f'<td valign="middle" style="padding:0 16px;">{self.info_cell(p)}</td>')
        if not logo_left:
            cells.append(f'<td width="{b["logo"]["width"]}" valign="middle" align="right" style="padding:0;">{self.img(b["logo"])}</td>')
        return (
            '<tr><td style="padding:0 0 14px 0;"><table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation"><tr>'
            + "".join(cells)
            + "</tr></table></td></tr>"
        )

    def logos_row(self, p: dict) -> str:
        b = self.brand
        logos = self.cfg["logo_rows"][p["logo_row"]]
        logo_cells = "".join(
            f'<td valign="middle" style="padding:0 8px 0 0;">{self.img(l)}</td>' for l in logos
        )
        pb = b["powered_by"]
        pb_img = self.img(pb)
        if pb.get("url"):
            pb_img = f'<a href="{attr(pb["url"])}" style="text-decoration:none;">{pb_img}</a>'
        powered = (
            '<table cellpadding="0" cellspacing="0" border="0" role="presentation">'
            f'<tr><td align="center" style="font-family:{FONT};font-size:8px;line-height:10px;font-weight:bold;'
            f'letter-spacing:1px;color:#5C5C5C;padding:0 0 3px 0;">POWERED BY</td></tr>'
            f"<tr><td>{pb_img}</td></tr></table>"
        )
        return (
            f'<tr><td style="border-top:1px solid {b["divider"]};padding:12px 0 12px 0;">'
            '<table width="100%" cellpadding="0" cellspacing="0" border="0" role="presentation"><tr>'
            '<td valign="middle"><table cellpadding="0" cellspacing="0" border="0" role="presentation"><tr>'
            + logo_cells
            + "</tr></table></td>"
            f'<td width="1" bgcolor="{b["divider"]}" style="width:1px;background-color:{b["divider"]};font-size:0;line-height:0;">&nbsp;</td>'
            f'<td width="{pb["width"]}" valign="middle" align="center" style="padding:0 0 0 12px;">{powered}</td>'
            "</tr></table></td></tr>"
        )

    def legal_row(self) -> str:
        b, legal = self.brand, self.cfg["legal"]
        muted, body, accent = b["text_muted"], b["text_body"], b["accent"]
        p_style = f"margin:0 0 8px 0;font-family:{FONT};font-size:10px;line-height:14px;color:{muted};"
        link_style = f"font-family:{FONT};font-size:12px;font-weight:bold;color:{accent};text-decoration:underline;"
        links = " &nbsp;&nbsp;|&nbsp;&nbsp; ".join(self.link(l["url"], l["label"], link_style) for l in legal["links"])
        return (
            f'<tr><td style="border-top:1px solid {b["divider"]};padding:12px 0 0 0;">'
            f'<p style="{p_style}"><strong style="color:{body};">Confidentiality Notice:</strong> {escape(legal["confidentiality"])}</p>'
            f'<p style="{p_style}"><strong style="color:{accent};">{escape(legal["market_title"])}</strong><br>{escape(legal["market_text"])}</p>'
            f'<p style="margin:0;font-family:{FONT};font-size:12px;line-height:18px;color:{body};">{links}</p>'
            "</td></tr>"
        )

    def signature(self, p: dict) -> str:
        return (
            '<table width="620" cellpadding="0" cellspacing="0" border="0" role="presentation" '
            f'style="width:620px;font-family:{FONT};background-color:#FFFFFF;">'
            + self.header_row(p)
            + self.logos_row(p)
            + self.legal_row()
            + "</table>"
        )


def page(title: str, body: str) -> str:
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        f"<title>{escape(title)}</title>\n</head>\n"
        '<body style="margin:0;padding:16px;background-color:#FFFFFF;">\n'
        f"{body}\n</body>\n</html>\n"
    )


def build(base_url: str) -> None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    renderer = Renderer(cfg, base_url)
    DIST.mkdir(exist_ok=True)
    gallery = []
    for person in cfg["people"]:
        sig = renderer.signature(person)
        out = DIST / f'{person["slug"]}.html'
        out.write_text(page(f'Email signature - {person["name"]}', sig), encoding="utf-8")
        gallery.append(
            f'<h2 style="font-family:{FONT};font-size:16px;color:#1F1F1F;margin:32px 0 8px 0;">'
            f'{escape(person["name"])} &mdash; <a href="{attr(out.name)}">open signature only</a></h2>{sig}'
        )
        print(f"wrote {out.relative_to(ROOT)}")
    index = (
        f'<p style="font-family:{FONT};font-size:14px;color:#4A4A4A;">To install a signature, open its '
        '"signature only" page, press Ctrl+A / Cmd+A, copy, and paste it into Outlook. See INSTALL-OUTLOOK.md.</p>'
        + "".join(gallery)
    )
    (DIST / "index.html").write_text(page("A2Z Move Management - Email signatures", index), encoding="utf-8")
    print("wrote dist/index.html")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--base-url", help="Public URL of the images/ folder (must end with /images/).")
    group.add_argument("--local", action="store_true", help="Use relative paths (../images/) for local preview.")
    args = parser.parse_args()
    build("../images/" if args.local else args.base_url)


if __name__ == "__main__":
    main()
