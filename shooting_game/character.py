"""Abstract base class for living objects: they have health and can be hurt."""
from game_object import GameObject


class Character(GameObject):
    """A GameObject with health points (the player and the monsters)."""

    def __init__(self, x, y, speed, image, max_health):
        super().__init__(x, y, speed, image)
        self._max_health = max_health      # "_" = protected: not changed from outside
        self._health = max_health

    @property
    def health(self):
        """Read-only access to the current health."""
        return self._health

    @property
    def max_health(self):
        return self._max_health

    @property
    def is_alive(self):
        return self._health > 0

    def take_damage(self, amount):
        """The only way to lower health: it can never go below 0."""
        self._health = max(0, self._health - amount)