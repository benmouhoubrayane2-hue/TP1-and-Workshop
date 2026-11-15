"""CrystalHuntModel: the rules of the second game (model only).

The wizard collects crystals before the time runs out, while rocks fall from the
sky. He can destroy the rocks with his bolts; a rock that hits him hurts him.
It reuses the existing model parts (Player, GameBoard, GameObject, weapons, events)
and implements GameModelInterface, so the same View and Controller can show and drive it.
"""
import random

import pygame
from settings import WIDTH, HEIGHT
from model.game_interface import GameModelInterface
from model.game_object import GameObject
from model.board import GameBoard
from model.player import Player
from model.events import GameEvent, SHOT, PLAYER_HURT, MONSTER_DEFEATED, GAME_OVER

COLLECTED = "collected"          # new event of this game (the theme gives it a sound)


class Crystal(GameObject):
    KIND = "crystal"
    SIZE = (40, 48)
    POINTS = 1

    def __init__(self, x, y):
        super().__init__(x, y, 0, self.SIZE)

    def update(self, dt):
        """A crystal does not move."""


class Rock(GameObject):
    KIND = "rock"
    SIZE = (56, 56)
    DAMAGE = 20

    def __init__(self, x, y, speed, board):
        super().__init__(x, y, speed, self.SIZE)
        self.board = board

    def update(self, dt):
        self.move(pygame.Vector2(0, 1), dt)          # falls straight down
        if self.board.is_outside(self):
            self.kill()


class CrystalHuntModel(GameModelInterface):
    TIME_LIMIT = 60          # seconds
    CRYSTAL_COUNT = 3        # crystals on the board at the same time
    ROCK_INTERVAL = 0.8      # seconds between two falling rocks

    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.board = GameBoard(self.width, self.height)
        self.player = Player(self.board)            # same wizard, same weapons
        self.objects = pygame.sprite.Group(self.player)
        self.crystals = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.time_left = float(self.TIME_LIMIT)
        self.game_over = False
        self.paused = False
        self.events = []
        self._next_rock = self.ROCK_INTERVAL
        for _ in range(self.CRYSTAL_COUNT):
            self.spawn_crystal()

    # ------------------------------------------------------------- state
    @property
    def score(self):
        return self.player.score

    @property
    def status(self):
        if self.game_over:
            return "Game over"
        return "Paused" if self.paused else "Playing"

    def info(self):
        return {
            "Score": self.score,
            "Health": (self.player.health, self.player.max_health),
            "Time": (max(0, round(self.time_left)), self.TIME_LIMIT),   # shown as a bar too
            "Weapon": self.player.weapon.NAME,
            "Status": self.status,
        }

    def drawables(self):
        return [*self.crystals, *self.rocks, self.player, *self.bullets]

    def pop_events(self):
        events, self.events = self.events, []
        return events

    def spawn_crystal(self):
        r = self.board.rect.inflate(-120, -160)
        crystal = Crystal(random.randint(r.left, r.right), random.randint(r.top, r.bottom))
        self.crystals.add(crystal)
        self.objects.add(crystal)

    def spawn_rock(self):
        pos = self.board.random_top_position(margin=Rock.SIZE[0])
        rock = Rock(pos.x, pos.y, random.randint(140, 240), self.board)
        self.rocks.add(rock)
        self.objects.add(rock)

    # ---------------------------------------------- commands (controller)
    def move_player(self, direction):
        self.player.direction = pygame.Vector2(direction)

    def set_trigger(self, pressed):
        self.player.trigger_pressed = bool(pressed)

    def switch_weapon(self, index=None):
        self.player.switch_weapon(index)

    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused

    def restart(self):
        if self.game_over:
            self.reset()

    # -------------------------------------------------------------- rules
    def update(self, dt):
        if self.game_over or self.paused:
            return
        self.time_left -= dt
        self.objects.update(dt)

        if self.player.trigger_pressed:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.add(bullet)
                self.objects.add(bullet)
                self.events.append(GameEvent(SHOT, pygame.Vector2(bullet.pos), name=bullet.KIND))

        self._next_rock -= dt
        if self._next_rock <= 0:
            self._next_rock = self.ROCK_INTERVAL
            self.spawn_rock()

        for crystal in pygame.sprite.spritecollide(self.player, self.crystals, True):
            self.player.score += crystal.POINTS
            self.events.append(GameEvent(COLLECTED, pygame.Vector2(crystal.pos), crystal.POINTS))
            self.spawn_crystal()

        for rock in pygame.sprite.groupcollide(self.rocks, self.bullets, True, True):
            self.events.append(GameEvent(MONSTER_DEFEATED, pygame.Vector2(rock.pos)))

        for rock in pygame.sprite.spritecollide(self.player, self.rocks, True):
            if self.player.hit(Rock.DAMAGE):
                self.events.append(GameEvent(PLAYER_HURT, pygame.Vector2(self.player.pos), Rock.DAMAGE))

        if self.time_left <= 0 or not self.player.is_alive:
            self.time_left = max(0.0, self.time_left)
            self.game_over = True
            self.events.append(GameEvent(GAME_OVER, pygame.Vector2(self.player.pos), self.score))
