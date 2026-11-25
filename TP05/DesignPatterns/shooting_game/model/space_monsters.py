"""Monsters of the space world: Alien and UFO (the Robot comes from new_monsters.py)."""
import math

from model.abilities import Shooter
from model.enemy_bolt import EnemyBolt
from model.monster import Monster
from model.monster_types import FlyingMonster


class Alien(Monster):
    """Fast: it dashes towards the player, pauses, then dashes again."""
    KIND = "alien"
    SPEED = 190
    MAX_HEALTH = 30
    SIZE = (70, 82)
    POINTS = 2
    RESISTANCES = {"laser": 1.5, "plasma": 0.5}

    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        self._time = 0.0

    def update(self, dt):
        self._time += dt
        dashing = math.sin(self._time * 5) > -0.3          # dash most of the time, then a short pause
        to_target = self.target.pos - self.pos
        if dashing and to_target.length() > 1:
            self.move(to_target, dt * 1.3)


class EnemyLaser(EnemyBolt):
    """Shot of the UFO: fast but weak."""
    KIND = "enemy_laser"
    RADIUS = 6
    DAMAGE = 8


class Ufo(FlyingMonster, Shooter):
    """A flying saucer: flies in waves and fires lasers at the player."""
    KIND = "ufo"
    SPEED = 130
    MAX_HEALTH = 40
    SIZE = (120, 72)
    POINTS = 4
    WAVE_FREQUENCY = 3.0
    WAVE_STRENGTH = 0.8
    RESISTANCES = {"laser": 0.5, "plasma": 1.5}
    FIRE_COOLDOWN = 1.4

    def __init__(self, x, y, target, board=None):
        super().__init__(x, y, target)
        self.board = board
        self._reload = self.FIRE_COOLDOWN

    def update(self, dt):
        self._reload = max(0.0, self._reload - dt)
        super().update(dt)

    def shoot(self):
        if self._reload > 0 or self.board is None:
            return None
        aim = self.target.pos - self.pos
        if aim.length_squared() == 0:
            return None
        self._reload = self.FIRE_COOLDOWN
        laser = EnemyLaser(self.pos.x, self.pos.y, aim.normalize(), self.board)
        laser.damage = EnemyLaser.DAMAGE
        return laser
