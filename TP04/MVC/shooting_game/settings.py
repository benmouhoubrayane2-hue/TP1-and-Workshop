"""Global game settings (constants only)."""

# Window
WIDTH = 960                      # size of the game area (the model's world)
HEIGHT = 640
PANEL_WIDTH = 250                # information panel, drawn by the view on the right
WINDOW_WIDTH = WIDTH + PANEL_WIDTH
TITLE = "Wizard vs Monsters"
FPS = 60

# Appearance: pictures, background, colours and sounds are chosen by a theme
# (assets/themes/*.json). Press T in the game to switch theme.
DEFAULT_THEME = "dungeon"

# Game board (the arena)
BOARD_MARGIN = 20                # space between the window edge and the arena (px)
BORDER_WIDTH = 4

# Player
PLAYER_WIDTH = 72          # size of the wizard on screen (px)
PLAYER_HEIGHT = 96
PLAYER_SPEED = 320         # pixels per second
PLAYER_MAX_HEALTH = 100

# Monster
MONSTER_WIDTH = 72
MONSTER_HEIGHT = 72
MONSTER_SPEED = 140        # slower than the player, so you can escape
MONSTER_HEALTH = 30
MONSTER_COUNT = 3         # monsters on the board at the same time

# Bullet (magic bolt)
BULLET_SPEED = 600         # pixels per second
BULLET_DAMAGE = 10         # a monster (30 HP) needs 3 hits
BULLET_RADIUS = 6
FIRE_COOLDOWN = 0.25       # seconds between two shots

# Health bar (drawn above each monster)
HEALTH_BAR_HEIGHT = 6
HEALTH_BAR_GAP = 4               # space between the bar and the top of the sprite (px)
HEALTH_BAR_BG = (60, 20, 28)     # empty part of the bar
HEALTH_BAR_BORDER = (10, 10, 16)
HEALTH_HIGH = (90, 220, 110)     # more than 60 % left
HEALTH_MID = (240, 180, 60)      # more than 30 % left
HEALTH_LOW = (230, 70, 70)       # 30 % or less

# Monster abilities
ENEMY_BOLT_SPEED = 260           # slower than the wizard's bolts
ENEMY_BOLT_DAMAGE = 10
ENEMY_BOLT_RADIUS = 7
SHIELD_COLOR = (110, 220, 255)

# Contact attacks
MONSTER_CONTACT_DAMAGE = 10      # damage when a monster touches the wizard
PLAYER_INVULNERABLE_TIME = 1.0   # seconds of protection (blinking) after being hit
KNOCKBACK_DISTANCE = 70          # how far a monster is pushed back after biting
