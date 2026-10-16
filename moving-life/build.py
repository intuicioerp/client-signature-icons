#!/usr/bin/env python3
"""Generate Moving Life signatures: rewrites the image paths of src/*.htm to public URLs.

Usage: python3 build.py --base-url https://intuicioerp.github.io/client-signature-icons/moving-life/images/
Output: dist/<slug>.html (signature only) and dist/index.html (gallery). Never hand-edit dist/.
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGE = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n'
        '<body style="margin:0;padding:16px;background-color:#FFFFFF;">\n{body}\n</body>\n</html>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    base = ap.parse_args().base_url.rstrip("/") + "/"
    (ROOT / "dist").mkdir(exist_ok=True)
    gallery = []
    for src in sorted((ROOT / "src").glob("*.htm")):
        slug = src.stem
        html = src.read_text(encoding="utf-8")
        body = re.search(r"<body[^>]*>\s*(.*?)\s*</body>", html, re.S).group(1)
        body = re.sub(r'src="[^"]*_archivos/foto\.png"', f'src="{base}foto-{slug}.png"', body)
        body = re.sub(r'src="[^"]*_archivos/([^"]+)"', lambda m: f'src="{base}{m.group(1)}"', body)
        assert "_archivos" not in body, slug
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        (ROOT / "dist" / f"{slug}.html").write_text(PAGE.format(title=title, body=body), encoding="utf-8")
        gallery.append(f'<h2 style="font-family:Arial;font-size:16px;margin:32px 0 8px 0;">{title} &mdash; '
                       f'<a href="{slug}.html">solo la firma</a></h2>{body}')
        print("wrote dist/%s.html" % slug)
    (ROOT / "dist" / "index.html").write_text(PAGE.format(title="Firmas Moving Life", body="".join(gallery)), encoding="utf-8")


if __name__ == "__main__":
    main()
