"""KeyboardController: reads the keyboard and gives orders to the model (the C of MVC).

It never draws and never applies a game rule itself: it only translates keys
into calls such as model.move_player() or model.switch_weapon()
(and view.next_theme() for the T key).
"""
import pygame

MOVE_KEYS = {                         # key -> (x, y) contribution to the direction
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
    pygame.K_LEFT: (-1, 0), pygame.K_q: (-1, 0),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_UP: (0, -1), pygame.K_z: (0, -1),
}
FIRE_KEY = pygame.K_SPACE
SUMMON_KEYS = {                       # key -> monster number 0, 1, 2 of the current world
    pygame.K_3: 0, pygame.K_KP3: 0,
    pygame.K_4: 1, pygame.K_KP4: 1,
    pygame.K_5: 2, pygame.K_KP5: 2,
}


class KeyboardController:

    def __init__(self, model, view=None):
        self.model = model
        self.view = view          # only used to ask for another theme (T key)
        self.running = True

    def handle_input(self):
        """Called once per frame by the main loop."""
        for event in pygame.event.get():
            self.handle_event(event)
        self.handle_keys(pygame.key.get_pressed())

    def handle_event(self, event):
        """One-time actions: quit, restart, choose a weapon."""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_r:
                self.model.restart()
            elif event.key == pygame.K_p:
                self.model.toggle_pause()
            elif event.key in SUMMON_KEYS:
                self.model.summon_slot(SUMMON_KEYS[event.key])
            elif event.key in (pygame.K_1, pygame.K_KP1):
                self.model.switch_weapon(0)
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.model.switch_weapon(1)
            elif event.key == pygame.K_TAB:
                self.model.switch_weapon()
            elif event.key == pygame.K_t and self.view is not None:
                self.view.next_theme()            # appearance only: the model is not touched

    def handle_keys(self, pressed):
        """Keys held down: movement direction and fire button."""
        x = y = 0
        for key, (dx, dy) in MOVE_KEYS.items():
            if pressed[key]:
                x += dx
                y += dy
        self.model.move_player((max(-1, min(1, x)), max(-1, min(1, y))))
        self.model.set_trigger(pressed[FIRE_KEY])
