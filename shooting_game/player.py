"""Player: the wizard controlled by the user."""
import pygame
from character import Character
from bullet import Bullet
from settings import (PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_MAX_HEALTH,
                      PLAYER_IMAGE, FIRE_COOLDOWN)


class Player(Character):
    """The wizard: moves and shoots as the controller says, inside the board."""

    def __init__(self, board):
        image = self.load_image(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
        start = board.player_start
        super().__init__(start.x, start.y, PLAYER_SPEED, image, PLAYER_MAX_HEALTH)
        self.board = board                      # the arena it must stay in
        self.score = 0
        self.direction = pygame.Vector2(0, 0)   # set by Game.handle_events()
        self.facing = pygame.Vector2(0, -1)     # last direction moved; bolts fly this way
        self.trigger_pressed = False            # set by Game.handle_events()

        # Weapon
        self.weapon = "magic bolt"
        self.fire_cooldown = FIRE_COOLDOWN
        self._reload = 0.0                      # seconds before the next shot is allowed

    def update(self, dt):
        """Remember where we face, reload, move, stay inside the arena."""
        if self.direction.length_squared() > 0:
            self.facing = self.direction.normalize()
        self._reload = max(0.0, self._reload - dt)
        self.move(self.direction, dt)
        self.board.keep_inside(self)

    def shoot(self):
        """Return a new Bullet if the weapon is ready, otherwise None."""
        if self._reload > 0:
            return None
        self._reload = self.fire_cooldown
        start = self.pos + self.facing * (self.rect.height / 2)   # just in front of the wizard
        return Bullet(start.x, start.y, self.facing, self.board)