#!/usr/bin/env python3
"""Genera PDFs de prueba mejorados para cada categoría."""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY

# Contenido para cada PDF
contenidos = {
    "articulo": """<b>La Inteligencia Artificial en el Mundo Moderno</b><br/><br/>
    La inteligencia artificial (IA) representa uno de los mayores avances tecnológicos del siglo XXI. 
    Se define como la rama de la informática que estudia la creación de máquinas inteligentes capaces 
    de realizar tareas que típicamente requieren inteligencia humana. Las aplicaciones de la IA son 
    cada vez más comunes en nuestra vida diaria, desde asistentes virtuales hasta sistemas de 
    recomendación en plataformas de streaming. Los expertos predicen que la IA seguirá transformando 
    industrias enteras en los próximos años. Sin embargo, esto también plantea preguntas importantes 
    sobre ética, privacidad y el futuro del empleo. Es fundamental que la sociedad desarrolle 
    regulaciones apropiadas para garantizar que la IA se use responsablemente.""",
    
    "refran": """Más vale tarde que nunca""",
    
    "poema": """Bajo la luna plateada,
    danza el viento en la noche,
    susurra historias olvidadas,
    de amores que el tiempo derroche.
    <br/>
    Las estrellas titilan,
    testigos del silencio profundo,
    mientras sombras se deslizan,
    en el velo del mundo.
    <br/>
    Y en la quietud del cielo,
    se encuentra la verdad,
    donde vuela el espíritu liviano,
    en búsqueda de eternidad.""",
    
    "fabula": """El Cuervo y la Jarra: Un cuervo sediento buscaba agua desesperadamente. 
    Finalmente encontró una jarra con agua, pero esta era tan profunda que su pico no alcanzaba. 
    Frustrado, el cuervo reunió pequeñas piedras y las fue dejando caer una a una dentro de la jarra. 
    Lentamente, el nivel del agua subió hasta que finalmente pudo beber y saciar su sed. 
    La moraleja de esta historia es que la persistencia, la paciencia y el ingenio pueden superar 
    cualquier obstáculo, sin importar cuán imposible parezca a primera vista. Incluso los problemas 
    más grandes pueden resolverse si pensamos creativamente.""",
    
    "romance": """Mi amor por ti es infinito, como el océano sin horizonte.
    Cada latido de mi corazón grita tu nombre.
    En tus ojos encuentro mi cielo, mi paz eterna.
    Te amo con la fuerza de mil soles ardientes.
    Sin ti, las noches son eternas y los días sin color.
    Eres mi razón de existir, mi verdadero destino.
    Quiero envejecer contigo, mano en mano, corazón con corazón.
    Mi amor es tuyo, completamente tuyo, por siempre jamás."""
}

# Crear PDFs
styles = getSampleStyleSheet()
custom_style = ParagraphStyle(
    'CustomStyle',
    parent=styles['BodyText'],
    fontSize=12,
    leading=16,
    alignment=TA_JUSTIFY
)

for categoria, contenido in contenidos.items():
    doc = SimpleDocTemplate(f"uploads/prueba_{categoria}.pdf", pagesize=letter)
    story = []
    
    p = Paragraph(contenido, custom_style)
    story.append(p)
    story.append(Spacer(1, 0.5*inch))
    
    doc.build(story)
    print(f"✓ Creado: uploads/prueba_{categoria}.pdf")

print("\n✓ PDFs de prueba mejorados generados")
