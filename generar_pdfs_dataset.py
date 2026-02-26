#!/usr/bin/env python3
"""Script para generar PDFs de prueba y crear un dataset limpio desde cero"""

import json
import os

# Dataset limpio con párrafos de calidad para cada categoría
dataset_nuevo = [
    # ARTÍCULOS
    {
        "texto": "La Inteligencia Artificial y su Impacto en la Sociedad Moderna. La inteligencia artificial ha revolucionado fundamentalmente la forma en que vivimos, trabajamos e interactuamos. Desde los sistemas de recomendación en redes sociales hasta los vehículos autónomos, la IA está transformando cada aspecto de nuestra sociedad. Los algoritmos de machine learning permiten que las máquinas aprendan patrones de datos sin ser programadas explícitamente. Este avance tecnológico ha generado tanto oportunidades como desafíos éticos que la sociedad debe enfrentar.",
        "categoria": "articulo"
    },
    {
        "texto": "El Cambio Climático: Una Amenaza Global. El cambio climático es uno de los desafíos más importantes del siglo XXI. La temperatura global ha aumentado aproximadamente 1.1 grados Celsius desde la era preindustrial. Las actividades humanas, especialmente la quema de combustibles fósiles, son la causa principal del calentamiento global. Es necesario implementar políticas de reducción de emisiones de carbono en todos los países para mitigar los efectos devastadores.",
        "categoria": "articulo"
    },
    {
        "texto": "La Transformación Digital en las Empresas. La transformación digital es esencial para la competitividad empresarial en el mundo moderno. Las empresas deben adoptar nuevas tecnologías para mejorar su eficiencia operacional y ofrecer mejores servicios a los clientes. El comercio electrónico ha experimentado un crecimiento exponencial, transformando la forma en que compramos y vendemos productos. La logística y distribución son aspectos críticos para el éxito en esta era digital.",
        "categoria": "articulo"
    },
    {
        "texto": "La Educación en Línea: Oportunidades y Desafíos. La educación en línea se ha convertido en una alternativa importante a la educación presencial. Plataformas como Coursera, Udemy y edX ofrecen cursos en diversas disciplinas para millones de estudiantes alrededor del mundo. La accesibilidad y flexibilidad de la educación en línea permite que personas de diferentes contextos accedan a conocimiento de calidad. Sin embargo, la brecha digital sigue siendo un obstáculo importante para muchas comunidades.",
        "categoria": "articulo"
    },
    
    # REFRANES
    {
        "texto": "Más vale tarde que nunca.",
        "categoria": "refran"
    },
    {
        "texto": "No hay mal que dure cien años, ni cuerpo que lo aguante.",
        "categoria": "refran"
    },
    {
        "texto": "A quien madruga, Dios lo ayuda.",
        "categoria": "refran"
    },
    {
        "texto": "Más vale prevenir que lamentar.",
        "categoria": "refran"
    },
    {
        "texto": "En boca cerrada no entran moscas.",
        "categoria": "refran"
    },
    {
        "texto": "El que mucho abarca poco aprieta.",
        "categoria": "refran"
    },
    {
        "texto": "Más vale un pájaro en mano que ciento volando.",
        "categoria": "refran"
    },
    {
        "texto": "Barriga llena, corazón contento.",
        "categoria": "refran"
    },
    
    # POEMAS
    {
        "texto": "Noche de Luna Llena\n\nBajo la luna llena y redonda,\nQue ilumina con su luz plateada,\nEl mundo entero parece una joya fonda,\nDe belleza infinita y sin nada.\n\nLas sombras bailan en el suelo,\nComo espíritus que suben al cielo,\nY la noche envuelve todo en su manto,\nDe misterio, paz y encanto.",
        "categoria": "poema"
    },
    {
        "texto": "Atardecer de Fuego\n\nAtardecer de colores dorados,\nQue pintan el horizonte de fuego,\nLas nubes vuelan como pájaros legaños,\nMientras el sol se va sin freno.\n\nEl cielo se tiñe de rojo y naranja,\nY la brisa trae aromas de la granja,\nLa noche llega lentamente,\nCon sus estrellas brillantes y luciente.",
        "categoria": "poema"
    },
    {
        "texto": "Agua Cristalina\n\nAgua cristalina que corre en el río,\nReflejando la luz del amanecer,\nLas piedras mojadas en el rocío,\nGuardan historias que no puedo creer.\n\nLos árboles se inclinan hacia el agua,\nComo si en ella quisieran mirarse,\nY el sonido del agua que canta,\nHace que mi alma quiera navegarse.",
        "categoria": "poema"
    },
    {
        "texto": "Silencio Profundo\n\nSilencio profundo en la madrugada,\nCuando la ciudad duerme sin pensar,\nLa luna brilla en la ventana helada,\nY las estrellas murmullan un azar.\n\nEl corazón late en la oscuridad,\nComo un reloj de eternidad,\nY en el silencio de la noche oscura,\nEncuentro la paz que mi alma procura.",
        "categoria": "poema"
    },
    {
        "texto": "Las Flores del Jardín\n\nLas flores abren sus pétalos al sol,\nRevelando colores que hipnotizan,\nEl aroma dulce de cada clavel,\nHace que los sentidos se libraricen.\n\nEn el jardín donde reina la calma,\nLa naturaleza toca el alma,\nCada flor es un poema silencioso,\nQue canta al mundo un cántico hermoso.",
        "categoria": "poema"
    },
    
    # FÁBULAS
    {
        "texto": "La Liebre y la Tortuga. Había una vez una liebre muy veloz que se burlaba constantemente de la lentitud de una tortuga. Un día, la tortuga, cansada de las burlas, propuso a la liebre una carrera. La liebre, confiada en su velocidad, aceptó sin dudarlo. Cuando comenzó la carrera, la liebre se adelantó rápidamente, pero al ver que la tortuga estaba muy lejos, decidió descansar bajo un árbol. La liebre se durmió profundamente. Mientras tanto, la tortuga siguió caminando lentamente pero sin parar. Cuando la liebre despertó, vio con sorpresa que la tortuga ya había cruzado la meta. Moraleja: la perseverancia vence la arrogancia.",
        "categoria": "fabula"
    },
    {
        "texto": "El Cuervo y la Jarra. Un cuervo sediento encontró una jarra con agua, pero el pico era muy largo para alcanzarla. El cuervo echó piedrecitas en la jarra hasta que el agua subió. Finalmente pudo beber y saciarse. Moraleja: la inteligencia y la paciencia resuelven los problemas.",
        "categoria": "fabula"
    },
    {
        "texto": "La Cigarra y la Hormiga. Durante el verano, la cigarra cantaba mientras la hormiga trabajaba recolectando alimento. Cuando llegó el invierno, la cigarra moría de hambre. La hormiga tenía suficiente comida para sobrevivir. La cigarra le pidió ayuda, pero la hormiga se la negó. Moraleja: el trabajo y la previsión son necesarios para la supervivencia.",
        "categoria": "fabula"
    },
    {
        "texto": "El Lobo con Piel de Oveja. Un lobo se disfrazó de oveja para infiltrarse en el rebaño. Comía ovejas durante la noche sin que nadie lo descubriera. Finalmente, el pastor lo descubrió y lo expulsó del rebaño. Moraleja: el engaño siempre es descubierto tarde o temprano.",
        "categoria": "fabula"
    },
    {
        "texto": "La Zorra y las Uvas. Una zorra hambrienta vio uvas maduras en una rama alta. Intentó saltar varias veces pero no podía alcanzarlas. Finalmente se fue diciendo que probablemente estaban agrias. Moraleja: es fácil despreciar lo que no podemos obtener.",
        "categoria": "fabula"
    },
    
    # ROMANCES
    {
        "texto": "Eres mi razón de ser, mi razón para sonreír cada mañana. Tu presencia en mi vida es un regalo del universo que nunca esperé recibir. Te amaré eternamente sin importar el tiempo ni la distancia que nos separe. Mi corazón late al unísono con el tuyo, en perfecta sincronía. En tus ojos veo nuestro futuro juntos, lleno de momentos preciosos e inolvidables.",
        "categoria": "romance"
    },
    {
        "texto": "Mi amor por ti es como el océano, profundo e infinito. Tus ojos brillan como estrellas en la noche oscura. Tu sonrisa ilumina mi vida como el sol ilumina el día. Eres todo lo que he deseado y más. Quiero pasar mi vida entera contigo, creando recuerdos hermosos que perdurarán para siempre.",
        "categoria": "romance"
    },
    {
        "texto": "En tus brazos encuentro la paz que mi alma buscaba. Tu amor es el refugio donde encuentro calma y serenidad. Cada momento contigo es un pedazo de cielo. Te amo más que a la vida misma. Bajo las estrellas te juro amor eterno, prometo amarte con cada fibra de mi ser.",
        "categoria": "romance"
    },
    {
        "texto": "Tu amor es mi salvación, mi ancla en este océano de incertidumbre. Sin ti, mi mundo sería oscuro y sin sentido. Eres la razón por la que mi corazón late. Quiero estar contigo para siempre, compartiendo nuestras vidas y nuestros sueños.",
        "categoria": "romance"
    },
    {
        "texto": "Rosa roja como la sangre, símbolo de amor eterno. Tus labios son pétalos suaves que acarician mi alma. Juntos seremos eternos en este amor sin fin. Tu amor es mi única verdad en un mundo lleno de mentiras.",
        "categoria": "romance"
    }
]

# Guardar el nuevo dataset
dataset_path = "data/dataset.json"
os.makedirs(os.path.dirname(dataset_path), exist_ok=True)

with open(dataset_path, "w", encoding="utf-8") as f:
    json.dump(dataset_nuevo, f, ensure_ascii=False, indent=4)

print(f"✓ Dataset limpio creado: {len(dataset_nuevo)} registros")
print("✓ Categorías:", {d["categoria"] for d in dataset_nuevo})
print("✓ Distribución por categoría:")
for cat in sorted({d["categoria"] for d in dataset_nuevo}):
    count = sum(1 for d in dataset_nuevo if d["categoria"] == cat)
    print(f"  - {cat}: {count} textos")
