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


class Blackjack():
    def __init__(self, size, money) -> None:
        pygame.init()

        with open('data.json', 'r') as f:
            config_file = json.load(f)
    
        self.running = True
        self.screenSize = size
        self.window_type = config_file['Config']['fullscreen']
        self.writing = False
    
        self.screen = pygame.Surface(self.screenSize)
        
        self.chipBalance = money

        self.chipsAmount = ''

        self.result = ''
        self.gameStarted = False
        self.turn = 'End'

        self.cards = ['2_hearts', '3_hearts', '4_hearts', '5_hearts', '6_hearts', '7_hearts', '8_hearts', '9_hearts', '10_hearts', 'jack_hearts', 'queen_hearts', 'king_hearts', 'ace_hearts',
                      '2_diamonds', '3_diamonds', '4_diamonds', '5_diamonds', '6_diamonds', '7_diamonds', '8_diamonds', '9_diamonds', '10_diamonds', 'jack_diamonds', 'queen_diamonds', 'king_diamonds', 'ace_diamonds',
                      '2_clubs', '3_clubs', '4_clubs', '5_clubs', '6_clubs', '7_clubs', '8_clubs', '9_clubs', '10_clubs', 'jack_clubs', 'queen_clubs', 'king_clubs', 'ace_clubs',
                      '2_spades', '3_spades', '4_spades', '5_spades', '6_spades', '7_spades', '8_spades', '9_spades', '10_spades', 'jack_spades', 'queen_spades', 'king_spades', 'ace_spades']

        self.cardsValues = [2,3,4,5,6,7,8,9,10,10,10,10,11,
                            2,3,4,5,6,7,8,9,10,10,10,10,11,
                            2,3,4,5,6,7,8,9,10,10,10,10,11,
                            2,3,4,5,6,7,8,9,10,10,10,10,11,]
        
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

        self.playerSum = 0
        self.playerFinSum = 0
        self.dealerSum = 0

        self.sizeRect = [0,0,0,0]

        self.chipsCoords = {'1' : (950,200),
                            '2' : (890,220),
                            '5' : (940,260),
                            '10' : (1000,240),
                            '50' : (880,285),
                            '100' : (828,238),
                            '500' : (995,310),
                            '1000' : (1060,280)}

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

        self.chipsInput = (self.screenSize[0] - 300,400)

        self.message = 'welcome to blackjack'
        self.messageOpacity = 1000
        self.meassageRect = [0,0,0,0]

    def sumUpScore(self, cards : list, tempSum, ace):
        self.sum = 0
        self.ace = ace
        for card in cards:
            if card.split('_')[0] == 'ace':
                self.ace += 1
            else:
                self.sum += self.cardsValues[self.cards.index(card)]

        for i in range(self.ace):
            if (self.sum + 11) <= 21:
                self.sum += 11
            else:
                self.sum += 1

        
        return self.sum

    def winCalc(self):
        print(self.result,  self.bet)
        self.chipBalance -= self.bet
        if self.result == 'YOU WIN':
            self.bet = self.bet * 1.5
        elif self.result == 'DRAW':
            self.bet = self.bet
        elif self.result == 'LOSE' or self.result == 'BUST':
            self.bet = 0
        elif self.result == 'BLACKJACK':
            self.bet = self.bet * 2
        print(self.bet)
        self.chipBalance += int(self.bet)
        self.chipsAmount = ''

    def giveCardsToDealer(self):
        card = random.choice(self.raffleCards)
        self.raffleCards.remove(card)
        self.dealerCards.append(card)
        self.dealerSum = self.sumUpScore(self.dealerCards, self.dealerSum, self.dealerAce)

    def giveCardsToPlayer(self):
        card = random.choice(self.raffleCards)
        self.raffleCards.remove(card)
        self.playerCards.append(card)
        self.playerSum = self.sumUpScore(self.playerCards, self.playerSum, self.playerAce)

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
                        if self.chipBalance > 0:
                            if self.chipsAmount != '':
                                if self.turn == 'End':
                                    self.canDouble = True
                                    self.double == False
                                    self.playerSum, self.dealerSum = 0, 0
                                    self.gameStarted = True
                                    self.bet = int(self.chipsAmount)
                                    self.raffleCards = self.cards[:]
                                    self.playerCards, self.dealerCards = [], []
                                    self.turn = 'Player'
                            else:
                                self.message = 'Make a bet first'
                                self.messageOpacity = 1000
                        else:
                            self.message = 'No more chips'
                            self.messageOpacity = 1000
                    
                    if event.key == pygame.K_d:
                        if self.turn == 'Player_waiting':
                            if self.canDouble == True:
                                if (self.chipBalance - (self.bet * 2)) > 0:
                                    self.bet = self.bet * 2
                                    self.getCardSound.play()
                                    self.giveCardsToPlayer()
                                    self.canDouble = False
                                    self.double == True
                                    self.turn = 'Dealer'
                                else:
                                    self.message = 'Not enough for double'
                                    self.messageOpacity = 1000


                    if event.key == pygame.K_q:
                        if self.turn == 'End':
                            print('finished')

                    if event.key == pygame.K_h:
                        if self.turn == 'Player_waiting':
                            self.getCardSound.play()
                            self.giveCardsToPlayer()

                    if event.key == pygame.K_s:
                        if self.turn == 'Player_waiting':
                            self.getCardSound.play()
                            self.turn = 'Dealer'
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.chipsAmount = self.chipsAmount[:-1]
                    else:
                        if event.unicode.isdigit() == True:
                            if self.chipBalance > 0:
                                self.chipsAmount += event.unicode
                                if int(self.chipsAmount) > self.chipBalance:
                                    self.message = 'Bet more than you have'
                                    self.messageOpacity = 1000
                                    self.chipsAmount = str(self.chipBalance)
                print(print(self.chipsAmount))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.gameStarted == False:
                    if mouse[0] > self.chipsInput[0] and mouse[0] < (self.chipsInput[0] + 200) and mouse[1] > self.chipsInput[1] and mouse[1] < self.chipsInput[1] + 40:
                        self.writing = True

        #88 124
               
    def update(self):
        self.playerCardsPosX = (self.screenSize[0] - (((len(self.playerCards) - 1) * 60) + 88)) // 2
        self.dealerCardsPosX = (self.screenSize[0] - (((len(self.dealerCards) - 1) * 60) + 88)) // 2
        if self.gameStarted:
            if self.turn == 'Player':
                for i in range(2):
                    self.getCardSound.play()
                    self.giveCardsToPlayer()
                if self.playerSum == 21:
                    self.result = 'BLACKJACK'
                    self.winCalc()
                    self.addChipsSound.play()
                    self.blackjackSound.play()
                    self.turn = 'End'
                    self.gameStarted = False
                else:
                    self.turn = 'Player_waiting'
                    
            if self.turn == 'Player_waiting':
                if self.playerSum > 21:
                    self.result = 'BUST'
                    self.winCalc()
                    self.turn = 'End'
                    self.gameStarted = False
                
            if self.turn == 'Dealer':
                if self.dealerSum < 17:
                    self.giveCardsToDealer()

                elif self.dealerSum > 21:
                    self.result = 'YOU WIN'
                    self.turn = 'End'
                    self.winCalc()
                    self.winSound.play()
                    self.addChipsSound.play()
                    self.gameStarted = False

                else:
                    if self.playerSum == self.dealerSum:
                        self.result = 'DRAW'
                    if self.playerSum < self.dealerSum:
                        self.result = 'LOSE'
                    if self.playerSum > self.dealerSum:
                        self.result = 'YOU WIN'
                        self.winSound.play()
                        self.addChipsSound.play()

                    self.winCalc()
                    self.turn = 'End'
                    self.gameStarted = False

            if self.playerSum > 21:
                self.turn = 'End'
                self.winCalc()
                self.result = 'BUST'
                self.gameStarted = False
        self.render()
            
    def render(self):
        self.screen.fill((211, 211, 211))
        self.bg = pygame.image.load(f"images/blackjack_bg.png")
        self.bg = pygame.transform.scale(self.bg, self.screenSize)
        self.screen.blit(self.bg, (0, 0))


        pygame.draw.rect(self.screen, (69,106,36), (self.screenSize[0] - 300,400,200,40))

        self.print_text(self.chipsAmount, 
                                    self.screenSize[0] - 300, 
                                    412, 
                                    (255,255,255), 
                                    font_size=24,
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

        
        if self.turn == 'Player_waiting':
            self.h_button = pygame.image.load(f"images/hotkeys/H_button.png")
            self.h_button = pygame.transform.scale(self.h_button, (32, 32))
            self.screen.blit(self.h_button, (10, self.screenSize[1] - 42))

            self.s_button = pygame.image.load(f"images/hotkeys/S_button.png")
            self.s_button = pygame.transform.scale(self.s_button, (32, 32))
            self.screen.blit(self.s_button, (150, self.screenSize[1] - 42))

            self.d_button = pygame.image.load(f"images/hotkeys/D_button.png")
            self.d_button = pygame.transform.scale(self.d_button, (32, 32))
            self.screen.blit(self.d_button, (300, self.screenSize[1] - 42))

            self.print_text("Hand", 
                                    52, 
                                    self.screenSize[1] - 36, 
                                    (255,255,255), 
                                    font_size=24,
                                    font_type='fonts/PixExtrusion.ttf')

            self.print_text("Stand", 
                                    192, 
                                    self.screenSize[1] - 36, 
                                    (255,255,255), 
                                    font_size=24,
                                    font_type='fonts/PixExtrusion.ttf')

            self.print_text("Double", 
                                    342, 
                                    self.screenSize[1] - 36, 
                                    (255,255,255), 
                                    font_size=24,
                                    font_type='fonts/PixExtrusion.ttf')
            
        if self.turn == 'End':
            if self.chipBalance > 0:
                self.f_button = pygame.image.load(f"images/hotkeys/F_button.png")
                self.f_button = pygame.transform.scale(self.f_button, (32, 32))
                self.screen.blit(self.f_button, (10, self.screenSize[1] - 42))

                self.q_button = pygame.image.load(f"images/hotkeys/Q_button.png")
                self.q_button = pygame.transform.scale(self.q_button, (32, 32))
                self.screen.blit(self.q_button, (300, self.screenSize[1] - 42))

                self.print_text("Start new game", 
                                        52, 
                                        self.screenSize[1] - 36, 
                                        (255,255,255), 
                                        font_size=24,
                                        font_type='fonts/PixExtrusion.ttf')

                self.print_text("Quit", 
                                        342, 
                                        self.screenSize[1] - 36, 
                                        (255,255,255), 
                                        font_size=24,
                                        font_type='fonts/PixExtrusion.ttf')
            if self.chipBalance <= 0:
                self.q_button = pygame.image.load(f"images/hotkeys/Q_button.png")
                self.q_button = pygame.transform.scale(self.q_button, (32, 32))
                self.screen.blit(self.q_button, (10, self.screenSize[1] - 42))

                self.print_text("Quit", 
                                        52, 
                                        self.screenSize[1] - 36, 
                                        (255,255,255), 
                                        font_size=24,
                                        font_type='fonts/PixExtrusion.ttf')
                
            self.sizeRect = self.print_text(self.result, 
                                    (self.screenSize[0] - list(self.sizeRect)[2]) // 2, 
                                    (self.screenSize[1] - list(self.sizeRect)[3]) // 2, 
                                    (255,255,255), 
                                    font_size=64,
                                    font_type='fonts/PixExtrusion.ttf')
            
        for i in range(len(self.playerCards)):
            self.card = pygame.image.load(f"images/cards/{self.playerCards[i]}.png")
            self.card = pygame.transform.scale(self.card, (88, 124))
            self.screen.blit(self.card, (self.playerCardsPosX + self.cardsDeltaX * i, self.playerCardsPosY))

        for i in range(len(self.dealerCards)):
            self.card = pygame.image.load(f"images/cards/{self.dealerCards[i]}.png")
            self.card = pygame.transform.scale(self.card, (88, 124))
            self.screen.blit(self.card, (self.dealerCardsPosX + self.cardsDeltaX * i, self.dealerCardsPosY))

        if self.chipsAmount != '':
            tempChipsAmount = int(self.chipsAmount)
            for i in range(tempChipsAmount // 1000):
                self.chip = pygame.image.load(f"images/chips/1000.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['1000'][0],self.chipsCoords['1000'][1] - (9 * i)))
            tempChipsAmount = tempChipsAmount % 1000
            for i in range(tempChipsAmount // 500):
                self.chip = pygame.image.load(f"images/chips/500.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['500'][0], self.chipsCoords['500'][1] - (9 * i) ))
            tempChipsAmount = tempChipsAmount % 500
            for i in range(tempChipsAmount // 100):
                self.chip = pygame.image.load(f"images/chips/100.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['100'][0], self.chipsCoords['100'][1] - (9 * i)))
            tempChipsAmount = tempChipsAmount % 100
            for i in range(int(tempChipsAmount) // 50):
                self.chip = pygame.image.load(f"images/chips/50.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['50'][0], self.chipsCoords['50'][1] - (9 * i)))
            tempChipsAmount = tempChipsAmount % 50
            for i in range(int(tempChipsAmount) // 10):
                self.chip = pygame.image.load(f"images/chips/10.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['10'][0], self.chipsCoords['10'][1] - (9 * i)))
            tempChipsAmount = tempChipsAmount % 10
            for i in range(int(tempChipsAmount) // 5):
                self.chip = pygame.image.load(f"images/chips/5.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['5'][0], self.chipsCoords['5'][1] - (9 * i)))
            tempChipsAmount = tempChipsAmount % 5
            for i in range(int(tempChipsAmount) // 2):
                self.chip = pygame.image.load(f"images/chips/2.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['2'][0], self.chipsCoords['2'][1] - (9 * i)))
            tempChipsAmount = tempChipsAmount % 2
            for i in range(int(tempChipsAmount)):
                self.chip = pygame.image.load(f"images/chips/1.png")
                self.chip = pygame.transform.scale(self.chip, (64, 72))
                self.screen.blit(self.chip, (self.chipsCoords['1'][0], self.chipsCoords['1'][1] - (9 * i)))

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
    menu = Blackjack()
    pygame.init()
    screen = pygame.display.set_mode(Blackjack().screenSize)
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