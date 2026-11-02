from pathlib import Path

VIEJO = "https://t.me/TU_CANAL"
NUEVO = "https://t.me/marcasderopayzapatillas"

cambiados = 0
for f in Path(".").rglob("*.html"):
    if ".git" in f.parts:
        continue
    txt = f.read_text(encoding="utf-8")
    if VIEJO in txt:
        f.write_text(txt.replace(VIEJO, NUEVO), encoding="utf-8")
        cambiados += 1
        print("Corregido:", f)

print(f"Total: {cambiados} archivos")
