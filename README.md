# 🎮 ANIMATE O DEJALO

<p align="center">
  <strong>Aplicación de escritorio gamer para Windows que ayuda a jugadores de League of Legends a regular sus sesiones mediante recordatorios de descanso adaptados a su ELO.</strong>
</p>

---

## 📌 Descripción del Proyecto

**ANIMATE O DEJALO** es una aplicación liviana, rápida y sin dependencias externas complejas, pensada especialmente para jugadores de League of Legends. Diseñada para funcionar con fluidez incluso en equipos con recursos limitados (4 GB de RAM), calcula automáticamente los tiempos óptimos de descanso según las horas de juego habituales del usuario y reproduce audios con personalidad ajustada a su rango competitivo.

---

## 🎯 Objetivo de la Aplicación

Evitar el desgaste visual, mental y el *tilt* durante partidas competitivas en la Grieta del Invocador, fomentando hábitos de descanso consistentes mediante una experiencia inmersiva, humorística y motivacional.

---

## 🚀 Funcionalidades Actuales

- 👤 **Perfil del Invocador**:
  - **Nick de Invocador**: Registro y visualización del nombre del jugador.
  - **Selector de Horas de Juego**: Menú desplegable con cálculo automático del intervalo de descanso:
    - `1 hora` habitual → **50 minutos** de intervalo.
    - `2–3 horas` habituales → **40 minutos** de intervalo.
    - `3–5 horas` habituales → **30 minutos** de intervalo.
    - `Más de 5 horas` habituales → **25 minutos** de intervalo.
  - **Rol Principal**: Selección única entre `Top`, `Jungla`, `Mid`, `ADC` y `Support`.
  - **Buscador Inteligente de Campeones**: Base de datos local de 172 campeones de LoL con autocompletado en tiempo real sin requerir APIs ni conexión a Internet. Selección fluida con teclado y ratón.
  - **Rango Actual (ELO)**: Configuración entre `Hierro`, `Bronce`, `Plata`, `Oro`, `Platino`, `Esmeralda`, `Diamante`, `Maestro`, `Gran Maestro` y `Challenger`.
- ⏱ **Temporizador Inteligente**:
  - Cuenta regresiva `MM:SS` visible y fluida basada en `after()` de Tkinter.
  - No bloquea la interfaz de usuario ni el hilo de ejecución.
  - Continúa operando con la ventana minimizada.
  - Botones de control: **Iniciar**, **Pausar / Reanudar** y **Detener**.
  - Reinicio automático al cumplirse la alarma de descanso.
  - Prevención de temporizadores duplicados o llamadas fantasma.
- 🎙 **Cabina del Entrenador**:
  - Panel interactivo para visualizar y probar audios disponibles por rango y categoría.
  - Botón de **Actualizar lista** para refrescar nuevos audios agregados en caliente sin reiniciar la app.
  - Control de reproducción con botón para detener audios en cualquier momento.
- 🔊 **Motor de Audio Local**:
  - Reproducción de archivos WAV mediante `winsound` nativo de Windows.
  - Selección aleatoria con memoria de último archivo para evitar repeticiones consecutivas.
  - Manejo seguro de carpetas vacías con avisos amigables sin lanzar errores.
- 🎨 **Interfaz Gamer Moderna**:
  - Paleta oscura original de alto contraste: Fondo `#0d0d0d`, paneles `#1a1a2e`, entradas `#0f3460`, acentos cyan `#00d2ff` y botones `#e94560`.
  - Ventana compacta, centrada automáticamente en pantalla, sin consolas secundarias innecesarias.
  - Espacio reservado para logotipo personalizado en `assets/icon.png`.

---

## 📂 Organización de Carpetas

