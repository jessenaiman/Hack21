# menu.py
"""Handles the startup menu and character creation."""

import pygame
from constants import *

class Menu:
    """Manages the startup menu."""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.buttons = [
            {"text": "New Game", "rect": pygame.Rect(300, 200, 200, 50)},
            {"text": "Load Game", "rect": pygame.Rect(300, 270, 200, 50)},
            {"text": "Options", "rect": pygame.Rect(300, 340, 200, 50)},
            {"text": "Exit", "rect": pygame.Rect(300, 410, 200, 50)}
        ]
        self.selected_button = None

    def draw(self):
        """Draw the menu screen with pixel-art-style buttons."""
        self.screen.fill(COLOR_BLACK)
        title = self.font.render("Roguelike Adventure", True, COLOR_WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        for button in self.buttons:
            color = COLOR_YELLOW if button == self.selected_button else COLOR_GRAY
            pygame.draw.rect(self.screen, color, button["rect"])
            text = self.small_font.render(button["text"], True, COLOR_BLACK)
            self.screen.blit(text, (button["rect"].x + 10, button["rect"].y + 10))

    def handle_event(self, event):
        """Handle menu interactions."""
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(pos):
                    self.selected_button = button
                    break
            else:
                self.selected_button = None
        elif event.type == pygame.MOUSEBUTTONDOWN and self.selected_button:
            return self.selected_button["text"]
        return None

class CharacterCreation:
    """Manages the character creation screen."""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.name = ""
        self.classes = ["Warrior", "Mage", "Rogue"]
        self.selected_class = 0
        self.appearances = [COLOR_RED, COLOR_GREEN, COLOR_BLUE]
        self.selected_appearance = 0
        self.input_active = True

    def draw(self):
        """Draw the character creation screen."""
        self.screen.fill(COLOR_BLACK)
        title = self.font.render("Create Your Character", True, COLOR_WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Name input
        name_label = self.small_font.render("Name:", True, COLOR_WHITE)
        self.screen.blit(name_label, (200, 150))
        name_text = self.small_font.render(self.name, True, COLOR_WHITE)
        self.screen.blit(name_text, (300, 150))

        # Class selection
        class_label = self.small_font.render("Class:", True, COLOR_WHITE)
        self.screen.blit(class_label, (200, 200))
        for i, cls in enumerate(self.classes):
            color = COLOR_YELLOW if i == self.selected_class else COLOR_GRAY
            cls_text = self.small_font.render(cls, True, color)
            self.screen.blit(cls_text, (300 + i * 100, 200))

        # Appearance selection (color blocks)
        appearance_label = self.small_font.render("Appearance:", True, COLOR_WHITE)
        self.screen.blit(appearance_label, (200, 250))
        for i, color in enumerate(self.appearances):
            pygame.draw.rect(self.screen, color, (300 + i * 50, 250, 40, 40))
            if i == self.selected_appearance:
                pygame.draw.rect(self.screen, COLOR_YELLOW, (300 + i * 50, 250, 40, 40), 2)

        # Stats preview
        stats = self.get_stats()
        stats_text = self.small_font.render(
            f"Health: {stats['health']} Strength: {stats['strength']} Defense: {stats['defense']}",
            True, COLOR_WHITE
        )
        self.screen.blit(stats_text, (200, 350))

        # Confirm button
        confirm_rect = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(self.screen, COLOR_GRAY, confirm_rect)
        confirm_text = self.small_font.render("Confirm", True, COLOR_BLACK)
        self.screen.blit(confirm_text, (confirm_rect.x + 10, confirm_rect.y + 10))

    def handle_event(self, event):
        """Handle character creation inputs."""
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == pygame.K_RETURN:
                self.input_active = False
            else:
                self.name += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Class selection
            for i in range(len(self.classes)):
                if 300 + i * 100 <= pos[0] <= 400 + i * 100 and 200 <= pos[1] <= 230:
                    self.selected_class = i
            # Appearance selection
            for i in range(len(self.appearances)):
                if 300 + i * 50 <= pos[0] <= 340 + i * 50 and 250 <= pos[1] <= 290:
                    self.selected_appearance = i
            # Confirm button
            if 300 <= pos[0] <= 500 and 400 <= pos[1] <= 450:
                if self.name and self.selected_class is not None:
                    return "confirm"
        return None

    def get_stats(self):
        """Return stats based on selected class."""
        if self.selected_class == 0:  # Warrior
            return {"health": 120, "strength": 15, "defense": 8}
        elif self.selected_class == 1:  # Mage
            return {"health": 80, "strength": 8, "defense": 4}
        elif self.selected_class == 2:  # Rogue
            return {"health": 100, "strength": 10, "defense": 6}