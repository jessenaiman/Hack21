# main.py
"""Main entry point for the roguelike game."""

import pygame
from game import Game
from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roguelike Adventure")
clock = pygame.time.Clock()
game = Game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game.state == STATE_PLAYING:
                if event.key == pygame.K_UP:
                    game.process_action(0, -1)
                elif event.key == pygame.K_DOWN:
                    game.process_action(0, 1)
                elif event.key == pygame.K_LEFT:
                    game.process_action(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.process_action(1, 0)
                elif event.key == pygame.K_i:
                    game.state = STATE_INVENTORY
            elif game.state == STATE_INVENTORY:
                if event.key == pygame.K_ESCAPE:
                    game.state = STATE_PLAYING
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                  pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0):
                    index = int(event.key - pygame.K_1)
                    game.player.use_item(index)
    screen.fill(COLOR_BLACK)
    game.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()