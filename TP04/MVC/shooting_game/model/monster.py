"""Monster: the base enemy. New monster types extend it without modifying it (OCP)."""
from model.character import Character
from settings import (MONSTER_WIDTH, MONSTER_HEIGHT, MONSTER_SPEED,
                      MONSTER_HEALTH, MONSTER_CONTACT_DAMAGE)


class Monster(Character):
    """A normal monster that walks towards a target (the player).

    Each monster type is described by the class attributes below. A new type only
    has to override them (and, if needed, update()) - this class never changes.
    """

    SPEED = MONSTER_SPEED                        # pixels per second
    MAX_HEALTH = MONSTER_HEALTH
    SIZE = (MONSTER_WIDTH, MONSTER_HEIGHT)
    KIND = "monster"                             # the view chooses the image from it
    POINTS = 1                                   # score given when defeated
    CONTACT_DAMAGE = MONSTER_CONTACT_DAMAGE      # damage when it touches the wizard
    RESISTANCES = {}                             # damage type -> multiplier (none = normal)

    def __init__(self, x, y, target):
        super().__init__(x, y, self.SPEED, self.SIZE, self.MAX_HEALTH)
        self.target = target               # the object it chases
        self.attack_type = "contact"       # hurts the player by touching them

    @classmethod
    def spawn_random(cls, board, target):
        """Create a monster of this type at a random place along the top of the board."""
        pos = board.random_top_position(margin=cls.SIZE[0])
        return cls(pos.x, pos.y, target)

    def update(self, dt):
        """Walk towards the target; stop when on top of it."""
        to_target = self.target.pos - self.pos
        if to_target.length() > 1:
            self.move(to_target, dt)
