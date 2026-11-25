"""Builder: each level is built step by step - background, monsters, weapons, rewards,
their positions, difficulty and goal."""
import pygame
import pytest

from model.game_model import GameModel
from model.level_builder import Level, LevelBuilder, LevelDirector
from model.worlds import FantasyWorld, SpaceWorld, default_worlds
from model.weapons import LaserGun, MagicWand
from model.rewards import HealthPotion, EnergyCell
from model.new_monsters import Zombie, Dragon
from view.game_view import GameView
from settings import WINDOW_WIDTH, HEIGHT


# --- The builder ---------------------------------------------------------------------

def test_a_level_is_built_step_by_step():
    level = (LevelBuilder()
             .set_world(FantasyWorld())
             .set_background("forest")
             .add_monster("dragon", 0.5, 0.2)
             .add_monster_row(["zombie"], 3, 0.1)
             .add_reward(0.2, 0.8)
             .set_difficulty(1.5)
             .set_goal(4)
             .build())
    assert isinstance(level, Level) and level.background == "forest"
    assert level.monsters == [("dragon", 0.5, 0.2), ("zombie", 0.25, 0.1),
                              ("zombie", 0.5, 0.1), ("zombie", 0.75, 0.1)]
    assert level.rewards == [(0.2, 0.8)] and level.difficulty == 1.5 and level.goal_points == 4
    assert isinstance(level.weapons[0], MagicWand)          # default: the world's weapons


@pytest.mark.parametrize("steps, message", [
    (lambda b: b.add_monster("zombie", 0.5, 0.1), "world"),
    (lambda b: b.set_world(FantasyWorld()), "monster"),
    (lambda b: b.set_world(FantasyWorld()).add_monster("zombie", 0.5, 0.1).set_goal(0), "goal"),
])
def test_build_refuses_an_incomplete_level(steps, message):
    builder = LevelBuilder()
    steps(builder)
    with pytest.raises(ValueError, match=message):
        builder.build()


def test_the_builder_is_ready_for_a_new_level_after_build():
    builder = LevelBuilder().set_world(SpaceWorld()).add_monster("robot", 0.5, 0.1)
    first = builder.build()
    second = builder.set_world(SpaceWorld()).add_monster("alien", 0.3, 0.1).build()
    assert first.monsters == [("robot", 0.5, 0.1)] and second.monsters == [("alien", 0.3, 0.1)]
    assert first.background == "space"                       # default: the world's own look


# --- The director: each level is harder ---------------------------------------------

def test_the_director_builds_harder_and_harder_levels():
    director = LevelDirector(default_worlds())
    levels = [director.make_level(n) for n in range(1, 6)]
    assert [lv.world.NAME for lv in levels] == ["fantasy", "space", "fantasy", "space", "fantasy"]
    assert [lv.background for lv in levels] == ["dungeon", "space", "forest", "space", "dungeon"]
    assert [len(lv.monsters) for lv in levels] == [3, 4, 5, 6, 7]
    assert [lv.difficulty for lv in levels] == [1.0, 1.15, 1.3, 1.45, 1.6]
    assert [len(lv.rewards) for lv in levels] == [0, 1, 2, 3, 3]
    assert all(lv.goal_points == 2 for lv in levels)


def test_level_monsters_are_of_their_world_and_inside_the_board():
    director = LevelDirector(default_worlds())
    space = director.make_level(4)
    assert {kind for kind, _, _ in space.monsters} == {"robot", "alien", "ufo"}
    assert all(0 < fx < 1 and 0 < fy < 1 for _, fx, fy in space.monsters + [(None, *r) for r in space.rewards])


# --- The game plays the built levels ----------------------------------------------------

def test_the_game_places_the_monsters_and_rewards_where_the_level_says():
    game = GameModel()
    game.next_level()                                        # level 2, space
    plan = game.plan
    assert len(game.monsters) == len(plan.monsters) == 4
    for monster, (kind, fx, fy) in zip(game.monsters, plan.monsters):
        assert monster.KIND == kind and monster.pos == game.place(fx, fy)
    assert [type(r) for r in game.rewards] == [EnergyCell]
    assert game.rewards.sprites()[0].pos == game.place(*plan.rewards[0])
    assert isinstance(game.player.weapon, LaserGun)


def test_monsters_are_faster_and_tougher_in_harder_levels():
    game = GameModel()
    for _ in range(2):
        game.next_level()                                    # level 3, difficulty x1.3
    zombies = [m for m in game.monsters if isinstance(m, Zombie)]
    assert zombies and zombies[0].speed == pytest.approx(Zombie.SPEED * 1.3)
    assert zombies[0].max_health == round(Zombie.MAX_HEALTH * 1.3)
    game.summon("zombie")                                    # new monsters too
    newest = [m for m in game.monsters if isinstance(m, Zombie)][-1]
    assert newest.speed == pytest.approx(Zombie.SPEED * 1.3)


def test_the_goal_is_2_more_points_each_level():
    game = GameModel()
    assert game.level_goal == 2
    game.player.score = 3                                    # one point too many
    game.update(1 / 60)
    assert game.level == 2 and game.level_goal == 5


def test_a_hand_made_level_can_be_played():
    class BossDirector(LevelDirector):
        def make_level(self, number):
            return (LevelBuilder()
                    .set_world(FantasyWorld())
                    .set_background("forest")
                    .add_monster("dragon", 0.5, 0.15)
                    .add_monster("zombie", 0.2, 0.3)
                    .add_monster("zombie", 0.8, 0.3)
                    .add_reward(0.5, 0.7)
                    .set_difficulty(2.0)
                    .build())

    game = GameModel(director=BossDirector(default_worlds()))
    assert sorted(m.KIND for m in game.monsters) == ["dragon", "zombie", "zombie"]
    dragon = next(m for m in game.monsters if isinstance(m, Dragon))
    assert dragon.max_health == Dragon.MAX_HEALTH * 2
    assert [type(r) for r in game.rewards] == [HealthPotion]


def test_the_view_shows_the_background_chosen_by_the_level():
    game = GameModel()
    view = GameView(game, pygame.Surface((WINDOW_WIDTH, HEIGHT)))
    view.render(0)
    assert view.theme.name == "Dungeon"                      # level 1
    game.next_level()
    view.render(0)
    assert view.theme.name == "Space"                        # level 2
    game.next_level()
    view.render(0)
    assert view.theme.name == "Forest"                       # level 3


def test_the_panel_shows_the_difficulty():
    game = GameModel()
    game.next_level()
    assert game.info()["Difficulty"] == "x1.15  (4 monsters)"
