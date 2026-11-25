"""GameModel: the state and the rules of the game (the M of MVC).

It holds the board, the player, the monsters and the projectiles, applies the
rules every frame and records what happened as GameEvents. It never draws,
never plays a sound and never reads the keyboard.
"""
import random

import pygame
from settings import WIDTH, HEIGHT, KNOCKBACK_DISTANCE
from model.board import GameBoard
from model.player import Player
from model.worlds import default_worlds
from model.level_builder import LevelDirector
from model.abilities import Shooter
from model.damage import ResistanceCalculator
from model.game_interface import GameModelInterface
from model.events import (GameEvent, SHOT, HIT, MONSTER_DEFEATED, PLAYER_HURT, GAME_OVER,
                          REWARD, LEVEL)

PLAYING = "Playing"
PAUSED = "Paused"
GAME_OVER_STATUS = "Game over"
LEVEL_GOAL = LevelDirector.GOAL     # points needed to finish each level
PLACED_REWARD_LIFETIME = 30         # seconds: rewards placed by the level last longer
REWARD_CHANCE = 0.35     # chance that a defeated monster leaves a reward


class GameModel(GameModelInterface):

    def __init__(self, damage_calculator=None, width=WIDTH, height=HEIGHT, spawners=None, worlds=None,
                 director=None):
        """`damage_calculator`: any DamageCalculator (DIP: the model depends on the abstraction).
        `worlds`: the WorldFactory of each level (Abstract Factory) - monsters, weapons, rewards.
        `director`: builds each Level with a LevelBuilder (Builder pattern).
        `spawners`: optional {name: MonsterSpawner} used instead of the worlds' monsters."""
        self.damage_calculator = damage_calculator or ResistanceCalculator()
        self.worlds = list(worlds) if worlds else default_worlds()
        self.director = director or LevelDirector(self.worlds)
        self._fixed_spawners = dict(spawners) if spawners else None
        self.width = width
        self.height = height
        self.reset()

    # ------------------------------------------------------------------ state
    def reset(self):
        """Create a new board, player and monsters (start or restart a game)."""
        self.board = GameBoard(self.width, self.height)
        self.player = Player(self.board)
        self.objects = pygame.sprite.Group(self.player)   # everything that updates itself
        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bolts = pygame.sprite.Group()   # fired by Shooter monsters
        self.rewards = pygame.sprite.Group()       # dropped by defeated monsters
        self.reward_chance = REWARD_CHANCE
        self.game_over = False
        self.paused = False
        self.events = []                           # what happened since the view last looked
        self.level = 1
        self.start_level()
        self.goal = self.plan.goal_points

    # ------------------------------------------------------------ levels & worlds
    @property
    def world(self):
        """The WorldFactory of the current level (chosen by the level)."""
        return self.plan.world

    @property
    def world_name(self):
        return self.world.NAME

    @property
    def background_name(self):
        """The arena picture chosen by the level (the view shows it)."""
        return self.plan.background

    @property
    def level_goal(self):
        return self.goal

    def place(self, fx, fy):
        """A position given as fractions of the board -> a point on the board."""
        r = self.board.rect
        return pygame.Vector2(r.left + fx * r.width, r.top + fy * r.height)

    def start_level(self):
        """Ask the director for the Level (Builder) and set it up: world, weapons,
        monsters at their positions, rewards at their positions, difficulty."""
        self.plan = self.director.make_level(self.level)
        self.spawners = self._fixed_spawners or self.plan.world.create_spawners()
        self.player.weapons = list(self.plan.weapons)
        self.player.switch_weapon(0)
        for group in (self.monsters, self.bullets, self.enemy_bolts, self.rewards):
            for obj in list(group):
                obj.kill()
        self.player.heal(self.player.max_health)
        for kind, fx, fy in self.plan.monsters:
            spawner = self.spawners.get(kind) or next(iter(self.spawners.values()))
            pos = self.place(fx, fy)
            self.add_monster(spawner.create_monster(pos.x, pos.y, self.player, self.board))
        for fx, fy in self.plan.rewards:
            self.drop_reward(self.place(fx, fy), lifetime=PLACED_REWARD_LIFETIME)

    def next_level(self):
        """Go to the next level, in the next world - only when the level's goal is reached."""
        if self.game_over:
            return
        self.level += 1
        self.start_level()
        self.goal = self.score + self.plan.goal_points
        self.events.append(GameEvent(LEVEL, pygame.Vector2(self.player.pos), self.level, name=self.world.NAME))

    @property
    def score(self):
        return self.player.score

    @property
    def status(self):
        if self.game_over:
            return GAME_OVER_STATUS
        return PAUSED if self.paused else PLAYING

    def info(self):
        """What the information panel shows, as plain data (the view decides how).
        A pair (current, maximum) is shown as a bar."""
        return {
            "Score": self.score,
            "Health": (self.player.health, self.player.max_health),
            "Level": f"{self.level} - {self.world.NAME.title()}",
            "Next level": (self.score, self.level_goal),
            "Difficulty": f"x{self.plan.difficulty:.2f}  ({len(self.plan.monsters)} monsters)",
            "Weapon": self.player.weapon.NAME,
            "Status": self.status,
        }

    def spawn_monster(self):
        """Ask a random spawner (Factory Method) for a monster and register it."""
        spawner = random.choice(list(self.spawners.values()))
        self.add_monster(spawner.spawn(self.board, target=self.player))

    def summon(self, name):
        """Create a monster of the kind `name` now ("on demand", keys 3/4/5).
        Returns False if there is no spawner of that name or the game is stopped."""
        if self.game_over or self.paused or name not in self.spawners:
            return False
        self.add_monster(self.spawners[name].spawn(self.board, target=self.player))
        return True

    def summon_slot(self, number):
        """Summon the monster number 0, 1 or 2 of the current world (keys 3, 4, 5)."""
        names = list(self.spawners)
        return number < len(names) and self.summon(names[number])

    def add_monster(self, monster):
        """Every new monster gets the difficulty of the current level."""
        if self.plan.difficulty != 1:
            monster.strengthen(self.plan.difficulty)
        self.monsters.add(monster)
        self.objects.add(monster)

    def drawables(self):
        """What the view draws, back to front."""
        return [*self.rewards, *self.monsters, self.player, *self.bullets, *self.enemy_bolts]

    def pop_events(self):
        """Give the events to the view and forget them."""
        events, self.events = self.events, []
        return events

    # --------------------------------------------- commands (from the controller)
    def move_player(self, direction):
        self.player.direction = pygame.Vector2(direction)

    def set_trigger(self, pressed):
        self.player.trigger_pressed = bool(pressed)

    def switch_weapon(self, index=None):
        self.player.switch_weapon(index)

    def toggle_pause(self):
        """Freeze or unfreeze the game (not once it is over)."""
        if not self.game_over:
            self.paused = not self.paused

    def restart(self):
        """Start a new game - only allowed once the current one is over."""
        if self.game_over:
            self.reset()

    # ------------------------------------------------------------------ rules
    def update(self, dt):
        """Every object updates itself, then shooting and hits are resolved."""
        if self.game_over or self.paused:
            return
        self.objects.update(dt)            # polymorphism: player, monsters AND projectiles

        if self.player.trigger_pressed:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.add(bullet)
                self.objects.add(bullet)
                self.events.append(GameEvent(SHOT, pygame.Vector2(bullet.pos), name=bullet.KIND))

        for monster in self.monsters:      # only monsters that CAN shoot are asked to
            if isinstance(monster, Shooter):
                bolt = monster.shoot()
                if bolt:
                    self.enemy_bolts.add(bolt)
                    self.objects.add(bolt)

        self.handle_hits()

    def handle_hits(self):
        """Projectiles that touch a monster disappear and damage it; monsters and
        enemy bolts that touch the wizard hurt him."""
        hits = pygame.sprite.groupcollide(self.monsters, self.bullets, False, True)
        for monster, bullets in hits.items():
            for bullet in bullets:
                damage = self.damage_calculator.compute(bullet.damage, bullet.damage_type, monster)
                monster.take_damage(damage)
                self.events.append(GameEvent(HIT, pygame.Vector2(monster.pos.x, monster.rect.top),
                                             damage, bullet.damage))
            if not monster.is_alive:
                monster.kill()
                self.player.score += monster.POINTS
                self.events.append(GameEvent(MONSTER_DEFEATED, pygame.Vector2(monster.pos), monster.POINTS))
                if random.random() < self.reward_chance:
                    self.drop_reward(monster.pos)
                self.spawn_monster()

        for reward in pygame.sprite.spritecollide(self.player, self.rewards, True):
            reward.apply(self.player)
            self.events.append(GameEvent(REWARD, pygame.Vector2(reward.pos), name=reward.KIND))


        for bolt in pygame.sprite.spritecollide(self.player, self.enemy_bolts, True):
            self.hurt_player(bolt.damage)

        for monster in pygame.sprite.spritecollide(self.player, self.monsters, False):
            if self.hurt_player(monster.CONTACT_DAMAGE):
                self.knock_back(monster)

        if not self.player.is_alive and not self.game_over:
            self.game_over = True
            self.events.append(GameEvent(GAME_OVER, pygame.Vector2(self.player.pos), self.score))
        elif not self.game_over and self.score >= self.level_goal:
            self.next_level()              # goal reached (only if the wizard is still alive)

    def drop_reward(self, pos, lifetime=None):
        """The current world decides which reward appears (Abstract Factory)."""
        reward = self.world.create_reward(pos.x, pos.y)
        if lifetime is not None:
            reward.time_left = lifetime
        self.rewards.add(reward)
        self.objects.add(reward)

    def hurt_player(self, amount):
        if self.player.hit(amount):
            self.events.append(GameEvent(PLAYER_HURT, pygame.Vector2(self.player.pos), amount))
            return True
        return False

    def knock_back(self, monster):
        """Push a monster away from the wizard after it bites, so it does not stick to him."""
        away = monster.pos - self.player.pos
        if away.length_squared() == 0:
            away = pygame.Vector2(0, -1)
        monster.pos += away.normalize() * KNOCKBACK_DISTANCE
        self.board.keep_inside(monster)
