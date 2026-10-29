"""Bullet: straight flight and removal outside the board."""
import pygame
import pytest

from bullet import Bullet
from settings import BULLET_SPEED


def test_flies_straight(board):
    bullet = Bullet(400, 300, pygame.Vector2(0, -1), board)
    bullet.update(0.1)
    assert bullet.pos.x == 400                                  # no sideways drift
    assert bullet.pos.y == pytest.approx(300 - BULLET_SPEED * 0.1)


def test_direction_is_copied(board):
    direction = pygame.Vector2(1, 0)
    bullet = Bullet(400, 300, direction, board)
    direction.update(0, 1)                  # changing the original...
    assert bullet.direction == pygame.Vector2(1, 0)   # ...does not affect the bullet


def test_removed_when_it_leaves_the_board(board):
    group = pygame.sprite.Group()
    bullet = Bullet(400, 300, pygame.Vector2(0, -1), board)
    group.add(bullet)
    for _ in range(120):                    # 2 seconds: far beyond the top edge
        bullet.update(1 / 60)
    assert not bullet.alive()
    assert len(group) == 0


def test_all_bullets_share_one_image(board):
    a = Bullet(100, 100, pygame.Vector2(1, 0), board)
    b = Bullet(200, 200, pygame.Vector2(0, 1), board)
    assert a.image is b.image
