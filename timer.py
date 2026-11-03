"""
timer.py
Temporizador no bloqueante usando Tkinter after().
"""


class BreakTimer:
    """
    Temporizador de descansos que usa Tkinter after() para no bloquear la UI.
    """

    def __init__(self, root, interval_minutes, on_tick=None, on_finish=None):
        """
        root: ventana principal de Tkinter
        interval_minutes: intervalo en minutos
        on_tick: callback(minutes, seconds) llamado cada segundo
        on_finish: callback() llamado al terminar el intervalo
        """
        self._root = root
        self._interval_minutes = interval_minutes
        self._remaining_seconds = interval_minutes * 60
        self._on_tick = on_tick
        self._on_finish = on_finish
        self._after_id = None
        self._running = False
        self._paused = False

    @property
    def is_running(self):
        return self._running

    @property
    def is_paused(self):
        return self._paused

    @property
    def remaining_seconds(self):
        return self._remaining_seconds

    @property
    def interval_minutes(self):
        return self._interval_minutes

    @interval_minutes.setter
    def interval_minutes(self, value):
        self._interval_minutes = value

    def start(self):
        """Inicia o reinicia el temporizador."""
        self.stop()  # Evitar temporizadores duplicados
        self._remaining_seconds = self._interval_minutes * 60
        self._running = True
        self._paused = False
        self._tick()

    def pause(self):
        """Pausa el temporizador."""
        if self._running and not self._paused:
            self._paused = True
            if self._after_id is not None:
                self._root.after_cancel(self._after_id)
                self._after_id = None

    def resume(self):
        """Reanuda el temporizador pausado."""
        if self._running and self._paused:
            self._paused = False
            self._tick()

    def stop(self):
        """Detiene el temporizador completamente."""
        self._running = False
        self._paused = False
        if self._after_id is not None:
            self._root.after_cancel(self._after_id)
            self._after_id = None
        self._remaining_seconds = self._interval_minutes * 60

    def restart(self):
        """Reinicia el temporizador con el mismo intervalo."""
        self.start()

    def _tick(self):
        """Actualización interna cada segundo."""
        if not self._running or self._paused:
            return

        minutes = self._remaining_seconds // 60
        seconds = self._remaining_seconds % 60

        if self._on_tick:
            self._on_tick(minutes, seconds)

        if self._remaining_seconds <= 0:
            self._running = False
            if self._on_finish:
                self._on_finish()
            return

        self._remaining_seconds -= 1
        self._after_id = self._root.after(1000, self._tick)

    def get_display_time(self):
        """Retorna el tiempo restante formateado como MM:SS."""
        minutes = self._remaining_seconds // 60
        seconds = self._remaining_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
