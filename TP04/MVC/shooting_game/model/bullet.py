"""Projectiles fired by the wizard: the magic bolt and the fireball (model side)."""
import pygame
from model.game_object import GameObject
from settings import BULLET_SPEED, BULLET_DAMAGE, BULLET_RADIUS


class Bullet(GameObject):
    """A magic bolt: flies in a straight line and disappears outside the board.

    A new projectile only overrides the class attributes below.
    """
    KIND = "magic_bolt"
    SPEED = BULLET_SPEED
    DAMAGE = BULLET_DAMAGE
    DAMAGE_TYPE = "magic"
    RADIUS = BULLET_RADIUS

    def __init__(self, x, y, direction, board):
        size = (self.RADIUS * 4, self.RADIUS * 4)        # hitbox, glow included
        super().__init__(x, y, self.SPEED, size)
        self.direction = pygame.Vector2(direction)   # copy, so it never changes
        self.damage = self.DAMAGE
        self.damage_type = self.DAMAGE_TYPE
        self.board = board

    def update(self, dt):
        """Fly straight; remove itself once it is outside the arena."""
        self.move(self.direction, dt)
        if self.board.is_outside(self):
            self.kill()                 # removes the projectile from every group


class Fireball(Bullet):
    """Second weapon's projectile: bigger, slower, stronger, and of type fire."""
    KIND = "fireball"
    SPEED = 420
    DAMAGE = 20
    DAMAGE_TYPE = "fire"
    RADIUS = 10
