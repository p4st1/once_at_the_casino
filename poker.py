import pygame
import socket
import json

from config import *
import random
from datetime import datetime
import pygame.scrap as scrap
from math import cos, sin, radians
from optionbox import OptionBox
from checkbox import Checkbox


class Poker():
    def __init__(self) -> None:
        pygame.init()

        with open('data.json', 'r') as f:
            config_file = json.load(f)
        size = [1280, 720]
        self.running = True
        self.screenSize = (size[0] - 100, size[1] - 100)
        self.window_type = config_file['Config']['fullscreen']
        self.writing = False
    
        self.screen = pygame.Surface(self.screenSize)
        
        self.chipBalance = 3000

        self.chipsAmount = 1668
        self.chipsAmountLabel = str(self.chipsAmount)

        self.result = ''
        self.gameStarted = False
        self.turn = 'End'

        self.cards = ['2_hearts', '3_hearts', '4_hearts', '5_hearts', '6_hearts', '7_hearts', '8_hearts', '9_hearts', '10_hearts', 'jack_hearts', 'queen_hearts', 'king_hearts', 'ace_hearts',
                      '2_diamonds', '3_diamonds', '4_diamonds', '5_diamonds', '6_diamonds', '7_diamonds', '8_diamonds', '9_diamonds', '10_diamonds', 'jack_diamonds', 'queen_diamonds', 'king_diamonds', 'ace_diamonds',
                      '2_clubs', '3_clubs', '4_clubs', '5_clubs', '6_clubs', '7_clubs', '8_clubs', '9_clubs', '10_clubs', 'jack_clubs', 'queen_clubs', 'king_clubs', 'ace_clubs',
                      '2_spades', '3_spades', '4_spades', '5_spades', '6_spades', '7_spades', '8_spades', '9_spades', '10_spades', 'jack_spades', 'queen_spades', 'king_spades', 'ace_spades']

        self.cardsValues = [2,3,4,5,6,7,8,9,10,11,12,13,14,
                            2,3,4,5,6,7,8,9,10,11,12,13,14,
                            2,3,4,5,6,7,8,9,10,11,12,13,14,
                            2,3,4,5,6,7,8,9,10,11,12,13,14,]
        
    
        self.chips = ['1', '2', '5', '10', '50', '100', '500', '1000']

        self.cardsDeltaX = 60
        
        self.playerCardsPosX = 0
        self.dealerCardsPosX = 0

        self.dealerCardsPosY = size[1] - 700
        self.playerCardsPosY = size[1] - 260

        self.playerCards = []
        self.dealerCards = []

        self.playerAce = 0
        self.dealerAce = 0

        
        self.ready = False
        self.playerSum = 0
        self.playerFinSum = 0
        self.dealerSum = 0
        self.canStart = False
        
        self.sizeRect = [0,0,0,0]
        #player : [roomNum : int, chipAmount, ready : bool, cards : list, turn]
        
        self.players = {1:[1, int(self.chipsAmount), False, [], ''],
                        2:[1, 100, True, [], ''],
                        3:[1, 100, True, [], ''],
                        4:[1, 100, True, [], ''],
                        5:[1, 100, True, [], ''],
                        6:[1, 100, True, [], ''],
                        7:[1, 100, True, [], ''],
                        8:[1, 100, True, [], ''],
                        9:[1, 100, True, [], ''],}
        
        self.table = [['6_clubs', '5_spades', 'king_diamonds', '10_diamonds', '9_clubs'], [0,0,0,0,0]]
        
        596,417585,456
        self.chipsCoords = {1 :{'1' : (520,433),
                                '2' : (480,450),
                                '5' : (596,417),
                                '10' : (651,460),
                                '50' : (576,387),
                                '100' : (559,427),
                                '500' : (633,421),
                                '1000' : (538,394)},
                            2 :{'1' : (850,463),
                                '2' : (820,450),
                                '5' : (885,456),
                                '10' : (921,460),
                                '50' : (896,417),
                                '100' : (859,427),
                                '500' : (933,421),
                                '1000' : (838,394)},
                            3 :{'1' : (1050,363),
                                '2' : (1020,350),
                                '5' : (1085,356),
                                '10' : (1121,360),
                                '50' : (1096,317),
                                '100' : (1059,327),
                                '500' : (1133,321),
                                '1000' : (1038,294)},
                            4 :{'1' : (1050,113),
                                '2' : (1020,100),
                                '5' : (1085,106),
                                '10' : (1121,100),
                                '50' : (1096,57),
                                '100' : (1059,77),
                                '500' : (1133,51),
                                '1000' : (1038,50)},
                            5 :{'1' : (750,203),
                                '2' : (720,190),
                                '5' : (785,196),
                                '10' : (821,200),
                                '50' : (796,157),
                                '100' : (759,167),
                                '500' : (833,161),
                                '1000' : (738,134)},
                            6 :{'1' : (350,203),
                                '2' : (320,190),
                                '5' : (385,196),
                                '10' : (421,200),
                                '50' : (396,157),
                                '100' : (359,167),
                                '500' : (433,161),
                                '1000' : (338,134)},
                            7 :{'1' : (50,113),
                                '2' : (20,100),
                                '5' : (85,106),
                                '10' : (121,100),
                                '50' : (96,57),
                                '100' : (59,77),
                                '500' : (133,51),
                                '1000' : (38,50)},
                            8 :{'1' : (50,363),
                                '2' : (20,350),
                                '5' : (85,356),
                                '10' : (121,350),
                                '50' : (96,307),
                                '100' : (59,327),
                                '500' : (133,301),
                                '1000' : (38,300)},
                            9 :{'1' : (250,463),
                                '2' : (220,450),
                                '5' : (285,456),
                                '10' : (321,460),
                                '50' : (296,417),
                                '100' : (259,427),
                                '500' : (333,421),
                                '1000' : (238,394)}}

        self.getCardSound = pygame.mixer.Sound(f'audio/blackjack/card_move_2.mp3')
        self.getCardSound.set_volume(1)

        self.winSound = pygame.mixer.Sound(f'audio/blackjack/win.mp3')
        self.winSound.set_volume(1)
        self.addChipsSound = pygame.mixer.Sound(f'audio/blackjack/win.mp3')
        self.addChipsSound.set_volume(1)

        self.blackjackSound = pygame.mixer.Sound(f'audio/blackjack/blackjack.mp3')
        self.blackjackSound.set_volume(1)

        self.canDouble = True
        self.double = False

        self.chipsInput = ((self.screenSize[0] - 100) //2,480,100,20)

        self.message = 'welcome to poker'
        self.messageOpacity = 1000
        self.meassageRect = [0,0,0,0]
        
        self.chipSize = (32, 36)

    def logs(self, log : str):
        with open('logs.txt', 'a') as logs:
            logs.write(f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S")}] {log}\n')
        
    def events(self, events):
        mouse = pygame.mouse.get_pos()
        
        if mouse[0] < self.chipsInput[0] or mouse[0] > (self.chipsInput[0] + 200) or mouse[1] < self.chipsInput[1] or mouse[1] > self.chipsInput[1] + 40:
            self.writing = False

        for event in events:                
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if self.writing == False:
                    if event.key == pygame.K_f:
                        if self.canStart:
                            self.ready = not self.ready
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.chipsAmountLabel = self.chipsAmountLabel[:-1]
                    else:
                        if event.unicode.isdigit() == True:
                            if self.chipsAmountLabel == '' and event.unicode == '0':
                                self.message = 'Amount can not start with 0'
                                self.messageOpacity = 1000
                            else:
                                if self.chipBalance > 0:
                                    self.chipsAmountLabel += event.unicode
                                    if self.chipsAmountLabel != '':
                                        if int(self.chipsAmountLabel) > self.chipBalance:
                                            self.message = 'Bet more than you have'
                                            self.messageOpacity = 1000
                                            self.chipsAmountLabel = str(self.chipBalance)
    

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.gameStarted == False:
                    if mouse[0] > self.chipsInput[0] and mouse[0] < (self.chipsInput[0] + 200) and mouse[1] > self.chipsInput[1] and mouse[1] < self.chipsInput[1] + 40:
                        self.writing = True
            

        #88 124
               
    def update(self):
        self.playerCardsPosX = (self.screenSize[0] - (((len(self.playerCards) - 1) * 60) + 88)) // 2
        self.dealerCardsPosX = (self.screenSize[0] - (((len(self.dealerCards) - 1) * 60) + 88)) // 2
        
        if self.chipsAmountLabel != '':
            self.chipsAmount = self.chipsAmountLabel
            self.canStart = True
        else:
            self.canStart = False
        
        
        self.players = {1:[int(self.chipsAmount), self.ready],
                        2:[100, True],
                        3:[100, True],
                        4:[100, True],
                        5:[100, True],
                        6:[100, True],
                        7:[100, True],
                        8:[100, True],
                        9:[100, True],}
        
        if self.gameStarted is False:
            for player in list(self.players.keys()):
                if self.players[player][1] == False:
                    break
            else:
                self.gameStarted = True
        


    def render(self):
        self.screen.fill((211, 211, 211))
        self.bg = pygame.image.load(f"images/poker_table.png")
        self.bg = pygame.transform.scale(self.bg, self.screenSize)
        self.screen.blit(self.bg, (0, 0))

        if self.gameStarted is False:
            self.input = pygame.draw.rect(self.screen, (14,97,46), ((self.screenSize[0] - 100) //2,480,100,20))

        self.print_text(str(self.chipsAmountLabel), 
                                    (self.screenSize[0] - 100) //2, 
                                    480, 
                                    (255,255,255), 
                                    font_size=18,
                                    font_type='fonts/PixExtrusion.ttf')

        self.meassageRect = self.print_text(f"{self.message}", 
                                        (self.screenSize[0] - list(self.meassageRect)[2]) // 2, 
                                        (self.screenSize[1] // 2) + 50, 
                                        (255,255,255), 
                                        font_size=24,
                                        font_type='fonts/PixExtrusion.ttf',
                                        opacity=self.messageOpacity)
        if self.messageOpacity > 0:
            self.messageOpacity -= 10
        
        if self.canStart and self.gameStarted is False:
            self.f_button = pygame.image.load(f"images/hotkeys/F_button.png")
            self.f_button = pygame.transform.scale(self.f_button, (32, 32))
            self.screen.blit(self.f_button, (10, self.screenSize[1] - 42))
            
            if self.ready is False:
                self.print_text("Ready", 
                                        52, 
                                        self.screenSize[1] - 36, 
                                        (255,255,255), 
                                        font_size=24,
                                        font_type='fonts/PixExtrusion.ttf')
            else:
                self.print_text("Unready", 
                                        52, 
                                        self.screenSize[1] - 36, 
                                        (255,255,255), 
                                        font_size=24,
                                        font_type='fonts/PixExtrusion.ttf')
            
        if self.chipsAmountLabel != '':
            for player_num in range(1, len(self.players) + 1):
                tempChipsAmount = self.players[player_num][0]
                for i in range(tempChipsAmount // 1000):
                    self.chip = pygame.image.load(f"images/chips/1000.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['1000'][0],self.chipsCoords[player_num]['1000'][1] - (5 * i)))
                tempChipsAmount = tempChipsAmount % 1000
                for i in range(tempChipsAmount // 500):
                    self.chip = pygame.image.load(f"images/chips/500.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['500'][0], self.chipsCoords[player_num]['500'][1] - (5 * i) ))
                tempChipsAmount = tempChipsAmount % 500
                for i in range(tempChipsAmount // 100):
                    self.chip = pygame.image.load(f"images/chips/100.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['100'][0], self.chipsCoords[player_num]['100'][1] - (5 * i)))
                tempChipsAmount = tempChipsAmount % 100
                for i in range(int(tempChipsAmount) // 50):
                    self.chip = pygame.image.load(f"images/chips/50.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['50'][0], self.chipsCoords[player_num]['50'][1] - (5 * i)))
                tempChipsAmount = tempChipsAmount % 50
                for i in range(int(tempChipsAmount) // 10):
                    self.chip = pygame.image.load(f"images/chips/10.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['10'][0], self.chipsCoords[player_num]['10'][1] - (5 * i)))
                tempChipsAmount = tempChipsAmount % 10
                for i in range(int(tempChipsAmount) // 5):
                    self.chip = pygame.image.load(f"images/chips/5.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['5'][0], self.chipsCoords[player_num]['5'][1] - (5 * i)))
                tempChipsAmount = tempChipsAmount % 5
                for i in range(int(tempChipsAmount) // 2):
                    self.chip = pygame.image.load(f"images/chips/2.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['2'][0], self.chipsCoords[player_num]['2'][1] - (5 * i)))
                tempChipsAmount = tempChipsAmount % 2
                for i in range(int(tempChipsAmount)):
                    self.chip = pygame.image.load(f"images/chips/1.png")
                    self.chip = pygame.transform.scale(self.chip, self.chipSize)
                    self.screen.blit(self.chip, (self.chipsCoords[player_num]['1'][0], self.chipsCoords[player_num]['1'][1] - (5 * i)))

        self.print_text(f"Balance {self.chipBalance}", 
                                    0, 
                                    0, 
                                    (255,255,255), 
                                    font_size=24,
                                    font_type='fonts/PixExtrusion.ttf')
        
    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0, opacity=1000):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.text.set_alpha(opacity)
        self.screen.blit(self.text, (x, y))
        return self.text.get_rect()

if __name__ == "__main__":
    menu = Poker()
    pygame.init()
    screen = pygame.display.set_mode(Poker().screenSize)
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