"""Resources and themes: pictures, backgrounds and sounds live in their own folders and
are chosen by theme files, so the look of the game changes without touching the logic."""
import json
from pathlib import Path

import pygame
import pytest

from model.game_model import GameModel
from model.events import GameEvent, SHOT, HIT, PLAYER_HURT, MONSTER_DEFEATED, GAME_OVER
from model.monster_types import MONSTER_TYPES
from model.player import Player
from model.bullet import Bullet, Fireball
from model.enemy_bolt import EnemyBolt
from view.theme import ThemeLibrary, ASSETS
from view.images import ImageLibrary
from view.game_view import GameView
from view.sound_player import SoundPlayer

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = {"player": ".png", "monsters": ".png", "bullets": ".png",
           "backgrounds": ".png", "sounds": ".wav", "themes": ".json"}
ALL_KINDS = [Player.KIND, Bullet.KIND, Fireball.KIND, EnemyBolt.KIND] + [t.KIND for t in MONSTER_TYPES]
THEMES = ThemeLibrary().themes


# --- 1. Resources are separated into folders ----------------------------------

@pytest.mark.parametrize("folder, extension", FOLDERS.items())
def test_each_kind_of_resource_has_its_own_folder(folder, extension):
    files = list((ASSETS / folder).iterdir())
    assert files and all(f.suffix == extension for f in files)


def test_no_loose_file_left_in_assets():
    assert all(p.is_dir() for p in ASSETS.iterdir())


@pytest.mark.parametrize("theme", THEMES, ids=lambda t: t.name)
def test_every_file_named_by_a_theme_exists(theme):
    assert theme.background_path().exists()
    for kind in theme.images:
        assert theme.image_path(kind).exists(), kind
    for event in theme.sounds:
        assert theme.sound_path(event).exists(), event


# --- 2. Images change without touching the behaviour code ---------------------

@pytest.mark.parametrize("theme", THEMES, ids=lambda t: t.name)
@pytest.mark.parametrize("kind", ALL_KINDS)
def test_every_object_of_the_game_has_a_picture_in_every_theme(theme, kind):
    assert kind in theme.images


@pytest.mark.parametrize("word", [".png", ".wav", ".json", "assets"])
def test_the_model_never_names_a_file(word):
    source = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "model").glob("*.py"))
    assert word not in source


def test_a_new_theme_is_only_a_json_file(tmp_path):
    """Give the wizard another picture: no Python code is changed, only a theme file."""
    data = json.loads((ASSETS / "themes" / "dungeon.json").read_text())
    data["name"] = "Test"
    data["images"]["player"] = "monsters/monster_strong.png"   # the wizard now looks like a red monster
    (tmp_path / "test.json").write_text(json.dumps(data))
    theme = ThemeLibrary(folder=tmp_path).current
    model = GameModel()
    normal = ImageLibrary(ThemeLibrary().current).get(model.player)
    changed = ImageLibrary(theme).get(model.player)
    assert pygame.image.tostring(normal, "RGBA") != pygame.image.tostring(changed, "RGBA")


# --- 3. Background and appearance change independently of the game logic ------

def test_there_are_several_themes_with_different_looks():
    assert len(THEMES) >= 2
    assert len({t.background for t in THEMES}) == len(THEMES)
    assert len({t.border_color for t in THEMES}) == len(THEMES)


def test_switching_theme_changes_the_pictures_but_not_the_model():
    model = GameModel()
    view = GameView(model, pygame.Surface((960, 640)))
    before_state = (tuple(model.player.pos), model.player.health, model.score, len(model.objects))
    first = view.theme.name
    picture_before = view.images.get(model.player)

    view.next_theme()                                    # what the T key does

    assert view.theme.name != first
    assert view.images.get(model.player) is not picture_before
    view.draw(pygame.Surface((960, 640)))                # the new background is drawn
    assert (tuple(model.player.pos), model.player.health, model.score, len(model.objects)) == before_state


def test_t_key_asks_the_view_for_the_next_theme():
    from controller.keyboard_controller import KeyboardController
    model = GameModel()
    view = GameView(model, pygame.Surface((960, 640)))
    first = view.theme.name
    KeyboardController(model, view).handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t))
    assert view.theme.name != first


# --- Sounds -----------------------------------------------------------------

@pytest.mark.parametrize("event, sound", [
    (GameEvent(SHOT, name="magic_bolt"), "shot"), (GameEvent(SHOT, name="fireball"), "shot_fireball"),
    (GameEvent(HIT), "hit"), (GameEvent(PLAYER_HURT), "hurt"),
    (GameEvent(MONSTER_DEFEATED), "defeated"), (GameEvent(GAME_OVER), "game_over")])
def test_every_event_has_a_sound_in_every_theme(event, sound):
    player = SoundPlayer(THEMES[0])
    assert player.sound_for(event) == sound
    for theme in THEMES:
        assert theme.sound_path(sound).exists()


def test_playing_sounds_never_crashes():
    player = SoundPlayer(THEMES[0])                       # silent if there is no sound card
    for kind in (SHOT, HIT, PLAYER_HURT, MONSTER_DEFEATED, GAME_OVER):
        player.play(GameEvent(kind))
