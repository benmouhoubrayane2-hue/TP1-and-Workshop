"""DIP: the game depends on DamageCalculator, the player on Weapon - not on concrete classes."""
import pygame
import pytest

from bullet import Bullet, Fireball
from damage import DamageCalculator, ResistanceCalculator, PlainCalculator
from damage_text import DamageText
from game import Game
from monster import Monster
from monster_types import StrongMonster, FlyingMonster
from player import Player
from weapons import Weapon, MagicWand, FireStaff


# --- Damage calculators -------------------------------------------------------

def test_abstractions_cannot_be_instantiated():
    with pytest.raises(TypeError):
        DamageCalculator()
    with pytest.raises(TypeError):
        Weapon()


@pytest.mark.parametrize("monster_type, damage_type, expected", [
    (Monster, "magic", 10),             # no resistance
    (StrongMonster, "magic", 5),        # resists magic
    (StrongMonster, "fire", 20),        # weak to fire
    (FlyingMonster, "magic", 15),       # weak to magic
    (FlyingMonster, "fire", 5),         # resists fire
])
def test_resistances_and_weaknesses(player, monster_type, damage_type, expected):
    monster = monster_type(400, 200, target=player)
    assert ResistanceCalculator().compute(10, damage_type, monster) == expected


def test_plain_calculator_ignores_resistances(player):
    strong = StrongMonster(400, 200, target=player)
    assert PlainCalculator().compute(10, "magic", strong) == 10


class OneShotCalculator(DamageCalculator):
    """A calculator the game has never heard of: every hit is deadly."""
    def compute(self, amount, damage_type, target):
        return 10_000


def game_with_strong_monster(calculator=None):
    game = Game(damage_calculator=calculator)
    for other in list(game.monsters):
        other.kill()
    strong = StrongMonster(game.player.pos.x, game.player.pos.y - 250, target=game.player)
    game.monsters.add(strong)
    game.all_sprites.add(strong)
    game.player.trigger_pressed = True
    return game, strong


def test_game_uses_the_calculator_it_is_given():
    game, strong = game_with_strong_monster(OneShotCalculator())
    for _ in range(60):
        game.update(1 / 60)
        if not strong.alive():
            break
    assert not strong.alive()           # one magic bolt was enough
    assert game.player.score == StrongMonster.POINTS


def test_default_game_applies_resistances():
    game, strong = game_with_strong_monster()
    for _ in range(60):
        game.update(1 / 60)
        if strong.health < strong.max_health:
            break
    assert strong.health == strong.max_health - 5      # magic bolt halved
    texts = [s for s in game.effects if isinstance(s, DamageText)]
    assert texts and texts[0].text == "-5"


# --- Weapons -------------------------------------------------------------------

def test_player_has_two_weapons_and_can_switch(player):
    assert isinstance(player.weapon, MagicWand)
    assert isinstance(player.shoot(), Bullet)
    player.switch_weapon()
    assert isinstance(player.weapon, FireStaff)
    fireball = player.shoot()
    assert isinstance(fireball, Fireball) and fireball.damage_type == "fire"
    player.switch_weapon()
    assert isinstance(player.weapon, MagicWand)        # back to the first one


def test_fireball_is_stronger_but_slower():
    assert Fireball.DAMAGE > Bullet.DAMAGE
    assert Fireball.SPEED < Bullet.SPEED


def test_each_projectile_type_has_its_own_image(board):
    bolt = Bullet(100, 100, pygame.Vector2(1, 0), board)
    fireball = Fireball(100, 100, pygame.Vector2(1, 0), board)
    assert bolt.image is not fireball.image
    assert fireball.image is Fireball(0, 0, pygame.Vector2(1, 0), board).image


class Slingshot(Weapon):
    """A weapon the Player class has never heard of."""
    NAME = "Slingshot"
    COOLDOWN = 1.0

    def make_projectile(self, x, y, direction, board):
        return Bullet(x, y, direction, board)


def test_player_accepts_any_weapon(board):
    player = Player(board, weapons=[Slingshot()])
    assert player.weapon.NAME == "Slingshot"
    assert player.shoot() is not None
    assert player.shoot() is None                      # its own 1 s cooldown
    player.update(1.0)
    assert player.shoot() is not None
