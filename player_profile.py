"""
player_profile.py
Gestión del perfil del jugador: carga, guardado y validación.
"""

import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

ROLES = ["Top", "Jungla", "Mid", "ADC", "Support"]

RANGOS = [
    "Hierro", "Bronce", "Plata", "Oro", "Platino",
    "Esmeralda", "Diamante", "Maestro", "Gran Maestro", "Challenger"
]

# Opciones del menú desplegable de horas y sus intervalos correspondientes
HORAS_OPCIONES = [
    "1 hora",
    "2–3 horas",
    "3–5 horas",
    "Más de 5 horas"
]

HORAS_INTERVALOS = {
    "1 hora": 50,
    "2–3 horas": 40,
    "3–5 horas": 30,
    "Más de 5 horas": 25
}

DEFAULT_PROFILE = {
    "nick": "",
    "horas_juego": "2–3 horas",
    "rol": "Mid",
    "campeon_favorito": "",
    "rango": "Hierro"
}


def load_profile():
    """Carga el perfil desde config.json. Retorna None si no existe."""
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Migrar formato antiguo: si horas_juego es un int, convertir al nuevo formato
        if isinstance(data.get("horas_juego"), int):
            old_horas = data["horas_juego"]
            if old_horas <= 1:
                data["horas_juego"] = "1 hora"
            elif old_horas <= 3:
                data["horas_juego"] = "2–3 horas"
            elif old_horas <= 5:
                data["horas_juego"] = "3–5 horas"
            else:
                data["horas_juego"] = "Más de 5 horas"
        # Agregar nick si no existía (migración)
        if "nick" not in data:
            data["nick"] = ""
        # Validar campos requeridos
        for key in DEFAULT_PROFILE:
            if key not in data:
                data[key] = DEFAULT_PROFILE[key]
        return data
    except (json.JSONDecodeError, IOError):
        return None


def save_profile(profile):
    """Guarda el perfil en config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4, ensure_ascii=False)


def profile_exists():
    """Verifica si existe un perfil guardado."""
    return os.path.exists(CONFIG_FILE)


def get_intervalo(horas_juego):
    """
    Calcula el intervalo de descanso en minutos según las horas de juego.
    Acepta tanto el nuevo formato string como el antiguo int.
    Mínimo: 20 minutos. Máximo: 50 minutos.
    """
    # Nuevo formato string
    if isinstance(horas_juego, str) and horas_juego in HORAS_INTERVALOS:
        return HORAS_INTERVALOS[horas_juego]

    # Formato antiguo int (compatibilidad)
    try:
        horas = int(horas_juego)
    except (ValueError, TypeError):
        return 40  # valor por defecto seguro

    if horas <= 1:
        intervalo = 50
    elif horas <= 3:
        intervalo = 40
    elif horas <= 5:
        intervalo = 30
    else:
        intervalo = 25

    # Aplicar límites
    intervalo = max(20, min(50, intervalo))
    return intervalo


def validate_profile(profile):
    """
    Valida que todos los campos del perfil estén completos.
    Retorna (es_valido, mensaje_error).
    """
    if not profile.get("nick", "").strip():
        return False, "Ingresá tu nick de invocador."
    if not profile.get("horas_juego") or profile["horas_juego"] not in HORAS_OPCIONES:
        return False, "Seleccioná las horas habituales de juego."
    if not profile.get("rol") or profile["rol"] not in ROLES:
        return False, "Seleccioná tu rol principal."
    if not profile.get("campeon_favorito", "").strip():
        return False, "Ingresá tu campeón favorito."
    if not profile.get("rango") or profile["rango"] not in RANGOS:
        return False, "Seleccioná tu rango actual."
    return True, ""


def get_elo_group(rango):
    """
    Retorna el grupo de personalidad según el rango.
    """
    rango_lower = rango.lower()
    if rango_lower in ("hierro", "bronce"):
        return "bajo"
    elif rango_lower in ("plata", "oro"):
        return "medio"
    elif rango_lower in ("platino", "esmeralda"):
        return "alto"
    else:
        return "elite"


def get_elo_description(rango):
    """
    Retorna una descripción del estilo de personalidad según el rango.
    """
    group = get_elo_group(rango)
    descriptions = {
        "bajo": "Insultos humorísticos, gritos, sarcasmo y mensajes de abandono",
        "medio": "Sarcasmo, desafíos y provocaciones para mejorar",
        "alto": "Motivación, humor y superación",
        "elite": "Mensajes épicos, motivacionales y de alto rendimiento"
    }
    return descriptions.get(group, "")
