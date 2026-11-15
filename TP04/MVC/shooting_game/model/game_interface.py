"""GameModelInterface: what the View and the Controller need from ANY game model.

The view and the controller depend only on this abstraction (DIP). Any game whose
model implements it can reuse them unchanged - see crystal_hunt/ for a second game.
"""
from abc import ABC, abstractmethod


class GameModelInterface(ABC):
    """A game model must also have these attributes:
    board (with .rect), score, game_over (bool) and paused (bool)."""

    # ---- read by the view
    @abstractmethod
    def drawables(self):
        """Objects to draw, back to front. Each has .KIND and .rect
        (and optionally .health_ratio for a health bar)."""

    @abstractmethod
    def info(self):
        """Data for the information panel, e.g. {"Score": 3, "Health": (70, 100)}."""

    @abstractmethod
    def pop_events(self):
        """GameEvents that happened since the last call."""

    # ---- called by the controller
    @abstractmethod
    def move_player(self, direction): ...

    @abstractmethod
    def set_trigger(self, pressed): ...

    @abstractmethod
    def switch_weapon(self, index=None): ...

    @abstractmethod
    def toggle_pause(self): ...

    @abstractmethod
    def restart(self): ...

    # ---- called by the main loop
    @abstractmethod
    def update(self, dt): ...
