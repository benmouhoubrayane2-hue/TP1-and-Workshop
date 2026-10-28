"""Player: the wizard controlled by the user."""
import pygame
from character import Character
from settings import (WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT,
                      PLAYER_SPEED, PLAYER_MAX_HEALTH, PLAYER_IMAGE)


class Player(Character):
    """The wizard: moves in the direction given by the controller."""

    def __init__(self, x, y):
        image = self.load_image(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
        super().__init__(x, y, PLAYER_SPEED, image, PLAYER_MAX_HEALTH)
        self.score = 0
        self.direction = pygame.Vector2(0, 0)   # set by Game.handle_events()

    def update(self, dt):
        """Move, then stay inside the screen."""
        self.move(self.direction, dt)

        half_w = self.rect.width / 2
        half_h = self.rect.height / 2
        self.pos.x = max(half_w, min(self.pos.x, WIDTH - half_w))
        self.pos.y = max(half_h, min(self.pos.y, HEIGHT - half_h))
        self.sync_rect()