import pygame
from config import *
from math import cos, sin, radians

class Menu():
    def __init__(self) -> None:
        pygame.init()
        # main config
        # main options
        self.name = "login"
        self.FPS = 60
        self.running = True
        self.screen = pygame.Surface(SIZE)
        self.clock = pygame.time.Clock()

        self.x_start = 400
        self.y_start = 200
        self.degree = 0

        self.writing = 0
        self.select_button = 0
        

    def events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = False
                    if self.select_button == 0:
                        return 1
                            
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
                    
        return 0

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

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.screen.blit(self.text, (x, y))

if __name__ == "__main__":
    menu = Menu()
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    running = 1

    while running:
        events = pygame.event.get()
        screen.fill((0, 0, 0))
        if menu.events(events):
            print("start game!!!")
            login = menu.name
            print(login)
        menu.update()
        menu.render()
        screen.blit(menu.screen, (0, 0))
        
        pygame.display.flip()