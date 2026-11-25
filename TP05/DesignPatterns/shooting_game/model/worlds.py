"""Worlds - the ABSTRACT FACTORY pattern.

A WorldFactory creates a whole family of objects that belong together: the monsters
(through their spawners), the player's weapons and the rewards. Each level of the
game is played in one world; the game only talks to the abstract WorldFactory, so
it never mixes a dragon with a laser gun or a robot with a health potion.
"""
from abc import ABC, abstractmethod

from model.rewards import HealthPotion, EnergyCell
from model.spawners import (ClassicSpawner, ZombieSpawner, DragonSpawner,
                            RobotSpawner, AlienSpawner, UfoSpawner)
from model.weapons import MagicWand, FireStaff, LaserGun, PlasmaCannon


class WorldFactory(ABC):
    """Abstract factory: one create_... method per kind of product."""
    NAME = "world"

    @abstractmethod
    def create_spawners(self):
        """{name: MonsterSpawner} - the monsters of this world, in the order of keys 3, 4, 5."""

    @abstractmethod
    def create_weapons(self):
        """The two weapons the player uses in this world."""

    @abstractmethod
    def create_reward(self, x, y):
        """The reward a defeated monster may leave at (x, y)."""


class FantasyWorld(WorldFactory):
    NAME = "fantasy"

    def create_spawners(self):
        return {s.NAME: s for s in (ZombieSpawner(), DragonSpawner(), ClassicSpawner())}

    def create_weapons(self):
        return [MagicWand(), FireStaff()]

    def create_reward(self, x, y):
        return HealthPotion(x, y)


class SpaceWorld(WorldFactory):
    NAME = "space"

    def create_spawners(self):
        return {s.NAME: s for s in (RobotSpawner(), AlienSpawner(), UfoSpawner())}

    def create_weapons(self):
        return [LaserGun(), PlasmaCannon()]

    def create_reward(self, x, y):
        return EnergyCell(x, y)


def default_worlds():
    """The worlds of the levels, in order (level 1 fantasy, level 2 space, then again)."""
    return [FantasyWorld(), SpaceWorld()]
