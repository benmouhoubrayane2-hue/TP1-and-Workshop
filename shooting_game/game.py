"""Entry point of the 2D shooting game."""
import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS, BG_COLOR
from board import GameBoard
from player import Player
from monster import Monster


class Game:
    """Owns the window, the clock and the main loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Game objects
        self.board = GameBoard(WIDTH, HEIGHT)
        self.player = Player(self.board)
        self.all_sprites = pygame.sprite.Group(self.player)   # everything to update and draw
        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.spawn_monster()

    def spawn_monster(self):
        """Create a monster and register it in the right groups."""
        monster = Monster.spawn_random(self.board, target=self.player)
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

        keys = pygame.key.get_pressed()
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        left = keys[pygame.K_LEFT] or keys[pygame.K_q]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        up = keys[pygame.K_UP] or keys[pygame.K_z]
        self.player.direction = pygame.Vector2(right - left, down - up)
        self.player.trigger_pressed = keys[pygame.K_SPACE]

    def update(self, dt):
        """Model: every object updates itself, then shooting and hits are resolved."""
        self.all_sprites.update(dt)        # polymorphism: player, monsters AND bullets

        if self.player.trigger_pressed:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

        self.handle_hits()

    def handle_hits(self):
        """Bullets that touch a monster disappear and damage it."""
        hits = pygame.sprite.groupcollide(self.monsters, self.bullets, False, True)
        for monster, bullets in hits.items():
            for bullet in bullets:
                monster.take_damage(bullet.damage)
            if not monster.is_alive:
                monster.kill()
                self.player.score += 1
                pygame.display.set_caption(f"{TITLE}  -  Score: {self.player.score}")
                self.spawn_monster()

    def draw(self):
        """View: board first, then every sprite on top, then show the frame."""
        self.screen.fill(BG_COLOR)
        self.board.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()