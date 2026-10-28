"""Player: the wizard controlled by the user."""
import pygame
from character import Character
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_MAX_HEALTH, PLAYER_IMAGE


class Player(Character):
    """The wizard: moves in the direction given by the controller, inside the board."""

    def __init__(self, board):
        image = self.load_image(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
        start = board.player_start
        super().__init__(start.x, start.y, PLAYER_SPEED, image, PLAYER_MAX_HEALTH)
        self.board = board                      # the arena it must stay in
        self.score = 0
        self.direction = pygame.Vector2(0, 0)   # set by Game.handle_events()

    def update(self, dt):
        """Move, then let the board keep the wizard inside the arena."""
        self.move(self.direction, dt)
        self.board.keep_inside(self)