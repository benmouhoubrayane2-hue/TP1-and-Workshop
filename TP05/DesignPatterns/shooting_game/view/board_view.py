"""BoardView: draws the arena (background picture and frame) from the board and the theme."""
import pygame
from settings import BORDER_WIDTH


class BoardView:

    def __init__(self, board, theme):
        self.board = board
        self.theme = theme
        picture = pygame.image.load(str(theme.background_path())).convert()
        self._background = pygame.transform.smoothscale(picture, board.rect.size)

    def draw(self, surface):
        rect = self.board.rect
        surface.blit(self._background, rect.topleft)
        pygame.draw.rect(surface, self.theme.border_color,
                         rect.inflate(BORDER_WIDTH * 2, BORDER_WIDTH * 2), BORDER_WIDTH, border_radius=6)
