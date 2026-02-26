import redis
import json
import os

# Conexión Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
CATEGORIAS_KEY = "categorias"

# Ruta de tu dataset JSON
DATASET_FILE = os.path.join("data", "dataset.json")

def ensure_categories_from_dataset_json():
    if not os.path.exists(DATASET_FILE):
        print("No se encontró el dataset:", DATASET_FILE)
        return

    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    categorias = {d["categoria"] for d in dataset if "categoria" in d}

    if categorias:
        r.delete(CATEGORIAS_KEY)
        r.sadd(CATEGORIAS_KEY, *categorias)
        print("Categorías cargadas en Redis:", categorias)
    else:
        print("No se encontraron categorías en el dataset")

def get_categories():
    cats = list(r.smembers(CATEGORIAS_KEY))
    if not cats:
        print("No hay categorías en Redis")
    return cats

# Ejecuta la carga
ensure_categories_from_dataset_json()
print("Categorías actuales en Redis:", get_categories())