import pygame
import socket
import pickle
import random
import json
import time

import pygame.locals

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
        
        
class SLOT_MACHINE():
    def __init__(self, size, money):
        self.size = size
        self.money = money
        self.screen = pygame.Surface((self.size))
        self.current_background_color = 1
        self.E_button_img = pygame.image.load(E_button_img).convert_alpha()
        self.Q_button_img = pygame.image.load(Q_button_img).convert_alpha()
        
        self.seven = pygame.image.load(seven_img).convert_alpha()
        self.cherry = pygame.image.load(cherry_img).convert_alpha()
        self.bell = pygame.image.load(bell_img).convert_alpha()
        self.bar = pygame.image.load(bar_img).convert_alpha()
        
        self.slots = pygame.image.load(slots_img).convert_alpha()
        self.slot_machine = pygame.image.load(slot_machine_img).convert_alpha()
        
        self.armup = pygame.image.load(armup_img).convert_alpha()
        self.armdown = pygame.image.load(armdown_img).convert_alpha()
        
        self.spining = 0
        self.slot_items = [random.randint(0, 99) for i in range(3)]
        self.distance = [0, 0, 0]
        self.slots_spining = [0, 0, 0]
        
        self.wheeling = pygame.mixer.Sound("audio/" + slot_wheel)
        self.click = pygame.mixer.Sound("audio/" + slot_arm_sound)
        self.coins = pygame.mixer.Sound("audio/" + coins_sound)
        self.win = pygame.mixer.Sound("audio/" + slot_win)
        self.big_win = pygame.mixer.Sound("audio/" + slot_big_win)
        
    def check_win(self):
        slots_reslut = [slot_line[i] for i in self.slot_items]
        max_item = max(slots_reslut, key=lambda x: slots_reslut.count(x))
        k = slots_reslut.count(max_item)
        if k > 1:
            if k == 3:
                self.big_win.stop()
                self.big_win.play()
            else:
                self.win.stop()
                self.win.play()
            n = 3
            binom = factorial(n) / (factorial(k) * factorial(n - k))
            p = slot_generator[max_item] / 100
            out = binom * (p ** k) * (1 - p) ** (n - k)
            win = int((round(100 / (out * 100), 3)) * 1 / 10 * 100)
            self.money += win 
            
        
        
    def spin_slots(self):
        if s := sum(self.distance):
            for i in range(3):
                if self.distance[i]:
                    self.distance[i] -= 1
                    s -= 1
                    self.slot_items[i] = (self.slot_items[i] + 1) % 100
                    
            if s == 0:
                self.spining = 0
                self.wheeling.stop()
                self.click.stop()
                self.click.play()
                self.wheeling = pygame.mixer.Sound("audio/" + slot_wheel)
                self.check_win()
                
        else:
            self.big_win.stop()
            self.win.stop()
            self.wheeling.stop()
            self.wheeling.play()
            self.click.stop()
            self.click.play()
            self.coins.stop()
            self.coins.play()
            self.money -= 100
            self.distance = [random.randint(30, 99) for i in range(3)]
            self.start_time = time.time()

        
    def update(self, button_size):
        self.button_size = button_size // 2
        self.bg = pygame.image.load(f"images/background/frame_{self.current_background_color}.png")
        self.bg = pygame.transform.scale(self.bg, self.size)
        if self.spining:
            self.spin_slots()
        
        
        self.current_background_color += 1
        self.current_background_color = 1 if self.current_background_color == 18 else self.current_background_color
        
        self.E_button = pygame.transform.scale(self.E_button_img, (32 * RATIO + self.button_size, 32 * RATIO + self.button_size))
        self.Q_button = pygame.transform.scale(self.Q_button_img, (32 * RATIO + self.button_size, 32 * RATIO + self.button_size))
        
        self.render()
        
    def render(self):
        self.screen.fill(background_color)
        self.screen.blit(self.bg, (0, 0))
        
        slot_coords = ((self.size[0] - (816 * RATIO / 2)) / 2, (self.size[1] - 624 * RATIO / 2))
        x, y = slot_coords
        self.screen.blit(self.slots, slot_coords)
        for item, i in zip(self.slot_items, range(3)):
            eval(f"self.screen.blit(self.{slot_line[item]}, (x + 816 / 3.5 + 816 / 6.2 * i, y + 300))")
        
        self.screen.blit(self.slot_machine, slot_coords)
        if self.spining:
            self.screen.blit(self.armdown, slot_coords)
        else:
            self.screen.blit(self.armup, slot_coords)
        
        self.screen.blit(self.Q_button, (30 - self.button_size / 2, 30 - self.button_size / 2))
        self.screen.blit(self.E_button, (250 - self.button_size / 2, 30 - self.button_size / 2))
        self.print_text(
                message=f'Exit',
                x=100,
                y=45,
                font_color=(255, 255, 255),
                font_size=40 + self.button_size // 2,
                font_type=definedFonts[0]
            )
        self.print_text(
                message=f'Spin',
                x=320,
                y=45,
                font_color=(255, 255, 255),
                font_size=40 + self.button_size // 2,
                font_type=definedFonts[0]
            )
        self.print_text(
                message=f'{self.money}$',
                x=self.size[0] - len(str(self.money)) * 40 - 30,
                y=45,
                font_color=(255, 255, 255),
                font_size=40 + self.button_size // 2,
                font_type=definedFonts[0]
            )

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.screen.blit(self.text, (x, y))


