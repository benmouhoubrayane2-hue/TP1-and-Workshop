"""Optional monster abilities, one small interface each (ISP).

A monster implements only the abilities it really has: no monster is forced to
have a shoot() method if it cannot shoot, or a shield if it has none.
"""
from abc import ABC, abstractmethod


class Flyer(ABC):
    """A monster that flies instead of walking."""

    @abstractmethod
    def fly(self, dt):
        """Move through the air for `dt` seconds."""


class Shooter(ABC):
    """A monster that fires projectiles at its target."""

    @abstractmethod
    def shoot(self):
        """Return a new projectile if the weapon is ready, otherwise None."""


class Shielded(ABC):
    """A monster protected by a shield that absorbs damage before its health."""

    @property
    @abstractmethod
    def shield(self):
        """Shield points left."""

    @property
    @abstractmethod
    def shield_ratio(self):
        """Fraction of the shield left: 1.0 = full, 0.0 = broken."""
