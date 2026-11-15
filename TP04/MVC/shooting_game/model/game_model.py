"""GameModel: the state and the rules of the game (the M of MVC).

It holds the board, the player, the monsters and the projectiles, applies the
rules every frame and records what happened as GameEvents. It never draws,
never plays a sound and never reads the keyboard.
"""
import random

import pygame
from settings import WIDTH, HEIGHT, MONSTER_COUNT, KNOCKBACK_DISTANCE
from model.board import GameBoard
from model.player import Player
from model.monster_types import MONSTER_TYPES
from model.abilities import Shooter
from model.damage import ResistanceCalculator
from model.game_interface import GameModelInterface
from model.events import GameEvent, SHOT, HIT, MONSTER_DEFEATED, PLAYER_HURT, GAME_OVER

PLAYING = "Playing"
PAUSED = "Paused"
GAME_OVER_STATUS = "Game over"


class GameModel(GameModelInterface):

    def __init__(self, damage_calculator=None, width=WIDTH, height=HEIGHT):
        """`damage_calculator`: any DamageCalculator (DIP: the model depends on the abstraction)."""
        self.damage_calculator = damage_calculator or ResistanceCalculator()
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
        self.game_over = False
        self.paused = False
        self.events = []                           # what happened since the view last looked
        for _ in range(MONSTER_COUNT):
            self.spawn_monster()

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
            "Weapon": self.player.weapon.NAME,
            "Monsters": len(self.monsters),
            "Status": self.status,
        }

    def spawn_monster(self):
        """Create a monster of a random type and register it."""
        monster_type = random.choice(MONSTER_TYPES)
        self.add_monster(monster_type.spawn_random(self.board, target=self.player))

    def add_monster(self, monster):
        self.monsters.add(monster)
        self.objects.add(monster)

    def drawables(self):
        """What the view draws, back to front."""
        return [*self.monsters, self.player, *self.bullets, *self.enemy_bolts]

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
                self.spawn_monster()

        for bolt in pygame.sprite.spritecollide(self.player, self.enemy_bolts, True):
            self.hurt_player(bolt.damage)

        for monster in pygame.sprite.spritecollide(self.player, self.monsters, False):
            if self.hurt_player(monster.CONTACT_DAMAGE):
                self.knock_back(monster)

        if not self.player.is_alive and not self.game_over:
            self.game_over = True
            self.events.append(GameEvent(GAME_OVER, pygame.Vector2(self.player.pos), self.score))

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
