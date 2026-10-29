"""Abstraction and inheritance: the class hierarchy is correct."""
import pygame
import pytest

from game_object import GameObject
from character import Character
from player import Player
from monster import Monster
from bullet import Bullet


def test_game_object_is_abstract():
    with pytest.raises(TypeError):
        GameObject(0, 0, 1, pygame.Surface((10, 10)))


def test_character_is_abstract():
    with pytest.raises(TypeError):
        Character(0, 0, 1, pygame.Surface((10, 10)), max_health=10)


def test_player_and_monster_are_characters():
    assert issubclass(Player, Character)
    assert issubclass(Monster, Character)


def test_bullet_is_a_game_object_but_not_a_character():
    assert issubclass(Bullet, GameObject)
    assert not issubclass(Bullet, Character)
