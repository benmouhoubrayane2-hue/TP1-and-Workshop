"""Factory Method: different monsters on demand (Zombie, Dragon, Robot) created by spawners."""
import inspect
from pathlib import Path

import pygame
import pytest

import model.game_model as game_model_module
from model.game_model import GameModel
from model.monster import Monster
from model.abilities import Flyer, Shooter, Shielded
from model.new_monsters import Zombie, Dragon, Robot, DragonFire
from model.spawners import (MonsterSpawner, ZombieSpawner, DragonSpawner, RobotSpawner,
                            ClassicSpawner, default_spawners)
from controller.keyboard_controller import KeyboardController

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = [(ZombieSpawner, Zombie), (DragonSpawner, Dragon), (RobotSpawner, Robot)]


def empty_game(**kwargs):
    game = GameModel(**kwargs)
    for monster in list(game.monsters):
        monster.kill()
    return game


# --- The pattern ------------------------------------------------------------------

def test_the_creator_is_abstract():
    with pytest.raises(TypeError):
        MonsterSpawner()


@pytest.mark.parametrize("spawner_type, product", PRODUCTS)
def test_each_spawner_overrides_only_the_factory_method(spawner_type, product):
    assert issubclass(spawner_type, MonsterSpawner)
    assert "create_monster" in spawner_type.__dict__
    assert "spawn" not in spawner_type.__dict__           # spawn() is inherited, written once


@pytest.mark.parametrize("spawner_type, product", PRODUCTS)
def test_spawn_creates_the_right_monster_at_the_top_of_the_board(spawner_type, product, board, player):
    monster = spawner_type().spawn(board, player)
    assert type(monster) is product and isinstance(monster, Monster)
    assert board.rect.collidepoint(monster.pos) and monster.pos.y < board.rect.centery


def test_classic_spawner_still_creates_the_old_monsters(board, player):
    kinds = {ClassicSpawner().spawn(board, player).KIND for _ in range(200)}
    assert {"monster", "monster_fast", "monster_turret"} <= kinds


def test_the_game_never_creates_a_concrete_monster_itself():
    source = inspect.getsource(game_model_module)
    for name in ("Zombie(", "Dragon(", "Robot(", "Monster(", "MONSTER_TYPES"):
        assert name not in source


# --- On demand, several types in the same game ------------------------------------

@pytest.mark.parametrize("key, product", [(pygame.K_3, Zombie), (pygame.K_4, Dragon), (pygame.K_5, Robot)])
def test_keys_3_4_5_summon_a_monster_on_demand(key, product):
    game = empty_game(spawners=default_spawners())          # zombie, dragon, robot (+ classic)
    game.spawners.pop("classic")
    KeyboardController(game).handle_event(pygame.event.Event(pygame.KEYDOWN, key=key))
    assert [type(m) for m in game.monsters] == [product]


def test_the_three_types_coexist_in_the_same_game():
    game = empty_game(spawners=default_spawners())
    for name in ("zombie", "dragon", "robot", "zombie"):
        assert game.summon(name)
    assert sorted(m.KIND for m in game.monsters) == ["dragon", "robot", "zombie", "zombie"]
    for _ in range(60):
        game.update(1 / 60)                                # they all live together


def test_no_summon_when_paused_or_unknown():
    game = empty_game()
    assert not game.summon("unicorn")
    game.toggle_pause()
    assert not game.summon("zombie")
    assert len(game.monsters) == 0


def test_a_new_kind_of_monster_only_needs_a_new_spawner():
    """Open/Closed: the game is not modified to create a monster it has never seen."""
    class Ghost(Monster):
        KIND = "ghost"

    class GhostSpawner(MonsterSpawner):
        NAME = "ghost"

        def create_monster(self, x, y, target, board):
            return Ghost(x, y, target)

    game = empty_game(spawners={"ghost": GhostSpawner()})
    assert game.summon("ghost")
    game.spawn_monster()
    assert [m.KIND for m in game.monsters] == ["ghost", "ghost"]


def test_default_spawners_have_unique_names():
    spawners = default_spawners()
    assert set(spawners) == {"classic", "zombie", "dragon", "robot"}


# --- The three new monsters -------------------------------------------------------

def test_each_new_monster_has_only_its_abilities():
    assert issubclass(Dragon, Flyer) and issubclass(Dragon, Shooter) and not issubclass(Dragon, Shielded)
    assert issubclass(Robot, Shielded) and not issubclass(Robot, Shooter)
    assert not any(issubclass(Zombie, a) for a in (Flyer, Shooter, Shielded))


def test_zombie_is_slower_than_a_normal_monster(player):
    zombie = Zombie(player.pos.x, player.pos.y - 300, player)
    normal = Monster(player.pos.x, player.pos.y - 300, player)
    for _ in range(60):
        zombie.update(1 / 60)
        normal.update(1 / 60)
    assert zombie.pos.distance_to(player.pos) > normal.pos.distance_to(player.pos)


def test_robot_moves_on_one_axis_at_a_time(player):
    robot = Robot(player.pos.x - 300, player.pos.y - 100, player)
    start = pygame.Vector2(robot.pos)
    robot.update(0.5)
    assert robot.pos.y == start.y and robot.pos.x > start.x    # only horizontally first


def test_robot_armour_absorbs_damage_first(player):
    robot = Robot(400, 200, player)
    robot.take_damage(30)
    assert robot.health == robot.max_health and robot.shield == 10


def test_dragon_spits_fire_at_the_player(board, player):
    dragon = Dragon(player.pos.x, player.pos.y - 300, player, board)
    assert dragon.shoot() is None                              # still reloading
    dragon.update(Dragon.FIRE_COOLDOWN)
    fire = dragon.shoot()
    assert isinstance(fire, DragonFire) and fire.damage == DragonFire.DAMAGE
    assert fire.direction.y > 0                                # aimed down at the player


def test_dragon_fire_hurts_the_player_in_the_game():
    game = empty_game()
    dragon = Dragon(game.player.pos.x, game.player.pos.y - 200, game.player, game.board)
    dragon.speed = 0
    dragon.update(Dragon.FIRE_COOLDOWN)
    game.add_monster(dragon)
    for _ in range(120):
        game.update(1 / 60)
    assert game.player.health < game.player.max_health


def test_dragon_is_immune_to_fire():
    game = empty_game()
    dragon = Dragon(400, 200, game.player)
    assert game.damage_calculator.compute(20, "fire", dragon) == 0
    assert game.damage_calculator.compute(10, "magic", dragon) == 15
