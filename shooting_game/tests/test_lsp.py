"""LSP: every monster type can be used wherever a Monster is expected, without breaking the game."""
import pygame
import pytest

from character import Character
from game import Game
from health_bar import HealthBar
from monster import Monster
from monster_types import MONSTER_TYPES, ImmobileMonster


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_is_a_monster_and_a_character(monster_type, player):
    monster = monster_type(400, 200, target=player)
    assert isinstance(monster, Monster) and isinstance(monster, Character)


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_never_moves_away_from_its_target(monster_type, player):
    monster = monster_type(player.pos.x + 150, player.pos.y - 350, target=player)
    distance = monster.pos.distance_to(player.pos)
    for _ in range(90):                                  # 1.5 seconds
        monster.update(1 / 60)                           # must not raise anything
        new_distance = monster.pos.distance_to(player.pos)
        assert new_distance <= distance + 1e-6
        distance = new_distance


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_health_rules_are_the_same(monster_type, player):
    monster = monster_type(400, 200, target=player)
    monster.take_damage(10_000)
    assert monster.health == 0 and not monster.is_alive


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_health_bar_works_for_every_type(monster_type, player):
    monster = monster_type(400, 200, target=player)
    monster.take_damage(10)
    HealthBar().draw(pygame.Surface((960, 640)), monster)


@pytest.mark.parametrize("monster_type", MONSTER_TYPES)
def test_game_logic_works_with_every_type(monster_type):
    """Same Game code, any monster type: it is hit, defeated and gives its points."""
    game = Game()
    for other in list(game.monsters):
        other.kill()
    monster = monster_type(game.player.pos.x, game.player.pos.y - 220, target=game.player)
    monster.speed = 0
    game.monsters.add(monster)
    game.all_sprites.add(monster)

    game.player.trigger_pressed = True
    for _ in range(600):                                 # up to 10 seconds
        game.update(1 / 60)
        if not monster.alive():
            break

    assert not monster.alive()
    assert game.player.score == monster_type.POINTS


def test_immobile_monster_stays_in_place(player):
    totem = ImmobileMonster(300, 200, target=player)
    start = pygame.Vector2(totem.pos)
    for _ in range(60):
        totem.update(1 / 60)
    assert totem.pos == start
