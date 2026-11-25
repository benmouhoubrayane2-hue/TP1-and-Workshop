"""Crystal Hunt: a second game built with a NEW model and the SAME view and controller.
Run:  python main_crystal.py"""
from main import run
from crystal_hunt.model import CrystalHuntModel
from view.theme import ThemeLibrary, ASSETS

if __name__ == "__main__":
    run(CrystalHuntModel(), ThemeLibrary(folder=ASSETS / "themes_crystal", first="cave"))
