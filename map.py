# map.py
"""Map generation and management."""

import random
from constants import *

class Room:
    """Represents a rectangular room in the dungeon."""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def overlaps(self, other):
        """Check if this room overlaps with another."""
        return (self.x < other.x + other.w and self.x + self.w > other.x and
                self.y < other.y + other.h and self.y + self.h > other.y)

    def center(self):
        """Return the center coordinates of the room."""
        return self.x + self.w // 2, self.y + self.h // 2

class Map:
    """Manages the dungeon map with tiles and properties."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[TILE_WALL for _ in range(width)] for _ in range(height)]
        self.explored = [[False for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.generate()

    def generate(self):
        """Generate a dungeon with rooms and corridors."""
        num_rooms = random.randint(8, 15)
        for _ in range(num_rooms):
            w = random.randint(5, 10)
            h = random.randint(5, 10)
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)
            new_room = Room(x, y, w, h)
            if not any(new_room.overlaps(room) for room in self.rooms):
                self.carve_room(new_room)
                self.rooms.append(new_room)
        for i in range(len(self.rooms) - 1):
            x1, y1 = self.rooms[i].center()
            x2, y2 = self.rooms[i + 1].center()
            self.create_corridor(x1, y1, x2, y2)
        self.place_stairs()

    def carve_room(self, room):
        """Carve out a room in the map."""
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                self.tiles[y][x] = TILE_FLOOR

    def create_corridor(self, x1, y1, x2, y2):
        """Create a corridor between two points."""
        if random.random() < 0.5:
            self.carve_h_corridor(x1, x2, y1)
            self.carve_v_corridor(y1, y2, x2)
        else:
            self.carve_v_corridor(y1, y2, x1)
            self.carve_h_corridor(x1, x2, y2)

    def carve_h_corridor(self, x1, x2, y):
        """Carve a horizontal corridor."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y][x] = TILE_FLOOR

    def carve_v_corridor(self, y1, y2, x):
        """Carve a vertical corridor."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[y][x] = TILE_FLOOR

    def place_stairs(self):
        """Place stairs up and down in the first and last rooms."""
        self.tiles[self.rooms[0].y + 1][self.rooms[0].x + 1] = TILE_STAIRS_UP
        self.tiles[self.rooms[-1].y + 1][self.rooms[-1].x + 1] = TILE_STAIRS_DOWN

    def is_walkable(self, x, y):
        """Check if a tile is walkable."""
        return (0 <= x < self.width and 0 <= y < self.height and
                self.tiles[y][x] in (TILE_FLOOR, TILE_STAIRS_DOWN, TILE_STAIRS_UP))

    def is_transparent(self, x, y):
        """Check if a tile allows light to pass through."""
        return (0 <= x < self.width and 0 <= y < self.height and
                self.tiles[y][x] in (TILE_FLOOR, TILE_STAIRS_DOWN, TILE_STAIRS_UP))