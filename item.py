# item.py
"""Item implementation."""

from entity import Entity
from constants import *

class Item(Entity):
    """A collectible item with an effect."""
    def __init__(self, x, y, name, color, effect):
        super().__init__(x, y, ITEM_CHAR, color)
        self.name = name
        self.effect = effect

def create_health_potion(x, y):
    """Create a health potion item."""
    def heal(player):
        player.health = min(player.health + 20, player.max_health)
    return Item(x, y, "Health Potion", COLOR_GREEN, heal)

def create_strength_boost(x, y):
    """Create a strength-boosting item."""
    def boost(player):
        player.strength += 5
    return Item(x, y, "Strength Elixir", COLOR_YELLOW, boost)