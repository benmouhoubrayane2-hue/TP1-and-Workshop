"""Abstract base class shared by every object of the game (model side: no image)."""
from abc import ABC, abstractmethod

import pygame


class GameObject(pygame.sprite.Sprite, ABC):
    """Anything with a position, a speed and a size (player, monster, bullet...).

    pygame.sprite.Sprite is only used for its groups and collision tests:
    a model object has a rectangle (its hitbox) but NO image. How it looks is
    decided by the view, from the object's KIND.
    """
    KIND = "object"          # name the view uses to choose an image

    def __init__(self, x, y, speed, size):
        super().__init__()
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = (x, y)
        self.pos = pygame.Vector2(x, y)    # exact position (floats)
        self.speed = speed                 # pixels per second

    def move(self, direction, dt):
        """Move along `direction` at `self.speed` pixels per second."""
        if direction.length_squared() > 0:
            direction = direction.normalize()      # same speed in every direction
        self.pos += direction * self.speed * dt
        self.sync_rect()

    def sync_rect(self):
        """Copy the exact position to the rectangle used for collisions."""
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    @abstractmethod
    def update(self, dt):
        """Called once per frame; each subclass defines its own behaviour."""
