"""Player: movement, boundaries, encapsulated health and shooting."""
import pygame
import pytest

from bullet import Bullet
from settings import PLAYER_SPEED, PLAYER_MAX_HEALTH, FIRE_COOLDOWN


def test_starts_at_bottom_centre(player, board):
    assert player.rect.centerx == board.rect.centerx
    assert board.rect.contains(player.rect)


def test_moves_at_its_speed(player):
    player.pos.update(400, 300)
    player.direction = pygame.Vector2(1, 0)
    player.update(0.5)
    assert player.pos.x == pytest.approx(400 + PLAYER_SPEED * 0.5)


def test_diagonal_is_not_faster(player):
    start = pygame.Vector2(400, 300)
    player.pos.update(start)
    player.direction = pygame.Vector2(1, 1)
    player.update(0.5)
    assert player.pos.distance_to(start) == pytest.approx(PLAYER_SPEED * 0.5)


@pytest.mark.parametrize("direction", [(1, 1), (1, -1), (-1, 1), (-1, -1)])
def test_never_leaves_the_board(player, board, direction):
    player.direction = pygame.Vector2(direction)
    for _ in range(300):                    # 5 seconds towards a corner
        player.update(1 / 60)
    assert board.rect.contains(player.rect)


def test_health_is_read_only(player):
    with pytest.raises(AttributeError):
        player.health = 999


def test_take_damage_never_goes_below_zero(player):
    player.take_damage(30)
    assert player.health == PLAYER_MAX_HEALTH - 30
    player.take_damage(1000)
    assert player.health == 0
    assert not player.is_alive


def test_shoot_respects_the_cooldown(player):
    assert isinstance(player.shoot(), Bullet)
    assert player.shoot() is None           # still reloading
    player.update(FIRE_COOLDOWN)            # wait one cooldown
    assert isinstance(player.shoot(), Bullet)


def test_shoots_in_the_facing_direction(player):
    player.direction = pygame.Vector2(-1, 0)
    player.update(0.01)
    bullet = player.shoot()
    assert bullet.direction == pygame.Vector2(-1, 0)
