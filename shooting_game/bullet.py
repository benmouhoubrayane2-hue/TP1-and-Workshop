"""Bullet: a magic bolt fired by the wizard."""
import pygame
from game_object import GameObject
from settings import BULLET_SPEED, BULLET_DAMAGE, BULLET_RADIUS, BULLET_COLOR


class Bullet(GameObject):
    """Flies in a straight line and disappears when it leaves the board."""

    _image = None   # class attribute: one image shared by every bullet

    def __init__(self, x, y, direction, board):
        if Bullet._image is None:
            Bullet._image = self._make_image()
        super().__init__(x, y, BULLET_SPEED, Bullet._image)
        self.direction = pygame.Vector2(direction)   # copy, so it never changes
        self.damage = BULLET_DAMAGE
        self.board = board

    def update(self, dt):
        """Fly straight; remove itself once it is outside the arena."""
        self.move(self.direction, dt)
        if self.board.is_outside(self):
            self.kill()                 # removes the bullet from every sprite group

    @staticmethod
    def _make_image():
        """Draw a glowing orb: soft halo, bright core, white centre."""
        size = BULLET_RADIUS * 4
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        centre = (size // 2, size // 2)
        pygame.draw.circle(image, (*BULLET_COLOR, 70), centre, BULLET_RADIUS * 2)   # halo
        pygame.draw.circle(image, BULLET_COLOR, centre, BULLET_RADIUS)               # core
        pygame.draw.circle(image, (240, 255, 255), centre, BULLET_RADIUS // 2)       # centre
        return image