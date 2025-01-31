import pygame

SIZE = (1280, 720)
FPS = 60

# HOST = '81.31.247.7'  # Адрес сервера
HOST = '127.0.0.1'  # Локальный хост

PORT = 5555

i = 62
GREEN = (2, 248, 170)
DARK_BLUE = (9, 124, 170)
PURPLE = 179, 66, 245

background_color = (0, 0, 0)
bg_img = "images/background.png"

NPS_SIZE_X = 48 / 1.5
NPS_SIZE_Y = 96 / 1.5

CUBE_SIZE = 80
SPEED = 5
SPEED45 = 5 / 2 ** 0.5

poker_img = 'images/poker table.png'
jazz = "music/jazz.mp3"

club_music = ['50 Cent - Just A Lil Bit.mp3',
              'Brandon Beal - Twerk It Like Miley.mp3',
              'FUCCBOI NIKKI - FUKK SLEEP.mp3',
              'Kanye West - I Love It.mp3',
              'Lil Eazzyy - Onna Come Up.mp3',
              'Lil Uzi Vert - Money Longer.mp3',
              'Lil Yachty - Flex Up.mp3',
              'LMFAO - Sexy and I Know It.mp3',
              'Playboi Carti - New Tank.mp3',
              'YEAT - Breathe.mp3',
              'YEAT - Turban.mp3',
              'Young Roc - We Are Not the Same (Sped Up).mp3']

minimap_image = 'images/fullsize.png'
RATIO = 2

E_button_img = 'images/E_button.png'
Q_button_img = 'images/Q_button.png'

slot_line = ['seven', 'bell', 'bell', 'cherry', 'cherry', 'bar', 'bell', 'cherry', 'bell', 'seven', 'bell', 'bell', 
             'seven', 'cherry', 'cherry', 'bell', 'bell', 'cherry', 'bar', 'seven', 'bar', 'bar', 'bell', 'bar', 
             'cherry', 'bell', 'cherry', 'seven', 'seven', 'bar', 'bell', 'bell', 'bell', 'bar', 'seven', 'cherry',
             'bar', 'bar', 'bell', 'bell', 'bar', 'cherry', 'bell', 'bell', 'bar', 'bar', 'cherry', 'cherry', 'seven', 'bell',
             'bar', 'bar', 'bell', 'bell', 'cherry', 'bell', 'bell', 'bell', 'cherry', 'cherry', 'cherry', 'cherry', 
             'bar', 'bar', 'bell', 'bar', 'cherry', 'cherry', 'bell', 'bell', 'bell', 'seven', 'cherry', 'bell', 
             'cherry', 'cherry', 'cherry', 'cherry', 'seven', 'cherry', 'cherry', 'bell', 'seven', 'cherry', 'cherry', 
             'seven', 'bell', 'bar', 'bell', 'seven', 'bell', 'bar', 'bar', 'seven', 'bell', 'cherry', 'bell', 'seven', 'cherry', 'bell']

slot_generator = {'bell': 35, 'cherry': 30, 'bar': 20, 'seven': 15}
slot_machine_img = 'SlotMachine/slot-machine4.png'
slots_img = 'SlotMachine/slot-machine5.png'
seven_img = "SlotMachine/slot-symbol1.png"
cherry_img = "SlotMachine/slot-symbol2.png"
bell_img = "SlotMachine/slot-symbol3.png"
bar_img = "SlotMachine/slot-symbol4.png"
armup_img = 'SlotMachine/slot-machine2.png'
armdown_img = 'SlotMachine/slot-machine3.png'


with open("lvl.txt", "r") as file:
    level_hitboxes = [list(i.rstrip()) for i in file.readlines()]

definedFonts = [
    'fonts/PixExtrusion.ttf',
    'fonts/TeletactileRus.ttf'
]

mainMenuTheme = [
    'audio/main_menu_2.mp3',
    'audio/main_menu_1.mp3'

]
# club_music = ["Playboi Carti - New Tank.mp3"]
