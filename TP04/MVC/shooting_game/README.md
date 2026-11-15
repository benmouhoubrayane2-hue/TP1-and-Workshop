# Wizard vs Monsters

A 2D shooting game written in Python with Pygame, developed as the semester project of the
**MTI — Methods & Technologies of Implementation** module (Master 1 GSI, University of Bouira).

The wizard must survive in an arena while monsters chase him, shoot at him or hide behind shields.
He defends himself with two weapons: a magic wand and a fire staff.

## Versions

| Version | Workshop | What was added |
|---|---|---|
| 1.0 | TP2 | Wizard, monsters, magic bolts, collisions, score, tests |
| 2.0 | TP3 | SOLID: health component, 7 monster types, abilities, resistances, 2 weapons |
| 3.0 | TP4 | MVC architecture, resource folders, themes, sounds, information panel, a second game |

## Run

```bash
cd shooting_game
pip install -r requirements.txt
python main.py            # Wizard vs Monsters
python main_crystal.py    # Crystal Hunt (same View and Controller, another Model)
python -m pytest          # 234 automated tests
```

## Controls

| Key | Action |
|---|---|
| Arrow keys / Z Q S D | Move |
| Space (hold) | Fire |
| 1 / 2 / Tab | Choose the weapon |
| P | Pause / resume |
| T | Change the theme (pictures, background, colours, sounds) |
| R | Play again after a game over |
| Esc | Quit |

## Architecture (MVC)

```
shooting_game/
├── main.py              # builds Model + View + Controller and runs the loop
├── main_crystal.py      # second game: new Model, same View and Controller
├── settings.py          # sizes, speeds, damage... (no file names)
├── model/               # M - state and rules only: no image, no drawing, no keyboard
│   ├── game_interface.py    # what any game model offers to the view and controller
│   ├── game_model.py        # rules of Wizard vs Monsters, events, info for the panel
│   ├── player.py, monster.py, monster_types.py, abilities.py
│   ├── bullet.py, enemy_bolt.py, weapons.py, damage.py
│   └── game_object.py, character.py, health.py, board.py, events.py
├── view/                # V - everything the player sees and hears
│   ├── game_view.py         # draws the model, turns events into effects and sounds
│   ├── theme.py, images.py, sound_player.py
│   └── board_view.py, info_panel.py, health_bar.py, shield_view.py, damage_text.py, game_over_view.py
├── controller/          # C - keyboard -> commands for the model
│   └── keyboard_controller.py
├── crystal_hunt/        # the model of the second game
├── assets/
│   ├── player/  monsters/  bullets/  items/  backgrounds/  sounds/
│   ├── themes/              # dungeon.json, forest.json  (Wizard vs Monsters)
│   └── themes_crystal/      # cave.json, meadow.json     (Crystal Hunt)
└── tests/
```

**Changing the look of the game** needs no Python code: a theme file (`assets/themes/*.json`)
says which picture each object uses (by its `KIND`), which background and colours the arena has,
and which sound each event makes. Add a JSON file and its pictures, and **T** will show it.
