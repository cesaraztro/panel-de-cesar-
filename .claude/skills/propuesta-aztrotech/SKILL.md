---
name: propuesta-aztrotech
description: "Genera propuestas comerciales de AztroTech en PDF de máximo 2 hojas, concretas y prácticas, con la marca ya aplicada (hero Eclipse, KPIs, tabla de 'lo que pides / lo que hace', inversión con formas de pago, requisitos para arrancar y firmas). Úsala SIEMPRE que César pida 'hazle una propuesta a X', 'cotízale', 'arma la propuesta', 'mándale precio', 'propuesta comercial', 'actualiza la propuesta de X', o cuando traiga un audio, notas o una reunión de un cliente y quiera convertirlo en propuesta."
---

# Propuesta AztroTech · 2 hojas, directa

Una propuesta de AztroTech **cabe en 2 hojas, sin excepción**, y se lee en dos minutos: qué necesita el cliente, qué va a poder hacer, cuánto cuesta, cuándo queda y qué falta para arrancar. Si algo no ayuda a que el cliente diga “sí”, no va.

## 1. Primero el contenido

Antes de abrir la plantilla, junta los hechos:

- **Fuente:** audio o mensaje del cliente, notas, reunión de Grain (`fetch_meeting_notes` / `fetch_meeting_transcript`), o lo que diga César.
- **CRM:** busca al cliente con `list_leads` (Aztrotech_Platform) para no contradecir montos o acuerdos previos.
- **Precios de referencia:** revisa las propuestas anteriores en `propuestas/` del repo `panel-de-cesar-` y el campo `amount_estimated` del CRM. Si el precio no está claro, **pon tu mejor estimado y avísale a César en el chat** qué supusiste; no lo dejes en blanco.
- **¿Se puede hacer?** Si hay algo que técnicamente no conviene (por ejemplo, automatizar el WhatsApp personal), va como fila en rojo en la tabla “Así funciona”, en una línea. Nada de letra chiquita escondida.

## 2. Reglas de redacción

- **Máximo 2 hojas.** Si no cabe, recorta contenido; nunca bajes la tipografía ni muevas medidas del CSS.
- **Concreto y práctico:** ejemplos reales de uso (“Mándale mensaje a la Lic. Pérez…” → qué pasa), no adjetivos.
- Frases cortas, una idea por renglón, tuteo, lenguaje llano. Sin jerga ni anglicismos (nada de “deliverable”, “kick-off”, “stakeholder”, “bloqueante”).
- **Prohibido:** secciones de “costo de esperar”, “cómo trabajamos” / pilares, filosofía, bonos inventados, garantías que César no ofreció, testimonios, historia de AztroTech.
- Precios siempre **MXN + IVA**. Pago en dos partes = ~10 % más caro que el pago único.
- La fase 2 (o lo que va “después”) va en **una sola nota**, con precio “desde”, no como sección. Si César pide enfocarse en lo que el cliente quiere, quítala.
- **Agentes, no chatbots:** cuando lo que se vende es un agente tipo Hermes (vive en WhatsApp o Telegram, tiene memoria, ejecuta órdenes), nunca lo llames chatbot ni lo compares con chatbots.
- **Precio especial** (familia, cliente fundador, referido): muestra el precio normal tachado con `<span class="was">$32,000</span>` junto al precio especial, y escribe en una línea qué da el cliente a cambio (testimonio, presentaciones con contactos, mensualidad fija 12 meses). Así nadie toma el precio especial como tarifa normal.
- **Gastos de operación:** di siempre quién paga qué. La mensualidad de AztroTech cubre servidor, IA, mantenimiento y soporte; lo que cobra un tercero directo al cliente (por ejemplo, los mensajes de WhatsApp de Meta) va en “No incluye” y, si aplica, en la tarjeta de la opción.

## 3. Estructura fija

