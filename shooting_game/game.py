"""Entry point of the 2D shooting game."""
import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS, BG_COLOR
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
        self.player = Player(WIDTH / 2, HEIGHT - 80)
        self.monster = Monster.spawn_random()
        self.all_sprites = pygame.sprite.Group(self.player, self.monster)
        self.direction = pygame.Vector2(0, 0)

    def run(self):
        """Main loop: input -> update -> draw, FPS times per second."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000   # seconds since last frame
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        """Read the event queue (keyboard, mouse, window close)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        # Continuous input: which keys are held down right now?
        keys = pygame.key.get_pressed()
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        left = keys[pygame.K_LEFT] or keys[pygame.K_q]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        up = keys[pygame.K_UP] or keys[pygame.K_z]
        self.direction = pygame.Vector2(right - left, down - up)

    def update(self, dt):
        """Move and update game objects."""
        self.player.update(dt, self.direction)
        self.monster.update(dt, self.player.pos)

    def draw(self):
        """Clear the screen, draw everything, then show the frame."""
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()