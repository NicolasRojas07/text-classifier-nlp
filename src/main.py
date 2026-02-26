import pdfplumber
import nltk
import string
import re
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


texto_completo = ""

dataset = []

with pdfplumber.open("RicoGarciaMiguelAngel2025.pdf") as pdf:
    for page in pdf.pages:
        texto_completo += page.extract_text() + "\n"

parrafos = re.split(r"\n\d+\.\s", texto_completo)
parrafos = [p.strip() for p in parrafos if len(p.strip()) > 30]

print(f"\nProcesando PDF: RicoGarciaMiguelAngel2025.pdf")
print(f"Total de párrafos extraídos: {len(parrafos)}\n")

stop_words = set(stopwords.words('spanish'))

def limpiar_texto(texto):
    texto = texto.lower()
    tokens = word_tokenize(texto,language="spanish")
    tokens = [
        t for t in tokens
        if t not in stop_words and t not in string.punctuation
    ]
    return tokens


def verificar_caracteristicas(texto):
    tokens = limpiar_texto(texto)
    texto_lower = texto.lower()
    
    palabras_romanticas = ["amor", "corazón", "beso", "pasión", "te amo", "te quiero"]
    palabras_noticia = ["anunció", "declaró", "informó", "según", "reveló", "confirmó"]
    palabras_cuento = ["érase", "había una vez", "moraleja", "enseña", "cierta vez"]
    palabras_academicas = ["investigación", "estudio", "análisis", "según", "datos", "resultado", "metodología", "conclusión"]
    
    palabras_tecnicas_crypto = ["encriptación", "cifrado", "criptografía", "cuántico", "caótico", "algoritmo", "seguridad", 
                                "desencriptación", "descifrado", "llave", "difusión", "confusión", "permutación"]
    palabras_matematicas = ["ecuación", "matriz", "función", "sistema", "parámetro", "valor", "cálculo", "operación",
                           "vector", "logarítmico", "iteración", "transformación"]
    palabras_investigacion = ["propuesto", "implementación", "resultados", "métricas", "evaluación", "comparación", "esquema",
                             "modelo", "pruebas", "simulación", "experimental"]
    palabras_capitulo = ["capítulo", "sección", "apartado", "introducción", "conclusión", "referencias", "bibliografía"]
    
    palabras_quantum = ["qubit", "qiskit", "compuerta", "circuito cuántico", "superposición", "entrelazamiento",
                       "cnot", "swap", "hadamard", "quantum"]
    
    palabras_chaos = ["caótico", "atractor", "lorenz", "logístico", "hipercaótico", "sensibilidad", "condiciones iniciales",
                     "secuencia", "aleatoriedad"]
    
    palabras_imagen = ["imagen", "pixel", "rgb", "escala de grises", "histograma", "correlación", "entropía"]
    
    tiene_ecuaciones = bool(re.search(r'[a-z]\s*=\s*[a-z0-9]|ecuación|fórmula|expresión\s+\d+', texto_lower))
    tiene_figuras = bool(re.search(r'figura\s+\d+|tabla\s+\d+|gráfico', texto_lower))
    tiene_referencias = bool(re.search(r'\(\d{4}\)|\[\d+\]|et\s+al\.|nota\.\s+fuente', texto_lower))
    tiene_porcentajes = bool(re.search(r'\d+\s*%|porcentaje', texto))
    tiene_citas = bool(re.search(r'\(.*?,\s*\d{4}\)', texto))
    tiene_metricas = bool(re.search(r'npcr|uaci|psnr|mse|entropía', texto_lower))
    
    return {
        "longitud_texto": len(texto),
        "num_palabras": len(tokens),
        "tiene_pregunta": "?" in texto,
        "num_preguntas": texto.count("?"),
        "tiene_dialogo": "—" in texto or '"' in texto,
        "empieza_como_acertijo": texto_lower.startswith(("es", "qué es", "qué cosa", "tiene")),
        "tiene_parentesis_respuesta": "respuesta:" in texto_lower,
        "palabra_romantica": any(palabra in texto_lower for palabra in palabras_romanticas),
        "palabra_noticia": any(palabra in texto_lower for palabra in palabras_noticia),
        "palabra_cuento": any(palabra in texto_lower for palabra in palabras_cuento),
        "palabra_academica": any(palabra in texto_lower for palabra in palabras_academicas),
        "tiene_moraleja": "moraleja" in texto_lower,
        "tiene_saltos_linea": texto.count("\n"),
        "tiene_fechas": bool(re.search(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', texto)),
        "tiene_numeros": bool(re.search(r'\d+', texto)),
        "promedio_palabras_por_linea": len(tokens) / max(texto.count("\n"), 1),
        "palabra_tecnica_crypto": any(palabra in texto_lower for palabra in palabras_tecnicas_crypto),
        "palabra_matematica": any(palabra in texto_lower for palabra in palabras_matematicas),
        "palabra_investigacion": any(palabra in texto_lower for palabra in palabras_investigacion),
        "palabra_capitulo": any(palabra in texto_lower for palabra in palabras_capitulo),
        "palabra_quantum": any(palabra in texto_lower for palabra in palabras_quantum),
        "palabra_chaos": any(palabra in texto_lower for palabra in palabras_chaos),
        "palabra_imagen": any(palabra in texto_lower for palabra in palabras_imagen),
        "tiene_ecuaciones": tiene_ecuaciones,
        "tiene_figuras": tiene_figuras,
        "tiene_referencias": tiene_referencias,
        "tiene_porcentajes": tiene_porcentajes,
        "tiene_citas": tiene_citas,
        "tiene_metricas": tiene_metricas
    }


def clasificacion_por_reglas(texto, caracteriticas):
    
    if (caracteriticas["empieza_como_acertijo"] and 
        caracteriticas["tiene_pregunta"] and 
        caracteriticas["num_palabras"] < 30):
        return "acertijo"
    
    if (caracteriticas["tiene_pregunta"] and 
        caracteriticas["tiene_parentesis_respuesta"] and 
        caracteriticas["num_palabras"] < 40):
        return "acertijo"
    
    if (caracteriticas["tiene_moraleja"] or 
        (caracteriticas["palabra_cuento"] and caracteriticas["tiene_dialogo"] and 
         caracteriticas["num_palabras"] > 80)):
        return "fabula"
    
    if (caracteriticas["palabra_quantum"] and 
        caracteriticas["palabra_tecnica_crypto"] and
        caracteriticas["num_palabras"] > 80):
        return "criptografia_cuantica"
    
    if (caracteriticas["palabra_chaos"] and 
        (caracteriticas["palabra_tecnica_crypto"] or caracteriticas["palabra_imagen"]) and
        caracteriticas["num_palabras"] > 60):
        return "sistemas_caoticos_crypto"
    
    if (caracteriticas["tiene_metricas"] and 
        (caracteriticas["tiene_porcentajes"] or caracteriticas["tiene_figuras"]) and
        caracteriticas["num_palabras"] > 50):
        return "analisis_metricas_seguridad"
    
    if (caracteriticas["palabra_tecnica_crypto"] and 
        (caracteriticas["palabra_matematica"] or caracteriticas["tiene_ecuaciones"]) and
        caracteriticas["num_palabras"] > 100):
        return "articulo_tecnico_criptografia"
    
    if (caracteriticas["palabra_investigacion"] and 
        caracteriticas["num_palabras"] > 80 and
        (caracteriticas["tiene_figuras"] or caracteriticas["palabra_matematica"])):
        return "metodologia_investigacion"
    
    if (caracteriticas["palabra_academica"] and 
        (caracteriticas["tiene_porcentajes"] or caracteriticas["tiene_ecuaciones"]) and
        caracteriticas["num_palabras"] > 60 and
        caracteriticas["num_palabras"] < 200):
        return "resumen_academico"
    
    if (caracteriticas["palabra_capitulo"] or
        (caracteriticas["tiene_referencias"] and caracteriticas["tiene_citas"]) and
        caracteriticas["num_palabras"] > 50):
        return "capitulo_tesis"
    
    if (caracteriticas["palabra_matematica"] and 
        caracteriticas["tiene_ecuaciones"] and
        caracteriticas["num_palabras"] > 40):
        return "texto_matematico"
    
    if (caracteriticas["palabra_imagen"] and 
        (caracteriticas["palabra_matematica"] or caracteriticas["tiene_ecuaciones"]) and
        caracteriticas["num_palabras"] > 50):
        return "procesamiento_imagenes"
    
    if ((caracteriticas["palabra_tecnica_crypto"] or 
         caracteriticas["palabra_matematica"] or 
         caracteriticas["palabra_imagen"]) and
        caracteriticas["num_palabras"] > 40):
        return "texto_tecnico"
    
    if (caracteriticas["num_palabras"] > 100 and 
        (caracteriticas["palabra_noticia"] or caracteriticas["tiene_fechas"] or 
         caracteriticas["palabra_academica"]) and 
        not caracteriticas["tiene_pregunta"]):
        return "articulo"
    
    if (caracteriticas["tiene_saltos_linea"] > 4 and 
        caracteriticas["promedio_palabras_por_linea"] < 10 and 
        caracteriticas["num_palabras"] < 150 and
        not caracteriticas["palabra_tecnica_crypto"] and
        not caracteriticas["palabra_matematica"] and
        not caracteriticas["palabra_imagen"]):
        return "poema"
    
    if (caracteriticas["palabra_romantica"] and 
        caracteriticas["num_palabras"] < 50):
        return "romance"
    
    if caracteriticas["num_palabras"] < 20 and caracteriticas["tiene_pregunta"]:
        return "refran"
    
    if (caracteriticas["palabra_cuento"] and 
        caracteriticas["num_palabras"] > 50 and 
        caracteriticas["num_palabras"] < 150):
        return "cuento"
    
    if (caracteriticas["palabra_noticia"] and 
        caracteriticas["tiene_fechas"] and 
        caracteriticas["num_palabras"] > 50):
        return "noticia"

    return "desconocido"


def mostrar_dataset_estilizado(dataset):
    print("\n" + "="*100)
    print(" "*35 + "DATASET DE CLASIFICACION DE TEXTOS")
    print("="*100 + "\n")
    
    conteo_etiquetas = {}
    for _, etiqueta in dataset:
        conteo_etiquetas[etiqueta] = conteo_etiquetas.get(etiqueta, 0) + 1
    
    print(f"Total de textos clasificados: {len(dataset)}")
    print(f"Tipos de textos encontrados: {len(conteo_etiquetas)}")
    print("\n" + "-"*100)
    print("DISTRIBUCION POR CATEGORIA:")
    print("-"*100)
    
    for etiqueta, cantidad in sorted(conteo_etiquetas.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (cantidad / len(dataset)) * 100
        barra = "#" * int(porcentaje / 2)
        print(f"  {etiqueta.upper():.<40} {cantidad:>3} textos ({porcentaje:>5.1f}%) {barra}")
    
    print("\n" + "-"*100)
    print("DETALLE DE TEXTOS CLASIFICADOS:")
    print("-"*100 + "\n")
    
    for idx, (caracteristicas, etiqueta) in enumerate(dataset, 1):
        print(f"Texto #{idx} - Categoria: {etiqueta.upper().replace('_', ' ')}")
        print(f"   Palabras: {caracteristicas['num_palabras']}")
        print(f"   Longitud: {caracteristicas['longitud_texto']} caracteres")
        
        caracteristicas_activas = []
        if caracteristicas.get('tiene_pregunta'):
            caracteristicas_activas.append(f"{caracteristicas['num_preguntas']} pregunta(s)")
        if caracteristicas.get('tiene_dialogo'):
            caracteristicas_activas.append("Dialogo")
        if caracteristicas.get('tiene_moraleja'):
            caracteristicas_activas.append("Moraleja")
        if caracteristicas.get('tiene_ecuaciones'):
            caracteristicas_activas.append("Ecuaciones")
        if caracteristicas.get('tiene_figuras'):
            caracteristicas_activas.append("Figuras/Tablas")
        if caracteristicas.get('tiene_referencias'):
            caracteristicas_activas.append("Referencias")
        if caracteristicas.get('palabra_tecnica_crypto'):
            caracteristicas_activas.append("Terminos cripto")
        if caracteristicas.get('palabra_matematica'):
            caracteristicas_activas.append("Terminos matematicos")
        if caracteristicas.get('palabra_quantum'):
            caracteristicas_activas.append("Computacion cuantica")
        if caracteristicas.get('palabra_chaos'):
            caracteristicas_activas.append("Sistemas caoticos")
        if caracteristicas.get('palabra_imagen'):
            caracteristicas_activas.append("Procesamiento de imagenes")
        if caracteristicas.get('tiene_metricas'):
            caracteristicas_activas.append("Metricas de seguridad")
        
        if caracteristicas_activas:
            print(f"   Caracteristicas: {', '.join(caracteristicas_activas)}")
        else:
            print(f"   Sin caracteristicas especiales")
        print()
    
    print("="*100 + "\n")


for p in parrafos:
    caracteriticas = verificar_caracteristicas(p)
    etiqueta = clasificacion_por_reglas(p, caracteriticas)

    if etiqueta != "desconocido":
        dataset.append((caracteriticas, etiqueta))

mostrar_dataset_estilizado(dataset)