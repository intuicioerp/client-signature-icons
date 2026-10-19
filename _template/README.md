# Nuevo cliente: firmas de correo

Pasos para preparar las firmas de un cliente nuevo. Copia como punto de partida la carpeta del cliente más parecido:

- `moving-life/`: cada persona tiene su propio `src/<slug>.htm` (diseño hecho a mano) y `build.py` cambia las rutas de las imágenes.
- `a2z/`: todos los datos están en `config/signatures.json` y `build.py` genera el HTML. Es la más fácil de ampliar con personas nuevas.

## Lista de comprobación

1. Recoger por persona: nombre, cargo, email, móvil/WhatsApp, foto y ciudad o país. Recoger también el logo, los sellos y las redes del cliente.
2. Crear `<cliente>/images/`, `<cliente>/src/` o `config/`, y `build.py`. Generar `dist/` con
   `python build.py --base-url https://intuicioerp.github.io/client-signature-icons/<cliente>/images/`. No editar `dist/` a mano.
3. Escribir las dos guías en el idioma del cliente:
   - `INSTALL-OUTLOOK(.md)`: ordenador y web, firma completa copiada desde el enlace.
   - `INSTALL-OUTLOOK-MOBILE` / `-MOVIL(.md)`: móvil, firma de **solo texto** con un bloque por persona.
4. Copiar la firma HTML de cada usuario también a su ficha en Odoo (Ajustes → Usuarios → Preferencias → Firma).
5. Añadir el cliente a la tabla de `README.md` de la raíz.
6. Enviar el correo de entrega (plantillas `EMAIL-ENTREGA.es.md` / `EMAIL-DELIVERY.en.md`). **Siempre incluye la parte del móvil**: Outlook para iPhone/Android no muestra la firma HTML completa.

## Al cambiar un dato (teléfono, cargo…)

Cambiarlo en los tres sitios: `src/` o `config/` y regenerar `dist/`, la guía del móvil y la firma en Odoo. Recordar a la persona que vuelva a copiar la firma en Outlook, porque Outlook guarda su propia copia.
