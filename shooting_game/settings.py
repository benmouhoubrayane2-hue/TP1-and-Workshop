"""Global game settings (constants only)."""

# Window
WIDTH = 960
HEIGHT = 640
TITLE = "Wizard vs Monsters"
FPS = 60

# Colors (R, G, B)
BG_COLOR = (18, 20, 30)

# Player
PLAYER_WIDTH = 72          # size of the wizard on screen (px)
PLAYER_HEIGHT = 96
PLAYER_SPEED = 320         # pixels per second
PLAYER_MAX_HEALTH = 100
PLAYER_IMAGE = "wizard.png"   # file inside the assets/ folder

# Monster
MONSTER_WIDTH = 72
MONSTER_HEIGHT = 72
MONSTER_SPEED = 140        # slower than the player, so you can escape
MONSTER_HEALTH = 30
MONSTER_IMAGE = "monster.png"