"""Player: the wizard controlled by the user."""
import pygame
from character import Character
from weapons import MagicWand, FireStaff
from settings import (PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_MAX_HEALTH,
                      PLAYER_IMAGE, PLAYER_INVULNERABLE_TIME)


class Player(Character):
    """The wizard: moves and shoots as the controller says, inside the board."""

    def __init__(self, board, weapons=None):
        """`weapons`: any list of Weapon objects (DIP: given from outside)."""
        image = self.load_image(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
        start = board.player_start
        super().__init__(start.x, start.y, PLAYER_SPEED, image, PLAYER_MAX_HEALTH)
        self.board = board                      # the arena it must stay in
        self.score = 0
        self.direction = pygame.Vector2(0, 0)   # set by Game.handle_events()
        self.facing = pygame.Vector2(0, -1)     # last direction moved; bolts fly this way
        self.trigger_pressed = False            # set by Game.handle_events()

        # Weapons: the Player only knows the Weapon abstraction
        self.weapons = weapons if weapons is not None else [MagicWand(), FireStaff()]
        self._weapon_index = 0

        # Protection after being hit
        self._invulnerable = 0.0                # seconds left; the wizard blinks meanwhile

    def update(self, dt):
        """Remember where we face, reload, move, stay inside the arena."""
        if self.direction.length_squared() > 0:
            self.facing = self.direction.normalize()
        for weapon in self.weapons:
            weapon.update(dt)                   # every weapon reloads
        self._invulnerable = max(0.0, self._invulnerable - dt)
        self.image.set_alpha(80 if self._invulnerable and int(self._invulnerable * 10) % 2 else 255)
        self.move(self.direction, dt)
        self.board.keep_inside(self)

    @property
    def is_invulnerable(self):
        return self._invulnerable > 0

    def hit(self, amount):
        """Damage from an attack: ignored while still protected by the previous hit.
        Returns True if the hit counted."""
        if self.is_invulnerable:
            return False
        self.take_damage(amount)
        self._invulnerable = PLAYER_INVULNERABLE_TIME
        return True

    @property
    def weapon(self):
        """The weapon currently in hand."""
        return self.weapons[self._weapon_index]

    def switch_weapon(self, index=None):
        """Take the weapon number `index`, or the next one if no index is given."""
        if index is None:
            index = self._weapon_index + 1
        self._weapon_index = index % len(self.weapons)

    def shoot(self):
        """Fire the current weapon: a new projectile, or None while it reloads."""
        start = self.pos + self.facing * (self.rect.height / 2)   # just in front of the wizard
        return self.weapon.fire(start.x, start.y, self.facing, self.board)
