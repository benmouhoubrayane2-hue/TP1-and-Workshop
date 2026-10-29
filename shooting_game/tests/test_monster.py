"""Monster: spawning, pursuit and health."""
import pytest

from monster import Monster
from settings import MONSTER_SPEED, BULLET_DAMAGE


def test_spawns_inside_the_board(board, player):
    for _ in range(50):
        monster = Monster.spawn_random(board, target=player)
        assert board.rect.contains(monster.rect)


def test_chases_its_target(monster, player):
    before = monster.pos.distance_to(player.pos)
    monster.update(1.0)
    after = monster.pos.distance_to(player.pos)
    assert before - after == pytest.approx(MONSTER_SPEED)


def test_stops_on_the_target(monster, player):
    monster.pos.update(player.pos)
    monster.update(1.0)
    assert monster.pos == player.pos


def test_dies_after_three_bolts(monster):
    for _ in range(3):
        assert monster.is_alive
        monster.take_damage(BULLET_DAMAGE)
    assert not monster.is_alive
