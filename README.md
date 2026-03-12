# Text Classifier NLP

[![Language](https://img.shields.io/badge/language-Python%203.10-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask%203.1.3-brightgreen.svg)](https://flask.palletsprojects.com/)
[![ML](https://img.shields.io/badge/ML-scikit--learn%201.3.0-orange.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/status-Estable-success.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Objetivos del proyecto](#objetivos-del-proyecto)
- [Características principales](#características-principales)
- [Arquitectura del sistema](#arquitectura-del-sistema)
- [Quick Start Guide](#quick-start-guide)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Fuente de datos](#fuente-de-datos)
- [Entrenamiento del modelo](#entrenamiento-del-modelo)
- [Visualizaciones](#visualizaciones)
- [Filtros o parámetros de interacción](#filtros-o-parámetros-de-interacción)
- [Autor](#autor)

---

## Descripción general

Este proyecto implementa un sistema de clasificación automática de textos en español a partir de documentos PDF, combinando técnicas de Procesamiento de Lenguaje Natural (NLP) y modelos de Machine Learning. El sistema expone una aplicación web basada en Flask que permite cargar documentos, clasificarlos en categorías literarias y técnicas, y mantener un dataset incremental para reentrenamiento.

Desde la perspectiva de negocio, la solución permite estandarizar y automatizar la categorización de textos (artículos, poemas, fábulas, resúmenes académicos, capítulos de tesis, textos técnicos de criptografía, entre otros), reduciendo el esfuerzo manual de revisión y mejorando la trazabilidad de los documentos procesados. La arquitectura está orientada a entornos académicos y empresariales que requieran experimentación controlada con modelos de clasificación de texto.

El sistema ofrece una interfaz web simple para usuarios finales, una API REST para integraciones y una capa de persistencia basada en archivos JSON, complementada con caché en Redis opcional para mejorar el rendimiento de lectura.

---

## Objetivos del proyecto

| # | Objetivo | Descripción |
|---:|:---------|:------------|
| 1 | Clasificar textos en español | Implementar un clasificador supervisado para asignar categorías a párrafos y documentos PDF. |
| 2 | Soportar flujo de carga de PDFs | Permitir que usuarios carguen documentos PDF, se extraiga su texto y se clasifique automáticamente. |
| 3 | Mantener un dataset incremental | Almacenar las clasificaciones realizadas en un dataset JSON reutilizable para reentrenamiento del modelo. |
| 4 | Proveer una interfaz web y API | Exponer un frontend HTML/JS y una API REST para consumo programático. |
| 5 | Facilitar experimentación académica | Servir como base para prácticas, análisis comparativos y extensión de modelos NLP/ML. |

---

## Características principales

- Clasificación automática de textos en español utilizando modelos entrenados con scikit-learn.
- Extracción de texto desde documentos PDF utilizando `pdfplumber`.
- Preprocesamiento de texto con NLTK y spaCy (tokenización, stopwords, lematización, features estructurales).
- Interfaz web en Flask para carga de archivos, visualización de resultados y métricas básicas.
- Persistencia de datos en archivos JSON (`dataset.json`, `model.joblib`) en la carpeta `data/`.
- API REST para consultar el dataset, clasificar nuevos documentos y obtener métricas del modelo.
- Uso opcional de Redis como caché de categorías y dataset para mejorar el rendimiento de lectura.

---

## Arquitectura del sistema

```text
+-----------------------------------------------------------+
|                    Capa de Presentación                   |
|  - Plantilla HTML (app/templates/index.html)              |
|  - CSS (app/static/css/style.css)                         |
|  - JavaScript ligero para actualización periódica         |
+-----------------------------------------------------------+
               |                         ^
               v                         |
+-----------------------------------------------------------+
|                Capa de Lógica / Aplicación                |
|  - Flask app (app/servicioClasificador.py)                |
|  - Rutas HTTP y API REST                                  |
|  - Coordinación de flujo: carga PDF → clasificar → guardar|
+-----------------------------------------------------------+
               |                         ^
               v                         |
+-----------------------------------------------------------+
|                Capa de Procesamiento NLP/ML               |
|  - Modelo ML (app/models/ModeloDeClasificacionTextos.py)  |
|  - Extracción de texto (pdfplumber)                       |
|  - Preprocesamiento (NLTK, spaCy)                         |
|  - Vectorización TF-IDF y features estructurales          |
|  - Clasificación con scikit-learn                         |
+-----------------------------------------------------------+
               |                         ^
               v                         |
+-----------------------------------------------------------+
|                        Capa de Datos                      |
|  - Archivos JSON (data/dataset.json)                      |
|  - Modelo serializado (data/model.joblib)                 |
|  - Caché Redis opcional (app/services/redis_store.py)     |
+-----------------------------------------------------------+
```

---

## Quick Start Guide

### Prerrequisitos

- Python 3.10
- pip
- (Opcional) Redis en ejecución local (`redis://localhost:6379/0`)

### Clonar o descargar el proyecto

Si el código está en un repositorio remoto, descargarlo o clonarlo en un directorio local.

```bash
# Ejemplo genérico (no requiere git obligatoriamente)
# Opción 1: Clonar si existe un repositorio remoto
# git clone <url-del-repositorio>
# cd text-classifier-nlp

# Opción 2: Descargar como ZIP y descomprimir
# cd ruta/donde/descomprimió/text-classifier-nlp
```

### Crear entorno virtual

#### macOS / Linux (bash/zsh)

```bash
cd text-classifier-nlp
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows CMD

```cmd
cd text-classifier-nlp
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

#### Windows PowerShell

```powershell
cd text-classifier-nlp
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalación de dependencias

Si existe un archivo `requirements.txt` en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

Tabla de paquetes principales:

| Paquete      | Versión mínima | Propósito                                   |
|:-------------|:---------------|:--------------------------------------------|
| Flask        | 3.1.3          | Framework web y API REST                    |
| scikit-learn | 1.3.0          | Modelos de Machine Learning                 |
| spaCy        | 3.7            | Procesamiento de lenguaje natural en español|
| nltk         | 3.8            | Tokenización y stopwords                    |
| pdfplumber   | 0.10           | Extracción de texto desde archivos PDF      |
| joblib       | 1.3            | Serialización de modelos                    |
| redis        | 5.0            | Cliente Redis (caché opcional)             |

Además, es necesario instalar el modelo de spaCy para español si aún no está instalado:

```bash
python -m spacy download es_core_news_sm
```

### Verificación de archivos necesarios

- `app/servicioClasificador.py` (servidor Flask)
- `app/models/ModeloDeClasificacionTextos.py` (modelo y pipeline ML/NLP)
- `app/services/redis_store.py` (capa de caché opcional)
- `app/templates/index.html` (plantilla principal)
- `app/static/css/style.css` (estilos)
- `data/dataset.json` (dataset de textos, si ya existe)
- `data/model.joblib` (modelo entrenado, si ya existe)

### Ejecución de la aplicación

Con el entorno virtual activado:

#### Opción 1: Ejecutar con módulo Flask

```bash
python -m flask -A app.servicioClasificador run --host 127.0.0.1 --port 5000
```

#### Opción 2: Ejecutar directamente el script (si definido en `__main__`)

```bash
python app/servicioClasificador.py
```

### URL de acceso

Una vez que el servidor esté en ejecución, acceder mediante navegador a:

- `http://127.0.0.1:5000`

### Comando rápido en una línea por sistema operativo

- macOS / Linux:

```bash
cd text-classifier-nlp && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python -m flask -A app.servicioClasificador run --host 127.0.0.1 --port 5000
```

- Windows CMD:

```cmd
cd text-classifier-nlp && py -3 -m venv .venv && .venv\Scripts\activate.bat && pip install -r requirements.txt && py -3 -m flask -A app.servicioClasificador run --host 127.0.0.1 --port 5000
```

- Windows PowerShell:

```powershell
cd text-classifier-nlp; py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; py -3 -m flask -A app.servicioClasificador run --host 127.0.0.1 --port 5000
```

---

## Estructura del proyecto

```text
text-classifier-nlp/
├─ app/
│  ├─ __init__.py
│  ├─ servicioClasificador.py        # Punto de entrada Flask, rutas y API
│  ├─ models/
│  │  ├─ __init__.py
│  │  └─ ModeloDeClasificacionTextos.py  # Lógica MLM/NLP y entrenamiento
│  ├─ services/
│  │  ├─ __init__.py
│  │  └─ redis_store.py              # Manejo de caché Redis (opcional)
│  ├─ templates/
│  │  └─ index.html                  # Interfaz web principal
│  └─ static/
│     └─ css/
│        └─ style.css                # Estilos CSS
├─ data/
│  ├─ dataset.json                   # Dataset de textos y etiquetas
│  └─ model.joblib                   # Modelo entrenado serializado
├─ src/
│  └─ main.py                        # Scripts de experimentación y utilidades
├─ requirements.txt
├─ README.md
└─ LICENSE (opcional)
```

---

## Fuente de datos

El sistema utiliza un dataset local en formato JSON para almacenar los textos y sus categorías asignadas. Este dataset puede crecer dinámicamente a medida que se clasifican nuevos documentos desde la interfaz web.

### Metadatos del dataset principal

| Elemento         | Valor                                   |
|:-----------------|:----------------------------------------|
| Archivo          | `data/dataset.json`                     |
| Formato          | JSON                                    |
| Idioma           | Español                                 |
| Origen           | Documentos PDF cargados y textos base   |
| Naturaleza       | Académica / demostrativa                |
| Sensibilidad     | Depende del contenido aportado por el usuario |

### Estructura lógica del dataset (ejemplo)

| Campo        | Tipo    | Descripción                                    |
|:-------------|:--------|:-----------------------------------------------|
| texto        | string  | Contenido textual del párrafo o documento      |
| categoria    | string  | Etiqueta asignada (poema, articulo, fabula, etc.) |
| fuente       | string  | Nombre del archivo PDF u origen                |
| confianza    | number  | Probabilidad o score de la predicción (0-1)    |

### Pipeline de limpieza y preparación

1. Extracción de texto desde PDF utilizando `pdfplumber`.
2. Normalización de texto (lowercase, eliminación de caracteres no deseados).
3. Tokenización y eliminación de stopwords en español (NLTK).
4. Opcional: lematización mediante modelo `es_core_news_sm` de spaCy.
5. Cálculo de features: TF-IDF y features estructurales (longitud, presencia de signos, etc.).
6. Entrenamiento y actualización de modelo con scikit-learn.

---

## Entrenamiento del modelo

El entrenamiento del modelo de clasificación se realiza de forma supervisada a partir del dataset almacenado en `data/dataset.json`. De manera resumida, el pipeline es el siguiente:

1. **Carga del dataset**  
   - Se leen todos los registros de `data/dataset.json`, obteniendo pares `(texto, categoria)`.
   - Se filtran entradas vacías o con etiquetas inválidas.

2. **Preprocesamiento de texto**  
   - Conversión a minúsculas y limpieza básica de caracteres especiales.
   - Tokenización y eliminación de stopwords en español con NLTK.
   - Opcionalmente, lematización utilizando el modelo `es_core_news_sm` de spaCy.

3. **Extracción de características**  
   - Vectorización del texto con **TF-IDF** para representar cada documento como un vector numérico.
   - Cálculo de **features estructurales** adicionales (por ejemplo, longitud del texto, cantidad de signos de puntuación, presencia de ciertos patrones, etc.).
   - Concatenación de todas las características en una única matriz de entrenamiento.

4. **Entrenamiento del clasificador**  
   - Uso de un modelo de **clasificación lineal** de scikit-learn (por ejemplo, `LogisticRegression`).
   - Entrenamiento del modelo con el conjunto de entrenamiento completo.
   - Validación mediante **validación cruzada K-fold** (por ejemplo, `K=5`) para estimar la capacidad de generalización del modelo.

5. **Evaluación y métricas internas**  
   - Cálculo de métricas estándar (accuracy y otras métricas internas) sobre las particiones de validación.
   - En experimentos realizados, se ha obtenido una precisión aproximada del **87.5%** sobre el conjunto de datos disponible.

6. **Serialización del modelo**  
   - Una vez entrenado y validado, el modelo se guarda en disco utilizando `joblib` en `data/model.joblib`.
   - El servicio Flask carga este archivo al iniciar, de manera que no es necesario entrenar en cada ejecución.

7. **Reentrenamiento**  
   - Cuando se añaden nuevos textos etiquetados al dataset (por ejemplo, tras la revisión manual de clasificaciones), puede dispararse un proceso de reentrenamiento que repite los pasos anteriores para actualizar el modelo.

---

## Visualizaciones

La interfaz web presenta tablas y resúmenes de la información procesada. Se pueden añadir visualizaciones adicionales en el frontend si se requiere.

| Gráfico           | Tipo         | Variables                      | Propósito |
|:------------------|:-------------|:-------------------------------|:---------|
| Tabla de dataset  | Tabla HTML   | texto, categoria, fuente       | Inspeccionar rápidamente las entradas del dataset. |
| Resumen de métricas | Texto/tablas | accuracy, tamaño de dataset   | Comunicar el rendimiento del modelo y el volumen de datos. |

---

## Filtros o parámetros de interacción

- Selección de archivo PDF a través del formulario de carga en la interfaz web.
- Actualización periódica del dataset mostrado mediante peticiones AJAX a la API.
- Potencial inclusión de filtros en la interfaz (por categoría o por fuente) si se amplía el frontend.

---

## Autor

| Nombre                         | Rol                                |
|:-------------------------------|:-----------------------------------|
| Nicolás Daniel Rojas Baracaldo | Desarrollador / Autor del proyecto |
