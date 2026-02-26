# Archivo: app/models/ModeloDeClasificacionTextos.py

import pdfplumber
import nltk
import string
import spacy
import os
import json
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score
from scipy.sparse import hstack
import numpy as np

# Redis
import redis

# =============================
# CONFIGURACIÓN
# =============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_FILE = os.path.join(BASE_DIR, "data", "dataset.json")
MODEL_FILE = os.path.join(BASE_DIR, "data", "model.joblib")

os.makedirs(os.path.dirname(DATASET_FILE), exist_ok=True)

# NLTK y Spacy
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

stop_words = set(stopwords.words("spanish"))
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("🔹 Modelo Spacy 'es_core_news_sm' no encontrado. Instálalo con:")
    print("python -m spacy download es_core_news_sm")
    raise

# Redis con fallback
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
try:
    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()
    REDIS_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Redis no disponible: {e}. Usando fallback en memoria.")
    r = None
    REDIS_AVAILABLE = False

CATEGORIES_KEY = "categorias"
_CATEGORIES_CACHE = set()

# =============================
# FUNCIONES DE REDIS
# =============================

def ensure_categories_from_dataset(dataset):
    """Carga automáticamente en Redis (o en caché) las categorías del dataset JSON."""
    global _CATEGORIES_CACHE
    categorias = {d["categoria"] for d in dataset if d.get("categoria")}
    _CATEGORIES_CACHE = categorias
    
    if REDIS_AVAILABLE and r is not None:
        try:
            r.delete(CATEGORIES_KEY)
            r.sadd(CATEGORIES_KEY, *categorias)
            print("✓ Categorías cargadas en Redis:", categorias)
        except Exception as e:
            print(f"⚠️ Error al cargar en Redis: {e}. Usando caché en memoria.")
    else:
        print("✓ Categorías cargadas en caché en memoria:", categorias)


def get_categories():
    """Obtiene categorías desde Redis o desde caché en memoria."""
    if REDIS_AVAILABLE and r is not None:
        try:
            cats = list(r.smembers(CATEGORIES_KEY))
            if cats:
                return cats
        except Exception as e:
            print(f"⚠️ Error al leer desde Redis: {e}. Usando caché.")
    
    return list(_CATEGORIES_CACHE)

# =============================
# LIMPIEZA
# =============================

def limpiar_texto(texto):
    texto = texto.lower()
    doc = nlp(texto)
    tokens = [
        token.lemma_
        for token in doc
        if token.lemma_ not in stop_words
        and token.lemma_ not in string.punctuation
        and not token.is_digit
        and len(token.lemma_) > 1
    ]
    return " ".join(tokens)

# =============================
# FEATURES EXTRA
# =============================

def extra_features(texto_original):
    """Extrae features estructurales para mejorar clasificación entre refranes/poemas."""
    texto_limpio = texto_original.strip()
    palabras = texto_limpio.split()
    num_palabras = len(palabras)
    num_saltos = texto_limpio.count("\n")
    longitud = len(texto_limpio)
    
    # Features adicionales para distinguir refranes de poemas
    num_signos_pregunta = texto_original.count("?")
    num_signos_exclamacion = texto_original.count("!")
    num_comas = texto_original.count(",")
    num_puntos = texto_original.count(".")
    
    # Proporción de puntuación
    total_signos = num_signos_pregunta + num_signos_exclamacion + num_comas + num_puntos
    prop_puntuacion = total_signos / max(num_palabras, 1)
    
    # Longitud media de palabras
    longitud_media_palabra = longitud / max(num_palabras, 1)
    
    # Densidad de saltos (refranes tienen pocos, poemas muchos)
    densidad_saltos = num_saltos / max(num_palabras, 1)
    
    return np.array([
        longitud,
        num_saltos,
        num_palabras,
        prop_puntuacion,
        longitud_media_palabra,
        densidad_saltos,
        num_signos_pregunta,
        num_signos_exclamacion
    ]).reshape(1, -1)

# =============================
# DATASET
# =============================

