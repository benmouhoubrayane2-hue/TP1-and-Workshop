"""Health: a component that stores and changes hit points (data only, no drawing)."""


class Health:
    """Current and maximum hit points, with the rules to lose or regain them."""

    def __init__(self, maximum):
        self._maximum = maximum
        self._current = maximum

    @property
    def current(self):
        return self._current

    @property
    def maximum(self):
        return self._maximum

    @property
    def ratio(self):
        """Fraction of health left: 1.0 = full, 0.0 = empty."""
        return self._current / self._maximum

    @property
    def is_empty(self):
        return self._current <= 0

    def take_damage(self, amount):
        """Lose `amount` points; never below 0."""
        self._current = max(0, self._current - amount)

    def heal(self, amount):
        """Regain `amount` points; never above the maximum."""
        self._current = min(self._maximum, self._current + amount)
