#!/usr/bin/env python3
"""Script para generar PDFs de prueba para cada categoría"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY
import os

OUTPUT_DIR = "uploads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Textos de prueba para cada categoría
TEXTOS = {
    "articulo": """
    La Inteligencia Artificial en el Siglo XXI
    
    La inteligencia artificial (IA) se ha convertido en una de las tecnologías más transformadoras de nuestro tiempo. 
    Desde aplicaciones en medicina hasta vehículos autónomos, la IA está redefiniendo cómo vivimos y trabajamos.
    
    La historia de la IA comienza en los años 1950, cuando científicos como Alan Turing se preguntaban si las máquinas 
    podían pensar. Hoy en día, los algoritmos de aprendizaje automático procesan millones de datos para identificar 
    patrones complejos que los humanos no pueden detectar a simple vista.
    
    Las redes neuronales profundas han revolucionado campos como la visión por computadora y el procesamiento del 
    lenguaje natural. Empresas tecnológicas invierten miles de millones en investigación de IA, sabiendo que será 
    fundamental para el futuro competitivo.
    
    Sin embargo, el crecimiento de la IA también plantea desafíos éticos importantes. ¿Cómo aseguramos que los sistemas 
    de IA sean justos y transparentes? ¿Quién es responsable cuando una IA comete errores? Estas preguntas requieren 
    soluciones multidisciplinarias que involucren tecnólogos, filósofos y legisladores.
    """,
    
    "refran": """
    Más vale tarde que nunca.
    """,
    
    "poema": """
    Atardecer de Fuego
    
    Cuando el sol se va cayendo,
    Y tiñe el cielo de rojo,
    Las nubes danzan en el cielo,
    Como bailarines sin fin.
    
    El horizonte se incendia,
    De colores imposibles,
    Naranjas, rojos, púrpuras,
    Que el corazón hace imposibles.
    
    La brisa trae aromas de la tierra,
    Mientras los pájaros regresan a casa,
    La noche llega lentamente,
    Y las estrellas comienzan a brillar.
    
    En este momento de quietud,
    El alma encuentra su paz,
    Bajo el cielo que se desvanece,
    En la eternidad del atardecer.
    """,
    
    "fabula": """
    El Águila y la Gallina
    
    Un águila majestuosa sobrevolaba el corral de una granja. Al ver a una gallina arañando la tierra, 
    le dijo: "¿Por qué desperdicias tu vida en el suelo cuando fuiste hecha para volar?"
    
    La gallina respondió: "Tengo responsabilidades aquí. Debo alimentar a mis polluelos y cuidar del corral."
    
    El águila se burló y se fue volando hacia las montañas. Meses después, hambrienta y sola en las montañas, 
    el águila tuvo que pedir ayuda a la gallina. La gallina le ofreció comida sin reproches.
    
    El águila aprendió que la verdadera grandeza no está en dónde vives, sino en quién eres y cómo cuidas 
    de los demás. La gallina demostró que el sacrificio y la responsabilidad son formas de nobleza.
    
    Moraleja: No desprecies los actos cotidianos de bondad, pues contienen una grandeza que supera toda ambición.
    """,
    
    "romance": """
    Amor Infinito
    
    Desde el primer momento en que vi tus ojos, supe que mi vida había cambiado para siempre. 
    Tu sonrisa es el amanecer que ilumina mis días más oscuros.
    
    Cada latido de mi corazón susurra tu nombre. Eres la razón por la cual despierto cada mañana 
    con esperanza y alegría. Tu presencia transforma el mundo en un lugar más bello.
    
    Te amo con una intensidad que desafía las palabras. Mi amor por ti es como el océano: 
    profundo, infinito e incontenible. Cada día te quiero más que el anterior.
    
    Bajo las estrellas te prometo amor eterno. Juntos construiremos un futuro lleno de sueños compartidos. 
    Eres mi alma gemela, mi complemento perfecto, mi razón de ser.
    
    Te amaré hasta el fin de los tiempos, en esta vida y en todas las vidas por venir.
    """
}

def crear_pdf(categoria, texto):
    """Crea un PDF para la categoría dada"""
    filename = f"{OUTPUT_DIR}/prueba_{categoria}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilo personalizado
    estilo = ParagraphStyle(
        'Custom',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Crear contenido
    content = []
    title = Paragraph(f"<b>Ejemplo: {categoria.upper()}</b>", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 0.3*inch))
    
    for linea in texto.strip().split('\n'):
        if linea.strip():
            content.append(Paragraph(linea.strip(), estilo))
    
    # Generar PDF
    doc.build(content)
    print(f"✓ PDF generado: {filename}")

if __name__ == "__main__":
    print("Generando PDFs de prueba...\n")
    for categoria, texto in TEXTOS.items():
        crear_pdf(categoria, texto)
    print(f"\n✓ Se han generado {len(TEXTOS)} PDFs en la carpeta '{OUTPUT_DIR}'")
