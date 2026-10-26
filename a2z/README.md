# A2Z Move Management — Email signatures

Outlook-compatible HTML email signatures for six team members, generated from one data file.

```
images/                  15 PNG assets at 2x resolution (logos, photo, social icons)
config/signatures.json   brand colors, legal text, links and per-person data
build.py                 generator (Python 3.8+, standard library only)
dist/                    generated output — one HTML file per person + index.html
INSTALL-OUTLOOK.md       end-user guide to paste the signature into Outlook
```

## Build

```bash
# Production: images served from GitHub Pages
python3 build.py --base-url https://intuicioerp.github.io/client-signature-icons/a2z/images/

# Local preview: open dist/index.html in a browser
python3 build.py --local
```

## Email-client compatibility

- Table-based layout with inline styles only (no flexbox, no CSS classes, no web fonts).
- Font: Arial / Helvetica.
- All images are PNG with explicit `width`/`height`. A person's `"photo"` must be pre-cropped into a
  circle (classic Outlook ignores `border-radius`); `"logo_position": "left"` puts the A2Z logo before
  the accent bar instead of on the right (Marly, no photo). `marly-photo.png` stays published because
  signatures installed before the change still load it.
- Images are loaded from absolute public URLs; embedded base64 images are avoided because Outlook
  and Gmail often block or strip them.

## Editing

Change names, titles, emails or legal text in `config/signatures.json`, re-run `build.py`, commit `dist/`.
