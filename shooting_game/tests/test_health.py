"""SRP: health rules (Health) and health display (HealthBar) are separate classes."""
import pygame

from health import Health
from health_bar import HealthBar
from settings import HEALTH_HIGH, HEALTH_MID, HEALTH_LOW, BULLET_DAMAGE


def test_health_starts_full():
    health = Health(30)
    assert health.current == 30 and health.ratio == 1.0 and not health.is_empty


def test_damage_and_heal_stay_within_limits():
    health = Health(30)
    health.take_damage(50)
    assert health.current == 0 and health.is_empty
    health.heal(100)
    assert health.current == 30


def test_character_delegates_to_its_health_component(monster):
    monster.take_damage(BULLET_DAMAGE)
    assert monster.health == monster.max_health - BULLET_DAMAGE
    assert monster.health_ratio == (monster.max_health - BULLET_DAMAGE) / monster.max_health


def test_bar_sits_above_the_character_and_has_its_width(monster):
    background, _ = HealthBar().rects(monster)
    assert background.bottom < monster.rect.top
    assert background.width == monster.rect.width


def test_filled_part_follows_the_health(monster):
    bar = HealthBar()
    monster.take_damage(monster.max_health / 3)
    background, filled = bar.rects(monster)
    assert filled.width == round(background.width * 2 / 3)


def test_colour_changes_with_health():
    assert HealthBar.color(1.0) == HEALTH_HIGH
    assert HealthBar.color(0.5) == HEALTH_MID
    assert HealthBar.color(0.2) == HEALTH_LOW


def test_bar_can_be_drawn_for_any_character(player, monster):
    surface = pygame.Surface((960, 640))
    HealthBar().draw(surface, player)      # same component works for the player
    HealthBar().draw(surface, monster)


def test_monster_does_not_draw_itself():
    from monster import Monster
    assert not hasattr(Monster, "draw_health_bar")
    assert "pygame.draw" not in open("monster.py", encoding="utf-8").read()
