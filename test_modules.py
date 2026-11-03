"""Script de prueba para validar los módulos y nuevas mejoras."""
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import player_profile
import audio_manager
import message_selector
import champions

print("=== 1. TEST PLAYER PROFILE ===")
# Test intervalos con nuevas opciones string
assert player_profile.get_intervalo("1 hora") == 50
assert player_profile.get_intervalo("2–3 horas") == 40
assert player_profile.get_intervalo("3–5 horas") == 30
assert player_profile.get_intervalo("Más de 5 horas") == 25
print("Intervalos por opciones de texto: OK")

# Test compatibilidad con formato anterior numérico
assert player_profile.get_intervalo(1) == 50
assert player_profile.get_intervalo(3) == 40
assert player_profile.get_intervalo(5) == 30
assert player_profile.get_intervalo(8) == 25
print("Compatibilidad numérica: OK")

# Test validación de perfil
valid_profile = {
    "nick": "FakerJunior",
    "horas_juego": "3–5 horas",
    "rol": "Mid",
    "campeon_favorito": "Ahri",
    "rango": "Challenger"
}
is_valid, msg = player_profile.validate_profile(valid_profile)
assert is_valid, f"Fallo validación válida: {msg}"

# Test validación con nick vacío
invalid_nick = valid_profile.copy()
invalid_nick["nick"] = ""
is_valid, msg = player_profile.validate_profile(invalid_nick)
assert not is_valid and "nick" in msg.lower()

# Test validación con horas inválidas
invalid_horas = valid_profile.copy()
invalid_horas["horas_juego"] = "20 horas"
is_valid, msg = player_profile.validate_profile(invalid_horas)
assert not is_valid and "horas" in msg.lower()

print("Validación de perfil: OK")

# Test save/load y migración segura
old_format_profile = {
    "horas_juego": 4,
    "rol": "Support",
    "campeon_favorito": "Thresh",
    "rango": "Diamante"
}
# Guardar formato antiguo simulando archivo existente
import json
with open(player_profile.CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(old_format_profile, f)

# Cargar y comprobar que migró horas_juego a string y agregó nick sin borrar datos
loaded = player_profile.load_profile()
assert loaded["campeon_favorito"] == "Thresh"
assert loaded["horas_juego"] == "3–5 horas"  # 4 horas migra a "3–5 horas"
assert "nick" in loaded
print("Migración segura de perfil existente: OK")

# Guardar perfil nuevo completo
player_profile.save_profile(valid_profile)
loaded_new = player_profile.load_profile()
assert loaded_new["nick"] == "FakerJunior"
assert loaded_new["horas_juego"] == "3–5 horas"
assert loaded_new["rol"] == "Mid"
assert loaded_new["campeon_favorito"] == "Ahri"
assert loaded_new["rango"] == "Challenger"
print("Guardado y recuperación nuevo perfil: OK")

# Restaurar estado limpio para tests posteriores
if os.path.exists(player_profile.CONFIG_FILE):
    os.remove(player_profile.CONFIG_FILE)

print("\n=== 2. TEST BUSCADOR DE CAMPEONES ===")
assert len(champions.CHAMPIONS) >= 165
print(f"Total campeones cargados: {len(champions.CHAMPIONS)}")

# Búsqueda por prefijo "Yas" -> Yasuo
results_yas = champions.search_champions("Yas")
assert "Yasuo" in results_yas
print(f"Búsqueda 'Yas': {results_yas} (OK)")

# Búsqueda insensible a mayúsculas "lee" -> Lee Sin
results_lee = champions.search_champions("lee")
assert "Lee Sin" in results_lee
print(f"Búsqueda 'lee': {results_lee} (OK)")

# Búsqueda substring "sol" -> Aurelion Sol
results_sol = champions.search_champions("sol")
assert "Aurelion Sol" in results_sol
print(f"Búsqueda 'sol': {results_sol} (OK)")

# Búsqueda sin coincidencias
results_none = champions.search_champions("XYZ12345")
assert len(results_none) == 0
print("Búsqueda sin coincidencias: OK (lista vacía retornada)")

print("\n=== 3. TEST AUDIO MANAGER ===")
assert audio_manager.has_any_audio("Hierro") == False
path, name = audio_manager.select_random_wav("Hierro")
assert path is None and name is None
print("Manejo de carpetas vacías: OK")

print("\n=== 4. TEST ASSETS & CARPETAS ===")
assert os.path.exists("assets")
print("Carpeta assets/: OK")

print("\n=== TODOS LOS TESTS PASARON EXITOSAMENTE ===")
