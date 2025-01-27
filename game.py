import pygame
import socket
import pickle
import random
import time

from config import *
from find_road import find_road

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
        
        
class NPS(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        img_path = f"NPC_images/{type}/down/0.png"
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
        self.create_textures()
        
        self.security_x, self.security_y = 2024, 1824
        self.security_colission = NPS(self.security_x, self.security_y, "security")
        self.all_sprites.add(self.security_colission)
        self.security_vector = "down"
        self.security_position = 0
        self.layers.append(self.security_colission)
        self.security_path = find_road((self.security_x // 32, self.security_y // 32), (111, 58))[1:-1]
        print(self.security_path)
        self.security_picture = "NPC_images/security/down/0.png"
        self.security = pygame.transform.scale(pygame.image.load(self.security_picture), (NPS_SIZE_X * RATIO, NPS_SIZE_Y * RATIO))
        
        self.dynamics_jazz = [(1671, 2136),  (701, 1251), (1571, 1056), (386, 611), (2526, 1596), (3166, 800)]
        pygame.mixer.music.load(jazz)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play()
        
        self.create_club_music()
        
        self.minimap = Minimap()
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        self.isNetGraphShown = False
        self.timePackcageSent = 0
        self.oldTimePackageSent = 0
        self.players = {}
        self.pingTime = 0
        self.chatSendMessage = ''
        self.chatHistory = []
        self.pingEnd, self.pingStart = time.time(), time.time()
        self.packet = (self.players, self.chatHistory, self.pingTime)
        self.packageToServer = (self.x, self.y, self.name, '')

        
        
        
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
                if event.key == pygame.K_F7:
                    self.isNetGraphShown = not self.isNetGraphShown
                    
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
    
    def security_move(self):
        if (self.security_x // 32, self.security_y // 32) != self.security_path[0][::-1]:
            if self.security_x // 32 == self.security_path[0][1]:
                if self.security_y // 32 < self.security_path[0][0]:
                    self.security_colission.rect.y += SPEED // 2
                    self.security_vector = "down"
                else:
                    self.security_colission.rect.y -= SPEED // 2
                    self.security_vector = "up"
            else:
                if self.security_x // 32 < self.security_path[0][1]:
                    self.security_colission.rect.x += SPEED // 2
                    self.security_vector = "right"
                else:
                    self.security_colission.rect.x -= SPEED // 2
                    self.security_vector = "left"
        else:
            self.security_path.pop(0)
        self.security_x, self.security_y = self.security_colission.rect.x, self.security_colission.rect.y
        
        
        
                
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
            
        if self.security_path:
            self.security_move()
            self.security_position += 1
        else:
            self.security_position = 0
            self.security_path = find_road((self.security_x // 32, self.security_y // 32), (random.randint(0, 144), random.randint(16, 85)))
        self.security_picture = f"NPC_images/security/{self.security_vector}/{((self.security_position // 10) % 2 + 1) * int(bool(self.security_position))}.png"
        self.security = pygame.transform.scale(pygame.image.load(self.security_picture), (NPS_SIZE_X * RATIO, NPS_SIZE_Y * RATIO))
                
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
        
        self.packageToServer = (self.x, self.y, self.name, self.chatSendMessage, self.vector, '')

        try:    
            self.client.sendall(pickle.dumps(self.packageToServer))
        except Exception as e:
            print(f'ERROR: {e}')

        self.players = self.packet[0]
        self.chatHistory = self.packet[1]
        self.pingTime = self.packet[2]
        print(self.players)

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.win.blit(self.text, (x, y))
        
    def render(self, fps=0):
        self.win.fill((0, 0, 0))
        self.bg_x, self.bg_y = -self.x * RATIO + (SIZE[0] // 2 - NPS_SIZE_X // 2), -self.y * RATIO + (SIZE[1] // 2 - NPS_SIZE_Y // 2)
        self.win.blit(self.bg, (self.bg_x, self.bg_y))
        self.win.blit(self.security, (self.bg_x + self.security_x * RATIO, self.bg_y + self.security_y * RATIO))
        self.win.blit(self.hero, (SIZE[0] // 2 - NPS_SIZE_X // 2, SIZE[1] // 2 - NPS_SIZE_Y // 2))
        for texture in self.textures:
            self.win.blit(texture, (self.bg_x, self.bg_y))
            if self.isNetGraphShown is True:
                self.print_text(
                    message=f'Ping: {self.pingTime}',
                    x=0,
                    y=(SIZE[1] - 20),
                    font_color=(255, 255, 255),
                    font_size=20,
                    font_type=definedFonts[0]
                )

                self.print_text(
                    message=f'FPS: {round(fps)}',
                    x=0,
                    y=(SIZE[1] - 40),
                    font_color=(255, 255, 255),
                    font_size=20,
                    font_type=definedFonts[0]
                )

        self.win.blit(self.minimap.minimap, (20, 20))
        # self.all_sprites.draw(self.win)

    def send_packeges(self):
        pingStart = time.time()
        try:
            serverRequests = pickle.loads(self.client.recv(1024))
            chatHistory = serverRequests[1]
            players = serverRequests[0]
        except Exception as e:
            print(f'Failed to get a package: {e}')
            players, chatHistory = {}, []
        pingEnd = time.time()
        self.pingTime = (pingEnd - pingStart) * 1000
        self.packet = (players, chatHistory, self.pingTime)




if __name__ == "__main__":
    screen = pygame.display.set_mode(SIZE)
    game = Game("login")
    pygame.init()
    clock = pygame.time.Clock()
    oldTimePackageSent = time.time()
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