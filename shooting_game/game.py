"""Entry point of the 2D shooting game."""
import pygame
from settings import WIDTH, HEIGHT, TITLE, FPS, BG_COLOR


class Game:
    """Owns the window, the clock and the main loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

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

    def update(self, dt):
        """Move and update game objects (empty for now)."""
        pass

    def draw(self):
        """Clear the screen, draw everything, then show the frame."""
        self.screen.fill(BG_COLOR)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()