import pygame
import json
from config import *
from datetime import datetime
from math import cos, sin, radians


class EndingScreen():
    def __init__(self) -> None:
        pygame.init()

        with open('data.json', 'r') as f:
            config_file = json.load(f)
    
        self.name = "login"
        self.running = True
        size = (1280, 720)
        self.screenSize = size
        self.window_type = config_file['Config']['fullscreen']
        self.address = config_file['last_server']
        if self.window_type == 'window':
            self.screen = pygame.Surface(self.screenSize)
        else:
            self.screen = pygame.Surface(self.screenSize, pygame.FULLSCREEN)
        self.current_background_color = 1
        self.i = 0
        self.degree = 0
        self.selected_button = 'None'
        self.play_main_menu_music()
        self.counter = 0
        self.speed = 3 
        self.menu_buttons = [[(self.screenSize[0] // 2) - 70, 600, ((self.screenSize[0] // 2) - 70) + 138, 600 + 38]]
        
        self.game = 'ONCE AT THE CASINO'
        self.gameWritten = False
        
        self.moveselect = pygame.mixer.Sound(f'audio/moveselect.mp3')
        self.select = pygame.mixer.Sound(f'audio/select.mp3')
        
        self.typingSound = pygame.mixer.Sound(f'audio/text_typing.mp3')
        self.typingSound.play()
        
        self.endSound = pygame.mixer.Sound(f'audio/end_game.ogg')
        self.endSoundPlayed = False
        
        self.gotoMenu = False
        
    def play_main_menu_music(self):
        self.main_menu_music = pygame.mixer.Sound('audio/ending_main_theme.mp3')
        self.main_menu_music.set_volume(0.1)
        self.channel = self.main_menu_music.play()
        
                
    def logs(self, log : str):
        with open('logs.txt', 'a') as logs:
            logs.write(f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S")}] {log}\n')
        
    def events(self, events):
        mouse = pygame.mouse.get_pos()

        if self.endSoundPlayed is True:
            if mouse[0] > self.menu_buttons[0][0] and mouse[0] < self.menu_buttons[0][2] and mouse[1] > self.menu_buttons[0][1] and mouse[1] < self.menu_buttons[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 0
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()  
            else:
                self.selected_button = 'None'
                    
        for event in events:                
            if event.type == pygame.QUIT:
                self.running = False
                quit()
                          
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.selected_button == 0:
                    self.select.play()
                    self.gotoMenu = True
        
        if self.gotoMenu is True:
            return 1
        else:
            return 0
                                  
               
    def update(self):
        if self.gameWritten == True:
            self.typingSound.stop()
            if self.endSoundPlayed is False:
                self.endSound.play()
                self.endSoundPlayed = True
        
    def render(self):        
        self.bg = pygame.image.load(f"images/background/frame_{self.current_background_color}.png")
        self.bg = pygame.transform.scale(self.bg, self.screenSize)
        self.screen.blit(self.bg, (0, 0))
        self.current_background_color += 1
        if self.current_background_color == 17:
            self.current_background_color = 1

        if self.counter < self.speed * len(self.game):
            self.counter += 1
            
        elif self.counter >= self.speed * len(self.game):
            self.gameWritten = True

        self.print_text(f'{self.game[0:self.counter//self.speed]}', 
                             (self.screenSize[0] - 728) // 2, 
                             200, 
                             (133 - self.i * 2, self.i * 2, 170), 
                             font_size=60,
                             degree=sin(radians(self.degree)) * 2,
                             font_type='fonts/PixExtrusion.ttf')
        self.i += 1
        if self.i == 63:
            self.i = 0
        
        self.print_text('game ver: 0.0.1',
                        0,
                        self.screenSize[1]-24,
                        (224, 224, 224),
                        font_size=24)
        if self.endSoundPlayed is True:
            self.print_text('Back',
                        (self.screenSize[0] // 2) - 70,
                        600,
                        (224, 224, 224),
                        font_size=48,
                        degree=sin(radians(self.degree)) * 2,
                        font_type='fonts/PixExtrusion.ttf')
            
        if self.selected_button != 'None':
            if self.endSoundPlayed is True:
                pygame.draw.circle(self.screen, (255, 255, 255), (self.menu_buttons[self.selected_button][0] - 30, self.menu_buttons[self.selected_button][1] + 20), 8)
            
            
        pygame.display.flip()

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.screen.blit(self.text, (x, y))
        return self.text.get_rect()

if __name__ == "__main__":
    menu = Menu()
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    running = 1

    while running:
        events = pygame.event.get()
        if menu.events(events):
            print("start game!!!")
            login = menu.name
            print(login)
        menu.update()
        menu.render()
        screen.blit(menu.screen, (0, 0))
        
        pygame.display.flip()