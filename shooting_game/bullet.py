"""Projectiles fired by the wizard: the magic bolt and the fireball."""
import pygame
from game_object import GameObject
from settings import BULLET_SPEED, BULLET_DAMAGE, BULLET_RADIUS, BULLET_COLOR


class Bullet(GameObject):
    """A magic bolt: flies in a straight line and disappears outside the board.

    A new projectile only overrides the class attributes below.
    """
    SPEED = BULLET_SPEED
    DAMAGE = BULLET_DAMAGE
    DAMAGE_TYPE = "magic"
    RADIUS = BULLET_RADIUS
    COLOR = BULLET_COLOR
    CORE_COLOR = (240, 255, 255)

    def __init__(self, x, y, direction, board):
        super().__init__(x, y, self.SPEED, self._shared_image())
        self.direction = pygame.Vector2(direction)   # copy, so it never changes
        self.damage = self.DAMAGE
        self.damage_type = self.DAMAGE_TYPE
        self.board = board

    def update(self, dt):
        """Fly straight; remove itself once it is outside the arena."""
        self.move(self.direction, dt)
        if self.board.is_outside(self):
            self.kill()                 # removes the projectile from every sprite group

    @classmethod
    def _shared_image(cls):
        """One image per projectile class, shared by all its projectiles."""
        if "_image" not in cls.__dict__:
            cls._image = cls._make_image()
        return cls._image

    @classmethod
    def _make_image(cls):
        """Draw a glowing orb: soft halo, bright core, light centre."""
        size = cls.RADIUS * 4
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        centre = (size // 2, size // 2)
        pygame.draw.circle(image, (*cls.COLOR, 70), centre, cls.RADIUS * 2)   # halo
        pygame.draw.circle(image, cls.COLOR, centre, cls.RADIUS)               # core
        pygame.draw.circle(image, cls.CORE_COLOR, centre, cls.RADIUS // 2)     # centre
        return image


class Fireball(Bullet):
    """Second weapon's projectile: bigger, slower, stronger, and of type fire."""
    SPEED = 420
    DAMAGE = 20
    DAMAGE_TYPE = "fire"
    RADIUS = 10
    COLOR = (255, 140, 30)
    CORE_COLOR = (255, 240, 150)
