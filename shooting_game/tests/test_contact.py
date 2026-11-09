"""Monsters that touch the wizard hurt him; a short protection follows each hit."""
from game import Game
from monster import Monster
from monster_types import StrongMonster
from settings import PLAYER_INVULNERABLE_TIME


def game_with(monster_type):
    game = Game()
    for other in list(game.monsters):
        other.kill()
    monster = monster_type(game.player.pos.x, game.player.pos.y, target=game.player)
    game.monsters.add(monster)
    game.all_sprites.add(monster)
    return game, monster


def test_touching_monster_hurts_the_player_and_is_pushed_back():
    game, monster = game_with(Monster)
    game.update(1 / 60)
    assert game.player.health == game.player.max_health - Monster.CONTACT_DAMAGE
    assert monster.pos.distance_to(game.player.pos) > 40      # knocked back


def test_strong_monster_hits_harder():
    game, _ = game_with(StrongMonster)
    game.update(1 / 60)
    assert game.player.health == game.player.max_health - StrongMonster.CONTACT_DAMAGE


def test_player_is_protected_for_a_moment_after_a_hit(player):
    assert player.hit(10)
    assert not player.hit(10)                                  # still blinking
    assert player.health == player.max_health - 10
    player.update(PLAYER_INVULNERABLE_TIME)
    assert player.hit(10)
    assert player.health == player.max_health - 20
