from os import walk
SIZE = (1280, 720)
FPS = 60

HOST = '81.31.247.7'  # Адрес сервера
# HOST = '127.0.0.1'  # Локальный хост

PORT = 5555

i = 62
GREEN = (2, 248, 170)
DARK_BLUE = (9, 124, 170)

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

with open("lvl.txt", "r") as file:
    level_hitboxes = [list(i.rstrip()) for i in file.readlines()]

definedFonts = [
    'fonts/PixExtrusion.ttf'
]
# club_music = ["Playboi Carti - New Tank.mp3"]
