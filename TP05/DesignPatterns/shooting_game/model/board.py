"""GameBoard: the arena where the game takes place (model side: limits and positions only)."""
import random

import pygame
from settings import BOARD_MARGIN


class GameBoard:
    """Knows the play area: its limits and where things can go. It does not draw itself
    (the view draws the arena from board.rect)."""

    def __init__(self, width, height):
        # Play area = window minus a margin on every side
        self.rect = pygame.Rect(BOARD_MARGIN, BOARD_MARGIN,
                                width - 2 * BOARD_MARGIN, height - 2 * BOARD_MARGIN)

    # ---------- positions ----------
    @property
    def player_start(self):
        """Where the player appears: bottom centre of the arena."""
        return pygame.Vector2(self.rect.centerx, self.rect.bottom - 70)

    def random_top_position(self, margin):
        """A random point along the top of the arena, `margin` px from the edges."""
        x = random.randint(self.rect.left + margin, self.rect.right - margin)
        return pygame.Vector2(x, self.rect.top + margin)

    # ---------- rules ----------
    def keep_inside(self, obj):
        """Push a GameObject back inside the arena if it went past an edge."""
        half_w = obj.rect.width / 2
        half_h = obj.rect.height / 2
        obj.pos.x = max(self.rect.left + half_w, min(obj.pos.x, self.rect.right - half_w))
        obj.pos.y = max(self.rect.top + half_h, min(obj.pos.y, self.rect.bottom - half_h))
        obj.sync_rect()

    def is_outside(self, obj):
        """True when a GameObject has completely left the arena (used for projectiles)."""
        return not self.rect.colliderect(obj.rect)
