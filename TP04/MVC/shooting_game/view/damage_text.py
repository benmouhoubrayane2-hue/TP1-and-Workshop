"""DamageText: a number that floats up above a monster when it is hit (display only)."""
import pygame

WEAK_COLOR = (255, 90, 60)       # weakness: more damage than normal
RESIST_COLOR = (150, 150, 165)   # resistance: less damage than normal
NORMAL_COLOR = (255, 255, 255)


class DamageText:
    """Shows the real damage; red if the monster is weak, grey if it resists.
    Created by the view from a HIT event of the model."""
    LIFETIME = 0.7
    SPEED = 60                   # pixels per second, upwards
    _font = None

    def __init__(self, x, y, damage, base_damage):
        if DamageText._font is None:
            DamageText._font = pygame.font.Font(None, 36)
        if damage > base_damage:
            colour, text = WEAK_COLOR, f"-{damage}!"
        elif damage < base_damage:
            colour, text = RESIST_COLOR, f"-{damage}"
        else:
            colour, text = NORMAL_COLOR, f"-{damage}"
        self.text = text
        self.image = self._outlined(text, colour)
        self.pos = pygame.Vector2(x, y)
        self._time_left = self.LIFETIME

    @property
    def alive(self):
        return self._time_left > 0

    @classmethod
    def _outlined(cls, text, colour):
        """The text with a black outline, readable on any monster."""
        inside = cls._font.render(text, True, colour)
        border = cls._font.render(text, True, (0, 0, 0))
        image = pygame.Surface((inside.get_width() + 4, inside.get_height() + 4), pygame.SRCALPHA)
        for dx, dy in ((0, 0), (4, 0), (0, 4), (4, 4), (2, 0), (0, 2), (4, 2), (2, 4)):
            image.blit(border, (dx, dy))
        image.blit(inside, (2, 2))
        return image

    def update(self, dt):
        self.pos.y -= self.SPEED * dt                      # float upwards
        self._time_left -= dt
        self.image.set_alpha(int(255 * max(0.0, self._time_left) / self.LIFETIME))

    def draw(self, surface):
        surface.blit(self.image, self.image.get_rect(center=(round(self.pos.x), round(self.pos.y))))
