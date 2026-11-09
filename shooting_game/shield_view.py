"""ShieldView: draws the shield of a Shielded monster (display only)."""
import pygame
from settings import SHIELD_COLOR


class ShieldView:
    """Draws a glowing ring around a monster; thinner as the shield weakens."""

    def draw(self, surface, monster):
        if monster.shield <= 0:
            return
        radius = max(monster.rect.width, monster.rect.height) // 2 + 6
        width = 1 + round(3 * monster.shield_ratio)
        pygame.draw.circle(surface, SHIELD_COLOR, monster.rect.center, radius, width)
