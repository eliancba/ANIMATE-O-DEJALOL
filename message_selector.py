"""
message_selector.py
Selecciona mensajes de texto según el ELO del jugador.
Estos mensajes se muestran en la interfaz cuando se activa un descanso.
"""

import random

# Mensajes de texto por grupo de ELO (se muestran en la interfaz)
MENSAJES = {
    "bajo": {
        "descanso": [
            "¡Dejá la grieta un rato, bestia! Tus ojos lo piden.",
            "Ni el minion más perdido juega tanto sin parar.",
            "¡DESCANSÁ! Tu equipo te lo agradece... y tus ojos también.",
            "¿Seguís ahí? Tomate un descanso antes de dar más kills gratis.",
            "El respawn más largo del día: tu descanso. ¡Tomalo ahora!",
            "Hasta el Baron se toma un descanso. Vos también deberías.",
            "¡Hora de alejarse del teclado! No, la tienda no cuenta.",
            "Si seguís así, vas a necesitar un support en la vida real.",
        ],
        "alerta": [
            "¿Otra partida más? Tu PC ya está pidiendo surrender.",
            "El FF15 que necesitás es levantarte de la silla.",
            "¡Salí de ahí! La grieta no se va a ir a ningún lado.",
            "Tu monitor merece un descanso de tu cara.",
        ]
    },
    "medio": {
        "descanso": [
            "Buen intento, pero hasta los pros descansan. ¡Movete!",
            "¿Querés subir de rango? Descansá y volvé con la mente fresca.",
            "El secreto de los challenger: descansos estratégicos. Hacé caso.",
            "Tu KDA mejora con descansos. Es ciencia, no opinión.",
            "Ni Faker juega sin parar. ¿Quién te creés que sos?",
            "Descanso táctico activado. Volvé más fuerte.",
        ],
        "alerta": [
            "¿Seguís en Plata? Capaz un descanso te ayude a pensar mejor.",
            "El tilt empieza cuando no descansás. No seas ese jugador.",
            "Levantate, estirá las piernas, tomá agua. Después seguí.",
        ]
    },
    "alto": {
        "descanso": [
            "¡Gran sesión! Ahora descansá para mantener ese nivel.",
            "Los mejores jugadores cuidan su cuerpo y su mente. ¡Descansá!",
            "Estás en el camino correcto. Un descanso te mantiene afilado.",
            "Rendimiento óptimo = descansos regulares. Vos sabés.",
            "Tu cuerpo es parte del equipo. Cuidalo con un buen descanso.",
        ],
        "alerta": [
            "Hora de recargar energía. Tu siguiente partida lo va a agradecer.",
            "El grindeo inteligente incluye pausas. Hacé la pausa.",
        ]
    },
    "elite": {
        "descanso": [
            "Sesión épica, crack. Ahora descansá como un profesional.",
            "En este nivel, cada descanso es una ventaja competitiva.",
            "Los grandes campeones saben cuándo parar. Es tu momento.",
            "Alto rendimiento requiere alta recuperación. ¡Descansá!",
            "Tu dedicación es admirable. Ahora honrala con un buen descanso.",
        ],
        "alerta": [
            "Hasta los mejores necesitan recuperarse. Es hora.",
            "Rendimiento de élite = recuperación de élite. Descansá.",
        ]
    }
}


def get_message(elo_group, tipo="descanso"):
    """
    Retorna un mensaje aleatorio según el grupo de ELO y tipo.
    tipo: 'descanso' o 'alerta'
    """
    group_messages = MENSAJES.get(elo_group, MENSAJES["bajo"])
    messages = group_messages.get(tipo, group_messages["descanso"])
    return random.choice(messages)


def get_welcome_message(rango, campeon):
    """Retorna un mensaje de bienvenida personalizado."""
    return f"¡Bienvenido, main {campeon}! Rango: {rango}. ¡A jugar!"
