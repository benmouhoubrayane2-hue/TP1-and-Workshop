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

    def summon(self, name):
        """Create a monster on demand. Optional: a game without spawners ignores it."""
        return False

    def summon_slot(self, number):
        """Create the monster number 0, 1 or 2 of the current world (keys 3, 4, 5). Optional."""
        return False

    def next_level(self):
        """Go to the next level (the model does it when the goal is reached). Optional."""

    @property
    def background_name(self):
        """Name of the arena picture chosen by the current level, or None."""
        return None

    @property
    def world_name(self):
        """Name of the current world (the view picks its themes from it), or None."""
        return None

    @abstractmethod
    def restart(self): ...

    # ---- called by the main loop
    @abstractmethod
    def update(self, dt): ...
