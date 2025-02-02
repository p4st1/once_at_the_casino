import pygame
import os

from config import *
from menu import Menu
from game import Game
from transition import Transition, Transition_cubes
from time import time

pygame.init()
screen = pygame.display.set_mode(SIZE)
running = 1

all_sprites = all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

scene = 0 
menu = Menu()

transition = 0
plus = 1
clock = pygame.time.Clock()
start = time()
cubes = [[0 for x in range(16)] for y in range(9)]
Transition_scenes = Transition_cubes(screen)
oldTimePackageSent = 0

while running:
    events = pygame.event.get()
    
    # screen.fill((0, 0, 0))

        
    if scene == 0:
        if transition:
            menu.update()
            menu.render()
            Transition(screen, menu.screen, 150)
            transition = 0
            continue
        if menu.events(events): #starting game
            scene = 1
            transition = 1
            game = Game("hunbaoabo")
        else:
            menu.update()
            menu.render()
            screen.blit(menu.screen, (0, 0))
    if scene == 1:
        if transition:
            game.update(1)
            game.render()
            Transition(screen, game.win, 150)
            transition = 0
            continue
        if game.event(events): #end game
            scene = 0
            transition = 1
            menu.startGame = False
            game = None
        else:
            if game.update(transition):
                pass #здесь должен быть переход в конечную сцену, как и в остальных ситуациях 
            game.render(clock.get_fps())
            timePackageSent = time()
            if timePackageSent - oldTimePackageSent > 0.05:
                oldTimePackageSent = time()
                game.send_packeges()
            screen.blit(game.win, (0, 0))
    clock.tick(60)
    pygame.display.flip()