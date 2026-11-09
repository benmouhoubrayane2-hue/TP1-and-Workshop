"""Abstract base class shared by every object of the game."""
from abc import ABC, abstractmethod
from pathlib import Path

import pygame

ASSETS = Path(__file__).parent / "assets"   # folder next to this file


class GameObject(pygame.sprite.Sprite, ABC):
    """Anything with a position, a speed and an image (player, monster, bullet...)."""

    def __init__(self, x, y, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)    # exact position (floats)
        self.speed = speed                 # pixels per second

    @staticmethod
    def load_image(filename, size):
        """Load a PNG from assets/ and scale it to `size` = (width, height)."""
        image = pygame.image.load(ASSETS / filename).convert_alpha()
        return pygame.transform.smoothscale(image, size)

    def move(self, direction, dt):
        """Move along `direction` at `self.speed` pixels per second."""
        if direction.length_squared() > 0:
            direction = direction.normalize()      # same speed in every direction
        self.pos += direction * self.speed * dt
        self.sync_rect()

    def sync_rect(self):
        """Copy the exact position to the rect used for drawing."""
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    @abstractmethod
    def update(self, dt):
        """Called once per frame; each subclass defines its own behaviour."""