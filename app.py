import os
import re
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)
CSV_FILE = "productos_falabella_bicicletas.csv"


def cargar_datos_bicicletas():
    """Lee el archivo CSV generado por el scraper y normaliza sus campos."""
    if not os.path.exists(CSV_FILE):
        return []

    df = pd.read_csv(CSV_FILE, sep=";", encoding="utf-8-sig").fillna("No disponible")
    registros = []

    for _, row in df.iterrows():
        valor_str = str(row.get("Valor", "$0"))
        digitos = re.sub(r"[^0-9]", "", valor_str)
        precio_num = int(digitos) if digitos else 0

        nombre_marca = str(row.get("Nombre/Marca", ""))
        if "[" in nombre_marca and "]" in nombre_marca:
            marca = nombre_marca.split("]")[0].replace("[", "").strip()
        else:
            marca = "Falabella"

        registros.append({
            "sku": str(row.get("Referencia (SKU)", "N/A")),
            "marca": marca,
            "nombre": nombre_marca,
            "valor": valor_str,
            "precio_num": precio_num,
            "caracteristicas": str(row.get("Características", "")),
        })

    return registros


@app.route("/")
def index():
    """Renderiza el dashboard web interactivo."""
    productos = cargar_datos_bicicletas()
    precios_validos = [p["precio_num"] for p in productos if p["precio_num"] > 0]

    stats = {
        "total": len(productos),
        "promedio": f"${sum(precios_validos) / len(precios_validos):,.0f}" if precios_validos else "$0",
        "minimo": f"${min(precios_validos):,.0f}" if precios_validos else "$0",
        "maximo": f"${max(precios_validos):,.0f}" if precios_validos else "$0",
    }
    return render_template("index.html", productos=productos, stats=stats)


@app.route("/api/bicicletas")
def api_bicicletas():
    """Endpoint REST en formato JSON con el catálogo completo."""
    productos = cargar_datos_bicicletas()
    return jsonify({
        "fuente": "Falabella Colombia - Categoría Bicicletas",
        "total": len(productos),
        "productos": productos,
    })


@app.route("/health")
def health():
    """Endpoint de monitoreo de salud del servicio en la nube."""
    return jsonify({"status": "ok", "service": "falabella-bicicletas-web"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
