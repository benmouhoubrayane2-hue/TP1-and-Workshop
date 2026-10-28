"""Monster: spawns at the top of the screen and chases its target."""
import random

from character import Character
from settings import (WIDTH, MONSTER_WIDTH, MONSTER_HEIGHT, MONSTER_SPEED,
                      MONSTER_HEALTH, MONSTER_IMAGE)


class Monster(Character):
    """An enemy that walks towards a target (the player)."""

    def __init__(self, x, y, target):
        image = self.load_image(MONSTER_IMAGE, (MONSTER_WIDTH, MONSTER_HEIGHT))
        super().__init__(x, y, MONSTER_SPEED, image, MONSTER_HEALTH)
        self.target = target               # the object it chases
        self.attack_type = "contact"       # hurts the player by touching them

    @classmethod
    def spawn_random(cls, target):
        """Create a monster at a random place along the top of the screen."""
        x = random.randint(MONSTER_WIDTH, WIDTH - MONSTER_WIDTH)
        return cls(x, MONSTER_HEIGHT, target)

    def update(self, dt):
        """Walk towards the target; stop when on top of it."""
        to_target = self.target.pos - self.pos
        if to_target.length() > 1:
            self.move(to_target, dt)