"""Information panel: score, health and game status, drawn by the view from model.info()."""
import pygame
import pytest

from settings import WIDTH, HEIGHT, WINDOW_WIDTH
from model.game_model import GameModel, PLAYING, PAUSED, GAME_OVER_STATUS
from model.monster import Monster
from view.game_view import GameView
from view.info_panel import InfoPanel
from controller.keyboard_controller import KeyboardController


def window():
    return pygame.Surface((WINDOW_WIDTH, HEIGHT))


def test_model_gives_the_panel_data_only():
    info = GameModel().info()
    assert {"Score", "Health", "Status", "Weapon"} <= set(info)
    assert info["Score"] == 0 and info["Health"] == (100, 100) and info["Status"] == PLAYING


def test_panel_lines():
    model = GameModel()
    model.player.take_damage(30)
    lines = InfoPanel.lines(model.info())
    assert "Score: 0" in lines and "Health: 70 / 100" in lines and "Status: Playing" in lines


def test_score_follows_the_game():
    model = GameModel()
    for other in list(model.monsters):
        other.kill()
    target = Monster(model.player.pos.x, model.player.pos.y - 200, target=model.player)
    target.speed = 0
    model.add_monster(target)
    model.set_trigger(True)
    for _ in range(120):
        model.update(1 / 60)
        if not target.alive():
            break
    assert model.info()["Score"] == Monster.POINTS


def test_health_follows_the_game():
    model = GameModel()
    model.hurt_player(25)
    assert model.info()["Health"] == (75, 100)


def test_status_playing_paused_game_over():
    model = GameModel()
    controller = KeyboardController(model)
    controller.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    assert model.info()["Status"] == PAUSED
    controller.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    assert model.info()["Status"] == PLAYING
    model.player.take_damage(model.player.max_health)
    model.update(1 / 60)
    assert model.info()["Status"] == GAME_OVER_STATUS


def test_pause_freezes_the_game():
    model = GameModel()
    model.toggle_pause()
    positions = [tuple(m.pos) for m in model.monsters]
    for _ in range(60):
        model.update(1 / 60)
    assert [tuple(m.pos) for m in model.monsters] == positions


def test_panel_is_beside_the_arena_not_on_it():
    view = GameView(GameModel(), window())
    assert view.info_panel.rect.left >= WIDTH
    assert not view.info_panel.rect.colliderect(view.model.board.rect)


@pytest.mark.parametrize("status_change", ["none", "pause", "game over"])
def test_panel_draws_in_every_state_without_changing_the_model(status_change):
    model = GameModel()
    if status_change == "pause":
        model.toggle_pause()
    elif status_change == "game over":
        model.player.take_damage(1000)
        model.update(1 / 60)
    view = GameView(model, window())
    before = model.info()
    surface = window()
    view.draw(surface)
    assert model.info() == before
    panel_pixels = pygame.image.tostring(surface.subsurface(view.info_panel.rect), "RGB")
    assert len(set(panel_pixels)) > 2                     # something was drawn there
