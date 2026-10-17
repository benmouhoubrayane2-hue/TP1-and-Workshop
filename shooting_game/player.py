"""Player character: position, movement and screen boundaries."""
from pathlib import Path

import pygame
from settings import (WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT,
                      PLAYER_SPEED, PLAYER_MAX_HEALTH, PLAYER_IMAGE)

ASSETS = Path(__file__).parent / "assets"   # folder next to this file


class Player(pygame.sprite.Sprite):
    """The wizard controlled by the user."""

    def __init__(self, x, y):
        super().__init__()
        # Appearance: load the PNG and scale it to the player size
        image = pygame.image.load(ASSETS / PLAYER_IMAGE).convert_alpha()
        self.image = pygame.transform.smoothscale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect(center=(x, y))

        # Data fields required by the project spec
        self.pos = pygame.Vector2(x, y)    # exact position (floats)
        self.speed = PLAYER_SPEED          # pixels per second
        self.health = PLAYER_MAX_HEALTH
        self.score = 0

    def update(self, dt, direction):
        """Move along `direction` (a Vector2) and stay inside the screen."""
        if direction.length_squared() > 0:
            direction = direction.normalize()      # same speed on diagonals
        self.pos += direction * self.speed * dt

        # Screen boundaries: the whole character must stay visible
        half_w = self.rect.width / 2
        half_h = self.rect.height / 2
        self.pos.x = max(half_w, min(self.pos.x, WIDTH - half_w))
        self.pos.y = max(half_h, min(self.pos.y, HEIGHT - half_h))

        self.rect.center = (round(self.pos.x), round(self.pos.y))