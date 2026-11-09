"""ISP: each monster has only the abilities it needs; no useless methods."""
import pygame
import pytest

from abilities import Flyer, Shooter, Shielded
from enemy_bolt import EnemyBolt
from game import Game
from monster import Monster
from monster_types import (FastMonster, StrongMonster, FlyingMonster, ImmobileMonster,
                           TurretMonster, ShieldedMonster)

ABILITIES = {
    Monster:         set(),
    FastMonster:     set(),
    StrongMonster:   set(),
    FlyingMonster:   {Flyer},
    ImmobileMonster: set(),
    TurretMonster:   {Shooter},
    ShieldedMonster: {Shielded},
}


@pytest.mark.parametrize("monster_type, expected", ABILITIES.items())
def test_each_type_has_exactly_its_abilities(monster_type, expected):
    has = {ability for ability in (Flyer, Shooter, Shielded) if issubclass(monster_type, ability)}
    assert has == expected


def test_monsters_that_cannot_shoot_have_no_shoot_method(player):
    for monster_type in (Monster, FlyingMonster, ShieldedMonster):
        assert not hasattr(monster_type(400, 200, target=player), "shoot")


def test_monsters_without_shield_have_no_shield(player):
    for monster_type in (Monster, FlyingMonster, TurretMonster):
        assert not hasattr(monster_type(400, 200, target=player), "shield")


def test_turret_shoots_at_the_player_after_its_cooldown(board, player):
    turret = TurretMonster(player.pos.x, player.pos.y - 300, target=player, board=board)
    assert turret.shoot() is None                       # still reloading
    turret.update(TurretMonster.FIRE_COOLDOWN)
    bolt = turret.shoot()
    assert isinstance(bolt, EnemyBolt)
    before = bolt.pos.distance_to(player.pos)
    bolt.update(0.1)
    assert bolt.pos.distance_to(player.pos) < before    # flies towards the player
    assert turret.shoot() is None                       # cooldown restarted


def test_shield_absorbs_damage_before_health(player):
    knight = ShieldedMonster(400, 200, target=player)
    knight.take_damage(10)
    assert knight.shield == 20 and knight.health == knight.max_health
    knight.take_damage(25)                              # 20 for the shield, 5 for health
    assert knight.shield == 0 and knight.health == knight.max_health - 5


def test_enemy_bolts_hurt_the_player():
    game = Game()
    for other in list(game.monsters):
        other.kill()
    bolt = EnemyBolt(game.player.pos.x, game.player.pos.y - 40, pygame.Vector2(0, 1), game.board)
    game.enemy_bolts.add(bolt)
    game.all_sprites.add(bolt)
    for _ in range(30):
        game.update(1 / 60)
    assert game.player.health == game.player.max_health - bolt.damage
    assert not bolt.alive()


def test_game_over_when_the_player_has_no_health_left():
    game = Game()
    game.player.take_damage(game.player.max_health)
    game.update(1 / 60)
    assert game.game_over
    position = pygame.Vector2(game.player.pos)
    game.player.direction = pygame.Vector2(1, 0)
    game.update(1 / 60)
    assert game.player.pos == position                  # the game is frozen


def test_restart_after_game_over():
    game = Game()
    game.player.score = 7
    game.player.take_damage(game.player.max_health)
    game.update(1 / 60)
    game.draw()                                         # the GAME OVER screen draws
    game.reset()
    assert not game.game_over
    assert game.player.is_alive and game.player.score == 0
    assert len(game.monsters) > 0
