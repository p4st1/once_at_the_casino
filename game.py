import pygame
import socket
import pickle
import random
import time

from config import *
from math import *
from pprint import pprint

class Minimap():
    def __init__(self):
        self.minimap = pygame.Surface((144 * RATIO, 96 * RATIO))
        self.image = pygame.image.load(minimap_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (144 * RATIO, 96 * RATIO))
        
    def update(self, players):
        self.minimap.fill((0, 0, 0))
        self.minimap.blit(self.image, (0, 0))
        for x, y in players:
            pygame.draw.rect(self.minimap, (255, 0, 0), (x * RATIO, y * RATIO, RATIO, RATIO))
        
        

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        super().__init__()
        
        self.image = pygame.transform.scale((pygame.image.load(img_path).convert_alpha()), (NPS_SIZE_X, NPS_SIZE_Y))
        self.rect = self.image.get_rect()
        self.rect.center = (NPS_SIZE_X // 2 + x, NPS_SIZE_Y // 2 + y)
        self.mask = pygame.mask.from_surface(self.image)
        
    


class Game():
    def __init__(self, name) -> None:
        pygame.init()
        self.win = pygame.Surface(SIZE)
        self.running = True
        self.name = name
        self.all_sprites = pygame.sprite.Group()
        self.hitboxes = pygame.sprite.Group()

        self.x, self.y = 2771, 1856
        self.r, self.l, self.u, self.d = 0, 0, 0, 0
        self.vector = "down"
        self.position = 0
        self.hero_img = random.randint(1, 4)
        self.hero_picture = f"NPC_images/player{self.hero_img}/down/0.png"
        self.hero = pygame.transform.scale(pygame.image.load(self.hero_picture), (NPS_SIZE_X * RATIO, NPS_SIZE_Y * RATIO))
        self.player = Player(self.x, self.y, self.hero_picture)
        self.all_sprites.add(self.player)
        
        self.create_bg()
        # self.map = [[0 for x in range(144)] for y in range(96)]
        
        
        # for y in range(96):
        #     for x in range(144):
        #         self.test_object = Obstacle(x * 32, y * 32, 32, 32)
        #         self.all_sprites.add(self.test_object)
        #         for layer in self.layers:
        #             if pygame.sprite.collide_mask(self.test_object, layer):
        #                 self.map[y][x] = 1
        #                 break
        #         self.test_object.kill()
        # with open("lvl.txt", "a") as file:
        #     for i in self.map:
        #         string = str("".join(list(map(str, i))))
        #         file.write(string + '\n')
                
        self.create_textures()
        
        self.dynamics_jazz = [(1671, 2136),  (701, 1251), (1571, 1056), (386, 611), (2526, 1596), (3166, 800)]
        pygame.mixer.music.load(jazz)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play()
        
        self.create_club_music()
        
        self.minimap = Minimap()
        
        
    def create_club_music(self):
        self.club_music = pygame.mixer.Sound("music/" + random.choice(club_music))
        self.club_music.set_volume(0)
        self.channel = self.club_music.play()
        
    def create_bg(self):
        self.bg = pygame.Surface((4608, 3072))
        images = ["bg.png", "upbackground.png", "underobject.png", "objects.png", "borders.png",]
        self.layers = []
        for img in images:
            layer = pygame.image.load("images/" + img).convert_alpha()
            if img in ("objects.png", "borders.png"):
                hb = Hitbox("images/" + img, 0, 0)
                self.all_sprites.add(hb)
                self.hitboxes.add(hb)
                self.layers.append(hb)
            self.bg.blit(layer, (0, 0))
        self.bg = pygame.transform.scale(self.bg, (4608 * RATIO, 3072 * RATIO))
            
    def create_textures(self):
        self.textures = []
        for texture in ["textures.png", "uptextures.png", "upertextures.png"]:
            txtr = pygame.transform.scale(pygame.image.load("images/" + texture).convert_alpha(), (4608 * RATIO, 3072 * RATIO))
            self.textures.append(txtr)
        
        
        
    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.club_music.stop()
                pygame.mixer.music.stop()
                return True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.u = 1
                if event.key == pygame.K_s:
                    self.d = 1
                if event.key == pygame.K_a:
                    self.l = 1
                if event.key == pygame.K_d:
                    self.r = 1
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.u = 0
                if event.key == pygame.K_s:
                    self.d = 0
                if event.key == pygame.K_a:
                    self.l = 0
                if event.key == pygame.K_d:
                    self.r = 0
                    
            if event.type == pygame.USEREVENT:
                print(10)
                # self.create_club_music()
                    
    def check_move(self):
        for layer in self.layers:
            if pygame.sprite.collide_mask(self.player, layer):
                return True
        return False
                
    def update(self, transition):
        if not transition:
            if not self.channel.get_busy():
                self.create_club_music()
                
            min_distance = ((self.x - self.dynamics_jazz[0][0]) ** 2 + (self.y - self.dynamics_jazz[0][1]) ** 2) ** 0.5
            for x, y in self.dynamics_jazz[1:]:
                distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
            pygame.mixer.music.set_volume(1 - min(1, round((min_distance / 1000), 2)))
        
            club_distance = ((self.x - 3466) ** 2 + (self.y - 2021) ** 2) ** 0.5
            minus = round((club_distance / 1000), 2)
            volume = 1 - min(1, (minus if minus < 0.6 else minus ** 0.25))
            self.club_music.set_volume(volume)
                
        self.all_sprites.update()
        if self.u or self.d or self.l or self.r:
            self.position += 1
        else:
            self.position = 0
        if self.u and self.l:
            self.vector = "up_left"
            self.player.rect.y -= SPEED45
            self.player.rect.x -= SPEED45
            if self.check_move():
                self.player.rect.y += SPEED45
                self.player.rect.x += SPEED45
        elif self.u and self.r:
            self.vector = "up_right"
            self.player.rect.y -= SPEED45
            self.player.rect.x += SPEED45
            if self.check_move():
                self.player.rect.y += SPEED45
                self.player.rect.x -= SPEED45
        elif self.d and self.l:
            self.vector = "down_left"
            self.player.rect.y += SPEED45
            self.player.rect.x -= SPEED45
            if self.check_move():
                self.player.rect.y -= SPEED45
                self.player.rect.x += SPEED45
        elif self.d and self.r:
            self.vector = "down_right"
            self.player.rect.y += SPEED45
            self.player.rect.x += SPEED45
            if self.check_move():
                self.player.rect.y -= SPEED45
                self.player.rect.x -= SPEED45
        elif self.u:
            self.vector = "up"
            self.player.rect.y -= SPEED
            if self.check_move():
                self.player.rect.y += SPEED
        elif self.d:
            self.vector = "down"
            self.player.rect.y += SPEED
            if self.check_move():
                self.player.rect.y -= SPEED
        elif self.l:
            self.vector = "left"
            self.player.rect.x -= SPEED
            if self.check_move():
                self.player.rect.x += SPEED
        elif self.r:
            self.vector = "right"
            self.player.rect.x += SPEED
            if self.check_move():
                self.player.rect.x -= SPEED
        # print(((self.position // 10) % 2 + 1) * int(bool(self.position)))
        self.hero_picture = f"NPC_images/player{self.hero_img}/{self.vector}/{((self.position // 10) % 2 + 1) * int(bool(self.position))}.png"
        self.hero = pygame.transform.scale(pygame.image.load(self.hero_picture), (NPS_SIZE_X * RATIO, NPS_SIZE_Y * RATIO))
        self.x, self.y = self.player.rect.x, self.player.rect.y
        self.minimap.update([(self.x // 32, self.y // 32)])
        # print(self.x, self.y)
    
    def render(self):
        self.win.fill((0, 0, 0))
        self.bg_x, self.bg_y = -self.x * RATIO + (SIZE[0] // 2 - NPS_SIZE_X // 2), -self.y * RATIO + (SIZE[1] // 2 - NPS_SIZE_Y // 2)
        self.win.blit(self.bg, (self.bg_x, self.bg_y))
        self.win.blit(self.hero, (SIZE[0] // 2 - NPS_SIZE_X // 2, SIZE[1] // 2 - NPS_SIZE_Y // 2))
        for texture in self.textures:
            self.win.blit(texture, (self.bg_x, self.bg_y))
        self.win.blit(self.minimap.minimap, (20, 20))
        # self.all_sprites.draw(self.win)



if __name__ == "__main__":
    screen = pygame.display.set_mode(SIZE)
    game = Game("login")
    pygame.init()
    clock = pygame.time.Clock()
    while game.running:
        events = pygame.event.get()
        if game.event(events):
            login = game.name
            print(login)
        game.update(0)
        game.render()
        screen.blit(game.win, (0, 0))
        clock.tick(60)
        
        pygame.display.flip()