class Game():
    def __init__(self, name) -> None:
        pygame.init()
        with open('data.json', 'r') as f:
            config_file = json.load(f)

        self.screenSize = config_file['Config']['resolution']
        self.win = pygame.Surface(self.screenSize)
        self.running = True
        self.name = name
        self.all_sprites = pygame.sprite.Group()
        self.hitboxes = pygame.sprite.Group()
        self.scene = 0

        self.money = 3000
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
        self.security_picture = "NPC_images/security/down/0.png"
        self.security = pygame.transform.scale(pygame.image.load(self.security_picture), (NPS_SIZE_X * RATIO, NPS_SIZE_Y * RATIO))
        
        self.dynamics_jazz = [(1671, 2136),  (701, 1251), (1571, 1056), (386, 611), (2526, 1596), (3166, 800)]
        pygame.mixer.music.load(jazz)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play()
        
        self.create_club_music()
        
        self.minimap = Minimap()
        
        

        address = config_file['last_server'].split(':')
        host = address[0]
        port = int(address[1])

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.isNetGraphShown = True
        self.timePackcageSent = 0
        self.oldTimePackageSent = 0
        self.players = {}
        self.pingTime = 0
        self.chatSendMessage = ''
        self.chatHistory = []
        self.chatActive = False
        self.chatOpacity = 50
        self.shownText = ''
        self.chatSendMessage = ''
        self.writing = False
        self.color = (0,0,0)
        
        self.font = pygame.font.Font(definedFonts[1], 24)
        self.pingEnd, self.pingStart = time.time(), time.time()
        self.packet = (self.players, self.chatHistory, self.pingTime)
        self.packageToServer = (self.x, self.y, self.name, '')

        self.games_pos_type = [[f"slot_machine{i}", (82 * 32, (41 - i * 4) * 32)] for i in range(4)] + \
            [[f"slot_machine{i + 4}", (91 * 32, (41 - i * 4) * 32)] for i in range(4)]
        self.E_button_img = pygame.image.load(E_button_img).convert_alpha()
        self.E_button = pygame.transform.scale(self.E_button_img, (32 * RATIO, 32 * RATIO))
        self.selected_game = None
        
        
        
        
        # (x, y, name, message, vector, state)
        self.other_players = []
        self.other_players_collisions = []
        self.other_players_vectors = []
        
        self.old_players = {}
        
    def update_other_players(self):
        players = list(self.players.keys())
        all_players_data = list(self.players.values())
        while 1:
            for i in range(len(self.other_players)):
                if self.other_players[i] not in players:
                    self.other_players.pop(i)
                    self.layers.remove(self.other_players_collisions[i])
                    self.other_players_collisions[i].kill()
                    self.other_players_collisions.pop(i)
                    break
            else:
                break
        for i in range(len(players)):
            players_data = all_players_data[i]
            if self.name != players_data[2]: #after change 
                if players[i] not in self.other_players:
                    self.other_players.append(players[i])
                    new_player = Player(players_data[0], players_data[1], "NPC_images/player1/down/0.png")
                    self.other_players_collisions.append(new_player)
                    self.other_players_vectors.append(players_data[4])
                    self.all_sprites.add(new_player)
                    self.layers.append(new_player)
                else:
                    ind = self.other_players.index(players[i])
                    self.other_players_collisions[ind].rect.x = players_data[0]
                    self.other_players_collisions[ind].rect.y = players_data[1]
                    self.other_players_vectors[ind] = players_data[4]                                  
        
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
                if not self.writing: 
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
                    if event.key == pygame.K_t:
                        self.chatActive = not self.chatActive
                        self.writing = not self.writing
                    if event.key == pygame.K_e:
                        if self.selected_game:
                            if self.scene == 1:
                                self.slot_machine.spining = 1
                            if self.selected_game[0].startswith("slot_machine") and self.scene != 1:
                                self.scene = 1
                                self.slot_machine = SLOT_MACHINE(self.screenSize, self.money)
                    if event.key == pygame.K_q:
                        self.scene = 0
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.chatSendMessage = self.chatSendMessage[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.writing = False
                        self.chatActive = False
                        self.chatSendMessage = ''
                    else:
                        if event.key != pygame.K_RETURN:
                            self.chatSendMessage += event.unicode
                            
                        else:
                            self.writing = False
                            self.chatActive = False
                            print(self.chatSendMessage)
                            self.chatSendMessage = ''
                    self.shownText = self.chatSendMessage

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
                    self.security_colission.rect.y += SPEED // 4
                    self.security_vector = "down"
                else:
                    self.security_colission.rect.y -= SPEED // 4
                    self.security_vector = "up"
            else:
                if self.security_x // 32 < self.security_path[0][1]:
                    self.security_colission.rect.x += SPEED // 4
                    self.security_vector = "right"
                else:
                    self.security_colission.rect.x -= SPEED // 4
                    self.security_vector = "left"
        else:
            self.security_path.pop(0)
        self.security_x, self.security_y = self.security_colission.rect.x, self.security_colission.rect.y
        
        
        
                
    def update(self, transition):
        button_size = round(time.time() * 20) % 20
        self.button_size = (button_size if button_size <= 10 else 10 - button_size + 10)
        if self.scene == 1:
            self.slot_machine.update(self.button_size)
            
        if not transition:
            if not self.channel.get_busy():
                self.create_club_music()
                
            min_distance = ((self.x - self.dynamics_jazz[0][0]) ** 2 + (self.y - self.dynamics_jazz[0][1]) ** 2) ** 0.5
            for x, y in self.dynamics_jazz[1:]:
                distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
            if self.scene:
                pygame.mixer.music.set_volume(0.2)
            else:
                pygame.mixer.music.set_volume(1 - min(1, round((min_distance / 1000), 2)))
        
            club_distance = ((self.x - 3466) ** 2 + (self.y - 2021) ** 2) ** 0.5
            minus = round((club_distance / 1000), 2)
            volume = 1 - min(1, (minus if minus < 0.6 else minus ** 0.25))
            self.club_music.set_volume(volume)
        
        min_distance_to_game = float("inf")
        for game_type, (x, y) in self.games_pos_type:
            distance = ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5
            if distance < min_distance_to_game and distance <= 250:
                min_distance_to_game = distance
                self.selected_game = [game_type, (x, y)]
        if min_distance_to_game == float('inf'):
            self.selected_game = None
            
            
        if self.security_path:
            self.security_move()
            self.security_position += 1
        else:
            self.security_position = 0
            self.security_path = find_road((self.security_x // 32, self.security_y // 32), (random.randint(0, 144), random.randint(16, 85)))
        self.security_picture = f"NPC_images/security/{self.security_vector}/{((self.security_position // 20) % 2 + 1) * int(bool(self.security_position))}.png"
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

        if self.chatActive is True:
            self.color = (0, 0, 0)
            self.chatOpacity = 50
        else:
            self.color = (0, 0, 0)
            self.chatOpacity = 0
        
        self.update_other_players()
    

            

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.win.blit(self.text, (x, y))
        
    def render(self, fps=0):
        self.win.fill((0, 0, 0))
        if self.scene == 0:
            self.bg_x, self.bg_y = -self.x * RATIO + (SIZE[0] // 2 - NPS_SIZE_X // 2), -self.y * RATIO + (SIZE[1] // 2 - NPS_SIZE_Y // 2)
            self.win.blit(self.bg, (self.bg_x, self.bg_y))
            self.win.blit(self.security, (self.bg_x + self.security_x * RATIO, self.bg_y + self.security_y * RATIO))
            for i in range(len(self.other_players)):
                other_x, other_y = self.other_players_collisions[i].rect.x, self.other_players_collisions[i].rect.y
                player_image = f"NPC_images/player1/{self.other_players_vectors[i]}/0.png"
                other_player = pygame.transform.scale(pygame.image.load(player_image), (NPS_SIZE_X * RATIO, NPS_SIZE_Y * RATIO))
                self.win.blit(other_player, (self.bg_x + other_x * RATIO, self.bg_y + other_y * RATIO))
                
            self.win.blit(self.hero, (SIZE[0] // 2 - NPS_SIZE_X // 2, SIZE[1] // 2 - NPS_SIZE_Y // 2))
            for texture in self.textures:
                self.win.blit(texture, (self.bg_x, self.bg_y))


            if self.selected_game:
                
                self.E_button = pygame.transform.scale(self.E_button_img, (32 * RATIO + self.button_size, 32 * RATIO + self.button_size))
                x, y = self.selected_game[1]
                self.win.blit(self.E_button, (self.bg_x + x * RATIO - self.button_size / 2, self.bg_y + y * RATIO - self.button_size / 2))
            self.win.blit(self.minimap.minimap, (20, 20))
        if self.scene == 1:
            self.win.blit(self.slot_machine.screen, (0, 0))
            
            
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
        
        self.chatSurface = pygame.Surface((325,300))
        self.chatSurface.fill((255, 255, 255))
    
        self.inputChatSurface = pygame.Surface((325,25))
        self.inputChatSurface.fill((255, 255, 255))

        txt_surface = self.font.render(self.shownText[-20:], True, self.color)

        self.chatSurface.set_alpha(self.chatOpacity)
        self.inputChatSurface.set_alpha(self.chatOpacity * 1.5)
        self.win.blit(txt_surface, (self.screenSize[0] - 325, 300))
        self.chatText_y, self.chatText_delta_y = 0, 25
        

        self.win.blit(self.chatSurface, (self.screenSize[0] - 325, 0))
        self.win.blit(self.inputChatSurface, (self.screenSize[0] - 325, 300))

        # self.all_sprites.draw(self.win)

    def send_packeges(self):
        pingStart = time.time()
        
        try:
            serverRequests = pickle.loads(self.client.recv(4096))
            chatHistory = serverRequests[1]
            players = serverRequests[0]
        except Exception as e:
            print(f'Failed to get a package: {e}')
            players = {}
            chatHistory = []
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
        game.update(0)
        game.render()
        screen.blit(game.win, (0, 0))
        clock.tick(60)
        
        pygame.display.flip()