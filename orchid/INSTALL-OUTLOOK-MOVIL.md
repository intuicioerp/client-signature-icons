# Cómo poner tu firma de Orchid MoveMex en Outlook del celular

El correo que se envía a Rodolfo y Lety está en [EMAIL-ENTREGA.html](EMAIL-ENTREGA.html). Galería de firmas para
celular: `https://intuicioerp.github.io/client-signature-icons/orchid/signatures/movil/index.html`.

## Firma para celular (recomendada)

Mismo diseño que la de la computadora, pero con la parte de arriba (logo, nombre, cargo, compañía y sellos) en **una
sola imagen** (`images/cabecera-<id>.png`) y los datos con sus enlaces debajo, en texto: celular/WhatsApp, teléfono,
email, web, dirección, Instagram, Facebook, LinkedIn y el registro en IAM. Igual que en la computadora, hay versión
con aviso de privacidad y sin aviso. Se genera con
`python build_mobile.py --base-url https://intuicioerp.github.io/client-signature-icons/orchid/images/`.

| Persona | Con aviso | Sin aviso | Imagen |
|---|---|---|---|
| Rodolfo Cerda | `signatures/movil/rodolfo-cerda.html` | `signatures/movil/rodolfo-cerda-sin-aviso.html` | `images/cabecera-rodolfo-cerda.png` |
| Lety de los Santos | `signatures/movil/lety-de-los-santos.html` | `signatures/movil/lety-de-los-santos-sin-aviso.html` | `images/cabecera-lety-de-los-santos.png` |

1. En el celular, abrir el enlace (delante va `https://intuicioerp.github.io/client-signature-icons/orchid/`).
2. Mantener presionado → **Seleccionar todo** → **Copiar**.
3. Outlook → foto o inicial (arriba a la izquierda) → **engranaje** → **Firma** (iPhone: activar antes
   **Firma por cuenta** si hay varias) → borrar el texto que trae → **Pegar** → guardar (✓ en Android; en iPhone
   basta con volver atrás).
4. Enviarse un correo de prueba y tocar los enlaces.
5. Si la imagen no aparece: descargar `images/cabecera-<id>.png` en el celular y en el editor de firma usar el icono
   de **imagen** → galería, dejando el texto debajo.

## Última opción: firma de solo texto

Si nada de lo anterior funciona en un teléfono concreto:

```
Rodolfo Cerda
CEO | Orchid MoveMex Enterprises®
Cel. / WhatsApp: +52 55 6971 8344
Tel.: +52 55 6530 5480
rodolfo@orchidmove.com
www.orchidmove.com
```

```
Lety de los Santos
Operations Manager | Orchid MoveMex Enterprises®
Tel.: +52 55 6530 5480
lety@orchidmove.com
www.orchidmove.com
```

En la computadora siguen usando la firma completa ([INSTALL-OUTLOOK.md](INSTALL-OUTLOOK.md)).
