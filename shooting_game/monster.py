"""Monster: spawns at the top of the screen and chases the player."""
import random
from pathlib import Path

import pygame
from settings import (WIDTH, MONSTER_WIDTH, MONSTER_HEIGHT, MONSTER_SPEED,
                      MONSTER_HEALTH, MONSTER_IMAGE)

ASSETS = Path(__file__).parent / "assets"


class Monster(pygame.sprite.Sprite):
    """An enemy that walks towards a target (the player)."""

    def __init__(self, x, y):
        super().__init__()
        image = pygame.image.load(ASSETS / MONSTER_IMAGE).convert_alpha()
        self.image = pygame.transform.smoothscale(image, (MONSTER_WIDTH, MONSTER_HEIGHT))
        self.rect = self.image.get_rect(center=(x, y))

        # Data fields required by the project spec
        self.pos = pygame.Vector2(x, y)
        self.speed = MONSTER_SPEED
        self.health = MONSTER_HEALTH
        self.attack_type = "contact"       # hurts the player by touching them

    @classmethod
    def spawn_random(cls):
        """Create a monster at a random place along the top of the screen."""
        x = random.randint(MONSTER_WIDTH, WIDTH - MONSTER_WIDTH)
        return cls(x, MONSTER_HEIGHT)

    def update(self, dt, target):
        """Move towards `target` (a Vector2, e.g. the player's position)."""
        to_target = target - self.pos
        if to_target.length() > 1:                 # avoid shaking when on top of it
            self.pos += to_target.normalize() * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))