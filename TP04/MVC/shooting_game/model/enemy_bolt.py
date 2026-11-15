"""EnemyBolt: a projectile fired by a monster towards the player (model side)."""
import pygame
from model.game_object import GameObject
from settings import ENEMY_BOLT_SPEED, ENEMY_BOLT_DAMAGE, ENEMY_BOLT_RADIUS


class EnemyBolt(GameObject):
    """Flies straight towards where the player was; disappears outside the board."""
    KIND = "enemy_bolt"
    RADIUS = ENEMY_BOLT_RADIUS

    def __init__(self, x, y, direction, board):
        size = (self.RADIUS * 4, self.RADIUS * 4)
        super().__init__(x, y, ENEMY_BOLT_SPEED, size)
        self.direction = pygame.Vector2(direction)
        self.damage = ENEMY_BOLT_DAMAGE
        self.board = board

    def update(self, dt):
        self.move(self.direction, dt)
        if self.board.is_outside(self):
            self.kill()
