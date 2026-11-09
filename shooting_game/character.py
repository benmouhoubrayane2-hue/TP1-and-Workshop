"""Abstract base class for living objects: they have health and can be hurt."""
from game_object import GameObject
from health import Health


class Character(GameObject):
    """A GameObject with health points (the player and the monsters)."""

    def __init__(self, x, y, speed, image, max_health):
        super().__init__(x, y, speed, image)
        self._health = Health(max_health)    # the health rules live in their own class

    @property
    def health(self):
        """Read-only access to the current health."""
        return self._health.current

    @property
    def max_health(self):
        return self._health.maximum

    @property
    def health_ratio(self):
        return self._health.ratio

    @property
    def is_alive(self):
        return not self._health.is_empty

    def take_damage(self, amount):
        """The only way to lower health: it can never go below 0."""
        self._health.take_damage(amount)
