# player.py
"""Player character implementation."""

import random
from entity import Entity
from constants import *

class Player(Entity):
    """The player character with stats and inventory."""
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_CHAR, COLOR_WHITE)
        self.health = 100
        self.max_health = 100
        self.strength = 10
        self.defense = 5
        self.inventory = []
        self.level = 1
        self.xp = 0
        self.xp_to_level = 50

    def attack(self, target):
        """
        Attack a target entity.

        Args:
            target: Entity to attack.

        Returns:
            int: Damage dealt.
        """
        damage = max(0, self.strength - target.defense + random.randint(-2, 2))
        target.health -= damage
        return damage

    def add_item(self, item):
        """Add an item to the inventory."""
        if len(self.inventory) < 10:  # Inventory limit
            self.inventory.append(item)
            return True
        return False

    def use_item(self, index):
        """
        Use an item from the inventory.

        Args:
            index (int): Index of the item to use.
        """
        if 0 <= index < len(self.inventory):
            item = self.inventory.pop(index)
            item.effect(self)

    def gain_xp(self, amount):
        """Gain experience points and level up if needed."""
        self.xp += amount
        while self.xp >= self.xp_to_level:
            self.level_up()

    def level_up(self):
        """Increase player level and stats."""
        self.level += 1
        self.xp -= self.xp_to_level
        self.xp_to_level = int(self.xp_to_level * 1.5)
        self.max_health += 10
        self.health = self.max_health
        self.strength += 2
        self.defense += 1