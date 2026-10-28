"""Global game settings (constants only)."""

# Window
WIDTH = 960
HEIGHT = 640
TITLE = "Wizard vs Monsters"
FPS = 60

# Colors (R, G, B)
BG_COLOR = (12, 13, 20)          # around the board

# Game board (the arena)
BOARD_MARGIN = 20                # space between the window edge and the arena (px)
TILE_SIZE = 64                   # size of one floor tile (px)
TILE_COLOR_A = (30, 33, 48)      # floor tiles alternate between these two colours
TILE_COLOR_B = (26, 29, 42)
TILE_LINE_COLOR = (38, 42, 60)   # thin lines between tiles
BORDER_COLOR = (130, 100, 220)   # magic purple frame
BORDER_WIDTH = 4

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
# Bullet (magic bolt)
BULLET_SPEED = 600         # pixels per second
BULLET_DAMAGE = 10         # a monster (30 HP) needs 3 hits
BULLET_RADIUS = 6
BULLET_COLOR = (120, 240, 255)
FIRE_COOLDOWN = 0.25       # seconds between two shots