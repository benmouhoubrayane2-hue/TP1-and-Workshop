"""Abstract Factory: each level has its own world, with a compatible set of monsters,
weapons and rewards (a fantasy world and a space world)."""
import inspect

import pygame
import pytest

import model.game_model as game_model_module
from model.game_model import GameModel, LEVEL_GOAL
from model.worlds import WorldFactory, FantasyWorld, SpaceWorld
from model.abilities import Shooter
from model.monster import Monster
from model.rewards import Reward, HealthPotion, EnergyCell
from model.spawners import ClassicSpawner, ZombieSpawner
from model.weapons import Weapon, MagicWand, FireStaff, LaserGun, PlasmaCannon
from model.new_monsters import Zombie, Dragon, Robot
from model.space_monsters import Alien, Ufo
from view.game_view import GameView
from view.theme import ThemeLibrary
from controller.keyboard_controller import KeyboardController
from settings import WINDOW_WIDTH, HEIGHT

FANTASY_MONSTERS = {"zombie", "dragon"} | {t.KIND for t in ClassicSpawner.TYPES}
SPACE_MONSTERS = {"robot", "alien", "ufo"}


def products(world, board, player):
    """Every KIND the world can put in the game: monsters, their shots, weapons' shots, reward."""
    kinds = set()
    for spawner in world.create_spawners().values():
        types = spawner.TYPES if isinstance(spawner, ClassicSpawner) else [None]
        for _ in range(60 if types != [None] else 1):
            monster = spawner.spawn(board, player)
            kinds.add(monster.KIND)
            if isinstance(monster, Shooter):
                monster._reload = 0
                kinds.add(monster.shoot().KIND)
    for weapon in world.create_weapons():
        kinds.add(weapon.fire(100, 100, pygame.Vector2(0, -1), board).KIND)
    kinds.add(world.create_reward(100, 100).KIND)
    return kinds


def key(k):
    return pygame.event.Event(pygame.KEYDOWN, key=k)


# --- The pattern ---------------------------------------------------------------------

def test_the_abstract_factory_cannot_be_used_directly():
    with pytest.raises(TypeError):
        WorldFactory()


@pytest.mark.parametrize("world", [FantasyWorld(), SpaceWorld()], ids=lambda w: w.NAME)
def test_each_world_creates_a_whole_family(world, board, player):
    spawners = world.create_spawners()
    assert len(spawners) == 3
    assert all(isinstance(s.spawn(board, player), Monster) for s in spawners.values())
    assert len(world.create_weapons()) == 2 and all(isinstance(w, Weapon) for w in world.create_weapons())
    assert isinstance(world.create_reward(10, 10), Reward)


def test_the_families_never_mix(board, player):
    fantasy = products(FantasyWorld(), board, player)
    space = products(SpaceWorld(), board, player)
    assert FANTASY_MONSTERS <= fantasy and "potion" in fantasy and "magic_bolt" in fantasy
    assert SPACE_MONSTERS <= space and "energy_cell" in space and "laser_bolt" in space
    assert not (fantasy & SPACE_MONSTERS) and not (space & FANTASY_MONSTERS)
    assert "energy_cell" not in fantasy and "potion" not in space


def test_the_game_only_knows_the_abstract_factory():
    source = inspect.getsource(game_model_module)
    for concrete in ("FantasyWorld", "SpaceWorld", "HealthPotion(", "EnergyCell(",
                     "MagicWand(", "LaserGun(", "Zombie(", "Robot("):
        assert concrete not in source


# --- Levels and worlds in the game ----------------------------------------------------

def test_level_1_fantasy_then_level_2_space_then_fantasy_again():
    game = GameModel()
    assert game.world_name == "fantasy" and isinstance(game.player.weapon, MagicWand)
    assert {m.KIND for m in game.monsters} <= FANTASY_MONSTERS

    game.next_level()
    assert (game.level, game.world_name) == (2, "space")
    assert [type(w) for w in game.player.weapons] == [LaserGun, PlasmaCannon]
    assert {m.KIND for m in game.monsters} <= SPACE_MONSTERS

    game.next_level()
    assert game.world_name == "fantasy" and isinstance(game.player.weapons[1], FireStaff)


def test_reaching_the_goal_starts_the_next_level():
    game = GameModel()
    for monster in list(game.monsters):
        monster.kill()
    game.player.score = LEVEL_GOAL - 1
    target = Monster(game.player.pos.x, game.player.pos.y - 200, game.player)
    target.speed = 0
    game.add_monster(target)
    game.set_trigger(True)
    for _ in range(120):
        game.update(1 / 60)
        if game.level == 2:
            break
    assert game.level == 2 and game.world_name == "space"
    assert "level" in [e.kind for e in game.pop_events()]