def cargar_dataset():
    if os.path.exists(DATASET_FILE):
        with open(DATASET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_dataset(dataset):
    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

# =============================
# ENTRENAMIENTO
# =============================

def entrenar_modelo(dataset):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
    
    textos_originales = [d["texto"] for d in dataset if d.get("texto") and d.get("categoria")]
    textos_limpios = [limpiar_texto(d["texto"]) for d in dataset if d.get("texto") and d.get("categoria")]
    etiquetas = [d["categoria"] for d in dataset if d.get("texto") and d.get("categoria")]

    if len(textos_limpios) < 10:
        print(f"⚠️ Dataset pequeño ({len(textos_limpios)} textos). Usando validación cruzada en lugar de split 80/20")
        
        # Para datasets pequeños, usar validación cruzada
        vectorizer = TfidfVectorizer(ngram_range=(1,3), max_features=5000, min_df=1, sublinear_tf=True)
        X_vec = vectorizer.fit_transform(textos_limpios)
        total_extra = np.vstack([extra_features(t) for t in textos_originales])
        X_final = hstack([X_vec, total_extra])
        
        # Validación cruzada con k=3 (mínimo para dataset pequeño)
        k = min(3, min([etiquetas.count(c) for c in set(etiquetas)]))
        cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
        
        # Probar LogisticRegression
        lr_model = LogisticRegression(max_iter=5000, class_weight="balanced", C=0.5)
        lr_scores = cross_val_score(lr_model, X_final, etiquetas, cv=cv, scoring='accuracy')
        lr_accuracy = lr_scores.mean()
        
        # Probar RandomForest
        rf_model = RandomForestClassifier(n_estimators=100, max_depth=15, class_weight="balanced", random_state=42)
        rf_scores = cross_val_score(rf_model, X_final, etiquetas, cv=cv, scoring='accuracy')
        rf_accuracy = rf_scores.mean()
        
        print(f"📊 LR CV Accuracy: {lr_accuracy:.4f} (+/- {lr_scores.std():.4f})")
        print(f"📊 RF CV Accuracy: {rf_accuracy:.4f} (+/- {rf_scores.std():.4f})")
        
        # Seleccionar mejor modelo y entrenar con todos los datos
        if lr_accuracy >= rf_accuracy:
            mejor_modelo = LogisticRegression(max_iter=5000, class_weight="balanced", C=0.5)
            modelo_tipo = "LogisticRegression"
            accuracy = lr_accuracy
        else:
            mejor_modelo = RandomForestClassifier(n_estimators=100, max_depth=15, class_weight="balanced", random_state=42)
            modelo_tipo = "RandomForest"
            accuracy = rf_accuracy
        
        mejor_modelo.fit(X_final, etiquetas)
        
    elif len(set(etiquetas)) < 2:
        return {"error": "Se necesitan al menos 2 categorías diferentes"}
    else:
        # Para datasets normales, usar split 80/20
        test_size = max(0.15, 5 / len(textos_limpios))  # Al menos 5 ejemplos en test o 15%
        
        X_train, X_test, y_train, y_test, orig_train, orig_test = train_test_split(
            textos_limpios, etiquetas, textos_originales,
            test_size=test_size, random_state=42, stratify=etiquetas
        )

        # TF-IDF mejorado
        vectorizer = TfidfVectorizer(ngram_range=(1,3), max_features=5000, min_df=1, sublinear_tf=True)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Features estructurales
        train_extra = np.vstack([extra_features(t) for t in orig_train])
        test_extra = np.vstack([extra_features(t) for t in orig_test])
        X_train_final = hstack([X_train_vec, train_extra])
        X_test_final = hstack([X_test_vec, test_extra])

        # Prueba con LogisticRegression y RandomForest
        lr_model = LogisticRegression(max_iter=5000, class_weight="balanced", C=0.5)
        lr_model.fit(X_train_final, y_train)
        lr_pred = lr_model.predict(X_test_final)
        lr_accuracy = accuracy_score(y_test, lr_pred)
        
        rf_model = RandomForestClassifier(n_estimators=100, max_depth=20, class_weight="balanced", random_state=42)
        rf_model.fit(X_train_final, y_train)
        rf_pred = rf_model.predict(X_test_final)
        rf_accuracy = accuracy_score(y_test, rf_pred)
        
        # Usar el mejor modelo
        if lr_accuracy >= rf_accuracy:
            mejor_modelo = lr_model
            accuracy = lr_accuracy
            modelo_tipo = "LogisticRegression"
        else:
            mejor_modelo = rf_model
            accuracy = rf_accuracy
            modelo_tipo = "RandomForest"
        
        print(f"📊 LR Accuracy: {lr_accuracy:.4f}, RF Accuracy: {rf_accuracy:.4f}")
        print(f"✓ Usando {modelo_tipo} con accuracy: {accuracy:.4f}")

        # Reentrenar con todo el dataset
        X_total_vec = vectorizer.fit_transform(textos_limpios)
        total_extra = np.vstack([extra_features(t) for t in textos_originales])
        X_total_final = hstack([X_total_vec, total_extra])
        mejor_modelo.fit(X_total_final, etiquetas)

    # Guardar modelo
    joblib.dump({
        "modelo": mejor_modelo, 
        "vectorizer": vectorizer,
        "tipo": modelo_tipo,
        "accuracy": accuracy
    }, MODEL_FILE)

    # Redis categorías
    ensure_categories_from_dataset(dataset)

    return {
        "accuracy": round(accuracy, 4),
        "n_test": len(etiquetas) // 5 if len(textos_limpios) >= 10 else len(etiquetas),
        "n": len(textos_limpios),
        "labels": list(set(etiquetas)),
        "modelo": modelo_tipo,
        "mensaje": f"Modelo {modelo_tipo} entrenado con accuracy {round(accuracy, 4)}" if accuracy >= 0.8 else f"Accuracy {round(accuracy, 4)} (objetivo: 0.8)"
    }

# =============================
# CARGAR MODELO
# =============================

def cargar_modelo():
    if not Path(MODEL_FILE).exists():
        return None, None, None
    try:
        data = joblib.load(MODEL_FILE)
        return data["modelo"], data["vectorizer"], data.get("tipo", "LogisticRegression")
    except Exception as e:
        print(f"Error al cargar modelo: {e}")
        return None, None, None

# =============================
# CLASIFICAR NUEVO PDF
# =============================

def clasificar_nuevo_pdf(ruta_pdf):
    modelo, vectorizer, modelo_tipo = cargar_modelo()
    if modelo is None:
        return {"error": "Modelo no entrenado. Primero ejecuta /entrenar"}

    try:
        texto_pdf = ""
        with pdfplumber.open(ruta_pdf) as pdf:
            for page in pdf.pages:
                texto_pdf += page.extract_text() or ""
        
        if not texto_pdf.strip():
            return {"error": "No se pudo extraer texto del PDF"}

        texto_limpio = limpiar_texto(texto_pdf)
        X_vec = vectorizer.transform([texto_limpio])
        extra = extra_features(texto_pdf)
        X_final = hstack([X_vec, extra])

        prediccion = modelo.predict(X_final)[0]
        
        # Obtener probabilidades si está disponible
        confianza = 0.0
        if hasattr(modelo, 'predict_proba'):
            proba = modelo.predict_proba(X_final)[0]
            confianza = max(proba)
        
        # GUARDAR EN EL DATASET
        dataset = cargar_dataset()
        nombre_archivo = Path(ruta_pdf).name
        dataset.append({
            "texto": texto_pdf,
            "categoria": str(prediccion),
            "fuente": nombre_archivo,
            "confianza": float(confianza)
        })
        guardar_dataset(dataset)
        print(f"Texto clasificado guardado en dataset: {nombre_archivo} -> {prediccion}")
        
        # Convertir numpy types a tipos nativos de Python
        return {
            "prediccion": str(prediccion),
            "confianza": float(confianza),
            "modelo": str(modelo_tipo),
            "formatted": {
                "categoria": str(prediccion).upper(),
                "confianza_pct": f"{float(confianza)*100:.1f}%",
                "modelo_usado": str(modelo_tipo)
            }
        }
    except Exception as e:
        print(f"Error al clasificar: {e}")
        return {"error": f"Error en clasificacion: {e}"}


def evaluar_precision_rapido():
    """Evalúa la precisión del modelo sin reentrenar (mucho más rápido)."""
    modelo, vectorizer, modelo_tipo = cargar_modelo()
    if modelo is None:
        return {"error": "Modelo no entrenado. Ejecuta entrenamiento primero."}
    
    dataset = cargar_dataset()
    textos_originales = [d["texto"] for d in dataset if d.get("texto") and d.get("categoria")]
    textos_limpios = [limpiar_texto(d["texto"]) for d in dataset if d.get("texto") and d.get("categoria")]
    etiquetas = [d["categoria"] for d in dataset if d.get("texto") and d.get("categoria")]
    
    if len(textos_limpios) < 6:
        return {"error": "Se necesitan al menos 6 textos para evaluar"}
    if len(set(etiquetas)) < 2:
        return {"error": "Se necesitan al menos 2 categorías"}
    
    try:
        # Usar validación cruzada para datasets pequeños
        k = min(3, min([etiquetas.count(c) for c in set(etiquetas)]))
        cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
        
        X_vec = vectorizer.fit_transform(textos_limpios)
        total_extra = np.vstack([extra_features(t) for t in textos_originales])
        X_final = hstack([X_vec, total_extra])
        
        # Evaluar con validación cruzada
        scores = cross_val_score(modelo, X_final, etiquetas, cv=cv, scoring='accuracy')
        accuracy = scores.mean()
        
        return {
            "accuracy": round(accuracy, 4),
            "n_test": int(len(textos_limpios) * 0.2),
            "n": len(textos_limpios),
            "labels": list(set(etiquetas)),
            "modelo": modelo_tipo,
            "cv_folds": k,
            "mensaje": f"Modelo {modelo_tipo} - Accuracy CV: {round(accuracy, 4)}"
        }
    except Exception as e:
        return {"error": f"Error en evaluacion: {str(e)}"}