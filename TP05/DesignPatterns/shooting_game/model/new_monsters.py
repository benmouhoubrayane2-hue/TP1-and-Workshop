"""Zombie, Dragon and Robot: the products created by the monster factories (Factory Method).

They are ordinary Monster subclasses (OCP, LSP) that only add the abilities they need (ISP).
"""
import math

import pygame
from model.abilities import Shooter, Shielded
from model.enemy_bolt import EnemyBolt
from model.monster import Monster
from model.monster_types import FlyingMonster


class Zombie(Monster):
    """Slow and tough; it lurches forward in jerks. Burns easily."""
    KIND = "zombie"
    SPEED = 80
    MAX_HEALTH = 50
    SIZE = (76, 76)
    POINTS = 2
    CONTACT_DAMAGE = 15
    RESISTANCES = {"fire": 2.0}

    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        self._time = 0.0

    def lurch(self):
        """Between half and full speed, changing all the time."""
        return 0.5 + 0.5 * abs(math.sin(self._time * 3))

    def update(self, dt):
        self._time += dt
        to_target = self.target.pos - self.pos
        if to_target.length() > 1:
            self.move(to_target, dt * self.lurch())


class DragonFire(EnemyBolt):
    """The dragon's fireball: bigger and stronger than an enemy bolt."""
    KIND = "dragon_fire"
    RADIUS = 10
    DAMAGE = 15

    def __init__(self, x, y, direction, board):
        super().__init__(x, y, direction, board)
        self.damage = self.DAMAGE


class Dragon(FlyingMonster, Shooter):
    """Flies in wide waves and spits fire at the player. Immune to fire, weak to magic."""
    KIND = "dragon"
    SPEED = 110
    MAX_HEALTH = 90
    SIZE = (130, 92)
    POINTS = 5
    WAVE_FREQUENCY = 2.0
    WAVE_STRENGTH = 0.7
    RESISTANCES = {"fire": 0.0, "magic": 1.5}
    FIRE_COOLDOWN = 2.2

    def __init__(self, x, y, target, board=None):
        super().__init__(x, y, target)
        self.board = board
        self._reload = self.FIRE_COOLDOWN

    def update(self, dt):
        self._reload = max(0.0, self._reload - dt)
        super().update(dt)                          # flies like a FlyingMonster

    def shoot(self):
        if self._reload > 0 or self.board is None:
            return None
        aim = self.target.pos - self.pos
        if aim.length_squared() == 0:
            return None
        self._reload = self.FIRE_COOLDOWN
        return DragonFire(self.pos.x, self.pos.y, aim.normalize(), self.board)


class Robot(Monster, Shielded):
    """Moves only horizontally or vertically, like on a grid; protected by armour plates."""
    KIND = "robot"
    SPEED = 130
    MAX_HEALTH = 40
    MAX_SHIELD = 40                 # armour
    SIZE = (80, 94)
    POINTS = 3
    RESISTANCES = {"fire": 0.5, "laser": 0.5, "plasma": 2.0}     # plasma = electric shock

    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        self._shield = self.MAX_SHIELD

    @property
    def shield(self):
        return self._shield

    @property
    def shield_ratio(self):
        return self._shield / self.MAX_SHIELD

    def take_damage(self, amount):
        absorbed = min(self._shield, amount)
        self._shield -= absorbed
        super().take_damage(amount - absorbed)

    def update(self, dt):
        """One axis at a time: the one where the target is farthest."""
        to_target = self.target.pos - self.pos
        if to_target.length() <= 1:
            return
        if abs(to_target.x) >= abs(to_target.y):
            step = pygame.Vector2(math.copysign(1, to_target.x), 0)
            room = abs(to_target.x)
        else:
            step = pygame.Vector2(0, math.copysign(1, to_target.y))
            room = abs(to_target.y)
        self.pos += step * min(self.speed * dt, room)    # never goes past the target
        self.sync_rect()
