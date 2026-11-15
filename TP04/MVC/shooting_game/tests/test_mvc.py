"""MVC: the model, the view and the controller each do their own job, and only that."""
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pygame
import pytest

from model.game_model import GameModel
from model.events import GameEvent, HIT
from model.weapons import MagicWand, FireStaff
from view.game_view import GameView
from controller.keyboard_controller import KeyboardController

ROOT = Path(__file__).resolve().parent.parent


def source_of(package):
    return "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / package).glob("*.py"))


# --- Each layer only does its own job ------------------------------------------

@pytest.mark.parametrize("forbidden", ["pygame.draw", "pygame.display", "pygame.image", "pygame.font",
                                       "blit", "pygame.event", "pygame.key",
                                       "from view", "import view", "from controller", "import controller"])
def test_model_never_draws_nor_reads_the_keyboard(forbidden):
    assert forbidden not in source_of("model")


@pytest.mark.parametrize("forbidden", ["pygame.event", "pygame.key", "from controller", "import controller"])
def test_view_never_reads_the_keyboard(forbidden):
    assert forbidden not in source_of("view")


@pytest.mark.parametrize("forbidden", ["pygame.draw", "blit", "pygame.display", "from view", "import view"])
def test_controller_never_draws(forbidden):
    assert forbidden not in source_of("controller")


def test_model_objects_have_no_image():
    model = GameModel()
    assert all(not hasattr(obj, "image") for obj in model.objects)


def test_model_runs_without_any_window():
    """The rules work on their own: no pygame.init(), no screen, no keyboard."""
    script = ("from model.game_model import GameModel\n"
              "m = GameModel()\n"
              "m.set_trigger(True)\n"
              "for _ in range(300): m.update(1 / 60)\n"
              "print('frames OK, score', m.score)\n")
    result = subprocess.run([sys.executable, "-c", script], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "frames OK" in result.stdout


# --- The view reads the model but never changes it ------------------------------

def snapshot(model):
    return (model.score, model.player.health, tuple(model.player.pos),
            sorted((tuple(m.pos), m.health) for m in model.monsters), len(model.objects))


def test_drawing_does_not_change_the_model():
    model = GameModel()
    view = GameView(model, pygame.Surface((960, 640)))
    before = snapshot(model)
    for _ in range(10):
        view.draw(pygame.Surface((960, 640)))
    assert snapshot(model) == before


def test_view_turns_hit_events_into_damage_numbers():
    model = GameModel()
    view = GameView(model, pygame.Surface((960, 640)))
    model.events.append(GameEvent(HIT, pygame.Vector2(300, 200), 20, 10))
    view.render(0)
    assert [t.text for t in view.damage_texts] == ["-20!"]       # weakness shown with "!"
    assert model.events == []                                     # the view consumed them


# --- The controller translates keys into model commands -------------------------

def keys(*pressed):
    state = defaultdict(bool)
    for key in pressed:
        state[key] = True
    return state


def key_down(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def test_arrows_and_space_become_model_commands():
    model = GameModel()
    controller = KeyboardController(model)
    controller.handle_keys(keys(pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE))
    assert model.player.direction == pygame.Vector2(1, -1)
    assert model.player.trigger_pressed
    controller.handle_keys(keys())
    assert model.player.direction == pygame.Vector2(0, 0) and not model.player.trigger_pressed


def test_number_keys_choose_the_weapon():
    model = GameModel()
    controller = KeyboardController(model)
    controller.handle_event(key_down(pygame.K_2))
    assert isinstance(model.player.weapon, FireStaff)
    controller.handle_event(key_down(pygame.K_TAB))
    assert isinstance(model.player.weapon, MagicWand)


def test_r_restarts_only_after_game_over():
    model = GameModel()
    controller = KeyboardController(model)
    player = model.player
    controller.handle_event(key_down(pygame.K_r))
    assert model.player is player                     # still playing: R does nothing
    player.take_damage(player.max_health)
    model.update(1 / 60)
    controller.handle_event(key_down(pygame.K_r))
    assert model.player is not player and not model.game_over


@pytest.mark.parametrize("event", [pygame.event.Event(pygame.QUIT),
                                   pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
def test_escape_or_closing_the_window_stops_the_game(event):
    controller = KeyboardController(GameModel())
    controller.handle_event(event)
    assert not controller.running
