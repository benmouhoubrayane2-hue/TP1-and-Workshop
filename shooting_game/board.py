"""GameBoard: the arena where the game takes place."""
import random

import pygame
from settings import (BOARD_MARGIN, TILE_SIZE, TILE_COLOR_A, TILE_COLOR_B,
                      TILE_LINE_COLOR, BORDER_COLOR, BORDER_WIDTH)


class GameBoard:
    """Knows the play area: its limits, its background, and where things can go."""

    def __init__(self, width, height):
        # Play area = window minus a margin on every side
        self.rect = pygame.Rect(BOARD_MARGIN, BOARD_MARGIN,
                                width - 2 * BOARD_MARGIN, height - 2 * BOARD_MARGIN)
        self._background = self._build_background()   # drawn once, reused every frame

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
        """True when a GameObject has completely left the arena (used for bullets)."""
        return not self.rect.colliderect(obj.rect)

    # ---------- drawing ----------
    def draw(self, surface):
        surface.blit(self._background, self.rect.topleft)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect.inflate(BORDER_WIDTH * 2, BORDER_WIDTH * 2),
                         BORDER_WIDTH, border_radius=6)

    def _build_background(self):
        """Paint a tiled stone floor on a surface the size of the arena."""
        floor = pygame.Surface(self.rect.size)
        for row, y in enumerate(range(0, self.rect.height, TILE_SIZE)):
            for col, x in enumerate(range(0, self.rect.width, TILE_SIZE)):
                color = TILE_COLOR_A if (row + col) % 2 == 0 else TILE_COLOR_B
                tile = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(floor, color, tile)
                pygame.draw.rect(floor, TILE_LINE_COLOR, tile, 1)
        return floor