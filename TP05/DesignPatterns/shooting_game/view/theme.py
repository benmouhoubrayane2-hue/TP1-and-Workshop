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
        self.world = data.get("world")                             # world of the model it is for
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

        self.world = None                    # None: every theme can be used

    @property
    def current(self):
        return self.themes[self.index]

    def _usable(self):
        return [i for i, t in enumerate(self.themes) if self.world is None or t.world == self.world]

    def select_world(self, world):
        """Use only the themes made for `world` (e.g. "space"); keep the current one if it fits."""
        self.world = world
        usable = self._usable()
        if usable and self.index not in usable:
            self.index = usable[0]
        return self.current

    def select_name(self, name):
        """Use the theme called `name` (e.g. "forest") if there is one."""
        for i, theme in enumerate(self.themes):
            if theme.name.lower() == name.lower():
                self.index = i
        return self.current

    def next(self):
        """Next theme of the current world."""
        usable = self._usable() or list(range(len(self.themes)))
        position = usable.index(self.index) if self.index in usable else -1
        self.index = usable[(position + 1) % len(usable)]
        return self.current
