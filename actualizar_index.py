import os
import re
import html

CARPETA_ARTICULOS = 'articulos'
ARCHIVO_INDEX = 'index.html'

# (palabras clave, categoría, icono). Gana la primera que coincida.
# Si no coincide ninguna: categoría "GUÍA" e icono vacío.
CATEGORIAS = [
    (['calentamiento', 'entrenar'], 'ENTRENAMIENTO', '⏱️'),
    (['oferta', 'descuento'], 'OFERTAS', '🏷️'),
    (['mochila', 'senderismo', 'monta'], 'MONTAÑA', '🥾'),
    (['zapatilla', 'running', 'correr'], 'RUNNING', '👟'),
    (['casa', 'gimnasio', 'fuerza', 'mancuerna'], 'FITNESS', '🏋️'),
]


def limpiar(texto):
    texto = re.sub(r'<[^>]+>', '', texto)
    return re.sub(r'\s+', ' ', html.unescape(texto)).strip()


def extraer(contenido, patrones):
    for p in patrones:
        m = re.search(p, contenido, re.IGNORECASE | re.DOTALL)
        if m and limpiar(m.group(1)):
            return limpiar(m.group(1))
    return None


def categoria(texto):
    t = texto.lower()
    for claves, nombre, icono in CATEGORIAS:
        if any(c in t for c in claves):
            return nombre, icono
    return 'GUÍA', ''


if not os.path.exists(CARPETA_ARTICULOS):
    print(f"La carpeta '{CARPETA_ARTICULOS}' no existe.")
    exit(1)

articulos = sorted(
    (f for f in os.listdir(CARPETA_ARTICULOS) if f.endswith('.html')),
    reverse=True
)

tarjetas = ""
for i, art in enumerate(articulos):
    with open(os.path.join(CARPETA_ARTICULOS, art), 'r', encoding='utf-8') as f:
        contenido = f.read()

    titulo = extraer(contenido, [r'<h1[^>]*>(.*?)</h1>', r'<title>(.*?)</title>']) \
        or art.replace('.html', '').replace('-', ' ').capitalize()

    descripcion = extraer(contenido, [
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        r'<p[^>]*class=["\']lede["\'][^>]*>(.*?)</p>',
        r'<p[^>]*>(.*?)</p>',
    ]) or ""
    if len(descripcion) > 130:
        descripcion = descripcion[:130].rsplit(' ', 1)[0] + '…'

    cuerpo = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', contenido, flags=re.DOTALL | re.IGNORECASE)
    minutos = max(1, round(len(limpiar(cuerpo).split()) / 200))

    kicker, icono = categoria(art + ' ' + titulo)

    tarjetas += (
        f'<a class="card" href="{CARPETA_ARTICULOS}/{art}">'
        f'<div class="thumb g{i % 5 + 1}"><span>{icono}</span></div>'
        f'<div class="cbody"><div><span class="kicker">{kicker}</span>'
        f'<span class="chip">{minutos} min</span></div>'
        f'<h3>{html.escape(titulo)}</h3><p>{html.escape(descripcion)}</p>'
        f'<span class="more">Leer guía →</span></div></a>\n'
    )

seccion = f"""<section class="block"><div class="wrap">
<h2 class="sec">Últimas guías</h2>
<p class="sec-sub">Contenido práctico y actualizado, pensado para que puedas aplicarlo hoy mismo.</p>
<div class="grid">
{tarjetas}</div>
</div></section>"""

with open(ARCHIVO_INDEX, 'r', encoding='utf-8') as f:
    contenido_index = f.read()

patron = r"<!-- START_ARTICULOS -->.*?<!-- END_ARTICULOS -->"
nuevo_bloque = f"<!-- START_ARTICULOS -->\n{seccion}\n<!-- END_ARTICULOS -->"

if not re.search(patron, contenido_index, re.DOTALL):
    print("Error: faltan las etiquetas START_ARTICULOS / END_ARTICULOS en index.html")
    exit(1)

nuevo_contenido = re.sub(patron, lambda m: nuevo_bloque, contenido_index, flags=re.DOTALL)

with open(ARCHIVO_INDEX, 'w', encoding='utf-8') as f:
    f.write(nuevo_contenido)

print("¡index.html actualizado con éxito!")
