import pygame
from constants import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        try:
            self.sounds['move'] = pygame.mixer.Sound('move.wav')
            self.sounds['attack'] = pygame.mixer.Sound('attack.wav')
            # Load background music
            pygame.mixer.music.load('songs/journeys_dawn.mid')
            pygame.mixer.music.play(-1)  # Play on loop
        except FileNotFoundError:
            print("Sound files not found; audio disabled.")
        except pygame.error as e:
            print(f"Error loading MIDI file: {e}")

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()