"""EnemyBolt: a projectile fired by a monster towards the player."""
import pygame
from game_object import GameObject
from settings import ENEMY_BOLT_SPEED, ENEMY_BOLT_DAMAGE, ENEMY_BOLT_RADIUS, ENEMY_BOLT_COLOR


class EnemyBolt(GameObject):
    """Flies straight towards where the player was; disappears outside the board."""

    _image = None   # one image shared by every enemy bolt

    def __init__(self, x, y, direction, board):
        if EnemyBolt._image is None:
            EnemyBolt._image = self._make_image()
        super().__init__(x, y, ENEMY_BOLT_SPEED, EnemyBolt._image)
        self.direction = pygame.Vector2(direction)
        self.damage = ENEMY_BOLT_DAMAGE
        self.board = board

    def update(self, dt):
        self.move(self.direction, dt)
        if self.board.is_outside(self):
            self.kill()

    @staticmethod
    def _make_image():
        size = ENEMY_BOLT_RADIUS * 4
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        centre = (size // 2, size // 2)
        pygame.draw.circle(image, (*ENEMY_BOLT_COLOR, 70), centre, ENEMY_BOLT_RADIUS * 2)
        pygame.draw.circle(image, ENEMY_BOLT_COLOR, centre, ENEMY_BOLT_RADIUS)
        pygame.draw.circle(image, (255, 230, 200), centre, ENEMY_BOLT_RADIUS // 2)
        return image
