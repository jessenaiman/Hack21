# sound.py
"""Sound effects and music management."""

import pygame
from constants import *

class SoundManager:
    """Manages game audio."""
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        try:
            # Load sound effects
            self.sounds['move'] = pygame.mixer.Sound('move.wav')
            self.sounds['attack'] = pygame.mixer.Sound('attack.wav')
            self.sounds['button_click'] = pygame.mixer.Sound('button_click.wav')
            # Load title screen music
            pygame.mixer.music.load('songs/journeys_dawn.mid')
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except FileNotFoundError:
            print("Warning: Sound files not found. Audio will be disabled.")
        except pygame.error as e:
            print(f"Error loading audio: {e}")

    def play(self, sound_name):
        """Play a sound effect if it exists."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()