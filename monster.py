# monster.py
"""Monster implementation with AI."""

import random
from entity import Entity
from constants import *

class Monster(Entity):
    """An enemy monster with stats and behavior."""
    def __init__(self, x, y, name="Goblin", health=20, strength=5, defense=2):
        super().__init__(x, y, MONSTER_CHAR, COLOR_RED)
        self.name = name
        self.health = health
        self.strength = strength
        self.defense = defense
        self.xp_value = 10

    def attack(self, target):
        """
        Attack a target entity.

        Returns:
            int: Damage dealt.
        """
        damage = max(0, self.strength - target.defense + random.randint(-1, 1))
        target.health -= damage
        return damage

    def update(self, player, game_map):
        """Update monster behavior (chase player if nearby)."""
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(abs(dx), abs(dy))
        if dist <= 5:  # Chase range
            if dist == 1:
                return  # Attack handled elsewhere
            move_x = 1 if dx > 0 else -1 if dx < 0 else 0
            move_y = 1 if dy > 0 else -1 if dy < 0 else 0
            new_x, new_y = self.x + move_x, self.y + move_y
            if game_map.is_walkable(new_x, new_y):
                self.move(move_x, move_y)