```
animate_o_dejalo/
├── main.py                 # Punto de entrada principal (oculta consola automáticamente)
├── main.pyw                # Lanzador nativo sin consola para Windows
├── interface.py            # Interfaz gráfica (Tkinter) centrada y compacta
├── champions.py            # Base local de 172 campeones y algoritmo de búsqueda
├── player_profile.py       # Lógica del perfil, cálculo de intervalos y validaciones
├── timer.py                # Temporizador no bloqueante
├── audio_manager.py        # Detección y reproducción de archivos WAV
├── message_selector.py     # Mensajes de texto motivacionales/humorísticos por ELO
├── test_modules.py         # Suite completa de pruebas unitarias
├── config.example.json     # Plantilla de configuración local
├── assets/                 # Recursos gráficos (icon.png)
└── sounds/                 # 40 carpetas organizadas por rango y categoría
    ├── hierro/ (insultos, abandono, descansos)
    ├── bronce/ (insultos, abandono, descansos)
    ├── plata/ (sarcasmo, desafios, descansos)
    ├── oro/ (sarcasmo, desafios, descansos)
    ├── platino/ (motivacion, desafios, descansos)
    ├── esmeralda/ (motivacion, desafios, descansos)
    ├── diamante/ (motivacion, desafios, descansos)
    ├── maestro/ (motivacion, desafios, descansos)
    ├── gran_maestro/ (motivacion, desafios, descansos)
    └── challenger/ (motivacion, desafios, descansos)
```

---

## 🎧 Cómo Agregar Audios Propios

La aplicación viene preparada con la estructura completa de carpetas sin necesidad de modificar el código fuente:

1. Graba o descarga tus pistas de audio en formato `.wav`.
2. Cópialas directamente en la carpeta correspondiente a tu rango y estilo de mensaje (por ejemplo: `sounds/oro/sarcasmo/mi_audio.wav`).
3. Abre **ANIMATE O DEJALO** o haz clic en **🎙 Cabina del Entrenador** para escucharlas y probarlas.

### Estilo de Audios según Rango:
- **Hierro y Bronce**: Insultos cómicos, gritos y sarcasmo sobre abandonar la Grieta.
- **Plata y Oro**: Desafíos, ironía y provocaciones para mejorar el nivel.
- **Platino y Esmeralda**: Mensajes de superación, motivación y humor.
- **Diamante a Challenger**: Mensajes épicos de alto rendimiento y mentalidad competitiva.

---

## 💻 Requisitos del Sistema

- **Sistema Operativo**: Windows 10 o Windows 11.
- **Lenguaje**: Python 3.8 o superior (probado en Python 3.12).
- **Memoria RAM**: 4 GB (uso de RAM inferior a 45 MB en ejecución).
- **Dependencias**: Ninguna librería pesada ni conexión a Internet requerida. Utiliza módulos nativos de la biblioteca estándar (`tkinter`, `winsound`, `json`).

---

## 🛠 Instalación y Ejecución

1. Clona este repositorio o descárgalo como archivo ZIP:
   ```bash
   git clone https://github.com/eliancba/ANIMATE-O-DEJALOL.git
   cd ANIMATE-O-DEJALOL
   ```

2. Ejecución directa:
   - **Opción estándar**:
     ```bash
     python main.py
     ```
   - **Opción sin consola de Windows**: Haz doble clic en `main.pyw` o ejecuta:
     ```bash
     pythonw main.pyw
     ```

---

## 🧪 Pruebas Unitarias

Para comprobar el correcto funcionamiento de todos los módulos y la integridad del sistema:

```bash
python test_modules.py
```

---

## 📋 Estado Actual del Desarrollo

- [x] Arquitectura modular separada (preparada para reutilización en versión Android).
- [x] Cuestionario inicial con nuevo orden de perfil validado.
- [x] Buscador local de campeones con autocompletado en tiempo real.
- [x] Ventana de escritorio compacta, centrada y sin consola secundaria.
- [x] Motor de reproducción WAV aleatorio sin repetición consecutiva.
- [x] Cabina del Entrenador con refresco dinámico de pistas.
- [x] Documentación y suite de pruebas completadas.
- [ ] Fase futura: Grabación y agregado de archivos WAV personalizados.
- [ ] Fase futura: Portabilidad móvil (Android).

---

## 📄 Licencia

Este proyecto se encuentra bajo la Licencia MIT.
