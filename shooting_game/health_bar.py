"""HealthBar: draws the health of a character (display only, no game rules)."""
import pygame
from settings import (HEALTH_BAR_HEIGHT, HEALTH_BAR_GAP, HEALTH_BAR_BG, HEALTH_BAR_BORDER,
                      HEALTH_HIGH, HEALTH_MID, HEALTH_LOW)


class HealthBar:
    """Draws a small bar above any Character. The character never draws itself."""

    def __init__(self, height=HEALTH_BAR_HEIGHT, gap=HEALTH_BAR_GAP):
        self.height = height
        self.gap = gap

    def rects(self, character):
        """Return (background, filled part) rectangles for this character."""
        background = pygame.Rect(character.rect.left,
                                 character.rect.top - self.gap - self.height,
                                 character.rect.width, self.height)
        filled = background.copy()
        filled.width = round(background.width * character.health_ratio)
        return background, filled

    @staticmethod
    def color(ratio):
        """Green when healthy, orange when hurt, red when almost dead."""
        if ratio > 0.6:
            return HEALTH_HIGH
        if ratio > 0.3:
            return HEALTH_MID
        return HEALTH_LOW

    def draw(self, surface, character):
        background, filled = self.rects(character)
        pygame.draw.rect(surface, HEALTH_BAR_BG, background, border_radius=2)
        if filled.width > 0:
            pygame.draw.rect(surface, self.color(character.health_ratio), filled, border_radius=2)
        pygame.draw.rect(surface, HEALTH_BAR_BORDER, background, 1, border_radius=2)
