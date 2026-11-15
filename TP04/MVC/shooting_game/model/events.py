"""GameEvent: something that happened in the model during one update.

The model only records events; the view decides how to show them
(floating damage numbers, sounds...). The model never knows about the screen.
"""
from dataclasses import dataclass, field

import pygame

SHOT = "shot"                  # the wizard fired           (name = projectile KIND)
HIT = "hit"                    # a monster was hit          (value = damage, base = damage before resistances)
MONSTER_DEFEATED = "defeated"  # a monster died             (value = points won)
PLAYER_HURT = "hurt"           # the wizard lost health     (value = damage)
GAME_OVER = "game_over"        # the wizard has no health left


@dataclass
class GameEvent:
    kind: str
    pos: pygame.Vector2 = field(default_factory=pygame.Vector2)
    value: int = 0
    base: int = 0
    name: str = ""
