# ui.py
"""User interface elements."""

import pygame
from constants import *

class HealthBar:
    """Displays the player's health."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, player):
        """Draw the health bar."""
        ratio = player.health / player.max_health
        pygame.draw.rect(screen, COLOR_RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, COLOR_GREEN, (self.x, self.y, int(self.width * ratio), self.height))
        font = pygame.font.Font(None, 24)
        text = font.render(f"HP: {player.health}/{player.max_health}", True, COLOR_WHITE)
        screen.blit(text, (self.x + self.width + 10, self.y))

class MessageLog:
    """Displays game messages."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.messages = []
        self.max_lines = height // 20

    def add(self, message):
        """Add a message to the log."""
        self.messages.append(message)
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)

    def draw(self, screen):
        """Draw the message log."""
        font = pygame.font.Font(None, 20)
        for i, msg in enumerate(self.messages):
            text = font.render(msg, True, COLOR_WHITE)
            screen.blit(text, (self.x, self.y + i * 20))

class InventoryScreen:
    """Displays the player's inventory."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, player):
        """Draw the inventory screen."""
        font = pygame.font.Font(None, 24)
        pygame.draw.rect(screen, COLOR_DARK_GRAY, (self.x, self.y, self.width, self.height))
        title = font.render("Inventory (Press number to use, ESC to close)", True, COLOR_WHITE)
        screen.blit(title, (self.x + 10, self.y + 10))
        for i, item in enumerate(player.inventory):
            text = font.render(f"{i + 1}: {item.name}", True, COLOR_WHITE)
            screen.blit(text, (self.x + 10, self.y + 40 + i * 20))