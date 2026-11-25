"""Levels - the BUILDER pattern.

A Level is a complex object: a world, a background, monsters with their positions,
weapons, rewards with their positions, a difficulty and a goal. LevelBuilder builds
it step by step (each method adds one part and returns the builder, so the steps
can be chained), and build() checks it and returns the finished Level.
LevelDirector knows the recipe of the game's levels and gives the builder the steps
in the right order; another director (or a hand-made sequence of steps) builds other levels
with the same builder.

Positions are fractions of the board (0.0 = left/top, 1.0 = right/bottom), so a level
does not depend on the size of the window.
"""
from dataclasses import dataclass, field


@dataclass
class Level:
    """The product: everything that describes one level."""
    number: int = 1
    world: object = None                     # a WorldFactory
    background: str = ""                     # which arena picture the view shows
    monsters: list = field(default_factory=list)     # [(spawner name, fx, fy), ...]
    weapons: list = field(default_factory=list)      # Weapon objects for the player
    rewards: list = field(default_factory=list)      # [(fx, fy), ...] placed at the start
    difficulty: float = 1.0                  # multiplies the monsters' speed and health
    goal_points: int = 2                     # points to earn in this level


class LevelBuilder:
    """Builds a Level one part at a time."""

    def __init__(self):
        self.reset()

    def reset(self, number=1):
        self._level = Level(number=number)
        return self

    # ---------------------------------------------------------------- steps
    def set_world(self, world):
        self._level.world = world
        return self

    def set_background(self, name):
        self._level.background = name
        return self

    def add_monster(self, kind, fx, fy):
        """One monster of the spawner `kind` (e.g. "zombie") at (fx, fy)."""
        self._level.monsters.append((kind, fx, fy))
        return self

    def add_monster_row(self, kinds, count, fy):
        """`count` monsters spread evenly on a row; their kinds go round `kinds`."""
        for i in range(count):
            fx = (i + 1) / (count + 1)
            self.add_monster(kinds[i % len(kinds)], fx, fy)
        return self

    def set_weapons(self, weapons):
        self._level.weapons = list(weapons)
        return self

    def add_reward(self, fx, fy):
        self._level.rewards.append((fx, fy))
        return self

    def set_difficulty(self, factor):
        self._level.difficulty = factor
        return self

    def set_goal(self, points):
        self._level.goal_points = points
        return self

    # --------------------------------------------------------------- result
    def build(self):
        """Check the level, give it, and get ready for the next one."""
        level = self._level
        if level.world is None:
            raise ValueError("a level needs a world")
        if not level.monsters:
            raise ValueError("a level needs at least one monster")
        if level.goal_points <= 0:
            raise ValueError("a level needs a goal")
        if not level.background:
            level.background = level.world.NAME      # default: the world's own look
        if not level.weapons:
            level.weapons = level.world.create_weapons()
        self.reset(level.number + 1)
        return level


class LevelDirector:
    """The recipe of the levels of Wizard vs Monsters: each level is a bit harder."""
    BACKGROUNDS = {"fantasy": ["dungeon", "forest"], "space": ["space"]}
    GOAL = 2                         # points per level
    DIFFICULTY_STEP = 0.15           # +15 % speed and health per level
    MAX_MONSTERS = 8
    REWARD_SPOTS = [(0.15, 0.75), (0.85, 0.75), (0.5, 0.55)]

    def __init__(self, worlds, builder=None):
        self.worlds = list(worlds)
        self.builder = builder or LevelBuilder()

    def make_level(self, number):
        world = self.worlds[(number - 1) % len(self.worlds)]
        visit = (number - 1) // len(self.worlds)              # how many times this world was used
        backgrounds = self.BACKGROUNDS.get(world.NAME, [world.NAME])
        kinds = list(world.create_spawners())
        count = min(2 + number, self.MAX_MONSTERS)            # 3, 4, 5 ... monsters
        first_row = min(count, 5)

        b = self.builder.reset(number)
        b.set_world(world)
        b.set_background(backgrounds[visit % len(backgrounds)])
        b.add_monster_row(kinds, first_row, 0.10)
        if count > first_row:
            b.add_monster_row(kinds[1:] + kinds[:1], count - first_row, 0.26)
        b.set_weapons(world.create_weapons())
        for fx, fy in self.REWARD_SPOTS[:min(number - 1, len(self.REWARD_SPOTS))]:
            b.add_reward(fx, fy)
        b.set_difficulty(round(1 + self.DIFFICULTY_STEP * (number - 1), 2))
        b.set_goal(self.GOAL)
        return b.build()
