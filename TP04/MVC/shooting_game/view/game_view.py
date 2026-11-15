"""GameView: draws the model on the screen (the V of MVC).

It reads the model (positions, health, score, status) and the events of the last
frame, and turns them into pictures. It never changes the model and never reads
the keyboard.
"""
import pygame
from settings import WIDTH, HEIGHT, WINDOW_WIDTH, DEFAULT_THEME
from model.abilities import Shielded
from model.events import HIT
from view.theme import ThemeLibrary
from view.images import ImageLibrary
from view.sound_player import SoundPlayer
from view.board_view import BoardView
from view.health_bar import HealthBar
from view.shield_view import ShieldView
from view.damage_text import DamageText
from view.game_over_view import GameOverView
from view.info_panel import InfoPanel


class GameView:

    def __init__(self, model, screen=None, themes=None):
        self.model = model
        self.screen = screen or pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
        self.themes = themes or ThemeLibrary(first=DEFAULT_THEME)
        self.images = ImageLibrary(self.theme)
        self.sounds = SoundPlayer(self.theme)
        self.health_bar = HealthBar()
        self.shield_view = ShieldView()
        self.game_over_view = GameOverView()
        self.info_panel = InfoPanel((WIDTH, 0, WINDOW_WIDTH - WIDTH, HEIGHT))   # right of the arena
        self.pause_font = pygame.font.Font(None, 72)
        self.damage_texts = []
        self._board_view = None
        self._caption = None
        self._time = 0.0                     # used to make the wizard blink

    # ----------------------------------------------------------------- themes
    @property
    def theme(self):
        return self.themes.current

    def next_theme(self):
        """Change the whole look (pictures, background, colours, sounds).
        Only the view changes: the model does not even know it happened."""
        theme = self.themes.next()
        self.images.set_theme(theme)
        self.sounds.set_theme(theme)
        self._board_view = None

    # ------------------------------------------------------------- per frame
    def render(self, dt=0.0):
        """Show the events of the frame, draw everything, then display the frame."""
        self._time += dt
        for event in self.model.pop_events():
            self.on_event(event)
        for text in self.damage_texts:
            text.update(dt)
        self.damage_texts = [t for t in self.damage_texts if t.alive]
        self.draw(self.screen)
        self.update_caption()
        pygame.display.flip()

    def on_event(self, event):
        """Turn a model event into something visible and audible."""
        self.sounds.play(event)
        if event.kind == HIT:
            self.damage_texts.append(DamageText(event.pos.x, event.pos.y - 24, event.value, event.base))

    # --------------------------------------------------------------- drawing
    def draw(self, surface):
        model = self.model
        surface.fill(self.theme.background_color)
        self.board_view().draw(surface)

        objects = model.drawables()            # any model: it only gives KIND + rect (+ health)
        for obj in objects:
            blinking = getattr(obj, "is_invulnerable", False) and int(self._time * 10) % 2
            if not blinking:                    # the wizard blinks after a hit
                self.draw_object(surface, obj)
        for obj in objects:
            if hasattr(obj, "health_ratio"):
                self.health_bar.draw(surface, obj)
            if isinstance(obj, Shielded):
                self.shield_view.draw(surface, obj)
        for text in self.damage_texts:
            text.draw(surface)

        arena = surface.subsurface((0, 0, min(WIDTH, surface.get_width()), min(HEIGHT, surface.get_height())))
        if model.game_over:
            self.game_over_view.draw(arena, model.score)
        elif model.paused:
            self.draw_paused(arena)
        if surface.get_width() >= WINDOW_WIDTH:
            self.info_panel.draw(surface, model.info(), self.theme, self.theme.title)

    def draw_paused(self, surface):
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 120))
        surface.blit(shade, (0, 0))
        text = self.pause_font.render("PAUSED", True, (245, 200, 70))
        surface.blit(text, text.get_rect(center=surface.get_rect().center))

    def draw_object(self, surface, obj):
        surface.blit(self.images.get(obj), obj.rect)

    def board_view(self):
        """The arena picture is rebuilt only when the model creates a new board."""
        if self._board_view is None or self._board_view.board is not self.model.board:
            self._board_view = BoardView(self.model.board, self.theme)
        return self._board_view

    def update_caption(self):
        """Window title (the score, health and status are now in the information panel)."""
        caption = self.theme.title
        if caption != self._caption:
            pygame.display.set_caption(caption)
            self._caption = caption
