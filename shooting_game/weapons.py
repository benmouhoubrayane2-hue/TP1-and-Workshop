"""Weapons of the wizard. The Player depends on the Weapon abstraction (DIP)."""
from abc import ABC, abstractmethod

from bullet import Bullet, Fireball
from settings import FIRE_COOLDOWN


class Weapon(ABC):
    """Anything the wizard can fire. Handles its own reload time."""
    NAME = "weapon"
    COOLDOWN = 0.5                  # seconds between two shots

    def __init__(self):
        self._reload = 0.0

    @property
    def ready(self):
        return self._reload <= 0

    def update(self, dt):
        self._reload = max(0.0, self._reload - dt)

    def fire(self, x, y, direction, board):
        """Return a new projectile if ready, otherwise None."""
        if not self.ready:
            return None
        self._reload = self.COOLDOWN
        return self.make_projectile(x, y, direction, board)

    @abstractmethod
    def make_projectile(self, x, y, direction, board):
        """Create the projectile of this weapon."""


class MagicWand(Weapon):
    """Fast magic bolts."""
    NAME = "Magic wand"
    COOLDOWN = FIRE_COOLDOWN

    def make_projectile(self, x, y, direction, board):
        return Bullet(x, y, direction, board)


class FireStaff(Weapon):
    """Slow but powerful fireballs."""
    NAME = "Fire staff"
    COOLDOWN = 0.6

    def make_projectile(self, x, y, direction, board):
        return Fireball(x, y, direction, board)
