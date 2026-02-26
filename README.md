# Clasificador de Textos NLP

Sistema de clasificación automática de textos en español usando Machine Learning y procesamiento de lenguaje natural (NLP).

## Características

- **Clasificación automática de PDFs** en 5 categorías: artículo, refrán, poema, fábula y romance
- **Precisión del modelo**: 87.5% (validación cruzada)
- **Interfaz web** con actualización en tiempo real
- **API REST** para integración con otros sistemas
- **Procesamiento NLP** con lemmatización usando spaCy
- **Features estructurales**: análisis de longitud, puntuación, saltos de línea, etc.

## Tecnologías

- **Backend**: Flask 3.1.3
- **ML**: scikit-learn (LogisticRegression, TF-IDF)
- **NLP**: spaCy (es_core_news_sm)
- **Extracción PDF**: pdfplumber
- **Caché**: Redis (con fallback in-memory)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd text-classifier-nlp
```

2. Crear y activar entorno virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

4. (Opcional) Instalar y configurar Redis:
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
```

## Uso

1. Entrenar el modelo (primera vez):
```bash
python -m flask -A app.servicioClasificador run
```
Luego acceder a `http://127.0.0.1:5000` y hacer clic en "Entrenar Modelo"

2. Clasificar PDFs:
- Subir un PDF mediante la interfaz web
- El sistema clasificará automáticamente el texto
- Los resultados se guardan en el dataset para reentrenamiento

## Estructura del Proyecto

```
text-classifier-nlp/
├── app/
│   ├── models/
│   │   └── ModeloDeClasificacionTextos.py  # Lógica ML
│   ├── services/
│   │   └── redis_store.py                  # Cache Redis
│   ├── static/
│   │   └── css/
│   │       └── style.css                   # Estilos
│   ├── templates/
│   │   └── index.html                      # Interfaz web
│   └── servicioClasificador.py             # API Flask
├── data/
│   └── dataset.json                        # Dataset de entrenamiento
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /` - Interfaz web principal
- `POST /clasificar` - Clasificar un PDF
- `GET /entrenar` - Entrenar/reentrenar el modelo
- `GET /precision` - Evaluar precisión del modelo
- `GET /api/dataset` - Obtener dataset (JSON)
- `GET /api/metricas` - Obtener métricas del modelo (JSON)

## Modelo

El modelo utiliza:
- **TF-IDF** con n-gramas (1-3), 5000 features max, sublinear_tf
- **8 features estructurales**: longitud de texto, número de palabras, densidad de puntuación, etc.
- **Lemmatización** con spaCy para español
- **LogisticRegression** con cross-validation estratificada

### Métricas
- Accuracy: 87.5% (validación cruzada)
- Dataset: 40+ textos etiquetados
- K-Folds: 3 (estratificado)

## Desarrollo

Para ejecutar en modo desarrollo:
```bash
python -m flask -A app.servicioClasificador run --debug
```

## Licencia

Este proyecto fue desarrollado como parte de un proyecto universitario de NLP.

## Autor

Nicolas Garcia - 2026
