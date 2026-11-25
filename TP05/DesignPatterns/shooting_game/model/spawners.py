"""Monster spawners - the FACTORY METHOD pattern.

MonsterSpawner is the creator: spawn() places a new monster on the board, and the
factory method create_monster() decides WHICH monster is created. Each concrete
spawner overrides only create_monster(). The game asks spawners for monsters and
never writes Zombie(...), Dragon(...) or Robot(...) itself, so a new kind of
monster only needs a new spawner.
"""
import random
from abc import ABC, abstractmethod

from model.abilities import Shooter
from model.monster_types import MONSTER_TYPES as CLASSIC_TYPES
from model.new_monsters import Zombie, Dragon, Robot
from model.space_monsters import Alien, Ufo


class MonsterSpawner(ABC):
    """Creator of the Factory Method pattern."""
    NAME = "monster"
    MARGIN = 70                     # distance from the edges of the board

    def spawn(self, board, target):
        """Same for every spawner: choose a place at the top, then let the
        factory method create the monster."""
        pos = board.random_top_position(margin=self.MARGIN)
        return self.create_monster(pos.x, pos.y, target, board)

    @abstractmethod
    def create_monster(self, x, y, target, board):
        """FACTORY METHOD: return a new monster at (x, y) chasing `target`."""


class ZombieSpawner(MonsterSpawner):
    NAME = "zombie"

    def create_monster(self, x, y, target, board):
        return Zombie(x, y, target)


class DragonSpawner(MonsterSpawner):
    NAME = "dragon"

    def create_monster(self, x, y, target, board):
        return Dragon(x, y, target, board)          # the dragon needs the board to shoot


class RobotSpawner(MonsterSpawner):
    NAME = "robot"

    def create_monster(self, x, y, target, board):
        return Robot(x, y, target)


class AlienSpawner(MonsterSpawner):
    NAME = "alien"

    def create_monster(self, x, y, target, board):
        return Alien(x, y, target)


class UfoSpawner(MonsterSpawner):
    NAME = "ufo"

    def create_monster(self, x, y, target, board):
        return Ufo(x, y, target, board)


class ClassicSpawner(MonsterSpawner):
    """The monsters of the previous versions (normal, fast, strong, flying, totem, turret, shielded)."""
    NAME = "classic"
    TYPES = [t for t in CLASSIC_TYPES]

    def create_monster(self, x, y, target, board):
        monster_type = random.choice(self.TYPES)
        if issubclass(monster_type, Shooter):
            return monster_type(x, y, target, board)
        return monster_type(x, y, target)


def default_spawners():
    """Four spawners by name (used by the tests; the game takes its spawners from the worlds)."""
    return {s.NAME: s for s in (ClassicSpawner(), ZombieSpawner(), DragonSpawner(), RobotSpawner())}
