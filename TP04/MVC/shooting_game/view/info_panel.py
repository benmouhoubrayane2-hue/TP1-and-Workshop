"""InfoPanel: shows the score, the health and the game status next to the arena (display only).

It asks the model for model.info() - plain data such as {"Score": 3, "Health": (70, 100)} -
and draws it. Any model that offers info() can use this panel.
"""
import pygame

STATUS_COLORS = {"Playing": (110, 220, 120), "Paused": (245, 200, 70), "Game over": (235, 80, 80)}
TEXT = (230, 232, 240)
DIM = (150, 155, 175)
BAR_BG = (60, 20, 28)
CONTROLS = ["Arrows / ZQSD  move", "Space  fire", "1 / 2 / Tab  weapon",
            "P  pause", "T  theme", "R  restart", "Esc  quit"]


class InfoPanel:

    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.title_font = pygame.font.Font(None, 30)
        self.label_font = pygame.font.Font(None, 24)
        self.value_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 22)

    @staticmethod
    def lines(info):
        """The panel as text, e.g. ["Score: 3", "Health: 70 / 100", ...] (used by the tests)."""
        out = []
        for label, value in info.items():
            if isinstance(value, tuple):
                value = f"{value[0]} / {value[1]}"
            out.append(f"{label}: {value}")
        return out

    def draw(self, surface, info, theme, title="Wizard vs Monsters"):
        pygame.draw.rect(surface, tuple(c // 2 for c in theme.background_color), self.rect)
        pygame.draw.line(surface, theme.border_color, self.rect.topleft, self.rect.bottomleft, 3)
        x = self.rect.left + 20
        width = self.rect.width - 40
        y = self.rect.top + 22

        surface.blit(self.title_font.render(title, True, theme.border_color), (x, y))
        y += 34
        surface.blit(self.small_font.render(f"Theme: {theme.name}", True, DIM), (x, y))
        y += 34

        for label, value in info.items():
            surface.blit(self.label_font.render(label.upper(), True, DIM), (x, y))
            y += 22
            if isinstance(value, tuple):                       # (current, maximum) -> a bar
                current, maximum = value
                ratio = max(0.0, min(1.0, current / maximum)) if maximum else 0
                bar = pygame.Rect(x, y + 4, width, 18)
                pygame.draw.rect(surface, BAR_BG, bar, border_radius=4)
                filled = bar.copy()
                filled.width = round(bar.width * ratio)
                color = (90, 220, 110) if ratio > 0.6 else (240, 180, 60) if ratio > 0.3 else (230, 70, 70)
                if filled.width:
                    pygame.draw.rect(surface, color, filled, border_radius=4)
                pygame.draw.rect(surface, (10, 10, 16), bar, 1, border_radius=4)
                text = self.small_font.render(f"{current} / {maximum}", True, TEXT)
                surface.blit(text, text.get_rect(center=bar.center))
                y += 34
            else:
                color = STATUS_COLORS.get(value, TEXT) if label == "Status" else TEXT
                surface.blit(self.value_font.render(str(value), True, color), (x, y))
                y += 36

        y = max(y + 6, self.rect.bottom - 22 * len(CONTROLS) - 16)
        pygame.draw.line(surface, DIM, (x, y - 8), (x + width, y - 8), 1)
        for line in CONTROLS:
            surface.blit(self.small_font.render(line, True, DIM), (x, y))
            y += 22
