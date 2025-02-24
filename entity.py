# entity.py
"""Base entity class."""

import pygame
from constants import *

class Entity:
    """Base class for all game entities."""
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        """Move the entity by dx, dy."""
        self.x += dx
        self.y += dy

    def draw(self, screen):
        """Draw the entity as a colored rectangle."""
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, self.color, rect)