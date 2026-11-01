import os
import re
import html

CARPETA_ARTICULOS = 'articulos'
ARCHIVO_INDEX = 'index.html'

CSS = """<style>
.cards-articulos{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;padding:0;margin:0;list-style:none}
.card-articulo{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.08);transition:transform .2s,box-shadow .2s}
.card-articulo:hover{transform:translateY(-6px);box-shadow:0 10px 24px rgba(0,0,0,.15)}
.card-articulo a{display:flex;flex-direction:column;height:100%;text-decoration:none;color:inherit}
.card-articulo img{width:100%;height:170px;object-fit:cover}
.card-articulo .sin-imagen{height:170px;background:linear-gradient(135deg,#1e3c72,#2a9d8f);display:flex;align-items:center;justify-content:center;font-size:3rem}
.card-articulo .contenido{padding:18px;display:flex;flex-direction:column;gap:10px;flex:1}
.card-articulo h3{margin:0;font-size:1.15rem;line-height:1.3;color:#1a1a1a}
.card-articulo p{margin:0;font-size:.92rem;line-height:1.5;color:#555}
.card-articulo .leer-mas{margin-top:auto;font-weight:600;font-size:.9rem;color:#2a9d8f}
</style>"""

def extraer(contenido, patrones):
    for p in patrones:
        m = re.search(p, contenido, re.IGNORECASE | re.DOTALL)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return None

if not os.path.exists(CARPETA_ARTICULOS):
    print(f"La carpeta '{CARPETA_ARTICULOS}' no existe.")
    exit(1)

articulos = sorted(
    (f for f in os.listdir(CARPETA_ARTICULOS) if f.endswith('.html')),
    reverse=True
)

tarjetas = ""
for art in articulos:
    with open(os.path.join(CARPETA_ARTICULOS, art), 'r', encoding='utf-8') as f:
        contenido = f.read()

    titulo = extraer(contenido, [r'<h1[^>]*>(.*?)</h1>', r'<title>(.*?)</title>']) \
        or art.replace('.html', '').replace('-', ' ').replace('_', ' ').capitalize()

    descripcion = extraer(contenido, [
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        r'<p[^>]*>(.*?)</p>'
    ]) or ""
    if len(descripcion) > 140:
        descripcion = descripcion[:140].rsplit(' ', 1)[0] + '…'

    imagen = extraer(contenido, [r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']'])
    if imagen and not imagen.startswith(('http', '/')):
        imagen = f"./{CARPETA_ARTICULOS}/{imagen}"

    media = (f'<img src="{html.escape(imagen)}" alt="{html.escape(titulo)}" loading="lazy">'
             if imagen else '<div class="sin-imagen">🏅</div>')

    tarjetas += f"""  <li class="card-articulo">
    <a href="./{CARPETA_ARTICULOS}/{art}">
      {media}
      <div class="contenido">
        <h3>{html.escape(titulo)}</h3>
        <p>{html.escape(descripcion)}</p>
        <span class="leer-mas">Leer artículo →</span>
      </div>
    </a>
  </li>
"""

html_lista = f'{CSS}\n<ul class="cards-articulos">\n{tarjetas}</ul>'

with open(ARCHIVO_INDEX, 'r', encoding='utf-8') as f:
    contenido_index = f.read()

patron = r"<!-- START_ARTICULOS -->.*?<!-- END_ARTICULOS -->"
nuevo_bloque = f"<!-- START_ARTICULOS -->\n{html_lista}\n<!-- END_ARTICULOS -->"

if not re.search(patron, contenido_index, re.DOTALL):
    print("Error: faltan las etiquetas START_ARTICULOS / END_ARTICULOS en index.html")
    exit(1)

# lambda: evita que re.sub interprete las barras invertidas del bloque
nuevo_contenido = re.sub(patron, lambda m: nuevo_bloque, contenido_index, flags=re.DOTALL)

with open(ARCHIVO_INDEX, 'w', encoding='utf-8') as f:
    f.write(nuevo_contenido)

print("¡index.html actualizado con éxito!")
