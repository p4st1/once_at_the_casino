import pygame
import socket
import pickle

from config import *
from math import *
from pprint import pprint


class Menu():
    def __init__(self) -> None:
        pygame.init()
        # main config
        # main options
        self.name = "login"
        self.FPS = 60
        self.running = True
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.x_start = 400
        self.y_start = 200
        self.degree = 0

        self.writing = 0
        self.select_button = 0

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = False
                    if self.select_button == 0:
                        try:
                            self.game.run()
                        except:
                            self.game = Game(self.name)
                            self.game.run()
                            
                    elif self.select_button == 1:
                        quit()
                        
                if event.key == pygame.K_DOWN:
                    self.select_button = self.select_button + 1 if self.select_button < 1 else 0
                    
                if event.key == pygame.K_UP:
                    self.select_button = self.select_button - 1 if self.select_button > 0 else 1
                    
                if self.writing:
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if self.x_start + 50 <= x <= self.x_start + 400:
                        if self.y_start + 70 <= y <= self.y_start + 120:
                            self.writing = 0 if self.writing else 1
                            continue
                    self.writing = 0

    def update(self):
        self.degree = (self.degree + 1) % 360
        self.clock.tick(FPS)
        if not self.writing:
            if not self.name:
                self.name = "login"

    def render(self):
        self.screen.fill(background_color)

        for i in range(62):
            self.print_text("ONCE AT THE CASINO", 
                            self.x_start + i/6 * -cos(radians(self.degree)), 
                            self.y_start + i/6 * sin(radians(self.degree)), 
                            (133 - i * 2, i * 2, 170), 
                            font_size=60,
                            degree=sin(radians(self.degree)) * 2)
            if self.writing:
                pygame.draw.line(self.screen, 
                                 (126 - i * 2, 124 + i * 2, 170), 
                                 (self.x_start + 50 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * sin(radians(self.degree))), 
                                 (self.x_start + 400 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * -sin(radians(self.degree))), 
                                 3)
                self.print_text(self.name, 
                                    self.x_start + 70 + i/15 * -cos(radians(self.degree)), 
                                    self.y_start + 80 + i/15 * sin(radians(self.degree)), 
                                    (126 - i * 2, 124 + i * 2, 170),  
                                    font_size=50,
                                    degree=sin(radians(self.degree)) * 2)
            else:
                pygame.draw.line(self.screen, 
                                 (133 - i * 2, i * 2, 170), 
                                 (self.x_start + 50 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * sin(radians(self.degree))), 
                                 (self.x_start + 400 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * -sin(radians(self.degree))), 
                                 3)
                self.print_text(self.name, 
                                    self.x_start + 70 + i/6 * -cos(radians(self.degree)), 
                                    self.y_start + 80 + i/6 * sin(radians(self.degree)), 
                                    (133 - i * 2, i * 2, 170), 
                                    font_size=50,
                                    degree=sin(radians(self.degree)) * 2)
            
            selected_color = (126 - i * 2, 124 + i * 2, 170)
            self.print_text("PLAY!", 
                            self.x_start + i/6 * -cos(radians(self.degree)) + 150, 
                            self.y_start + i/6 * sin(radians(self.degree)) + 150, 
                            (133 - i * 2, i * 2, 170) if self.select_button != 0 else selected_color, 
                            font_size=60,
                            degree=sin(radians(self.degree)) * 2)
            
            self.print_text("QUIT", 
                            self.x_start + i/6 * -cos(radians(self.degree)) + 155, 
                            self.y_start + i/6 * sin(radians(self.degree)) + 220, 
                            (133 - i * 2, i * 2, 170) if self.select_button != 1 else selected_color, 
                            font_size=60,
                            degree=sin(radians(self.degree)) * 2)
        
        pygame.display.flip()

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.screen.blit(self.text, (x, y))

    def run(self):
        while self.running:
            self.update()
            self.render()
            self.events()


