# Wizard vs Monsters

A 2D shooting game written in Python with Pygame, developed as the semester project of the
**MTI — Methods & Technologies of Implementation** module (Master 1 GSI, University of Bouira).

The player controls a wizard who must survive in an arena while monsters chase him.
The wizard defends himself by firing magic bolts.

## Features (v1.0 — TP2)

- Wizard moving freely inside the arena (arrow keys or Z/Q/S/D)
- Magic bolts fired with **Space** in the direction the wizard faces, with a fire cooldown
- Monsters spawning at the top of the arena and chasing the wizard
- Hits: a bolt damages a monster; 3 hits defeat it, the score increases and a new monster appears
- Tiled arena with a frame; nothing can leave the play area

## Controls

| Key | Action |
|---|---|
| Arrow keys / Z Q S D | Move |
| Space (hold) | Fire magic bolts |
| Esc | Quit |

## Installation and launch

```bash
cd shooting_game
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python game.py
```

## Tests

```bash
cd shooting_game
python -m pytest -v
```

29 automated tests check the class hierarchy, the board limits, player movement and shooting,
monster pursuit, bullet behaviour and the interaction between objects.

## Project structure

```
shooting_game/
├── assets/              # sprites (wizard.png, monster.png)
├── tests/               # pytest test suite
├── conftest.py          # pytest setup (pygame without a window, shared fixtures)
├── game.py              # entry point: Game class and main loop
├── game_object.py       # GameObject  (abstract base class)
├── character.py         # Character   (abstract: GameObject + health)
├── player.py            # Player      (the wizard)
├── monster.py           # Monster
├── bullet.py            # Bullet      (magic bolt)
├── board.py             # GameBoard   (the arena)
├── settings.py          # all constants (sizes, speeds, colours…)
└── requirements.txt
```

## Object-oriented design

```
pygame.sprite.Sprite
└── GameObject (abstract)      position, speed, image · move() · update() is abstract
    ├── Character (abstract)   + protected health · take_damage() · is_alive
    │   ├── Player             + score, direction, facing, weapon · shoot()
    │   └── Monster            + target, attack_type · spawn_random()
    └── Bullet                 + direction, damage · removed outside the board

Game  ──has a──>  GameBoard, Player, Monsters, Bullets
```

- **Abstraction** — `GameObject` and `Character` cannot be instantiated.
- **Inheritance** — shared code (image loading, position, movement) is written once.
- **Encapsulation** — health can only change through `take_damage()`; the fire rate through `shoot()`.
- **Polymorphism** — `Game.update()` calls `update(dt)` on every object; each one behaves its own way.

## Git workflow

Each feature was developed on its own branch and merged into `main`:

| Branch | Content |
|---|---|
| `feature/game-abstraction` | `GameObject` and `Character` base classes |
| `feature/game-board` | `GameBoard` class |
| `feature/game-bullet` | `Bullet` class, shooting and hits |
| `feature/game-tests` | pytest tests and this README |

Version **v1.0** is tagged `game-v1.0`.

## Roadmap

- TP3 — SOLID: monster health bar, monster types and abilities, damage system
- Next — rewards, levels, menus and game states (Game Over / Victory)
