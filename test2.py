import random

cards = ['2_hearts', '3_hearts', '4_hearts', '5_hearts', '6_hearts', '7_hearts', '8_hearts', '9_hearts', '10_hearts', 'jack_hearts', 'queen_hearts', 'king_hearts', 'ace_hearts',
        '2_diamonds', '3_diamonds', '4_diamonds', '5_diamonds', '6_diamonds', '7_diamonds', '8_diamonds', '9_diamonds', '10_diamonds', 'jack_diamonds', 'queen_diamonds', 'king_diamonds', 'ace_diamonds',
        '2_clubs', '3_clubs', '4_clubs', '5_clubs', '6_clubs', '7_clubs', '8_clubs', '9_clubs', '10_clubs', 'jack_clubs', 'queen_clubs', 'king_clubs', 'ace_clubs',
        '2_spades', '3_spades', '4_spades', '5_spades', '6_spades', '7_spades', '8_spades', '9_spades', '10_spades', 'jack_spades', 'queen_spades', 'king_spades', 'ace_spades']

pokerCombsRoyalFlush = {
         'Royal Flush1' : ['ace_clubs', 'king_clubs', 'queen_clubs', 'jack_clubs', '10_clubs'],
         'Royal Flush2' : ['ace_diamonds', 'king_diamonds', 'queen_diamonds', 'jack_diamonds', '10_diamonds'],
         'Royal Flush3' : ['ace_hearts', 'king_hearts', 'queen_hearts', 'jack_hearts', '10_hearts'],
         'Royal Flush4' : ['ace_spades', 'king_spades', 'queen_spades', 'jack_spades', '10_spades'],
}
StraightFlush = ['2_clubs3_clubs4_clubs5_clubs6_clubs7_clubs8_clubs9_clubs10_clubsjack_clubsqueen_clubsking_clubsace_clubs',
                  '2_diamonds3_diamonds4_diamonds5_diamonds6_diamonds7_diamonds8_diamonds9_diamonds10_diamondsjack_diamondsqueen_diamondsking_diamondsace_diamond',
                  '2_hearts3_hearts4_hearts5_hearts6_hearts7_hearts8_hearts9_hearts10_heartsjack_heartsqueen_heartsking_heartsace_hearts',
                  '2_spades3_spades4_spades5_spades6_spades7_spades8_spades9_spades10_spadesjack_spadesqueen_spadesking_spadesace_spades',
]
pokerCombsFourOfAKind = {
         'Four of a kind1' : ['ace_clubs', 'ace_diamonds', 'ace_hearts', 'ace_spades'],
         'Four of a kind2' : ['king_clubs', 'king_diamonds', 'king_hearts', 'king_spades'],
         'Four of a kind3' : ['queen_clubs', 'queen_diamonds', 'queen_hearts', 'queen_spades'],
         'Four of a kind4' : ['jack_clubs', 'jack_diamonds', 'jack_hearts', 'jack_spades'],
         'Four of a kind5' : ['10_clubs', '10_diamonds', '10_hearts', '10_spades'],
         'Four of a kind6' : ['9_clubs', '9_diamonds', '9_hearts', '9_spades'],
         'Four of a kind7' : ['8_clubs', '8_diamonds', '8_hearts', '8_spades'],
         'Four of a kind8' : ['7_clubs', '7_diamonds', '7_hearts', '7_spades'],
         'Four of a kind9' : ['6_clubs', '6_diamonds', '6_hearts', '6_spades'],
         'Four of a kindA' : ['5_clubs', '5_diamonds', '5_hearts', '5_spades'],
         'Four of a kindB' : ['4_clubs', '4_diamonds', '4_hearts', '4_spades'],
         'Four of a kindC' : ['3_clubs', '3_diamonds', '3_hearts', '3_spades'],
         'Four of a kindD' : ['2_clubs', '2_diamonds', '2_hearts', '2_spades'],
        }

cardsValuesList = [2,3,4,5,6,7,8,9,10,11,12,13,14,
            2,3,4,5,6,7,8,9,10,11,12,13,14,
            2,3,4,5,6,7,8,9,10,11,12,13,14,
            2,3,4,5,6,7,8,9,10,11,12,13,14,]
run = 0

def checkCombination(playerCards : list, tableCards : list):
    sumCards = tableCards + playerCards
    deuce, three = 0,0
    cardSuit = {
        'clubs' : 0,
        'diamonds' : 0, 
        'hearts' : 0, 
        'spades' : 0
        }
    cardsValues = {}
    for combination in list(pokerCombsRoyalFlush.values()):
        if set(combination).issubset(sumCards):
            print('Royal Flush')
            print(combination)
            return 9
    for card in sumCards:
        card = card.split('_')
        if card[0] not in cardsValues:
            cardsValues[card[0]] = 1
        else:
            cardsValues[card[0]] += 1
        cardSuit[card[1]] += 1
    for suit in list(cardSuit.values()):
        if suit == 5:
            temp_list = []
            temp_list2 = []
            temp_card = ''
            for card in sumCards:
                card = card.split('_')
                temp_card = card[1]
                if card[1] == list(cardSuit.keys())[list(cardSuit.values()).index(suit)]:
                    curCard = '_'.join(card)
                    cardVal = cards.index(curCard)
                    temp_list.append(cardsValuesList[cardVal])
            temp_list.sort()
            for val in temp_list:
                temp_list2.append(f'{cards[val - 2].split('_')[0]}_{temp_card}')
            for j in StraightFlush:
                if ''.join(temp_list2) in j:
                    print('Straight Flush')
                    print(combination)
                    return 8
    for combination in list(pokerCombsFourOfAKind.values()):
        if set(combination).issubset(sumCards):
            print('Four of a kind')
            print(combination)
            return 7
    for value in list(cardsValues.keys()):
        if cardsValues[value] >= 3:
            num = cardsValues[value]
            cardsValues[value] = num % 3
            three += 1
        if cardsValues[value] >= 2:
            num = cardsValues[value]
            cardsValues[value] = num % 2
            deuce += 1
    if deuce > 0 and three > 0:
        print('Full house')
        return 6
    for suit in list(cardSuit.values()):
        if suit == 5:
            print('Flash')
            return 5
    temp_list = []
    temp_list2 = []
    for card in sumCards:
        card = card.split('_')
        temp_card = card[1]
        curCard = '_'.join(card)
        cardVal = cards.index(curCard)
        if cardsValuesList[cardVal] not in temp_list:
            temp_list.append(cardsValuesList[cardVal])
    temp_list.sort()
    for i in temp_list:
        temp_list2.append(str(i))
    for i in range(len(temp_list2) % 5):
        if ''.join(temp_list2[(0+i):(5+i)]) in '1234567891011121314':
            print('Straight')
            return 4
    if three > 0:
        print('Tree of a kind')
        return 3
    if deuce >= 2:
        print('Two pair')
        return 2 
    if deuce >= 1:
        print('Pair')
        return 1
    return 0
raffleCards = cards[:]


    
    
tableCards = []   
for i in range(5):
        card = random.choice(raffleCards)
        tableCards.append(card)
        raffleCards.remove(card) 
print(tableCards)

for i in range(9):
    playerCards = []
    for i in range(2):
        card = random.choice(raffleCards)
        playerCards.append(card)
        raffleCards.remove(card) 
    print(playerCards)
    checkCombination(playerCards, tableCards)