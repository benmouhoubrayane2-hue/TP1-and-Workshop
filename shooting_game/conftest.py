"""Shared pytest setup: start pygame without a window and build common objects."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")   # no real window during tests
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from settings import WIDTH, HEIGHT
from board import GameBoard
from player import Player
from monster import Monster


@pytest.fixture(scope="session", autouse=True)
def pygame_display():
    """Start pygame once for all tests (convert_alpha() needs a display)."""
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT))
    yield
    pygame.quit()


@pytest.fixture
def board():
    return GameBoard(WIDTH, HEIGHT)


@pytest.fixture
def player(board):
    return Player(board)


@pytest.fixture
def monster(board, player):
    """A monster placed 300 px above the player."""
    return Monster(player.pos.x, player.pos.y - 300, target=player)
