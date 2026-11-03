"""
interface.py
Interfaz gráfica principal de ANIMATE O DEJALO.
Estética oscura, gamer, compacta, moderna y de alta legibilidad.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import player_profile
import audio_manager
import message_selector
import champions
from timer import BreakTimer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_PATH = os.path.join(ASSETS_DIR, "icon.png")

# ─── Paleta de colores gamer (Identidad original optimizada) ─────────────────
BG_DARK = "#0d0d0d"        # Fondo principal negro profundo
BG_PANEL = "#1a1a2e"       # Paneles contenedores azul violáceo oscuro
BG_CARD = "#16213e"        # Tarjetas / bloques interiores
BG_INPUT = "#0f3460"       # Entradas de texto y controles interactivos
BG_HOVER = "#1f3b64"       # Hover de controles

FG_PRIMARY = "#e94560"     # Acento principal: Rosa / Rojo neón
FG_PRIMARY_HOVER = "#ff6b81"
FG_SECONDARY = "#00d2ff"   # Acento secundario: Celeste / Cyan neón
FG_TEXT = "#ffffff"        # Texto principal blanco de alto contraste
FG_TEXT_MUTED = "#cfd8dc"  # Texto secundario claro y legible
FG_DIM = "#8fa3bf"         # Texto atenuado pero legible

FG_SUCCESS = "#00e676"     # Verde brillante
FG_WARNING = "#ffd600"     # Amarillo brillante
FG_DANGER = "#ff1744"      # Rojo alerta

BTN_BG = "#e94560"
BTN_HOVER = "#ff6b81"
BTN_SECONDARY = "#0f3460"
BTN_SECONDARY_HOVER = "#1a467f"
BTN_GREEN = "#00c853"
BTN_GREEN_HOVER = "#00e676"
BTN_YELLOW = "#ffb300"
BTN_YELLOW_HOVER = "#ffd54f"
BTN_STOP = "#d50000"
BTN_STOP_HOVER = "#ff1744"

# ─── Tipografías equilibradas y legibles ──────────────────────────────────────
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 12, "bold")
FONT_SECTION = ("Segoe UI", 10, "bold")
FONT_BODY = ("Segoe UI", 9)
FONT_BODY_BOLD = ("Segoe UI", 9, "bold")
FONT_TIMER = ("Consolas", 42, "bold")
FONT_SMALL = ("Segoe UI", 8)
FONT_SMALL_BOLD = ("Segoe UI", 8, "bold")
FONT_BTN = ("Segoe UI", 9, "bold")


def center_window(window, width, height):
    """Centra una ventana de Tkinter en la pantalla de forma precisa."""
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = max(0, (screen_w - width) // 2)
    y = max(0, (screen_h - height) // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


class ChampionSearchWidget(tk.Frame):
    """
    Buscador de campeones con sugerencias inteligentes en tiempo real.
    Permite filtrar al escribir y seleccionar vía mouse o teclado (Up/Down/Return).
    """

    def __init__(self, parent, variable, on_select_callback=None, **kwargs):
        super().__init__(parent, bg=BG_PANEL, **kwargs)
        self.variable = variable
        self.on_select_callback = on_select_callback
        self._suppress_search = False

        # Campo de entrada
        entry_frame = tk.Frame(self, bg=BG_INPUT, bd=1, relief="solid")
        entry_frame.pack(fill="x")

        self.entry = tk.Entry(
            entry_frame,
            textvariable=self.variable,
            font=FONT_BODY_BOLD,
            bg=BG_INPUT,
            fg=FG_TEXT,
            insertbackground=FG_SECONDARY,
            relief="flat",
            bd=0
        )
        self.entry.pack(fill="x", ipady=5, padx=8)

        # Eventos del Entry
        self.entry.bind("<KeyRelease>", self._on_key_release)
        self.entry.bind("<Down>", self._focus_suggestions)
        self.entry.bind("<Return>", self._on_entry_enter)
        self.entry.bind("<Escape>", lambda e: self._hide_suggestions())

        # Contenedor flotante de sugerencias
        self.sugg_container = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid")
        
        self.no_matches_label = tk.Label(
            self.sugg_container,
            text="",
            font=FONT_SMALL,
            fg=FG_WARNING,
            bg=BG_CARD,
            pady=4,
            padx=6
        )

        self.listbox = tk.Listbox(
            self.sugg_container,
            font=FONT_BODY,
            bg=BG_CARD,
            fg=FG_SECONDARY,
            selectbackground=FG_PRIMARY,
            selectforeground=FG_TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            height=4,
            activestyle="none"
        )
        self.listbox.bind("<ButtonRelease-1>", self._on_listbox_click)
        self.listbox.bind("<Return>", self._on_listbox_enter)
        self.listbox.bind("<Up>", self._on_listbox_up)
        self.listbox.bind("<Escape>", lambda e: self._hide_suggestions())

        self.help_label = tk.Label(
            self.sugg_container,
            text="↕ Usa flechas o clic para elegir | Enter confirma",
            font=("Segoe UI", 7),
            fg=FG_DIM,
            bg=BG_CARD,
            pady=2
        )

    def _on_key_release(self, event):
        if event.keysym in ("Down", "Up", "Return", "Escape", "Tab"):
            return
        if self._suppress_search:
            self._suppress_search = False
            return

        query = self.variable.get().strip()
        if not query:
            self._hide_suggestions()
            return

        matches = champions.search_champions(query, limit=5)
        self.listbox.delete(0, tk.END)

        if matches:
            self.no_matches_label.pack_forget()
            for champ in matches:
                self.listbox.insert(tk.END, f"  {champ}")
            self.listbox.pack(fill="x", padx=2, pady=1)
            self.help_label.pack(fill="x")
            self.sugg_container.pack(fill="x", pady=(2, 0))
        else:
            self.listbox.pack_forget()
            self.help_label.pack_forget()
            self.no_matches_label.config(
                text=f"✖ No se encontraron coincidencias para \"{query}\""
            )
            self.no_matches_label.pack(fill="x")
            self.sugg_container.pack(fill="x", pady=(2, 0))

    def _focus_suggestions(self, event):
        if self.listbox.winfo_ismapped() and self.listbox.size() > 0:
            self.listbox.focus_set()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return "break"

    def _on_listbox_up(self, event):
        if self.listbox.curselection() and self.listbox.curselection()[0] == 0:
            self.entry.focus_set()
            return "break"

    def _on_entry_enter(self, event):
        query = self.variable.get().strip()
        if self.listbox.winfo_ismapped() and self.listbox.size() > 0:
            first_match = self.listbox.get(0).strip()
            self._select_champion(first_match)
            return "break"
        elif query:
            matches = champions.search_champions(query, limit=1)
            if matches:
                self._select_champion(matches[0])
                return "break"

    def _on_listbox_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            champ_name = self.listbox.get(selection[0]).strip()
            self._select_champion(champ_name)

    def _on_listbox_enter(self, event):
        selection = self.listbox.curselection()
        if selection:
            champ_name = self.listbox.get(selection[0]).strip()
            self._select_champion(champ_name)
            return "break"

    def _select_champion(self, name):
        self._suppress_search = True
        self.variable.set(name)
        self._hide_suggestions()
        self.entry.focus_set()
        self.entry.icursor(tk.END)
        if self.on_select_callback:
            self.on_select_callback(name)

    def _hide_suggestions(self):
        self.sugg_container.pack_forget()


class AnimateApp:
    """Aplicación principal de ANIMATE O DEJALO."""

    # Dimensiones estándar compactas y equilibradas
    WINDOW_WIDTH = 780
    WINDOW_HEIGHT = 590

    def __init__(self, root):
        self.root = root
        self.root.title("ANIMATE O DEJALO")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(740, 560)

        # Centrar la ventana al iniciar
        center_window(self.root, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Configurar estilos de ttk para menús desplegables
        self._setup_ttk_styles()

        # Caché de imagen del logo
        self._logo_image = None

        # Variables de estado
        self.profile = None
        self.timer = None
        self.status_var = tk.StringVar(value="Detenido")
        self.timer_var = tk.StringVar(value="00:00")
        self.message_var = tk.StringVar(value="")
        self.audio_status_var = tk.StringVar(value="")
        self.player_status_var = tk.StringVar(value="")

        # Cargar perfil existente o mostrar cuestionario
        self.profile = player_profile.load_profile()
        if self.profile and player_profile.validate_profile(self.profile)[0]:
            self._build_main_screen()
        else:
            self._build_setup_screen(edit_mode=False)

    def _setup_ttk_styles(self):
        """Estiliza los componentes ttk para mantener la estética gamer y legible."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Gamer.TCombobox",
            background=BG_INPUT,
            foreground=FG_TEXT,
            fieldbackground=BG_INPUT,
            darkcolor=BG_PANEL,
            lightcolor=FG_SECONDARY,
            arrowcolor=FG_SECONDARY,
            bordercolor=BG_PANEL,
            insertcolor=FG_SECONDARY,
            padding=5,
            font=FONT_BODY_BOLD
        )
        style.map(
            "Gamer.TCombobox",
            fieldbackground=[("readonly", BG_INPUT)],
            foreground=[("readonly", FG_TEXT)],
            background=[("readonly", BG_INPUT), ("active", BG_HOVER)]
        )

        self.root.option_add("*TCombobox*Listbox.background", BG_CARD)
        self.root.option_add("*TCombobox*Listbox.foreground", FG_TEXT)
        self.root.option_add("*TCombobox*Listbox.selectBackground", FG_PRIMARY)
        self.root.option_add("*TCombobox*Listbox.selectForeground", FG_TEXT)
        self.root.option_add("*TCombobox*Listbox.font", FONT_BODY)

    def _create_logo_widget(self, parent, size=(46, 46)):
        """
        Crea el widget del logo.
        Si assets/icon.png existe, lo carga.
        Si no existe, muestra un espacio reservado estilizado sin provocar errores.
        """
        logo_frame = tk.Frame(parent, bg=BG_PANEL, width=size[0], height=size[1])
        logo_frame.pack_propagate(False)

        loaded = False
        if os.path.exists(ICON_PATH):
            try:
                img = tk.PhotoImage(file=ICON_PATH)
                w, h = img.width(), img.height()
                if w > size[0] and size[0] > 0:
                    factor = max(1, w // size[0])
                    img = img.subsample(factor, factor)
                self._logo_image = img
                lbl = tk.Label(logo_frame, image=self._logo_image, bg=BG_PANEL)
                lbl.pack(expand=True, fill="both")
                loaded = True
            except Exception:
                loaded = False

        if not loaded:
            box = tk.Frame(logo_frame, bg=BG_CARD, bd=1, relief="solid")
            box.pack(expand=True, fill="both", padx=2, pady=2)
            tk.Label(box, text="⚡", font=("Segoe UI", 14, "bold"),
                     fg=FG_SECONDARY, bg=BG_CARD).pack(pady=(2, 0))
            tk.Label(box, text="LOGO", font=("Segoe UI", 6, "bold"),
                     fg=FG_DIM, bg=BG_CARD).pack()

        return logo_frame

    # ═══════════════════════════════════════════════════════════════════════════
    # 1. PANTALLA DE CONFIGURACIÓN DEL PERFIL (Orden exacto y sin scroll forzado)
    # ═══════════════════════════════════════════════════════════════════════════

    def _build_setup_screen(self, edit_mode=False):
        """Pantalla de configuración inicial o edición con distribución compacta."""
        self._clear_root()

        defaults = self.profile if self.profile else player_profile.DEFAULT_PROFILE

        container = tk.Frame(self.root, bg=BG_DARK)
        container.pack(expand=True, fill="both", padx=30, pady=12)

        # ─── HEADER ────────────────────────────────────────────────────────
        header_frame = tk.Frame(container, bg=BG_DARK)
        header_frame.pack(fill="x", pady=(0, 10))

        logo_box = self._create_logo_widget(header_frame, size=(46, 46))
        logo_box.pack(side="left", padx=(0, 12))

        titles_frame = tk.Frame(header_frame, bg=BG_DARK)
        titles_frame.pack(side="left", fill="y")

        tk.Label(
            titles_frame,
            text="ANIMATE O DEJALO",
            font=FONT_TITLE,
            fg=FG_PRIMARY,
            bg=BG_DARK,
            anchor="w"
        ).pack(anchor="w")

        subtitle_text = "EDITAR PERFIL DEL JUGADOR" if edit_mode else "CONFIGURACIÓN INICIAL DEL JUGADOR"
        tk.Label(
            titles_frame,
            text=subtitle_text,
            font=FONT_SUBTITLE,
            fg=FG_SECONDARY,
            bg=BG_DARK,
            anchor="w"
        ).pack(anchor="w")

        # ─── FORMULARIO COMPACTO ───────────────────────────────────────────
        form = tk.Frame(container, bg=BG_PANEL, bd=1, relief="solid")
        form.pack(fill="x", pady=(0, 10))

        form_inner = tk.Frame(form, bg=BG_PANEL, padx=22, pady=12)
        form_inner.pack(fill="x")

        # 1.1 NICK DE INVOCADOR
        tk.Label(
            form_inner,
            text="1. Nick de invocador *",
            font=FONT_SECTION,
            fg=FG_TEXT,
            bg=BG_PANEL,
            anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self.nick_var = tk.StringVar(value=defaults.get("nick", ""))
        nick_entry_frame = tk.Frame(form_inner, bg=BG_INPUT, bd=1, relief="solid")
        nick_entry_frame.pack(fill="x", pady=(0, 8))

        nick_entry = tk.Entry(
            nick_entry_frame,
            textvariable=self.nick_var,
            font=FONT_BODY_BOLD,
            bg=BG_INPUT,
            fg=FG_TEXT,
            insertbackground=FG_SECONDARY,
            relief="flat",
            bd=0
        )
        nick_entry.pack(fill="x", ipady=5, padx=8)

        # 1.2 HORAS HABITUALES DE JUEGO
        tk.Label(
            form_inner,
            text="2. Horas habituales de juego *",
            font=FONT_SECTION,
            fg=FG_TEXT,
            bg=BG_PANEL,
            anchor="w"
        ).pack(fill="x", pady=(0, 2))

        current_horas = defaults.get("horas_juego", "2–3 horas")
        if current_horas not in player_profile.HORAS_OPCIONES:
            current_horas = "2–3 horas"

        self.horas_var = tk.StringVar(value=current_horas)
        self.horas_combo = ttk.Combobox(
            form_inner,
            textvariable=self.horas_var,
            values=player_profile.HORAS_OPCIONES,
            state="readonly",
            style="Gamer.TCombobox",
            font=FONT_BODY_BOLD
        )
        self.horas_combo.pack(fill="x", pady=(0, 3))
        self.horas_combo.bind("<<ComboboxSelected>>", self._on_horas_selected)

        self.intervalo_desc_var = tk.StringVar()
        self._update_intervalo_label(current_horas)
        interval_banner = tk.Frame(form_inner, bg=BG_CARD, padx=8, pady=4)
        interval_banner.pack(fill="x", pady=(0, 8))
        tk.Label(
            interval_banner,
            textvariable=self.intervalo_desc_var,
            font=FONT_BODY_BOLD,
            fg=FG_SECONDARY,
            bg=BG_CARD
        ).pack(anchor="w")

        # 1.3 ROL PRINCIPAL
        tk.Label(
            form_inner,
            text="3. Rol principal *",
            font=FONT_SECTION,
            fg=FG_TEXT,
            bg=BG_PANEL,
            anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self.rol_var = tk.StringVar(value=defaults.get("rol", "Mid"))
        rol_frame = tk.Frame(form_inner, bg=BG_PANEL)
        rol_frame.pack(fill="x", pady=(0, 8))

        for rol in player_profile.ROLES:
            rb = tk.Radiobutton(
                rol_frame,
                text=rol,
                variable=self.rol_var,
                value=rol,
                font=FONT_BODY_BOLD,
                fg=FG_TEXT,
                bg=BG_PANEL,
                selectcolor=BG_INPUT,
                activebackground=BG_PANEL,
                activeforeground=FG_PRIMARY,
                cursor="hand2"
            )
            rb.pack(side="left", padx=(0, 16))

        # 1.4 CAMPEÓN FAVORITO (Buscador inteligente con sugerencias)
        tk.Label(
            form_inner,
            text="4. Campeón favorito (escribí para sugerencias en tiempo real) *",
            font=FONT_SECTION,
            fg=FG_TEXT,
            bg=BG_PANEL,
            anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self.campeon_var = tk.StringVar(value=defaults.get("campeon_favorito", ""))
        self.champ_widget = ChampionSearchWidget(
            form_inner,
            variable=self.campeon_var
        )
        self.champ_widget.pack(fill="x", pady=(0, 8))

        # 1.5 RANGO ACTUAL
        tk.Label(
            form_inner,
            text="5. Rango actual *",
            font=FONT_SECTION,
            fg=FG_TEXT,
            bg=BG_PANEL,
            anchor="w"
        ).pack(fill="x", pady=(0, 3))

        self.rango_var = tk.StringVar(value=defaults.get("rango", "Hierro"))
        rango_container = tk.Frame(form_inner, bg=BG_PANEL)
        rango_container.pack(fill="x", pady=(0, 4))

        row1 = tk.Frame(rango_container, bg=BG_PANEL)
        row1.pack(fill="x", pady=1)
        row2 = tk.Frame(rango_container, bg=BG_PANEL)
        row2.pack(fill="x", pady=1)

        for i, rango in enumerate(player_profile.RANGOS):
            target_row = row1 if i < 5 else row2
            rb = tk.Radiobutton(
                target_row,
                text=rango,
                variable=self.rango_var,
                value=rango,
                font=FONT_BODY,
                fg=FG_TEXT_MUTED,
                bg=BG_PANEL,
                selectcolor=BG_INPUT,
                activebackground=BG_PANEL,
                activeforeground=FG_PRIMARY,
                cursor="hand2"
            )
            rb.pack(side="left", padx=(0, 12), pady=1)

        # ─── BOTONES DE ACCIÓN ─────────────────────────────────────────────
        btn_bar = tk.Frame(container, bg=BG_DARK)
        btn_bar.pack(pady=6)

        save_btn = tk.Button(
            btn_bar,
            text="💾 GUARDAR PERFIL",
            font=FONT_BTN,
            bg=BTN_BG,
            fg=FG_TEXT,
            activebackground=BTN_HOVER,
            activeforeground=FG_TEXT,
            relief="flat",
            padx=22,
            pady=8,
            cursor="hand2",
            command=self._save_setup
        )
        save_btn.pack(side="left", padx=6)

        if edit_mode:
            cancel_btn = tk.Button(
                btn_bar,
                text="✖ CANCELAR",
                font=FONT_BTN,
                bg=BTN_SECONDARY,
                fg=FG_TEXT,
                activebackground=BTN_SECONDARY_HOVER,
                activeforeground=FG_TEXT,
                relief="flat",
                padx=18,
                pady=8,
                cursor="hand2",
                command=self._build_main_screen
            )
            cancel_btn.pack(side="left", padx=6)

    def _on_horas_selected(self, event):
        val = self.horas_var.get()
        self._update_intervalo_label(val)

    def _update_intervalo_label(self, horas_val):
        intervalo = player_profile.get_intervalo(horas_val)
        self.intervalo_desc_var.set(
            f"⏱ Intervalo calculado: {intervalo} minutos para '{horas_val}' de juego"
        )

    def _save_setup(self):
        nick = self.nick_var.get().strip()
        horas = self.horas_var.get().strip()
        rol = self.rol_var.get().strip()
        campeon = self.campeon_var.get().strip()
        rango = self.rango_var.get().strip()

        candidate = {
            "nick": nick,
            "horas_juego": horas,
            "rol": rol,
            "campeon_favorito": campeon,
            "rango": rango
        }

        is_valid, error_msg = player_profile.validate_profile(candidate)
        if not is_valid:
            messagebox.showwarning("Campo incompleto", error_msg)
            return

        self.profile = candidate
        player_profile.save_profile(self.profile)
        self._build_main_screen()

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. PANTALLA PRINCIPAL
    # ═══════════════════════════════════════════════════════════════════════════

    def _build_main_screen(self):
        """Pantalla principal compacta, equilibrada y sin elementos cortados."""
        self._clear_root()

        if not self.profile:
            self.profile = player_profile.load_profile()

        nick = self.profile.get("nick", "Invocador")
        horas = self.profile.get("horas_juego", "2–3 horas")
        rol = self.profile.get("rol", "Mid")
        campeon = self.profile.get("campeon_favorito", "Desconocido")
        rango = self.profile.get("rango", "Hierro")

        intervalo = player_profile.get_intervalo(horas)
        elo_group = player_profile.get_elo_group(rango)
        elo_desc = player_profile.get_elo_description(rango)

        self.timer_var.set(f"{intervalo:02d}:00")
        self.status_var.set("Detenido")
        self.message_var.set(
            f"¡Bienvenido {nick}! Main {campeon} ({rol}) | Rango: {rango}. ¡A jugar concentrado!"
        )
        self.audio_status_var.set(audio_manager.get_status_message(rango))
        self.player_status_var.set("")

        main_frame = tk.Frame(self.root, bg=BG_DARK)
        main_frame.pack(expand=True, fill="both", padx=20, pady=12)

        # ─── HEADER ────────────────────────────────────────────────────────
        header = tk.Frame(main_frame, bg=BG_DARK)
        header.pack(fill="x", pady=(0, 10))

        logo_box = self._create_logo_widget(header, size=(44, 44))
        logo_box.pack(side="left", padx=(0, 10))

        title_box = tk.Frame(header, bg=BG_DARK)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="ANIMATE O DEJALO",
            font=FONT_TITLE,
            fg=FG_PRIMARY,
            bg=BG_DARK
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text=f"Invocador: {nick} • {rol} ({campeon})",
            font=FONT_SMALL_BOLD,
            fg=FG_DIM,
            bg=BG_DARK
        ).pack(anchor="w")

        btn_row = tk.Frame(header, bg=BG_DARK)
        btn_row.pack(side="right")

        config_btn = tk.Button(
            btn_row,
            text="⚙ Editar Perfil",
            font=FONT_SMALL_BOLD,
            bg=BTN_SECONDARY,
            fg=FG_TEXT,
            activebackground=BTN_SECONDARY_HOVER,
            activeforeground=FG_TEXT,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=lambda: self._build_setup_screen(edit_mode=True)
        )
        config_btn.pack(side="left", padx=3)

        cabina_btn = tk.Button(
            btn_row,
            text="🎙 Cabina del Entrenador",
            font=FONT_SMALL_BOLD,
            bg=BTN_SECONDARY,
            fg=FG_SECONDARY,
            activebackground=BTN_SECONDARY_HOVER,
            activeforeground=FG_TEXT,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self._show_cabina
        )
        cabina_btn.pack(side="left", padx=3)

        # ─── TARJETAS DE INFORMACIÓN (3 Columnas compactas) ────────────────
        cards_frame = tk.Frame(main_frame, bg=BG_DARK)
        cards_frame.pack(fill="x", pady=(0, 10))
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)

        # Card 1: Perfil
        self._create_card(cards_frame, 0, f"👤 {nick}", [
            f"Rol: {rol}",
            f"Campeón: {campeon}",
            f"Sesión: {horas}"
        ], accent=FG_SECONDARY)

        # Card 2: ELO
        self._create_card(cards_frame, 1, f"🏆 {rango.upper()}", [
            f"Personalidad: {elo_group.upper()}",
            elo_desc
        ], accent=FG_PRIMARY)

        # Card 3: Intervalo
        self._create_card(cards_frame, 2, "⏱ INTERVALO", [
            f"Descanso: cada {intervalo} min",
            f"Basado en {horas}"
        ], accent=FG_SUCCESS)

        # ─── PANEL CENTRAL: TEMPORIZADOR ──────────────────────────────────
        timer_panel = tk.Frame(main_frame, bg=BG_PANEL, bd=1, relief="solid", padx=18, pady=12)
        timer_panel.pack(fill="x", pady=(0, 10))

        tk.Label(
            timer_panel,
            text="CUENTA REGRESIVA PARA EL DESCANSO",
            font=FONT_SMALL_BOLD,
            fg=FG_DIM,
            bg=BG_PANEL
        ).pack()

        tk.Label(
            timer_panel,
            textvariable=self.timer_var,
            font=FONT_TIMER,
            fg=FG_SECONDARY,
            bg=BG_PANEL
        ).pack(pady=2)

        status_box = tk.Frame(timer_panel, bg=BG_PANEL)
        status_box.pack()
        tk.Label(
            status_box,
            text="Estado: ",
            font=FONT_BODY,
            fg=FG_TEXT_MUTED,
            bg=BG_PANEL
        ).pack(side="left")
        self.status_label = tk.Label(
            status_box,
            textvariable=self.status_var,
            font=FONT_BODY_BOLD,
            fg=FG_WARNING,
            bg=BG_PANEL
        )
        self.status_label.pack(side="left")

        # ─── CONTROLES ────────────────────────────────────────────────────
        ctrl_frame = tk.Frame(main_frame, bg=BG_DARK)
        ctrl_frame.pack(pady=(0, 10))

        self.start_btn = tk.Button(
            ctrl_frame,
            text="▶ INICIAR",
            font=FONT_BTN,
            bg=BTN_GREEN,
            fg=FG_TEXT,
            activebackground=BTN_GREEN_HOVER,
            activeforeground=FG_TEXT,
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._start_timer
        )
        self.start_btn.pack(side="left", padx=4)

        self.pause_btn = tk.Button(
            ctrl_frame,
            text="⏸ PAUSAR",
            font=FONT_BTN,
            bg=BTN_YELLOW,
            fg="#1a1a2e",
            activebackground=BTN_YELLOW_HOVER,
            activeforeground="#000000",
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._pause_timer,
            state="disabled"
        )
        self.pause_btn.pack(side="left", padx=4)

        self.stop_btn = tk.Button(
            ctrl_frame,
            text="⏹ DETENER",
            font=FONT_BTN,
            bg=BTN_STOP,
            fg=FG_TEXT,
            activebackground=BTN_STOP_HOVER,
            activeforeground=FG_TEXT,
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._stop_timer,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=4)

        test_btn = tk.Button(
            ctrl_frame,
            text="🔊 PROBAR SONIDO",
            font=FONT_BTN,
            bg=BTN_SECONDARY,
            fg=FG_TEXT,
            activebackground=BTN_SECONDARY_HOVER,
            activeforeground=FG_TEXT,
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._test_sound
        )
        test_btn.pack(side="left", padx=4)

        # ─── MENSAJE DINÁMICO ─────────────────────────────────────────────
        msg_box = tk.Frame(main_frame, bg=BG_CARD, bd=1, relief="solid", padx=12, pady=8)
        msg_box.pack(fill="x", pady=(0, 8))

        tk.Label(
            msg_box,
            textvariable=self.message_var,
            font=FONT_BODY_BOLD,
            fg=FG_TEXT,
            bg=BG_CARD,
            wraplength=720,
            justify="center"
        ).pack()

        # ─── ESTADO INFERIOR ──────────────────────────────────────────────
        status_bar = tk.Frame(main_frame, bg=BG_DARK)
        status_bar.pack(fill="x")

        tk.Label(
            status_bar,
            textvariable=self.audio_status_var,
            font=FONT_SMALL,
            fg=FG_DIM,
            bg=BG_DARK
        ).pack(side="left")

        tk.Label(
            status_bar,
            textvariable=self.player_status_var,
            font=FONT_SMALL_BOLD,
            fg=FG_SECONDARY,
            bg=BG_DARK
        ).pack(side="right")

        # Temporizador
        self.timer = BreakTimer(
            self.root,
            intervalo,
            on_tick=self._on_tick,
            on_finish=self._on_timer_finish
        )

    def _create_card(self, parent, col, title, lines, accent=FG_TEXT):
        card = tk.Frame(parent, bg=BG_CARD, bd=1, relief="solid", padx=10, pady=8)
        card.grid(row=0, column=col, sticky="nsew", padx=3, pady=1)

        tk.Label(
            card,
            text=title,
            font=FONT_SUBTITLE,
            fg=accent,
            bg=BG_CARD
        ).pack(anchor="w", pady=(0, 2))

        for line in lines:
            tk.Label(
                card,
                text=line,
                font=FONT_BODY,
                fg=FG_TEXT_MUTED,
                bg=BG_CARD,
                wraplength=220,
                justify="left"
            ).pack(anchor="w", pady=1)

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. LÓGICA DEL TEMPORIZADOR Y AUDIO
    # ═══════════════════════════════════════════════════════════════════════════

    def _start_timer(self):
        if self.timer:
            if self.timer.is_paused:
                self.timer.resume()
                self.status_var.set("En marcha")
                self.status_label.config(fg=FG_SUCCESS)
                self.pause_btn.config(text="⏸ PAUSAR")
            else:
                self.timer.start()
                self.status_var.set("En marcha")
                self.status_label.config(fg=FG_SUCCESS)

            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.stop_btn.config(state="normal")

    def _pause_timer(self):
        if self.timer:
            if self.timer.is_paused:
                self.timer.resume()
                self.status_var.set("En marcha")
                self.status_label.config(fg=FG_SUCCESS)
                self.pause_btn.config(text="⏸ PAUSAR")
                self.start_btn.config(state="disabled")
            else:
                self.timer.pause()
                self.status_var.set("Pausado")
                self.status_label.config(fg=FG_WARNING)
                self.pause_btn.config(text="▶ REANUDAR")
                self.start_btn.config(state="normal")

    def _stop_timer(self):
        if self.timer:
            self.timer.stop()
            intervalo = player_profile.get_intervalo(self.profile["horas_juego"])
            self.timer_var.set(f"{intervalo:02d}:00")
            self.status_var.set("Detenido")
            self.status_label.config(fg=FG_WARNING)
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled", text="⏸ PAUSAR")
            self.stop_btn.config(state="disabled")
            audio_manager.stop_playback()

    def _on_tick(self, minutes, seconds):
        self.timer_var.set(f"{minutes:02d}:{seconds:02d}")

    def _on_timer_finish(self):
        elo_group = player_profile.get_elo_group(self.profile["rango"])
        msg = message_selector.get_message(elo_group, "descanso")
        nick = self.profile.get("nick", "Invocador")
        self.message_var.set(f"💬 {nick}: {msg}")
        self.status_var.set("¡TIEMPO DE DESCANSO!")
        self.status_label.config(fg=FG_PRIMARY)

        rango = self.profile["rango"]
        if audio_manager.has_any_audio(rango):
            path, name = audio_manager.select_random_wav(rango)
            if path:
                self.player_status_var.set(f"🔊 Reproduciendo: {name}")
                audio_manager.play_wav(path, callback=self._on_playback_done)
        else:
            self.player_status_var.set("⚠ Sin audios WAV para reproducir")

        self.root.after(5000, self._auto_restart)

    def _on_playback_done(self, success, message):
        self.player_status_var.set("")

    def _auto_restart(self):
        if self.timer and not self.timer.is_running:
            self.timer.restart()
            self.status_var.set("En marcha")
            self.status_label.config(fg=FG_SUCCESS)
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.stop_btn.config(state="normal")

    def _test_sound(self):
        rango = self.profile["rango"]
        if not audio_manager.has_any_audio(rango):
            self.player_status_var.set("⚠ No hay audios. Agregá archivos WAV en sounds/")
            folder_name = audio_manager.RANGO_FOLDER_MAP.get(rango, "hierro")
            messagebox.showinfo(
                "Sin audios WAV",
                f"No se encontraron archivos WAV para el rango {rango}.\n\n"
                f"Ubicación de destino:\n"
                f"sounds/{folder_name}/\n\n"
                "Podés agregar tus archivos .wav en cualquier momento sin tocar código."
            )
            return

        path, name = audio_manager.select_random_wav(rango)
        if path:
            self.player_status_var.set(f"🔊 Probando: {name}")
            audio_manager.play_wav(path, callback=self._on_playback_done)

    # ═══════════════════════════════════════════════════════════════════════════
    # 4. CABINA DEL ENTRENADOR (Con actualización dinámica y centrado)
    # ═══════════════════════════════════════════════════════════════════════════

    def _show_cabina(self):
        cabina = tk.Toplevel(self.root)
        cabina.title("🎙 CABINA DEL ENTRENADOR — ANIMATE O DEJALO")
        cabina.configure(bg=BG_DARK)
        cabina.minsize(600, 420)
        center_window(cabina, 700, 520)

        header = tk.Frame(cabina, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(12, 6))

        title_subframe = tk.Frame(header, bg=BG_DARK)
        title_subframe.pack(side="left")

        tk.Label(
            title_subframe,
            text="🎙 CABINA DEL ENTRENADOR",
            font=FONT_TITLE,
            fg=FG_PRIMARY,
            bg=BG_DARK
        ).pack(anchor="w")

        tk.Label(
            title_subframe,
            text="Explorá tus audios WAV por rango y probalos en vivo.",
            font=FONT_BODY,
            fg=FG_DIM,
            bg=BG_DARK
        ).pack(anchor="w")

        # Botón de refresco
        refresh_btn = tk.Button(
            header,
            text="🔄 Actualizar lista",
            font=FONT_SMALL_BOLD,
            bg=BTN_SECONDARY,
            fg=FG_SECONDARY,
            activebackground=BTN_SECONDARY_HOVER,
            activeforeground=FG_TEXT,
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: self._populate_cabina(scroll_frame)
        )
        refresh_btn.pack(side="right")

        container = tk.Frame(cabina, bg=BG_DARK)
        container.pack(expand=True, fill="both", padx=16, pady=4)

        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_DARK)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_cabina_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        cabina.bind("<MouseWheel>", _on_cabina_mousewheel)

        self._populate_cabina(scroll_frame)

        stop_bar = tk.Frame(cabina, bg=BG_DARK)
        stop_bar.pack(pady=8)
        tk.Button(
            stop_bar,
            text="⏹ DETENER REPRODUCCIÓN",
            font=FONT_BTN,
            bg=BTN_STOP,
            fg=FG_TEXT,
            relief="flat",
            padx=16,
            pady=5,
            cursor="hand2",
            command=audio_manager.stop_playback
        ).pack()

    def _populate_cabina(self, parent_frame):
        """Llena o recarga dinámicamente la lista de audios en la cabina."""
        for widget in parent_frame.winfo_children():
            widget.destroy()

        summary = audio_manager.get_folder_summary()

        for rango, categories in summary.items():
            rango_frame = tk.Frame(parent_frame, bg=BG_PANEL, bd=1, relief="solid", padx=10, pady=8)
            rango_frame.pack(fill="x", pady=3)

            total = sum(info["count"] for info in categories.values())
            color = FG_SUCCESS if total > 0 else FG_WARNING

            top_row = tk.Frame(rango_frame, bg=BG_PANEL)
            top_row.pack(fill="x")

            tk.Label(
                top_row,
                text=f"🏆 RANGO: {rango.upper()}",
                font=FONT_SUBTITLE,
                fg=color,
                bg=BG_PANEL
            ).pack(side="left")

            tk.Label(
                top_row,
                text=f"Total: {total} audio(s)",
                font=FONT_SMALL_BOLD,
                fg=FG_TEXT_MUTED,
                bg=BG_PANEL
            ).pack(side="right")

            for cat, info in categories.items():
                cat_frame = tk.Frame(rango_frame, bg=BG_CARD, padx=8, pady=4)
                cat_frame.pack(fill="x", pady=2, padx=(8, 0))

                cat_header = tk.Frame(cat_frame, bg=BG_CARD)
                cat_header.pack(fill="x")

                count_color = FG_SUCCESS if info["count"] > 0 else FG_DIM
                tk.Label(
                    cat_header,
                    text=f"📁 {cat}/",
                    font=FONT_BODY_BOLD,
                    fg=FG_TEXT,
                    bg=BG_CARD
                ).pack(side="left")

                tk.Label(
                    cat_header,
                    text=f"({info['count']} WAVs)",
                    font=FONT_SMALL,
                    fg=count_color,
                    bg=BG_CARD
                ).pack(side="left", padx=5)

                if info["count"] > 0:
                    test_btn = tk.Button(
                        cat_header,
                        text="▶ Probar aleatorio",
                        font=FONT_SMALL_BOLD,
                        bg=BTN_SECONDARY,
                        fg=FG_SECONDARY,
                        relief="flat",
                        padx=6,
                        pady=1,
                        cursor="hand2",
                        command=lambda r=rango, c=cat: self._test_category_sound(r, c)
                    )
                    test_btn.pack(side="right")

                    for filename in info["files"]:
                        file_frame = tk.Frame(cat_frame, bg=BG_CARD)
                        file_frame.pack(fill="x", padx=(12, 0), pady=1)

                        tk.Label(
                            file_frame,
                            text=f"  🎵 {filename}",
                            font=FONT_SMALL,
                            fg=FG_TEXT_MUTED,
                            bg=BG_CARD
                        ).pack(side="left")

                        play_btn = tk.Button(
                            file_frame,
                            text="▶",
                            font=FONT_SMALL_BOLD,
                            bg=BG_CARD,
                            fg=FG_SECONDARY,
                            relief="flat",
                            padx=4,
                            cursor="hand2",
                            command=lambda p=info["path"], f=filename: self._play_specific(p, f)
                        )
                        play_btn.pack(side="right")
                else:
                    tk.Label(
                        cat_frame,
                        text="   (Carpeta lista para recibir archivos .wav)",
                        font=FONT_SMALL,
                        fg=FG_DIM,
                        bg=BG_CARD
                    ).pack(anchor="w")

    def _test_category_sound(self, rango, categoria):
        path, name = audio_manager.select_random_wav(rango, categoria)
        if path:
            self.player_status_var.set(f"🔊 Probando: {name}")
            audio_manager.play_wav(path, callback=self._on_playback_done)

    def _play_specific(self, folder, filename):
        path = os.path.join(folder, filename)
        self.player_status_var.set(f"🔊 Reproduciendo: {filename}")
        audio_manager.play_wav(path, callback=self._on_playback_done)

    def _clear_root(self):
        if self.timer and self.timer.is_running:
            self.timer.stop()
        for widget in self.root.winfo_children():
            widget.destroy()
