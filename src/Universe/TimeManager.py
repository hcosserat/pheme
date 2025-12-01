import time
from typing import Callable, List


class TimeManager:
    """
    Gestionnaire du temps pour la simulation.
    Permet de faire évoluer les personnages et relations au fil du temps.
    """

    def __init__(self, tick_duration: float = 1.0):
        """
        Args:
            tick_duration: Durée d'un tick en secondes (par défaut 1 seconde)
        """
        self.tick_duration = tick_duration
        self.current_tick = 0
        self.is_running = False
        self.callbacks: List[Callable] = []
        self.last_tick_time = 0

    def register_callback(self, callback: Callable):
        """
        Enregistre une fonction à appeler à chaque tick.
        
        Args:
            callback: Fonction à appeler (doit accepter current_tick comme paramètre)
        """
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable):
        """Retire une fonction des callbacks."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def start(self):
        """Démarre le gestionnaire de temps."""
        self.is_running = True
        self.last_tick_time = time.time()

    def stop(self):
        """Arrête le gestionnaire de temps."""
        self.is_running = False

    def pause(self):
        """Met en pause le gestionnaire de temps."""
        self.is_running = False

    def resume(self):
        """Reprend le gestionnaire de temps."""
        self.is_running = True
        self.last_tick_time = time.time()

    def tick(self):
        """
        Effectue un tick si le temps est écoulé.
        Retourne True si un tick a été effectué.
        """
        if not self.is_running:
            return False

        current_time = time.time()
        elapsed = current_time - self.last_tick_time

        if elapsed >= self.tick_duration:
            self.current_tick += 1
            self.last_tick_time = current_time

            # Appeler tous les callbacks enregistrés
            for callback in self.callbacks:
                try:
                    callback(self.current_tick)
                except Exception as e:
                    print(f"Erreur dans callback: {e}")

            return True

        return False

    def reset(self):
        """Réinitialise le gestionnaire de temps."""
        self.current_tick = 0
        self.last_tick_time = time.time()

    def set_tick_duration(self, duration: float):
        """Modifie la durée d'un tick."""
        self.tick_duration = max(0.1, duration)  # Minimum 0.1 seconde

    def get_current_tick(self) -> int:
        """Retourne le tick actuel."""
        return self.current_tick
