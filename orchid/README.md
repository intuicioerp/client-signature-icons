# Orchid MoveMex — email signatures

Outlook-safe HTML signatures (tables, inline styles, Arial, hosted PNG images) for Orchid MoveMex Enterprises.
Powered by intuiCIO.

Each person has two variants: with the privacy notice inside the signature, and without it (their mail server can
append the notice on its own, but only at the very end of the message, below the quoted thread).

| Person | Computer, with notice | Computer, without notice | Phone, with notice | Phone, without notice |
|---|---|---|---|---|
| Rodolfo Cerda — CEO | `signatures/rodolfo-cerda.html` | `signatures/rodolfo-cerda-sin-aviso.html` | `signatures/movil/rodolfo-cerda.html` | `signatures/movil/rodolfo-cerda-sin-aviso.html` |
| Lety de los Santos — Operations Manager | `signatures/lety-de-los-santos.html` | `signatures/lety-de-los-santos-sin-aviso.html` | `signatures/movil/lety-de-los-santos.html` | `signatures/movil/lety-de-los-santos-sin-aviso.html` |

Galleries: `preview.html` (computer) and `signatures/movil/index.html` (phone).

## Build

```
python build.py --base-url https://intuicioerp.github.io/client-signature-icons/orchid/images/
python build_mobile.py --base-url https://intuicioerp.github.io/client-signature-icons/orchid/images/
```

- Data lives in `config/signatures.json` (company block + one entry per person). Change data there and rerun both
  scripts; never hand-edit `signatures/`, `preview.html` or `images/cabecera-*.png`.
- `mobile` and `whatsapp_url` are optional per person; when `whatsapp_url` is set a WhatsApp icon is added next to the
  company social icons.
- Badge links (`badges[].url`): IAMX and IAM point to Orchid's IAM directory profile (taken from Rodolfo's own
  signature). Movers P.O.E. has no link yet.
- `build_mobile.py` draws one header image per person (`images/cabecera-<id>.png`: logo, name, title, company,
  badges) and puts every link in text underneath, because Outlook for iPhone/Android breaks the desktop signature.
- Do not rename or move files in `images/`: sent emails load them from their public URL.

## Guides and delivery email

- Computer: [INSTALL-OUTLOOK.md](INSTALL-OUTLOOK.md)
- Phone: [INSTALL-OUTLOOK-MOVIL.md](INSTALL-OUTLOOK-MOVIL.md)
- Delivery email (Mexican Spanish, computer + phone, both variants): [EMAIL-ENTREGA.html](EMAIL-ENTREGA.html)
