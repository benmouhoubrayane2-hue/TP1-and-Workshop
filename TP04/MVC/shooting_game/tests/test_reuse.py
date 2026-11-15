"""Optional part: the SAME View and Controller drive a DIFFERENT Model (Crystal Hunt)."""
from collections import defaultdict
from pathlib import Path

import pygame
import pytest

from settings import WINDOW_WIDTH, HEIGHT
from model.game_interface import GameModelInterface
from model.game_model import GameModel
from model.player import Player
from crystal_hunt.model import CrystalHuntModel, Crystal, Rock, COLLECTED
from view.game_view import GameView
from view.theme import ThemeLibrary, ASSETS
from view.info_panel import InfoPanel
from controller.keyboard_controller import KeyboardController

ROOT = Path(__file__).resolve().parent.parent
CRYSTAL_THEMES = ASSETS / "themes_crystal"


def crystal_view(model):
    return GameView(model, pygame.Surface((WINDOW_WIDTH, HEIGHT)),
                    themes=ThemeLibrary(folder=CRYSTAL_THEMES, first="cave"))


# --- The view and the controller only depend on the abstraction ----------------

@pytest.mark.parametrize("model_type", [GameModel, CrystalHuntModel])
def test_both_games_implement_the_same_interface(model_type):
    assert issubclass(model_type, GameModelInterface)


@pytest.mark.parametrize("package", ["view", "controller"])
def test_view_and_controller_know_no_concrete_game(package):
    source = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / package).glob("*.py"))
    assert "game_model import" not in source and "crystal_hunt" not in source


def test_second_game_reuses_existing_model_parts():
    model = CrystalHuntModel()
    assert isinstance(model.player, Player)                  # same wizard, health and weapons


# --- The same view shows the new game --------------------------------------------

def test_same_view_draws_the_new_game():
    model = CrystalHuntModel()
    view = crystal_view(model)
    surface = pygame.Surface((WINDOW_WIDTH, HEIGHT))
    view.draw(surface)
    assert view.theme.title == "Crystal Hunt"
    assert "Time: 60 / 60" in InfoPanel.lines(model.info())


@pytest.mark.parametrize("theme", ThemeLibrary(folder=CRYSTAL_THEMES).themes, ids=lambda t: t.name)
@pytest.mark.parametrize("kind", ["player", Crystal.KIND, Rock.KIND, "magic_bolt", "fireball"])
def test_new_game_pictures_come_from_its_own_theme_files(theme, kind):
    assert theme.image_path(kind).exists()


# --- The same controller drives the new game -------------------------------------

def test_same_controller_drives_the_new_game():
    model = CrystalHuntModel()
    controller = KeyboardController(model)
    pressed = defaultdict(bool, {pygame.K_LEFT: True, pygame.K_SPACE: True})
    controller.handle_keys(pressed)
    start = pygame.Vector2(model.player.pos)
    model.update(0.2)
    assert model.player.pos.x < start.x and len(model.bullets) == 1
    controller.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    assert model.status == "Paused"


# --- Rules of the new game ---------------------------------------------------------

def test_collecting_a_crystal_scores():
    model = CrystalHuntModel()
    crystal = next(iter(model.crystals))
    model.player.pos.update(crystal.pos)
    model.player.sync_rect()
    model.update(1 / 60)
    assert model.score == 1 and len(model.crystals) == CrystalHuntModel.CRYSTAL_COUNT
    assert COLLECTED in [e.kind for e in model.pop_events()]


def test_a_falling_rock_hurts_the_wizard():
    model = CrystalHuntModel()
    rock = Rock(model.player.pos.x, model.player.pos.y - 40, 200, model.board)
    model.rocks.add(rock)
    model.objects.add(rock)
    for _ in range(30):
        model.update(1 / 60)
    assert model.player.health == model.player.max_health - Rock.DAMAGE


def test_the_game_ends_when_the_time_is_up():
    model = CrystalHuntModel()
    model.time_left = 0.01
    model.update(1 / 60)
    assert model.game_over and model.info()["Time"] == (0, 60)