@pytest.mark.parametrize("level, reward_type", [(1, HealthPotion), (2, EnergyCell)])
def test_defeated_monsters_leave_the_reward_of_their_world(level, reward_type):
    game = GameModel()
    if level == 2:
        game.next_level()
    game.reward_chance = 1.0
    for obj in list(game.monsters) + list(game.rewards):   # also the rewards placed by the level
        obj.kill()
    target = Monster(game.player.pos.x, game.player.pos.y - 250, game.player)
    target.speed = 0
    game.add_monster(target)
    game.set_trigger(True)
    for _ in range(240):
        game.update(1 / 60)
        if game.rewards:
            break
    assert [type(r) for r in game.rewards] == [reward_type]


def test_picking_up_rewards():
    game = GameModel()
    game.player.take_damage(50)
    game.drop_reward(game.player.pos)            # a health potion, right under the wizard
    game.update(1 / 60)
    assert game.player.health == 50 + HealthPotion.HEAL and not game.rewards
    assert "reward" in [e.kind for e in game.pop_events()]

    game.next_level()                            # space: the energy cell also gives points
    score = game.score
    game.drop_reward(game.player.pos)
    game.update(1 / 60)
    assert game.score == score + EnergyCell.POINTS


def test_a_reward_disappears_after_a_while():
    game = GameModel()
    game.drop_reward(pygame.Vector2(100, 100))
    for _ in range(int(60 * (HealthPotion.LIFETIME + 0.5))):
        game.update(1 / 60)
    assert not game.rewards


def test_a_new_world_only_needs_a_new_factory():
    class IceWorld(WorldFactory):
        NAME = "ice"

        def create_spawners(self):
            return {"zombie": ZombieSpawner()}

        def create_weapons(self):
            return [MagicWand()]

        def create_reward(self, x, y):
            return HealthPotion(x, y)

    game = GameModel(worlds=[IceWorld()])
    assert game.world_name == "ice" and {m.KIND for m in game.monsters} == {"zombie"}


# --- Controller and view -------------------------------------------------------------

def test_the_world_cannot_be_changed_from_the_keyboard():
    game = GameModel()
    controller = KeyboardController(game)
    for k in (pygame.K_n, pygame.K_w, pygame.K_l, pygame.K_TAB, pygame.K_t):
        controller.handle_event(key(k))
    assert (game.level, game.world_name) == (1, "fantasy")     # only reaching the goal changes it


def test_keys_3_4_5_summon_the_monsters_of_the_current_world():
    game = GameModel()
    controller = KeyboardController(game)
    game.next_level()                                          # as when the goal is reached
    for monster in list(game.monsters):
        monster.kill()
    for k in (pygame.K_3, pygame.K_4, pygame.K_5):
        controller.handle_event(key(k))
    assert [m.KIND for m in game.monsters] == ["robot", "alien", "ufo"]


def test_the_view_switches_to_a_theme_of_the_new_world():
    game = GameModel()
    view = GameView(game, pygame.Surface((WINDOW_WIDTH, HEIGHT)))
    view.render(0)
    assert view.theme.world == "fantasy"
    game.next_level()
    view.render(0)
    assert view.theme.name == "Space"
    view.next_theme()                                      # T stays in the space world
    assert view.theme.world == "space"


@pytest.mark.parametrize("world", [FantasyWorld(), SpaceWorld()], ids=lambda w: w.NAME)
def test_every_theme_of_a_world_has_a_picture_for_its_products(world, board, player):
    themes = [t for t in ThemeLibrary().themes if t.world == world.NAME]
    assert themes
    for theme in themes:
        for kind in products(world, board, player) | {"player"}:
            assert theme.image_path(kind) and theme.image_path(kind).exists(), (theme.name, kind)


def test_space_monsters_and_weapons():
    assert issubclass(Ufo, Shooter) and not issubclass(Alien, Shooter)
    assert LaserGun.COOLDOWN < PlasmaCannon.COOLDOWN
    game = GameModel()
    robot = Robot(400, 200, game.player)
    assert game.damage_calculator.compute(25, "plasma", robot) == 50      # electric shock
    assert game.damage_calculator.compute(8, "laser", robot) == 4


def test_a_new_world_every_2_points():
    game = GameModel()
    assert game.level_goal == 2
    game.player.score = 2
    game.update(1 / 60)
    assert (game.level, game.world_name, game.level_goal) == (2, "space", 4)
    game.player.score = 4
    game.update(1 / 60)
    assert (game.level, game.world_name) == (3, "fantasy")


def test_no_new_level_once_the_wizard_is_dead():
    game = GameModel()
    game.player.score = 5
    game.player.take_damage(game.player.max_health)
    game.update(1 / 60)
    assert game.game_over and game.level == 1
