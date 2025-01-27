import pygame
from config import *
from time import time

class Transition_cubes:
    def __init__(self, screen):
        self.cubes = [[0 for x in range(16)] for y in range(9)]
        self.start = time()
        self.plus = 1
        self.screen = screen
        
    def update(self):
        delta = time() - self.start
        # if not self.plus:
        #     self.screen.blit(self.screen, (0, 0))
        for x in range(16):
            for y in range(9):
                if x * y <= delta * 80:
                    if self.plus:
                        if self.cubes[y][x] == 0:
                            self.cubes[y][x] = 1.5
                        self.cubes[y][x] *= 1.5
                        if self.cubes[y][x] >= 80:
                            self.cubes[y][x] = 80
                        if self.cubes[-1][-1] >= 80:
                            self.plus = 0
                            self.start = time()
                    else:
                        self.cubes[y][x] /= 1.5
                        if self.cubes[y][x] <= 1.5:
                            self.cubes[y][x] = 0
                        if self.cubes[-1][-1] == 0:
                            self.plus = 1
                            return True
                k = 80 - self.cubes[y][x]
                pygame.draw.rect(self.screen, DARK_BLUE if (x + y % 2) % 2 else GREEN, (80 * x + (0 if self.plus else k), 80 * y + (0 if self.plus else k), self.cubes[y][x], self.cubes[y][x]))

def Transition(screen, next_scene, velocity=80):
    running = 1
    size = 0
    plus = 1
    # screen = pygame.display.set_mode((1280, 720))
    # screen = pygame.Surface(SIZE)
    clock = pygame.time.Clock()
    start = time()
    cubes = [[0 for x in range(16)] for y in range(9)]
    while running:
        delta = time() - start
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = 0
        clock.tick(60)
        if not plus:
            # screen.fill((0, 0, 0))
            screen.blit(next_scene, (0, 0))
        for x in range(16):
            for y in range(9):
                if x * y <= delta * velocity:
                    if plus:
                        if cubes[y][x] == 0:
                            cubes[y][x] = 1.5
                        cubes[y][x] *= 1.5
                        if cubes[y][x] >= 80:
                            cubes[y][x] = 80
                        if cubes[-1][-1] >= 80:
                            plus = 0
                            start = time()
                    else:
                        cubes[y][x] /= 1.5
                        if cubes[y][x] <= 1.5:
                            cubes[y][x] = 0
                        if cubes[-1][-1] == 0:
                            running = 0
                k = 80 - cubes[y][x]
                pygame.draw.rect(screen, DARK_BLUE if (x + y % 2) % 2 else GREEN, (80 * x + (0 if plus else k), 80 * y + (0 if plus else k), cubes[y][x], cubes[y][x]))
        pygame.display.flip()