**Hoja 1 · El problema y la solución**
1. **Hero:** logo · píldora `PROPUESTA · CLIENTE · MES AAAA` · H1 de una línea con la segunda mitad en `<b>` · intro de 2 renglones máximo · meta (Para / De / Fecha).
2. **4 KPIs:** Qué resolvemos · Operando en · Inversión · Mensualidad (el último en dorado, clase `gold`). Valores de 1–3 palabras.
3. **01 · Lo que necesitas:** 3 renglones, en las palabras del cliente.
4. **02 · Así funciona:** tabla de 4 a 6 filas `TÚ LE DICES / EL SISTEMA HACE` (o `NECESITAS / LO QUE HACEMOS`), cada una con chip `SÍ`, `SÍ, CON CONDICIÓN` o `NO` (fila `class="no"`).
5. **Opciones** (si el cliente debe elegir, por ejemplo WhatsApp o Telegram): bloque `.opts` con dos `.card.opt` (la recomendada con clase `rec` y chip RECOMENDADO), 2 viñetas cada una y un renglón `.cost` con el gasto extra. Si no hay opciones, puede ir la **nota de fase 2** (una sola).

**Hoja 2 · Alcance, inversión y arranque**
6. **03 · Qué incluye:** dos tarjetas, Incluye (≤6) y No incluye (≤4).
7. **04 · Calendario:** 3 a 4 renglones por semana.
8. **05 · Inversión:** 3 tarjetas (Pago único `rec` con chip MEJOR PRECIO · 2 pagos · Mensualidad). Si hay varios conceptos con precio distinto, usa en su lugar la tabla `table.price` con fila `total`.
9. **06 · Para arrancar necesitamos:** 4 a 6 requisitos concretos del cliente (accesos, números, información, anticipo).
10. **Siguiente paso** (tarjeta oscura `next`): la acción concreta (Zoom, firma, anticipo) + vigencia 30 días.
11. **Firmas** (Propone / Acepta) y **footer**.

## 4. Cómo se arma

La plantilla vive en `assets/` (fuentes Poppins y Cinzel embebidas, logo vectorial y CSS calibrado). Tú solo escribes el **cuerpo** (`<section class="page">…</section>` × 2). Parte de `assets/ejemplo-cuerpo.html` (propuesta de Raúl Echave) y reemplaza el contenido; no inventes clases nuevas salvo que sea indispensable.

```bash
SKILL=<ruta de esta skill>
mkdir -p propuestas/<cliente>
cp $SKILL/assets/ejemplo-cuerpo.html propuestas/<cliente>/cuerpo.html   # y edítalo
python3 $SKILL/scripts/build.py propuestas/<cliente>/cuerpo.html \
  propuestas/<cliente>/propuesta_<cliente>_v1 \
  --title "Propuesta · <Cliente> · AZTROTECH" --previews <scratchpad>/prev
```

`build.py` genera el `.html` autocontenido y el `.pdf`, crea las vistas previas PNG y **falla si pasa de 2 hojas**. Usa el Chromium del entorno (`/opt/pw-browsers/chromium`, `chromium` o Playwright como respaldo).

## 5. Verificación antes de entregar

1. **Mira las dos imágenes de vista previa.** Revisa que nada quede cortado al pie de cada hoja (firmas y footer completos), que los chips sean píldoras compactas y que no haya renglones huérfanos feos.
2. Si la hoja 2 se desborda: quita filas de “Incluye”, junta renglones del calendario o acorta textos. Si la hoja 1 queda con mucho aire, sube el calendario o agrega una fila útil a “Así funciona”.
3. Precios consistentes en KPIs, tarjetas de pago y nota de fase 2.

## 6. Entrega

- Guarda en `propuestas/<cliente>/`: `cuerpo.html` (fuente editable), `propuesta_<cliente>_vN.html` y `.pdf`. Una versión nueva = `vN+1`; borra versiones que César descartó.
- Entrega el PDF con `SendUserFile` y, en el chat, solo: qué supusiste (precios, alcance), qué falta confirmar y un mensaje corto listo para mandarle al cliente.
- Contacto del footer: `www.aztrotech.mx · cesarholguin61@gmail.com · 662 107 2254`.
