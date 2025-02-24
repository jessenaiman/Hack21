# game.py
"""Main game logic."""

import random
from map import Map
from player import Player
from monster import Monster
from item import create_health_potion, create_strength_boost
from ui import HealthBar, MessageLog, InventoryScreen
from utils import calculate_fov
from constants import *

class Game:
    """Manages the game state and mechanics."""
    def __init__(self):
        self.current_level = 1
        self.map = Map(MAP_WIDTH, MAP_HEIGHT)
        self.player = None
        self.monsters = []
        self.items = []
        self.visible_tiles = set()
        self.state = STATE_PLAYING
        self.health_bar = HealthBar(10, MAP_SCREEN_HEIGHT + 10, 200, 20)
        self.message_log = MessageLog(220, MAP_SCREEN_HEIGHT + 10, SCREEN_WIDTH - 230, SCREEN_HEIGHT - MAP_SCREEN_HEIGHT - 20)
        self.inventory_screen = InventoryScreen(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.sound = SoundManager()
        self.initialize_level()

    def initialize_level(self):
        """Set up the current dungeon level."""
        self.map = Map(MAP_WIDTH, MAP_HEIGHT)
        self.player = Player(self.map.rooms[0].x + 2, self.map.rooms[0].y + 2)
        self.monsters = [Monster(room.x + random.randint(0, room.w - 1), room.y + random.randint(0, room.h - 1))
                         for room in self.map.rooms[1:-1]]
        self.items = [random.choice([create_health_potion, create_strength_boost])(room.x + 1, room.y + 1)
                      for room in self.map.rooms[1:]]
        self.update_fov()

    def update_fov(self):
        """Update the player's field of view."""
        self.visible_tiles = calculate_fov(self.map, self.player.x, self.player.y, 8)
        for x, y in self.visible_tiles:
            self.map.explored[y][x] = True

    def process_action(self, dx, dy):
        """Process player movement or action."""
        new_x, new_y = self.player.x + dx, self.player.y + dy
        if not self.map.is_walkable(new_x, new_y):
            return
        for monster in self.monsters[:]:
            if monster.x == new_x and monster.y == new_y:
                damage = self.player.attack(monster)
                self.message_log.add(f"You hit the {monster.name} for {damage} damage.")
                self.sound.play('attack')
                if monster.health <= 0:
                    self.message_log.add(f"You killed the {monster.name}!")
                    self.player.gain_xp(monster.xp_value)
                    self.monsters.remove(monster)
                return
        for i, item in enumerate(self.items):
            if item.x == new_x and item.y == new_y:
                if self.player.add_item(item):
                    self.message_log.add(f"Picked up {item.name}.")
                    self.items.pop(i)
                    break
                else:
                    self.message_log.add("Inventory full!")
                    return
        tile = self.map.tiles[new_y][new_x]
        if tile == TILE_STAIRS_DOWN:
            self.current_level += 1
            self.message_log.add(f"You descend to level {self.current_level}.")
            self.initialize_level()
        elif tile == TILE_STAIRS_UP and self.current_level > 1:
            self.current_level -= 1
            self.message_log.add(f"You ascend to level {self.current_level}.")
            self.initialize_level()
        else:
            self.player.move(dx, dy)
            self.sound.play('move')
        self.update_monsters()
        self.update_fov()

    def update_monsters(self):
        """Update all monsters."""
        for monster in self.monsters[:]:
            if (monster.x, monster.y) in self.visible_tiles:
                monster.update(self.player, self.map)
                if abs(monster.x - self.player.x) <= 1 and abs(monster.y - self.player.y) <= 1:
                    damage = monster.attack(self.player)
                    self.message_log.add(f"The {monster.name} hits you for {damage} damage.")
                    self.sound.play('attack')
                    if self.player.health <= 0:
                        self.message_log.add("You have died!")
                        self.state = "dead"

    def draw(self, screen):
        """Render the game state."""
        for y in range(self.map.height):
            for x in range(self.map.width):
                if (x, y) in self.visible_tiles:
                    tile = self.map.tiles[y][x]
                    color = COLOR_GRAY if tile == TILE_FLOOR else COLOR_YELLOW if tile in (TILE_STAIRS_DOWN, TILE_STAIRS_UP) else COLOR_BLACK
                elif self.map.explored[y][x]:
                    tile = self.map.tiles[y][x]
                    color = COLOR_DARK_GRAY if tile == TILE_FLOOR else COLOR_BLACK
                else:
                    color = COLOR_BLACK
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, color, rect)
        for item in self.items:
            if (item.x, item.y) in self.visible_tiles:
                item.draw(screen)
        for monster in self.monsters:
            if (monster.x, monster.y) in self.visible_tiles:
                monster.draw(screen)
        self.player.draw(screen)
        self.health_bar.draw(screen, self.player)
        self.message_log.draw(screen)
        if self.state == STATE_INVENTORY:
            self.inventory_screen.draw(screen, self.player)