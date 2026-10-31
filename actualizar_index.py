import os
import re

# 1. Configuración de carpetas
CARPETA_ARTICULOS = 'articulos'
ARCHIVO_INDEX = 'index.html'

# 2. Leer todos los archivos de la carpeta de artículos
if not os.path.exists(CARPETA_ARTICULOS):
    print(f"La carpeta '{CARPETA_ARTICULOS}' no existe.")
    exit(1)

archivos = os.listdir(CARPETA_ARTICULOS)
# Filtramos solo archivos HTML (puedes cambiarlo a .md si tus artículos usan Markdown)
articulos = [f for f in archivos if f.endswith('.html')]
articulos.sort(reverse=True) # Los más nuevos saldrán arriba (alfabéticamente)

# 3. Generar el código HTML de la lista
html_lista = "<ul>\n"
for art in articulos:
    # Creamos un título bonito quitando la extensión y cambiando guiones por espacios
    titulo_bonito = art.replace('.html', '').replace('-', ' ').replace('_', ' ').capitalize()
    ruta_enlace = f"./{CARPETA_ARTICULOS}/{art}"
    html_lista += f'  <li><a href="{ruta_enlace}">{titulo_bonito}</a></li>\n'
html_lista += "</ul>"

# 4. Leer el index.html actual
with open(ARCHIVO_INDEX, 'r', encoding='utf-8') as f:
    contenido_index = f.read()

# 5. Reemplazar el bloque de artículos usando Expresiones Regulares
patron = r"<!-- START_ARTICULOS -->.*?<!-- END_ARTICULOS -->"
nuevo_bloque = f"<!-- START_ARTICULOS -->\n{html_lista}\n<!-- END_ARTICULOS -->"

if not re.search(patron, contenido_index, re.DOTALL):
    print("Error: No se encontraron las etiquetas <!-- START_ARTICULOS --> y <!-- END_ARTICULOS --> en index.html")
    exit(1)

nuevo_contenido = re.sub(patron, nuevo_bloque, contenido_index, flags=re.DOTALL)

# 6. Guardar los cambios en index.html
with open(ARCHIVO_INDEX, 'w', encoding='utf-8') as f:
    f.write(nuevo_contenido)

print("¡index.html actualizado con éxito!")
