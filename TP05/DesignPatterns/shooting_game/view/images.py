"""ImageLibrary: gives the picture of each object, using the current theme (view side)."""
import pygame


class ImageLibrary:
    """The model object only says WHAT it is (its KIND); the theme says which file
    shows it. Each picture is loaded once per size and shared."""

    def __init__(self, theme):
        self.theme = theme
        self._cache = {}

    def set_theme(self, theme):
        self.theme = theme
        self._cache.clear()

    def get(self, obj):
        return self.image(obj.KIND, obj.rect.size)

    def image(self, kind, size):
        key = (kind, tuple(size))
        if key not in self._cache:
            self._cache[key] = self._load(kind, size)
        return self._cache[key]

    def _load(self, kind, size):
        path = self.theme.image_path(kind)
        if path is None or not path.exists():                # unknown kind: a pink box
            missing = pygame.Surface(size, pygame.SRCALPHA)
            missing.fill((255, 0, 200, 160))
            return missing
        picture = pygame.image.load(str(path)).convert_alpha()
        return pygame.transform.smoothscale(picture, size)
