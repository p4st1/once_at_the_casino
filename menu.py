import pygame
import socket
import json
from config import *
from datetime import datetime
import pygame.scrap as scrap
from math import cos, sin, radians
from optionbox import OptionBox
from checkbox import Checkbox


class Menu():
    def __init__(self) -> None:
        pygame.init()

        with open('data.json', 'r') as f:
            config_file = json.load(f)
    
        self.name = "login"
        self.FPS = 60
        self.running = True
        self.screenSize = config_file['Config']['resolution']
        if config_file['Config']['fullscreen'] == 'window':
            self.screen = pygame.Surface(self.screenSize)
        else:
            self.screen = pygame.Surface(self.screenSize, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.x_start = self.screenSize[0] / 4.5
        self.y_start = self.screenSize[1] / 4.5
        self.degree = 0

        self.writing = 0
        
        self.current_background_color = 1
        self.i = 0
        self.menu_buttons = [[(self.screenSize[0] // 2) - 70, self.y_start + 100, ((self.screenSize[0] - 140) // 2) + 141, (self.y_start + 100) + 38], 
                                  [(self.screenSize[0] // 2) - 140, self.y_start + 150, ((self.screenSize[0] // 2) - 140) + 279, self.y_start + 150 + 41], 
                                  [(self.screenSize[0] // 2) - 120, self.y_start + 200, ((self.screenSize[0] // 2) - 120) + 240, self.y_start + 200 + 40], 
                                  [(self.screenSize[0] // 2) - 171, self.y_start + 250, ((self.screenSize[0] // 2) - 171) + 342, self.y_start + 250 + 42], 
                                  [(self.screenSize[0] // 2) - 70, self.y_start + 300, ((self.screenSize[0] // 2) - 70) + 138, self.y_start + 300 + 38]]
        
        self.menu_lobby = [[(self.screenSize[0] - 144) // 2, (self.screenSize[0] - 144) // 2 + 145, self.y_start + 100, self.y_start + 100 + 40],
                           [(self.screenSize[0] - 396) // 2, (self.screenSize[0] - 396) // 2 + 396, self.y_start + 150, self.y_start + 150 + 48],
                           [(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 144, self.y_start + 250, self.y_start + 250 + 40]]
        
        self.menu_lobby_join = [[(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2+145, self.y_start + 350, self.y_start + 350 + 40],
                                [(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2+145, self.y_start + 400, self.y_start + 400 + 40]]
        
        self.setting_buttons = [[(self.screenSize[0] - 240) // 2, (self.screenSize[0] - 240) // 2 + 240, self.y_start + 100, self.y_start + 100 + 40],
                                [(self.screenSize[0] - 216) // 2, (self.screenSize[0] - 216) // 2 + 216, self.y_start + 150, self.y_start + 150 + 40],
                                [(self.screenSize[0] - 274) // 2, (self.screenSize[0] - 274) // 2 + 274, self.y_start + 200, self.y_start + 200 + 40],
                                [(self.screenSize[0] - 148) // 2, (self.screenSize[0] - 148) // 2 + 148, self.y_start + 250, self.y_start + 250 + 40],
                                [(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 140, self.y_start + 300, self.y_start + 300 + 40]]
        
        self.setting_graphics_buttons = [[(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 145, self.y_start + 250, self.y_start + 250 + 40]]
        
        self.setting_sounds_buttons = [[(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 145, self.y_start + 250, self.y_start + 250 + 40]]
        
        self.setting_controls_buttons = [[(self.screenSize[0]) // 2  - 300, (self.screenSize[0]) // 2  - 300 + 252, self.y_start + 100, self.y_start + 100 + 18],
                                         [(self.screenSize[0]) // 2  - 300, (self.screenSize[0]) // 2  - 300 + 252, self.y_start + 125, self.y_start + 125 + 18],
                                         [(self.screenSize[0]) // 2  - 300, (self.screenSize[0]) // 2  - 300 + 252, self.y_start + 150, self.y_start + 150 + 18],
                                         [(self.screenSize[0]) // 2  - 300, (self.screenSize[0]) // 2  - 300 + 252, self.y_start + 175, self.y_start + 175 + 18],
                                         [(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 145, self.y_start + 250, self.y_start + 250 + 40]]
        
        self.last_selected_button = 0
        self.selected_button = 0
        self.key_interuption_button = False
        self.old_mouse_coords = ()
        self.max_selected_buttons = 4
        self.selectHotKey = 'None'
        
        self.screenChecked = 0
        self.screenCheckedOld = 0
        
        pygame.mixer.music.load('audio/main_menu.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)
        
        self.moveselect = pygame.mixer.Sound(f'audio/moveselect.mp3')
        self.select = pygame.mixer.Sound(f'audio/select.mp3')
        
        self.current_scene_menu = 'main_menu'
        self.resolutions =  ['1920 x 1080', '1280 x 720']
        self.fullscreens = ['Exclusive', 'Window']
        self.resolutionBox = OptionBox((self.screenSize[0]) // 2 + 50, self.y_start + 100, 240, 52, 
                                           (150, 150, 255), 
                                           (100, 200, 255), 
                                           pygame.font.Font('fonts/PixExtrusion.ttf', 32), 
                                            self.resolutions,
                                            selected=1)
        self.fullscreenBox = OptionBox((self.screenSize[0]) // 2 + 50, self.y_start + 175, 240, 52, 
                                           (150, 150, 255), 
                                           (100, 200, 255), 
                                           pygame.font.Font('fonts/PixExtrusion.ttf', 32), 
                                            self.fullscreens,
                                            selected=1)
        
        self.binds = {
            'move_forward' : config_file['hot_keys']['keyboard']['move_forward'],
            'move_backward' : config_file['hot_keys']['keyboard']['move_backward'],
            'move_left' : config_file['hot_keys']['keyboard']['move_left'],
            'move_right' : config_file['hot_keys']['keyboard']['move_right']
        }
    
        self.address_label = [0,0,0,0]

        self.startGame = False
        self.address = ''
        self.volume = 0
        
        self.lkm = False
        
    def main_menu_button_pressed(self):
        if self.current_scene_menu == 'main_menu':
            self.max_selected_buttons = 4
            if self.selected_button == 0:
                self.current_scene_menu = 'lobby'
                self.select.play()
            elif self.selected_button == 1:
                self.current_scene_menu = 'settings'
                self.selected_button = 'None'
                self.select.play()
            elif self.selected_button == 2:
                self.current_scene_menu = 'authors'
                self.select.play()
            elif self.selected_button == 3:
                self.current_scene_menu = 'scoreboard'
                self.select.play()
            elif self.selected_button == 4:
                self.running = False
                self.select.play()
                quit()
    
        elif self.current_scene_menu == 'settings':
            self.max_selected_buttons = 3
            if self.selected_button == 0:
                self.current_scene_menu = 'settings/graphics'
                self.select.play()
            elif self.selected_button == 1:
                self.current_scene_menu = 'settings/sounds'
                self.select.play()
            elif self.selected_button == 2:
                self.current_scene_menu = 'settings/controls'
                self.select.play()
            elif self.selected_button == 3:
                self.current_scene_menu = 'settings/game'
                self.selected_button = 'None'
                self.select.play()
            elif self.selected_button == 4:
                self.current_scene_menu = 'main_menu'
                self.selected_button = 'None'
                self.select.play()               
            
        elif self.current_scene_menu == 'settings/graphics':
            self.max_selected_buttons = 0
            if self.selected_button == 0:
                self.current_scene_menu = 'settings'
                self.select.play()
        
        elif self.current_scene_menu == 'settings/game':
            self.max_selected_buttons = 0
            if self.selected_button == 0:
                self.current_scene_menu = 'settings'
                self.select.play()
                
        elif self.current_scene_menu == 'settings/sounds':
            self.max_selected_buttons = 0
            if self.selected_button == 0:
                self.current_scene_menu = 'settings'
                self.select.play()
                
        elif self.current_scene_menu == 'settings/controls':
            self.max_selected_buttons = 4
            if self.selected_button == 0:
                self.selectHotKey = 'move_forward'
                self.binds['move_forward'] = '-'
                self.select.play()
            elif self.selected_button == 1:
                self.selectHotKey = 'move_backward'
                self.binds['move_backward'] = '-'
                self.select.play()
            elif self.selected_button == 2:
                self.selectHotKey = 'move_right'
                self.binds['move_right'] = '-'
                self.select.play()
            elif self.selected_button == 3:
                self.selectHotKey = 'move_left'
                self.binds['move_left'] = '-'
                self.select.play()
            elif self.selected_button == 4:
                self.selectHotKey = False
                self.current_scene_menu = 'settings'
                self.select.play()
        
        elif self.current_scene_menu == 'lobby':
            self.max_selected_buttons = 2
            if self.selected_button == 0:
                self.current_scene_menu = 'lobby/join'
                self.select.play()
                self.writing = True
            elif self.selected_button == 1:
                self.current_scene_menu = 'settings'
                self.select.play()
            elif self.selected_button == 2:
                self.current_scene_menu = 'main_menu'
                self.select.play()
                
        elif self.current_scene_menu == 'lobby/join':
            self.max_selected_buttons = 1
            if self.selected_button == 0:
                self.current_scene_menu = 'lobby/join'
                self.select.play()
                self.writing = True
                try:
                    temp = self.address.split(':')
                    HOST = temp[0]
                    PORT = int(temp[1])
                except:
                    self.logs('Invalid IP address')
                else:
                    try:
                        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.client.connect((HOST, PORT))
                    except Exception as e:
                        self.logs(f'Unable to connect to server: {HOST}:{PORT}')
                        self.logs(f'Error: {e}')
                    else:
                        self.logs(f'Connecting to server: {HOST}:{PORT}')
                        self.client.close()
                        self.startGame = True
            elif self.selected_button == 1:
                self.current_scene_menu = 'lobby'
                self.select.play()
                
    def logs(self, log : str):
        with open('logs.txt', 'a') as logs:
            logs.write(f'[{datetime.now().strftime('%d.%m.%y %H:%M:%S')}] {log}\n')
        
    def events(self, events):
        mouse = pygame.mouse.get_pos()
        selected_option = self.resolutionBox.update(events)
        if selected_option >= 0:
            self.screenSize = list(map(int, self.resolutions[selected_option].split(' x ')))
            self.screen = pygame.display.set_mode(self.screenSize)
            self.x_start = self.screenSize[0] / 4.5
            self.y_start = self.screenSize[1] / 4.5
            self.menu_buttons = [[(self.screenSize[0] // 2) - 70, self.y_start + 100, ((self.screenSize[0] - 140) // 2) + 141, (self.y_start + 100) + 38], 
                                  [(self.screenSize[0] // 2) - 140, self.y_start + 150, ((self.screenSize[0] // 2) - 140) + 279, self.y_start + 150 + 41], 
                                  [(self.screenSize[0] // 2) - 120, self.y_start + 200, ((self.screenSize[0] // 2) - 120) + 240, self.y_start + 200 + 40], 
                                  [(self.screenSize[0] // 2) - 171, self.y_start + 250, ((self.screenSize[0] // 2) - 171) + 342, self.y_start + 250 + 42], 
                                  [(self.screenSize[0] // 2) - 70, self.y_start + 300, ((self.screenSize[0] // 2) - 70) + 138, self.y_start + 300 + 38]]
        
            self.setting_buttons = [[(self.screenSize[0] - 240) // 2, (self.screenSize[0] - 240) // 2 + 240, self.y_start + 100, self.y_start + 100 + 40],
                                [(self.screenSize[0] - 216) // 2, (self.screenSize[0] - 216) // 2 + 216, self.y_start + 150, self.y_start + 150 + 40],
                                [(self.screenSize[0] - 274) // 2, (self.screenSize[0] - 274) // 2 + 274, self.y_start + 200, self.y_start + 200 + 40],
                                [(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 140, self.y_start + 250, self.y_start + 250 + 40]]
            self.setting_graphics_buttons = [[(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 145, self.y_start + 250, self.y_start + 250 + 40]]
            self.resolutionBox = OptionBox((self.screenSize[0] + 50) // 2, self.y_start + 100, 240, 52, 
                                           (150, 150, 255), 
                                           (100, 200, 255), 
                                           pygame.font.Font('fonts/PixExtrusion.ttf', 32), 
                                            self.resolutions,
                                            selected=selected_option)
            self.fullscreenBox = OptionBox((self.screenSize[0] + 50) // 2 , self.y_start + 175, 240, 52, 
                                           (150, 150, 255), 
                                           (100, 200, 255), 
                                           pygame.font.Font('fonts/PixExtrusion.ttf', 32), 
                                            self.fullscreens,
                                            selected=1)
            self.setting_sounds_buttons = [[(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 145, self.y_start + 250, self.y_start + 250 + 40]]
            self.setting_controls_buttons = [[(self.screenSize[0] - 140) // 2, (self.screenSize[0] - 140) // 2 + 145, self.y_start + 250, self.y_start + 250 + 40]]
            
            with open("data.json", "w") as fh:
                json.dump({'Config' : {'resolution' : self.screenSize, 
                           'fullscreen': 'window',
                           }, 
              'hot_keys' : {'keyboard' : {'move_forward' : '1',
                                          'move_backward' : '3',
                                          'move_left' : '4',
                                          'move_right' : '3'}, 
                            'mouse': {}}}, fh)
            
                
        selected_option_2 = self.fullscreenBox.update(events)
        if selected_option_2 >= 0:
            if selected_option_2 == 0:
                self.window_type = 'fullscreen'
                self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
            elif selected_option_2 == 1:
                self.screen = pygame.display.set_mode(self.screenSize)
                self.window_type = 'window'
            with open("data.json", "w") as fh:
                json.dump({'Config' : {'resolution' : self.screenSize, 
                           'fullscreen': self.window_type,
                           }, 
              'hot_keys' : {'keyboard' : {'move_forward' : '1',
                                          'move_backward' : '3',
                                          'move_left' : '4',
                                          'move_right' : '3'}, 
                            'mouse': {}}}, fh)
        
        if self.old_mouse_coords != mouse:
            self.key_interuption_button = False
            
        for event in events:                
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_button_pressed()
                     
                if event.key == pygame.K_DOWN:
                    self.moveselect.play()
                    self.key_interuption_button = True
                    self.old_mouse_coords = mouse
                    if self.selected_button == 'None':
                        self.selected_button = 0
                    else:
                        if self.selected_button == self.max_selected_buttons:
                            self.selected_button = 0
                        else:
                            self.selected_button += 1
         
                if event.key == pygame.K_UP:
                    self.moveselect.play()
                    self.key_interuption_button = True
                    self.old_mouse_coords = mouse
                    if self.selected_button == 'None':
                        self.selected_button = 0
                    else:
                        if self.selected_button == 0:
                            self.selected_button = self.max_selected_buttons
                        else:
                            self.selected_button -= 1              
                    
                if self.writing:
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                        self.address = self.address[:-1]
                    else:
                        if event.key != pygame.K_RETURN:
                            self.name += event.unicode
                            self.address += event.unicode

                if self.selectHotKey != 'None':
                    if event.unicode.upper() in self.binds.values():
                        self.binds[list(self.binds.keys())[list(self.binds.values()).index(event.unicode.upper())]] = '-'
                    self.binds[self.selectHotKey] = event.unicode.upper()                    
                    
                    with open("data.json", "w") as fh:
                        json.dump({'Config' : {'resolution' : [1280, 720], 
                                            'fullscreen': 'window',
                                            }, 
                                'hot_keys' : {'keyboard' : self.binds, 
                                                'mouse': {}}}, fh)
            
                    self.selectHotKey = 'None'
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.main_menu_button_pressed()
                                  
        if self.current_scene_menu == 'main_menu':      
            if mouse[0] > self.menu_buttons[0][0] and mouse[0] < self.menu_buttons[0][2] and mouse[1] > self.menu_buttons[0][1] and mouse[1] < self.menu_buttons[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 0
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
                
            elif mouse[0] > self.menu_buttons[1][0] and mouse[0] < self.menu_buttons[1][2] and mouse[1] > self.menu_buttons[1][1] and mouse[1] < self.menu_buttons[1][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 1
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
                
            elif mouse[0] > self.menu_buttons[2][0] and mouse[0] < self.menu_buttons[2][2] and mouse[1] > self.menu_buttons[2][1] and mouse[1] < self.menu_buttons[2][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 2
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
                
            elif mouse[0] > self.menu_buttons[3][0] and mouse[0] < self.menu_buttons[3][2] and mouse[1] > self.menu_buttons[3][1] and mouse[1] < self.menu_buttons[3][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 3
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
                
            elif mouse[0] > self.menu_buttons[4][0] and mouse[0] < self.menu_buttons[4][2] and mouse[1] > self.menu_buttons[4][1] and mouse[1] < self.menu_buttons[4][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 4
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
                
            else:
                if self.key_interuption_button == False:
                    self.selected_button = 'None'
                
        if self.current_scene_menu == 'settings':
            if mouse[0] > self.setting_buttons[0][0] and mouse[0] < self.setting_buttons[0][1] and mouse[1] > self.setting_buttons[0][2] and mouse[1] < self.setting_buttons[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 0
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.setting_buttons[1][0] and mouse[0] < self.setting_buttons[1][1] and mouse[1] > self.setting_buttons[1][2] and mouse[1] < self.setting_buttons[1][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 1
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.setting_buttons[2][0] and mouse[0] < self.setting_buttons[2][1] and mouse[1] > self.setting_buttons[2][2] and mouse[1] < self.setting_buttons[2][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 2
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.setting_buttons[3][0] and mouse[0] < self.setting_buttons[3][1] and mouse[1] > self.setting_buttons[3][2] and mouse[1] < self.setting_buttons[3][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 3
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            else:
                if self.key_interuption_button == False:
                    self.selected_button = 'None'
                 
        if self.current_scene_menu == 'settings/graphics':
            if mouse[0] > self.setting_graphics_buttons[0][0] and mouse[0] < self.setting_graphics_buttons[0][1] and mouse[1] > self.setting_graphics_buttons[0][2] and mouse[1] < self.setting_graphics_buttons[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 0
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            else:
                if self.key_interuption_button == False:
                    self.selected_button = 'None'

        if self.current_scene_menu == 'settings/sounds':
            if mouse[0] > self.setting_sounds_buttons[0][0] and mouse[0] < self.setting_sounds_buttons[0][1] and mouse[1] > self.setting_sounds_buttons[0][2] and mouse[1] < self.setting_sounds_buttons[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 2
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            else:
                if self.key_interuption_button == False:
                    self.selected_button = 'None'

        if self.current_scene_menu == 'settings/controls':
            if mouse[0] > self.setting_controls_buttons[0][0] and mouse[0] < self.setting_controls_buttons[0][1] and mouse[1] > self.setting_controls_buttons[0][2] and mouse[1] < self.setting_controls_buttons[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 0
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.setting_controls_buttons[1][0] and mouse[0] < self.setting_controls_buttons[1][1] and mouse[1] > self.setting_controls_buttons[1][2] and mouse[1] < self.setting_controls_buttons[1][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 1
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.setting_controls_buttons[2][0] and mouse[0] < self.setting_controls_buttons[2][1] and mouse[1] > self.setting_controls_buttons[2][2] and mouse[1] < self.setting_controls_buttons[2][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 2
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.setting_controls_buttons[3][0] and mouse[0] < self.setting_controls_buttons[3][1] and mouse[1] > self.setting_controls_buttons[3][2] and mouse[1] < self.setting_controls_buttons[3][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 3
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()   
            elif mouse[0] > self.setting_controls_buttons[4][0] and mouse[0] < self.setting_controls_buttons[4][1] and mouse[1] > self.setting_controls_buttons[4][2] and mouse[1] < self.setting_controls_buttons[4][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 4
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            else:
                if self.key_interuption_button == False:
                    self.selected_button = 'None'
                
        if self.current_scene_menu == 'lobby/join':
            if mouse[0] > self.menu_lobby_join[0][0] and mouse[0] < self.menu_lobby_join[0][1] and mouse[1] > self.menu_lobby_join[0][2] and mouse[1] < self.menu_lobby_join[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 0
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.menu_lobby_join[1][0] and mouse[0] < self.menu_lobby_join[1][1] and mouse[1] > self.menu_lobby_join[1][2] and mouse[1] < self.menu_lobby_join[1][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 1
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            else:
                if self.key_interuption_button == False:
                    self.selected_button = 'None'
            
        if self.current_scene_menu == 'lobby':  
            if mouse[0] > self.menu_lobby[0][0] and mouse[0] < self.menu_lobby[0][1] and mouse[1] > self.menu_lobby[0][2] and mouse[1] < self.menu_lobby[0][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 0
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.menu_lobby[1][0] and mouse[0] < self.menu_lobby[1][1] and mouse[1] > self.menu_lobby[1][2] and mouse[1] < self.menu_lobby[1][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 1
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            elif mouse[0] > self.menu_lobby[2][0] and mouse[0] < self.menu_lobby[2][1] and mouse[1] > self.menu_lobby[2][2] and mouse[1] < self.menu_lobby[2][3]:
                self.last_selected_button = self.selected_button
                self.selected_button = 2
                if self.last_selected_button != self.selected_button:
                    self.moveselect.play()
            else:
                if self.key_interuption_button == False:
                    self.selected_button = 'None'

        if self.startGame is True:
                return 1
        else:
            return 0
               
    def update(self):
        self.degree = (self.degree + 1) % 360
        self.clock.tick(FPS)
        if not self.writing:
            if not self.name:
                self.name = "login"

    def render(self):
        self.screen.fill(background_color)
        
        self.bg = pygame.image.load(f"images/background/frame_{self.current_background_color}.png")
        self.bg = pygame.transform.scale(self.bg, self.screenSize)
        self.screen.blit(self.bg, (0, 0))
        self.current_background_color += 1
        if self.current_background_color == 17:
            self.current_background_color = 1

        self.print_text("ONCE AT THE CASINO", 
                             (self.screenSize[0] - 728) // 2, 
                             self.y_start, 
                             (133 - self.i * 2, self.i * 2, 170), 
                             font_size=60,
                             degree=sin(radians(self.degree)) * 2,
                             font_type='fonts/PixExtrusion.ttf')
        self.i += 1
        if self.i == 63:
            self.i = 0
        
        if self.current_scene_menu == 'main_menu':
            self.print_text("Play", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 100, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
            
            self.print_text("Settings", 
                                (self.screenSize[0] // 2) - 140, 
                                self.y_start + 150, 
                                (212, 212, 212), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
            self.print_text("Authors", 
                                (self.screenSize[0] // 2) - 120, 
                                self.y_start + 200, 
                                (200, 200, 200), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
            self.print_text("Scoreboard", 
                                (self.screenSize[0] // 2) - 171, 
                                self.y_start + 250, 
                                (188, 188, 188), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
            self.print_text("Exit", 
                                (self.screenSize[0] // 2) - 70, 
                                self.y_start + 300, 
                                (175, 175, 175), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
        
        if self.current_scene_menu == 'settings':
            self.print_text("Graphic", 
                                (self.screenSize[0] - 240) // 2, 
                                self.y_start + 100, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text("Sounds", 
                                (self.screenSize[0] - 216) // 2, 
                                self.y_start + 150, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text("Controls", 
                                (self.screenSize[0] - 274) // 2, 
                                self.y_start + 200, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            a = self.print_text("Game", 
                                (self.screenSize[0] - 148 ) // 2, 
                                self.y_start + 250, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text("Back", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 300, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
            print(a)
        
        if self.current_scene_menu == 'lobby':
            self.print_text("Join", 
                                (self.screenSize[0] - 144) // 2, 
                                self.y_start + 100, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text("Create lobby", 
                                (self.screenSize[0] - 396) // 2, 
                                self.y_start + 150, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                            font_type='fonts/PixExtrusion.ttf')
            self.print_text("Back", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 250, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
        if self.current_scene_menu == 'settings/graphics':
            self.print_text("Resolution:", 
                                (self.screenSize[0]//2) - 372, 
                                self.y_start + 100, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text("Fullscreen:", 
                                (self.screenSize[0]//2) - 364, 
                                self.y_start + 187, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.fullscreenBox.draw(self.screen)
            self.resolutionBox.draw(self.screen)
            self.print_text("Back", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 250, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
        if self.current_scene_menu == 'settings/game':
            
            self.print_text("Back", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 250, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
        if self.current_scene_menu == 'settings/sounds':
            
            self.print_text("Back", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 250, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
        if self.current_scene_menu == 'settings/controls':
            self.print_text(f"Move forward [{self.binds['move_forward']}]", 
                                (self.screenSize[0]) // 2  - 300, 
                                self.y_start + 100, 
                                (225, 225, 225), 
                                font_size=24,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text(f"Move backward [{self.binds['move_backward']}]", 
                                (self.screenSize[0]) // 2 - 300, 
                                self.y_start + 125, 
                                (225, 225, 225), 
                                font_size=24,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text(f"Move right [{self.binds['move_right']}]", 
                                (self.screenSize[0]) // 2 - 300, 
                                self.y_start + 150, 
                                (225, 225, 225), 
                                font_size=24,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text(f"Move left [{self.binds['move_left']}]", 
                                (self.screenSize[0]) // 2 - 300, 
                                self.y_start + 175, 
                                (225, 225, 225), 
                                font_size=24,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            self.print_text("Back", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 250, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
        if self.current_scene_menu == 'lobby/join':
            self.print_text("enter the IP address:", 
                                (self.screenSize[0] - 650) // 2, 
                                self.y_start + 100, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
            self.address_label = self.print_text(f"{self.address}", 
                                (self.screenSize[0] - list(self.address_label)[2]) // 2, 
                                self.y_start + 200, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
        
            self.print_text("Join", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 350, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
            
            self.print_text("Back", 
                                (self.screenSize[0] - 140) // 2, 
                                self.y_start + 400, 
                                (225, 225, 225), 
                                font_size=48,
                                degree=sin(radians(self.degree)) * 2,
                                font_type='fonts/PixExtrusion.ttf')
        self.print_text('game ver: 0.0.1',
                        0,
                        self.screenSize[1]-24,
                        (224, 224, 224),
                        font_size=24)
        
        if self.selected_button != 'None':
            if self.current_scene_menu == 'main_menu':
                pygame.draw.circle(self.screen, (255, 255, 255), (self.menu_buttons[self.selected_button][0] - 30, self.menu_buttons[self.selected_button][1] + 20), 8)
            if self.current_scene_menu == 'settings':
                pygame.draw.circle(self.screen, (255, 255, 255), (self.setting_buttons[self.selected_button][0] - 30, self.setting_buttons[self.selected_button][2] + 20), 8)
            if self.current_scene_menu == 'settings/graphics':
                pygame.draw.circle(self.screen, (255, 255, 255), (self.setting_graphics_buttons[self.selected_button][0] - 30, self.setting_graphics_buttons[self.selected_button][2] + 20), 8)
            if self.current_scene_menu == 'settings/sounds':
                pygame.draw.circle(self.screen, (255, 255, 255), (self.setting_sounds_buttons[self.selected_button][0] - 30, self.setting_sounds_buttons[self.selected_button][2] + 20), 8)
            if self.current_scene_menu == 'settings/controls':
                pygame.draw.circle(self.screen, (255, 255, 255), (self.setting_controls_buttons[self.selected_button][0] - 30, self.setting_controls_buttons[self.selected_button][2] + 20), 8)
            if self.current_scene_menu == 'lobby':
                pygame.draw.circle(self.screen, (255, 255, 255), (self.menu_lobby[self.selected_button][0] - 30, self.menu_lobby[self.selected_button][2] + 20), 8)
            if self.current_scene_menu == 'lobby/join':
                pygame.draw.circle(self.screen, (255, 255, 255), (self.menu_lobby_join[self.selected_button][0] - 30, self.menu_lobby_join[self.selected_button][2] + 20), 8)
            
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