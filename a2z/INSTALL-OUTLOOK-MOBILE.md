# How to add your A2Z signature to Outlook on your phone

The email sent to the team is [EMAIL-MOBILE.html](EMAIL-MOBILE.html). Gallery of mobile signatures: `https://intuicioerp.github.io/client-signature-icons/a2z/dist/mobile/index.html`.

## Mobile signature (recommended)

Same design as the desktop one, but the top part (photo, name, title, logo, badges) is **one image** (`images/header-<slug>.png`) and the details and links are text underneath. Generated with `python build_mobile.py --base-url https://intuicioerp.github.io/client-signature-icons/a2z/` from `config/signatures.json`.

1. On the phone, open `https://intuicioerp.github.io/client-signature-icons/a2z/dist/mobile/<slug>.html`.
2. Press and hold → **Select all** → **Copy**.
3. Outlook → picture or initial → **gear icon** → **Signature** (iPhone: **Per Account Signature** if several accounts) → delete → **Paste** → save (✓ on Android).
4. Send yourself a test email and tap the links.
5. If the image does not show: save `images/header-<slug>.png` on the phone and use the **image** icon in the signature editor → photo library, keeping the text underneath.

## Last resort: text-only signature

If nothing above works on a given phone:

```
Marly Springer
CEO | A2Z Move Management
marlyspringer@a2zmovemgmt.com
WhatsApp/Cell: +1 305-986-6650
www.a2zmovemgmt.com
```

```
Richard Riddle
Vice President | A2Z Move Management
info@a2zmovemgmt.com
www.a2zmovemgmt.com
```

```
Eduardo Texeira
Senior Move Services Consultant | A2Z Move Management
imports@a2zmovemgmt.com
www.a2zmovemgmt.com
```

```
Ana Torres
Senior Move Services Consultant | A2Z Move Management
exports@a2zmovemgmt.com
www.a2zmovemgmt.com
```

```
Vania Masanovic
Senior Move Services Consultant | A2Z Move Management
vaniamasanovic@a2zmovemgmt.com
www.a2zmovemgmt.com
```

```
Julieta Vangeli
Regional Partner Europe | A2Z Move Management
julietavangeli@a2zmovemgmt.com
www.a2zmovemgmt.com
```

## 2. Paste it into Outlook

**iPhone**

1. Open Outlook and tap your profile picture or initial (top left).
2. Tap the **gear icon** (Settings).
3. Tap **Signature**.
4. If you have several accounts, turn on **Per Account Signature** and pick your A2Z account.
5. Delete the default text ("Get Outlook for iOS"), paste your signature and go back. It saves automatically.

**Android**

1. Open Outlook and tap your profile picture or initial (top left).
2. Tap the **gear icon** (Settings).
3. Tap **Signature**. If you have several accounts, pick your A2Z account first.
4. Delete the default text ("Get Outlook for Android"), paste your signature and tap **✓** to save.

## 3. Test it

Send yourself an email from your phone and check that the signature appears at the bottom.

On your computer, keep using the full signature from your personal link ([INSTALL-OUTLOOK.md](INSTALL-OUTLOOK.md)).
