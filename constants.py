# constants.py
"""Game constants for the roguelike."""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_SCREEN_HEIGHT = 500  # Reserve space for UI

# Tile properties
TILE_SIZE = 16
MAP_WIDTH = 50
MAP_HEIGHT = 30

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (100, 100, 100)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)

# Tile types
TILE_FLOOR = 0
TILE_WALL = 1
TILE_STAIRS_DOWN = 2
TILE_STAIRS_UP = 3

# Entity characters (for reference, not displayed directly)
PLAYER_CHAR = '@'
MONSTER_CHAR = 'M'
ITEM_CHAR = '!'
STAIRS_DOWN_CHAR = '>'
STAIRS_UP_CHAR = '<'

# Game states
STATE_PLAYING = 'playing'
STATE_INVENTORY = 'inventory'