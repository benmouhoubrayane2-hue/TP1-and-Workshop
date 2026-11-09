"""New monster types: each one EXTENDS Monster; monster.py is not modified (OCP).
Each type implements only the abilities it needs (ISP): see abilities.py."""
import math

from abilities import Flyer, Shooter, Shielded
from enemy_bolt import EnemyBolt
from monster import Monster


class FastMonster(Monster):
    """Quick but fragile."""
    SPEED = 240
    MAX_HEALTH = 20                 # 2 bolts
    SIZE = (56, 56)
    IMAGE = "monster_fast.png"
    POINTS = 2


class StrongMonster(Monster):
    """Slow but very resistant."""
    SPEED = 90
    MAX_HEALTH = 80                 # 8 bolts
    SIZE = (100, 100)
    IMAGE = "monster_strong.png"
    POINTS = 3
    CONTACT_DAMAGE = 20             # hits twice as hard
    RESISTANCES = {"magic": 0.5, "fire": 2.0}    # tough skin, but burns easily


class FlyingMonster(Monster, Flyer):
    """Flies towards the player in a zigzag, which makes it harder to hit."""
    SPEED = 170
    MAX_HEALTH = 30                 # 3 bolts
    SIZE = (102, 72)
    IMAGE = "monster_flying.png"
    RESISTANCES = {"magic": 1.5, "fire": 0.5}    # fragile wings, too fast to catch fire
    POINTS = 2
    WAVE_FREQUENCY = 4.0            # zigzags per second (radians x 1/2pi)
    WAVE_STRENGTH = 0.9             # how wide the zigzag is

    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        self._flight_time = 0.0

    def update(self, dt):
        """Same goal as Monster (reach the target), but it flies."""
        self.fly(dt)

    def fly(self, dt):
        self._flight_time += dt
        to_target = self.target.pos - self.pos
        if to_target.length() > 1:
            forward = to_target.normalize()
            sideways = forward.rotate(90) * math.sin(self._flight_time * self.WAVE_FREQUENCY)
            self.move(forward + sideways * self.WAVE_STRENGTH, dt)


class ImmobileMonster(Monster):
    """A stone totem: it never moves, but it is still a Monster in every other way
    (it has health, a health bar, can be hit, defeated and give points)."""
    SPEED = 0
    MAX_HEALTH = 40                 # 4 bolts
    SIZE = (80, 80)
    IMAGE = "monster_immobile.png"
    RESISTANCES = {"magic": 2.0, "fire": 0.5}    # a stone totem: fire does little
    POINTS = 1

    def update(self, dt):
        """Same contract as Monster.update(): it never moves away from its target.
        It simply stays where it is - it does NOT raise an error or do something unexpected."""


class TurretMonster(ImmobileMonster, Shooter):
    """A totem that cannot move but shoots at the player: immobile + Shooter only."""
    MAX_HEALTH = 50                 # 5 bolts
    IMAGE = "monster_turret.png"
    POINTS = 2
    FIRE_COOLDOWN = 1.6             # seconds between two shots

    def __init__(self, x, y, target, board=None):
        super().__init__(x, y, target)
        self.board = board
        self._reload = self.FIRE_COOLDOWN

    @classmethod
    def spawn_random(cls, board, target):
        pos = board.random_top_position(margin=cls.SIZE[0])
        return cls(pos.x, pos.y, target, board)

    def update(self, dt):
        self._reload = max(0.0, self._reload - dt)      # still never moves

    def shoot(self):
        if self._reload > 0 or self.board is None:
            return None
        self._reload = self.FIRE_COOLDOWN
        aim = self.target.pos - self.pos
        if aim.length_squared() == 0:
            return None
        return EnemyBolt(self.pos.x, self.pos.y, aim.normalize(), self.board)


class ShieldedMonster(Monster, Shielded):
    """A walking monster with a shield: damage hits the shield first."""
    SPEED = 120
    MAX_HEALTH = 30
    MAX_SHIELD = 30                 # 3 extra bolts
    RESISTANCES = {"fire": 1.5}                  # fire melts the shield
    IMAGE = "monster_shielded.png"
    POINTS = 2

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
        """The shield absorbs what it can; the rest goes to health."""
        absorbed = min(self._shield, amount)
        self._shield -= absorbed
        super().take_damage(amount - absorbed)


# The monster types the game can spawn. To add a new type: write its class and add it here.
MONSTER_TYPES = [Monster, FastMonster, StrongMonster, FlyingMonster, ImmobileMonster,
                 TurretMonster, ShieldedMonster]
