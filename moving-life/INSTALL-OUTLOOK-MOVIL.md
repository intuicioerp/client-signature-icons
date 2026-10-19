# Cómo poner tu firma de Moving Life en Outlook del móvil

El correo que se envía al equipo está en [EMAIL-MOVIL.html](EMAIL-MOVIL.html). Galería de firmas móviles: `https://intuicioerp.github.io/client-signature-icons/moving-life/dist/movil/index.html`.

## Firma móvil (recomendada)

Mismo diseño que la del ordenador, pero con la parte de arriba (logo, foto, nombre, cargo, sellos) en **una sola imagen** (`images/cabecera-<slug>.png`) y los datos con sus enlaces debajo, en texto. Se genera con `python build_mobile.py --base-url https://intuicioerp.github.io/client-signature-icons/moving-life/` a partir de `src/*.htm`.

1. En el móvil, abrir `https://intuicioerp.github.io/client-signature-icons/moving-life/dist/movil/<slug>.html`.
2. Mantener pulsado → **Seleccionar todo** → **Copiar**.
3. Outlook → foto o inicial → **engranaje** → **Firma** (iPhone: **Firma por cuenta** si hay varias) → borrar → **Pegar** → guardar (✓ en Android).
4. Enviarse un correo de prueba y tocar los enlaces.
5. Si la imagen no aparece: descargar `images/cabecera-<slug>.png` en el móvil y en el editor de firma usar el icono de **imagen** → galería, dejando el texto debajo.

## Última opción: firma de solo texto

Si nada de lo anterior funciona en un teléfono concreto:

```
Arelys Montilla
Founder & CEO | Moving Life
arelys@movinglife.com.ve
(+58) 414-204.66.51
www.movinglife.com.ve
```

```
Erika Arciniegas
Operations Manager | Moving Life
erika@movinglife.com.ve
+54 9 11 3590-4816
www.movinglife.com.ve
```

```
José Martínez
Administration Manager | Moving Life
jose@movinglife.com.ve
+58 424 1879452
www.movinglife.com.ve
```

```
Moraima Pinto
Operations Assistant | Moving Life
moraima@movinglife.com.ve
+58 414 2894949
www.movinglife.com.ve
```

## 2. Pégala en Outlook

**iPhone**

1. Abre Outlook y toca tu foto o la inicial de tu cuenta (arriba a la izquierda).
2. Toca el **engranaje** (Configuración).
3. Entra en **Firma**.
4. Si tienes varias cuentas, activa **Firma por cuenta** y elige la de Moving Life.
5. Borra el texto que trae ("Obtener Outlook para iOS"), pega tu firma y vuelve atrás. Se guarda sola.

**Android**

1. Abre Outlook y toca tu foto o la inicial de tu cuenta (arriba a la izquierda).
2. Toca el **engranaje** (Configuración).
3. Toca **Firma**. Si tienes varias cuentas, elige primero la de Moving Life.
4. Borra el texto que trae ("Obtener Outlook para Android"), pega tu firma y toca **✓** para guardar.

## 3. Comprueba que funciona

Envíate un correo desde el móvil y mira que la firma salga al final.

En el ordenador sigue usando la firma completa de tu enlace personal ([INSTALL-OUTLOOK.md](INSTALL-OUTLOOK.md)).