class Game():
    def __init__(self, name) -> None:
        pygame.init()
        pygame.display.set_caption("Online Game")
        self.win = pygame.display.set_mode(SIZE)
        self.running = True
        self.name = name

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.clock = pygame.time.Clock()

        hero = pygame.image.load(hero_img)
        self.hero = pygame.transform.scale(hero, HERO_SIZE)
        self.x, self.y = 2910, 3640
        # self.x, self.y = 0, 0
        self.right, self.left, self.up, self.down = 0, 0, 0, 0
        self.hero_cords = (SIZE[0] // 2 - HERO_SIZE[0] // 2 - 20, SIZE[1] // 2 - HERO_SIZE[1] // 2)

        self.bg = pygame.image.load(bg_img)
        self.bg_x, self.bg_y = 0, 0
        self.x_switch, self.y_switch = self.hero_cords
        
        self.games_hitboxes = [
            [1350, 3000, 1700, 3500], #left poker table
            [4220, 3000, 4570, 3500], #right poker table 
            
        ]
        self.hitboxes = [
            [0, 3741, 5020, 3760],
            [2700, 3400, 2750, 3640], #entrance left box
            [3170, 3400, 3220, 3640], #-//- right box
            [1200, 2890, 1210, 3741], #left border
            [1200, 2650, 2690, 2880], #up border
            [2700, 2110, 2750, 3230], #left border
            [3170, 2110, 3220, 3230], #right border
            [3170, 2650, 4710, 2880], #up border
            [4710, 2650, 4720, 3640], #down border
            [3170, 2110, 5220, 2120], #down
            [5220, 610, 5230, 2110],
            [3340, 590, 5220, 610],
            [2570, 810, 3340, 830],
            [680, 590, 2570, 610],
            [670, 590, 690, 2470],
            [670, 2150, 2600, 2130],    

        ] + self.games_hitboxes

        self.players = {}

    def send_packeges(self, packege: tuple):
        self.client.sendall(pickle.dumps(packege))

    def check_move(self, hitboxes: list, x: int, y: int, move_x: int, move_y: int, size: tuple) -> bool:
        hitboxes += self.hitboxes
        x += move_x
        y += move_y
        print(x, y, x + 100, y + 100)
        # pprint(hitboxes)
        for x1, y1, x2, y2 in hitboxes:
            if y1 <= y <= y2 or y1 <= y + size[1] <= y2 or y <= y1 <= y + size[1] or y <= y2 <= y + size[1]:
                if x1 <= x <= x2 or x1 <= x + size[0] <= x2 or x <= x1 <= x + size[0] or x <= x2 <= size[0]:
                    return False
        return True

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.right = 1
                if event.key == pygame.K_a:
                    self.left = 1
                if event.key == pygame.K_w:
                    self.up = 1
                if event.key == pygame.K_s:
                    self.down = 1
                if event.key == pygame.K_ESCAPE:
                    Menu().run()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.right = 0
                if event.key == pygame.K_a:
                    self.left = 0
                if event.key == pygame.K_w:
                    self.up = 0
                if event.key == pygame.K_s:
                    self.down = 0

    def update(self):
        # print(self.x, self.y)
        self.clock.tick(60)
        hitboxes = [[i[0], i[1], i[0] + HERO_SIZE[0], i[1] + HERO_SIZE[1]]
                    for i in self.players.values() if i[2] != self.name]
        # hitboxes = []
        if self.right:
            if self.check_move(hitboxes, self.x, self.y, 10, 0, HERO_SIZE):
                self.x += 10
        if self.left:
            if self.check_move(hitboxes, self.x, self.y, -10, 0, HERO_SIZE):
                self.x -= 10
        if self.up:
            if self.check_move(hitboxes, self.x, self.y, 0, -10, HERO_SIZE):
                self.y -= 10
        if self.down:
            if self.check_move(hitboxes, self.x, self.y, 0, 10, HERO_SIZE):
                self.y += 10

        self.send_packeges((self.x, self.y, self.name))

        # Читаем позиции всех игроков из сервера
        try:
            self.players = pickle.loads(self.client.recv(4096))
        except Exception as e:
            print(f"[ERROR] {e}")
            self.players = {}
        
    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.win.blit(self.text, (x, y))

    def render(self):
        # Обновляем экран
        self.win.fill((0, 0, 0))

        # Рисуем всех игроков
        self.bg_x, self.bg_y = -self.x, -self.y
        self.win.blit(self.bg, (self.bg_x, self.bg_y))
        self.win.blit(
            self.hero, self.hero_cords)
        self.print_text(self.name, SIZE[0] // 2 - HERO_SIZE[0] // 2, SIZE[1] // 2 - HERO_SIZE[1] // 2 - 30, (255, 255, 255), 30)
        for x, y, name in self.players.values():
            if name == self.name:
                continue
            self.win.blit(self.hero, nick := self.convert_coords(x, y))
            self.print_text(self.win, nick[0], nick[1] - 30, (255, 255, 255), 30)

        for x1, y1, x2, y2 in self.hitboxes:
            pygame.draw.rect(self.win, (255, 0, 0), pygame.Rect(self.rect_coords(x1, y1, x2 - x1, y2 - y1)))
        pygame.display.update()
        
    def rect_coords(self, x1, y1, x2, y2):
        return (self.bg_x + x1 + self.x_switch, self.bg_y + y1 + self.y_switch, x2, y2)
        
    def convert_coords(self, x, y):
        return (self.bg_x + x + self.x_switch, self.bg_y + y + self.y_switch)

    def run(self):
        while self.running:
            self.update()
            self.event()
            self.render()


if __name__ == "__main__":
    Menu().run()
