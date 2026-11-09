"""Entry point of the 2D shooting game."""
import random

import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS, BG_COLOR, MONSTER_COUNT, KNOCKBACK_DISTANCE
from board import GameBoard
from player import Player
from monster_types import MONSTER_TYPES
from health_bar import HealthBar
from shield_view import ShieldView
from game_over_view import GameOverView
from abilities import Shooter, Shielded
from damage import ResistanceCalculator
from damage_text import DamageText


class Game:
    """Owns the window, the clock and the main loop."""

    def __init__(self, damage_calculator=None):
        """`damage_calculator`: any DamageCalculator (DIP: the game depends on the abstraction)."""
        pygame.init()
        self.damage_calculator = damage_calculator or ResistanceCalculator()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.health_bar = HealthBar()        # view component for health
        self.shield_view = ShieldView()      # view component for shields
        self.game_over_view = GameOverView() # view component for the end screen
        self.reset()

    def reset(self):
        """Create a new board, player and monsters (start or restart a game)."""
        self.board = GameBoard(WIDTH, HEIGHT)
        self.player = Player(self.board)
        self.all_sprites = pygame.sprite.Group(self.player)   # everything to update and draw
        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bolts = pygame.sprite.Group()   # fired by Shooter monsters
        self.effects = pygame.sprite.Group()       # floating damage numbers, drawn on top
        self.game_over = False
        for _ in range(MONSTER_COUNT):
            self.spawn_monster()
        self.update_caption()

    def update_caption(self):
        """Window title: score and weapon in hand (or GAME OVER)."""
        if self.game_over:
            pygame.display.set_caption(f"{TITLE}  -  GAME OVER  -  Score: {self.player.score}")
        else:
            pygame.display.set_caption(f"{TITLE}  -  Score: {self.player.score}"
                                       f"  -  Weapon: {self.player.weapon.NAME}")

    def spawn_monster(self):
        """Create a monster of a random type and register it in the right groups."""
        monster_type = random.choice(MONSTER_TYPES)
        monster = monster_type.spawn_random(self.board, target=self.player)
        self.monsters.add(monster)
        self.all_sprites.add(monster)

    def run(self):
        """Main loop: input -> update -> draw, FPS times per second."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000   # seconds since last frame
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        """Controller: read the keyboard and pass the player's intentions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                self.reset()
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_KP1):
                self.player.switch_weapon(0)
                self.update_caption()
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_2, pygame.K_KP2):
                self.player.switch_weapon(1)
                self.update_caption()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.player.switch_weapon()
                self.update_caption()

        keys = pygame.key.get_pressed()
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        left = keys[pygame.K_LEFT] or keys[pygame.K_q]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        up = keys[pygame.K_UP] or keys[pygame.K_z]
        self.player.direction = pygame.Vector2(right - left, down - up)
        self.player.trigger_pressed = keys[pygame.K_SPACE]

    def update(self, dt):
        """Model: every object updates itself, then shooting and hits are resolved."""
        if self.game_over:
            return
        self.all_sprites.update(dt)        # polymorphism: player, monsters AND bullets
        self.effects.update(dt)

        if self.player.trigger_pressed:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

        for monster in self.monsters:      # only monsters that CAN shoot are asked to
            if isinstance(monster, Shooter):
                bolt = monster.shoot()
                if bolt:
                    self.enemy_bolts.add(bolt)
                    self.all_sprites.add(bolt)

        self.handle_hits()

    def handle_hits(self):
        """Bullets that touch a monster disappear and damage it."""
        hits = pygame.sprite.groupcollide(self.monsters, self.bullets, False, True)
        for monster, bullets in hits.items():
            for bullet in bullets:
                damage = self.damage_calculator.compute(bullet.damage, bullet.damage_type, monster)
                monster.take_damage(damage)
                self.effects.add(DamageText(monster.pos.x, monster.rect.top - 24, damage, bullet.damage))
            if not monster.is_alive:
                monster.kill()
                self.player.score += monster.POINTS
                self.update_caption()
                self.spawn_monster()

        for bolt in pygame.sprite.spritecollide(self.player, self.enemy_bolts, True):
            self.player.hit(bolt.damage)

        for monster in pygame.sprite.spritecollide(self.player, self.monsters, False):
            if self.player.hit(monster.CONTACT_DAMAGE):
                self.knock_back(monster)
        if not self.player.is_alive:
            self.game_over = True
            self.update_caption()

    def knock_back(self, monster):
        """Push a monster away from the wizard after it bites, so it does not stick to him."""
        away = monster.pos - self.player.pos
        if away.length_squared() == 0:
            away = pygame.Vector2(0, -1)
        monster.pos += away.normalize() * KNOCKBACK_DISTANCE
        self.board.keep_inside(monster)

    def draw(self):
        """View: board, then sprites, then the monsters' health bars, then show the frame."""
        self.screen.fill(BG_COLOR)
        self.board.draw(self.screen)
        self.all_sprites.draw(self.screen)
        for monster in self.monsters:
            self.health_bar.draw(self.screen, monster)
            if isinstance(monster, Shielded):
                self.shield_view.draw(self.screen, monster)
        self.health_bar.draw(self.screen, self.player)   # the player's health too
        self.effects.draw(self.screen)
        if self.game_over:
            self.game_over_view.draw(self.screen, self.player.score)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
