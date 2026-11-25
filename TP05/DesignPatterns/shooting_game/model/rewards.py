"""Rewards dropped by defeated monsters; each world has its own (Abstract Factory products)."""
from abc import abstractmethod

from model.game_object import GameObject


class Reward(GameObject):
    """An item lying on the board for a few seconds; the player picks it up by touching it."""
    KIND = "reward"
    SIZE = (40, 40)
    LIFETIME = 8.0                  # seconds before it disappears

    def __init__(self, x, y, lifetime=None):
        super().__init__(x, y, 0, self.SIZE)
        self.time_left = self.LIFETIME if lifetime is None else lifetime

    def update(self, dt):
        self.time_left -= dt
        if self.time_left <= 0:
            self.kill()

    @abstractmethod
    def apply(self, player):
        """What the reward gives to the player."""


class HealthPotion(Reward):
    """Fantasy world: restores health."""
    KIND = "potion"
    HEAL = 25

    def apply(self, player):
        player.heal(self.HEAL)


class EnergyCell(Reward):
    """Space world: restores a little health and gives bonus points."""
    KIND = "energy_cell"
    HEAL = 15
    POINTS = 2

    def apply(self, player):
        player.heal(self.HEAL)
        player.score += self.POINTS
