"""SoundPlayer: plays the sound of each model event, as chosen by the theme (view side)."""
import pygame
from model.events import SHOT, HIT, PLAYER_HURT, MONSTER_DEFEATED, GAME_OVER


class SoundPlayer:
    """If the computer has no sound card, the game simply stays silent."""

    def __init__(self, theme):
        self.enabled = self._start_mixer()
        self.set_theme(theme)

    @staticmethod
    def _start_mixer():
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return True
        except pygame.error:
            return False

    def set_theme(self, theme):
        self.theme = theme
        self._sounds = {}

    def sound_for(self, event):
        """Name of the theme sound for this event (the fireball has its own shot sound)."""
        if event.kind == SHOT:
            return "shot_fireball" if event.name == "fireball" else "shot"
        names = {HIT: "hit", PLAYER_HURT: "hurt", MONSTER_DEFEATED: "defeated", GAME_OVER: "game_over"}
        return names.get(event.kind, event.kind)      # other events: the sound with the same name

    def play(self, event):
        name = self.sound_for(event)
        if not self.enabled or name is None:
            return
        if name not in self._sounds:
            path = self.theme.sound_path(name)
            self._sounds[name] = pygame.mixer.Sound(str(path)) if path and path.exists() else None
        if self._sounds[name]:
            self._sounds[name].play()
