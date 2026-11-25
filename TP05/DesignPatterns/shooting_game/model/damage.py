"""How much damage a hit really does. The game depends on the abstraction (DIP)."""
from abc import ABC, abstractmethod


class DamageCalculator(ABC):
    """Turns the damage of a projectile into the damage the target really takes."""

    @abstractmethod
    def compute(self, amount, damage_type, target):
        """Return the final damage (an int >= 0)."""


class ResistanceCalculator(DamageCalculator):
    """Uses the target's RESISTANCES: 0.5 = resists (half damage), 2.0 = weakness (double)."""

    def compute(self, amount, damage_type, target):
        multiplier = getattr(target, "RESISTANCES", {}).get(damage_type, 1.0)
        return max(0, round(amount * multiplier))


class PlainCalculator(DamageCalculator):
    """Ignores resistances and weaknesses (e.g. an easy mode)."""

    def compute(self, amount, damage_type, target):
        return amount
