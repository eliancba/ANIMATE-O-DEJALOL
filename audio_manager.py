"""
audio_manager.py
Módulo independiente de gestión de audio.
Detecta, selecciona y reproduce archivos WAV.
"""

import os
import random
import threading
import winsound

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

# Mapa de rango a nombre de carpeta
RANGO_FOLDER_MAP = {
    "Hierro": "hierro",
    "Bronce": "bronce",
    "Plata": "plata",
    "Oro": "oro",
    "Platino": "platino",
    "Esmeralda": "esmeralda",
    "Diamante": "diamante",
    "Maestro": "maestro",
    "Gran Maestro": "gran_maestro",
    "Challenger": "challenger"
}

# Categorías por rango
CATEGORIAS_POR_RANGO = {
    "hierro": ["insultos", "abandono", "descansos"],
    "bronce": ["insultos", "abandono", "descansos"],
    "plata": ["sarcasmo", "desafios", "descansos"],
    "oro": ["sarcasmo", "desafios", "descansos"],
    "platino": ["motivacion", "desafios", "descansos"],
    "esmeralda": ["motivacion", "desafios", "descansos"],
    "diamante": ["motivacion", "desafios", "descansos"],
    "maestro": ["motivacion", "desafios", "descansos"],
    "gran_maestro": ["motivacion", "desafios", "descansos"],
    "challenger": ["motivacion", "desafios", "descansos"]
}

# Último audio reproducido por carpeta para evitar repeticiones
_last_played = {}

# Flag para detener reproducción
_is_playing = False


def get_sound_folder(rango):
    """Retorna la carpeta de sonidos para un rango dado."""
    folder_name = RANGO_FOLDER_MAP.get(rango, "hierro")
    return os.path.join(SOUNDS_DIR, folder_name)


def get_categories(rango):
    """Retorna las categorías de audio disponibles para un rango."""
    folder_name = RANGO_FOLDER_MAP.get(rango, "hierro")
    return CATEGORIAS_POR_RANGO.get(folder_name, ["motivacion", "desafios", "descansos"])


def list_wav_files(folder_path):
    """Lista todos los archivos WAV en una carpeta."""
    if not os.path.exists(folder_path):
        return []
    return [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".wav") and os.path.isfile(os.path.join(folder_path, f))
    ]


def get_all_wav_for_rank(rango):
    """
    Retorna un diccionario con todas las categorías y sus archivos WAV
    para un rango dado.
    """
    base_folder = get_sound_folder(rango)
    categories = get_categories(rango)
    result = {}
    for cat in categories:
        cat_path = os.path.join(base_folder, cat)
        files = list_wav_files(cat_path)
        result[cat] = {
            "path": cat_path,
            "files": files,
            "count": len(files)
        }
    return result


def count_total_wavs(rango):
    """Cuenta el total de archivos WAV disponibles para un rango."""
    all_wavs = get_all_wav_for_rank(rango)
    return sum(info["count"] for info in all_wavs.values())


def has_any_audio(rango):
    """Verifica si existe al menos un archivo WAV para el rango."""
    return count_total_wavs(rango) > 0


def select_random_wav(rango, categoria=None):
    """
    Selecciona un archivo WAV aleatorio para el rango y categoría dados.
    Evita repetir el mismo audio consecutivamente.
    Si no se especifica categoría, elige de todas las disponibles (excepto descansos).
    Retorna (ruta_completa, nombre_archivo) o (None, None) si no hay audios.
    """
    all_wavs = get_all_wav_for_rank(rango)

    if categoria:
        # Buscar en categoría específica
        if categoria in all_wavs and all_wavs[categoria]["count"] > 0:
            candidates = all_wavs[categoria]
            folder = candidates["path"]
            files = candidates["files"]
        else:
            return None, None
    else:
        # Buscar en todas las categorías excepto descansos
        combined_files = []
        for cat, info in all_wavs.items():
            if cat != "descansos":
                for f in info["files"]:
                    combined_files.append((info["path"], f))

        if not combined_files:
            # Si no hay audios en otras categorías, buscar en descansos
            for cat, info in all_wavs.items():
                for f in info["files"]:
                    combined_files.append((info["path"], f))

        if not combined_files:
            return None, None

        # Evitar repetir el último audio
        last_key = f"{rango}_{categoria}"
        last = _last_played.get(last_key)

        if len(combined_files) > 1 and last:
            combined_files = [
                (p, f) for p, f in combined_files
                if os.path.join(p, f) != last
            ]

        folder, filename = random.choice(combined_files)
        full_path = os.path.join(folder, filename)
        _last_played[last_key] = full_path
        return full_path, filename

    # Evitar repetir el último audio
    last_key = f"{rango}_{categoria}"
    last = _last_played.get(last_key)

    if len(files) > 1 and last:
        available = [f for f in files if os.path.join(folder, f) != last]
        if available:
            files = available

    filename = random.choice(files)
    full_path = os.path.join(folder, filename)
    _last_played[last_key] = full_path
    return full_path, filename


def select_break_wav(rango):
    """Selecciona un audio de la categoría descansos."""
    return select_random_wav(rango, categoria="descansos")


def play_wav(file_path, callback=None):
    """
    Reproduce un archivo WAV en un hilo separado para no bloquear la interfaz.
    callback se ejecuta al terminar la reproducción.
    """
    global _is_playing

    if not file_path or not os.path.exists(file_path):
        if callback:
            callback(False, "Archivo no encontrado")
        return

    def _play():
        global _is_playing
        _is_playing = True
        try:
            winsound.PlaySound(file_path, winsound.SND_FILENAME)
            if callback:
                callback(True, "Reproducción completada")
        except Exception as e:
            if callback:
                callback(False, str(e))
        finally:
            _is_playing = False

    thread = threading.Thread(target=_play, daemon=True)
    thread.start()


def stop_playback():
    """Detiene la reproducción actual."""
    global _is_playing
    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
        _is_playing = False
    except Exception:
        pass


def is_playing():
    """Retorna True si se está reproduciendo audio."""
    return _is_playing


def get_status_message(rango):
    """
    Retorna un mensaje de estado sobre los audios disponibles.
    """
    total = count_total_wavs(rango)
    if total == 0:
        return "⚠ No hay audios cargados. Agregá archivos WAV en la carpeta sounds/"
    return f"🎵 {total} audio(s) disponible(s)"


def get_folder_summary():
    """
    Retorna un resumen completo de todas las carpetas y sus archivos WAV.
    Útil para la Cabina del Entrenador.
    """
    summary = {}
    for rango, folder_name in RANGO_FOLDER_MAP.items():
        rank_data = get_all_wav_for_rank(rango)
        summary[rango] = rank_data
    return summary
