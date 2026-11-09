"""OCP: new monster types extend Monster without modifying it."""
import pygame
import pytest

from monster import Monster
from monster_types import MONSTER_TYPES, FastMonster, StrongMonster, FlyingMonster
from settings import BULLET_DAMAGE


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_every_type_is_a_monster(monster_type):
    assert issubclass(monster_type, Monster)


def test_types_have_their_own_characteristics():
    assert FastMonster.SPEED > Monster.SPEED > StrongMonster.SPEED
    assert StrongMonster.MAX_HEALTH > Monster.MAX_HEALTH > FastMonster.MAX_HEALTH
    assert len({t.IMAGE for t in MONSTER_TYPES}) == len(MONSTER_TYPES)   # one look per type


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_each_type_uses_its_own_size_and_health(monster_type, player):
    monster = monster_type(400, 200, target=player)
    assert monster.rect.size == monster_type.SIZE
    assert monster.health == monster_type.MAX_HEALTH


def test_bolts_needed_depend_on_the_type(player):
    assert FastMonster.MAX_HEALTH // BULLET_DAMAGE == 2
    assert StrongMonster.MAX_HEALTH // BULLET_DAMAGE == 8


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_every_type_spawns_inside_the_board(monster_type, board, player):
    for _ in range(20):
        assert board.rect.contains(monster_type.spawn_random(board, target=player).rect)


def test_flying_monster_zigzags_but_gets_closer(player):
    flyer = FlyingMonster(player.pos.x, player.pos.y - 400, target=player)
    start = pygame.Vector2(flyer.pos)
    xs = []
    for _ in range(60):                                  # 1 second
        flyer.update(1 / 60)
        xs.append(flyer.pos.x)
    assert flyer.pos.distance_to(player.pos) < start.distance_to(player.pos)
    assert max(xs) - min(xs) > 10                        # not a straight line


def test_a_new_type_needs_no_change_to_monster(board, player):
    """Adding a type = writing a subclass. Monster itself is untouched."""
    class GiantMonster(Monster):
        SPEED = 40
        MAX_HEALTH = 200
        SIZE = (140, 140)

    giant = GiantMonster.spawn_random(board, target=player)
    assert giant.health == 200 and giant.rect.size == (140, 140)
    before = giant.pos.distance_to(player.pos)
    giant.update(1.0)
    assert before - giant.pos.distance_to(player.pos) == pytest.approx(40)
