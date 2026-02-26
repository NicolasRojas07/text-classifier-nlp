from flask import Flask, request, render_template, jsonify
import os
import time

# =========================
# CREAR APP
# =========================
app = Flask(__name__)

# =========================
# IMPORTS DEL MODELO (SOLO LO QUE EXISTE)
# =========================
from app.models.ModeloDeClasificacionTextos import (
    entrenar_modelo,
    clasificar_nuevo_pdf,
    cargar_dataset,
    ensure_categories_from_dataset,
    get_categories,
    evaluar_precision_rapido
)

# =========================
# CONFIGURACIÓN
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Variables globales para caché
_dataset_cache = None
_dataset_cache_time = 0
CACHE_TTL = 10  # 10 segundos

def cargar_dataset_cached():
    """Carga el dataset con caché para evitar lecturas repetidas"""
    global _dataset_cache, _dataset_cache_time
    now = time.time()
    
    if _dataset_cache is None or (now - _dataset_cache_time) > CACHE_TTL:
        print(f"Recargando dataset del disco...")
        _dataset_cache = cargar_dataset()
        _dataset_cache_time = now
        if _dataset_cache:
            ensure_categories_from_dataset(_dataset_cache)
    return _dataset_cache or []

# Cargar categorías al iniciar la app
print("Iniciando servidor...")
dataset_inicial = cargar_dataset_cached()
if dataset_inicial:
    print(f"Categorias inicializadas: {get_categories()}")
else:
    print("Dataset vacio al iniciar")



def construir_tabla_dataset(dataset):
    dataset_tabla = []
    for d in dataset[-5:] if len(dataset) > 5 else dataset:
        texto_completo = d.get("texto", "")
        texto = texto_completo[:50] + "..." if len(texto_completo) > 50 else texto_completo

        dataset_tabla.append({
            "texto_preview": texto,
            "categoria": d.get("categoria", "N/A"),
            "tamaño": len(texto_completo)
        })
    return dataset_tabla


@app.route("/", methods=["GET"])
def index():
    dataset = cargar_dataset_cached()
    categorias = get_categories()

    return render_template(
        "index.html",
        dataset_tabla=construir_tabla_dataset(dataset),
        total_textos=len(dataset),
        categorias=categorias
    )


@app.route("/entrenar", methods=["GET"])
def entrenar():
    global _dataset_cache
    dataset = cargar_dataset_cached()
    resultado = entrenar_modelo(dataset)
    categorias = get_categories()
    # Invalidar caché después de entrenar
    _dataset_cache = None

    return render_template(
        "index.html",
        metricas=resultado,
        dataset_tabla=construir_tabla_dataset(dataset),
        total_textos=len(dataset),
        categorias=categorias
    )


@app.route("/clasificar", methods=["POST"])
def clasificar_pdf():
    global _dataset_cache
    if "archivo" not in request.files:
        return "No se envió archivo", 400

    archivo = request.files["archivo"]

    if archivo.filename == "":
        return "Archivo vacío", 400

    ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
    archivo.save(ruta)

    categoria = clasificar_nuevo_pdf(ruta)
    
    # Invalidar caché después de clasificar para reflejar nuevos datos
    _dataset_cache = None

    dataset = cargar_dataset_cached()
    categorias = get_categories()

    return render_template(
        "index.html",
        resultado=categoria,
        dataset_tabla=construir_tabla_dataset(dataset),
        total_textos=len(dataset),
        categorias=categorias
    )

@app.route("/precision", methods=["GET"])
def precision():
    dataset = cargar_dataset_cached()
    resultado = evaluar_precision_rapido()
    categorias = get_categories()

    return render_template(
        "index.html",
        metricas=resultado,
        dataset_tabla=construir_tabla_dataset(dataset),
        total_textos=len(dataset),
        categorias=categorias
    )

@app.route("/api/dataset", methods=["GET"])
def api_dataset():
    """Retorna el dataset en JSON para actualización en tiempo real"""
    try:
        dataset = cargar_dataset_cached()
        dataset_tabla = construir_tabla_dataset(dataset)
        categorias = get_categories()
        
        return jsonify({
            "total_textos": len(dataset),
            "dataset": dataset_tabla,
            "categorias": categorias,
            "success": True
        })
    except Exception as e:
        print(f"Error en /api/dataset: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route("/api/metricas", methods=["GET"])
def api_metricas():
    """Retorna las métricas del modelo en JSON"""
    try:
        resultado = evaluar_precision_rapido()
        return jsonify(resultado)
    except Exception as e:
        print(f"Error en /api/metricas: {e}")
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)