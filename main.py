"""
main.py
Punto de entrada de la aplicación ANIMATE O DEJALO.
Optimizado para ejecución de escritorio en Windows sin ventana de consola secundaria.
"""

import os
import sys
import tkinter as tk

# Asegurar que el directorio de trabajo sea el del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Si se ejecuta en Windows mediante python.exe sin el flag --debug,
# ocultar la consola asociada para que solo exista una única ventana visible.
if sys.platform == "win32" and "--debug" not in sys.argv:
    try:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
    except Exception:
        pass

# Estructura de carpetas de sonidos
SOUND_FOLDERS = [
    "sounds/hierro/insultos",
    "sounds/hierro/abandono",
    "sounds/hierro/descansos",
    "sounds/bronce/insultos",
    "sounds/bronce/abandono",
    "sounds/bronce/descansos",
    "sounds/plata/sarcasmo",
    "sounds/plata/desafios",
    "sounds/plata/descansos",
    "sounds/oro/sarcasmo",
    "sounds/oro/desafios",
    "sounds/oro/descansos",
    "sounds/platino/motivacion",
    "sounds/platino/desafios",
    "sounds/platino/descansos",
    "sounds/esmeralda/motivacion",
    "sounds/esmeralda/desafios",
    "sounds/esmeralda/descansos",
    "sounds/diamante/motivacion",
    "sounds/diamante/desafios",
    "sounds/diamante/descansos",
    "sounds/maestro/motivacion",
    "sounds/maestro/desafios",
    "sounds/maestro/descansos",
    "sounds/gran_maestro/motivacion",
    "sounds/gran_maestro/desafios",
    "sounds/gran_maestro/descansos",
    "sounds/challenger/motivacion",
    "sounds/challenger/desafios",
    "sounds/challenger/descansos",
    "assets",
]


def create_folders():
    """Crea todas las carpetas necesarias y asegura archivos .gitkeep para git."""
    for folder in SOUND_FOLDERS:
        os.makedirs(folder, exist_ok=True)
        keep = os.path.join(folder, ".gitkeep")
        if not os.path.exists(keep):
            try:
                with open(keep, "w", encoding="utf-8") as f:
                    pass
            except Exception:
                pass


def main():
    """Punto de entrada principal de la aplicación."""
    create_folders()

    from interface import AnimateApp

    root = tk.Tk()

    # Icono de ventana (si existe en assets/icon.png o icon.ico)
    icon_png = os.path.join("assets", "icon.png")
    if os.path.exists(icon_png):
        try:
            icon_img = tk.PhotoImage(file=icon_png)
            root.iconphoto(True, icon_img)
        except Exception:
            pass
    elif os.path.exists("icon.ico"):
        try:
            root.iconbitmap("icon.ico")
        except tk.TclError:
            pass

    app = AnimateApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
