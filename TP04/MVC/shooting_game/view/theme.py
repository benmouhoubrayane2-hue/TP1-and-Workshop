"""Theme: the look and sound of the game, described in a JSON file (view side).

A theme says which picture each kind of object uses, which background and colours
the arena has and which sound each event makes. Changing the look of the game
means editing or adding a file in assets/themes/ - no Python code changes.
"""
import json
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
THEMES = ASSETS / "themes"


class Theme:

    def __init__(self, path, assets=ASSETS):
        self.path = Path(path)
        self.assets = Path(assets)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.name = data["name"]
        self.title = data.get("title", "Wizard vs Monsters")          # name of the game
        self.background = data["background"]                       # file in assets/
        self.background_color = tuple(data.get("background_color", (0, 0, 0)))
        self.border_color = tuple(data.get("border_color", (255, 255, 255)))
        self.images = data["images"]                               # KIND  -> file in assets/
        self.sounds = data.get("sounds", {})                       # event -> file in assets/

    def image_path(self, kind):
        return self.assets / self.images[kind] if kind in self.images else None

    def sound_path(self, event):
        return self.assets / self.sounds[event] if event in self.sounds else None

    def background_path(self):
        return self.assets / self.background


class ThemeLibrary:
    """All the themes found in assets/themes/, and which one is in use."""

    def __init__(self, folder=THEMES, assets=ASSETS, first="dungeon"):
        files = sorted(Path(folder).glob("*.json"))
        self.themes = [Theme(f, assets) for f in files]
        names = [f.stem for f in files]
        self.index = names.index(first) if first in names else 0

    @property
    def current(self):
        return self.themes[self.index]

    def next(self):
        self.index = (self.index + 1) % len(self.themes)
        return self.current
