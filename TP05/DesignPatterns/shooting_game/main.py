"""Entry point of Wizard vs Monsters: builds the Model, the View and the Controller
and runs the main loop.   Run:  python main.py"""
import pygame
from settings import FPS
from model.game_model import GameModel
from view.game_view import GameView
from controller.keyboard_controller import KeyboardController


def run(model, themes=None):
    """The main loop works with ANY game model (see main_crystal.py)."""
    pygame.init()
    view = GameView(model, themes=themes)          # V: opens the window, draws the model
    controller = KeyboardController(model, view)   # C: keyboard -> commands

    clock = pygame.time.Clock()
    while controller.running:
        dt = clock.tick(FPS) / 1000                # seconds since last frame
        controller.handle_input()                  # 1. input
        model.update(dt)                           # 2. rules
        view.render(dt)                            # 3. display
    pygame.quit()


def main():
    run(GameModel())                               # M: state and rules of Wizard vs Monsters


if __name__ == "__main__":
    main()
