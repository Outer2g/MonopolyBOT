
#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

def RollDice():
    dice1 = random.randrange(1,7)
    dice2 = random.randrange(1,7)
    return dice1 + dice2
# 16 cartas de Suerte, 16 cartas de Caja de Comunidad
# cartas de community que te mueven de la casilla: Go to jail, advance to go. 2 de 16

class SetOfCards:
    def __init__(self):
        pass

    def Shuffle(self):
        random.shuffle(self.cards)
        self.drawn = 0
    def PrintCards(self):
        print self.cards

class CommCards(SetOfCards):
    def __init__(self):
        self.cards = [0] * 14
        self.cards += [1,2]
        self.Shuffle()
        # returns at which position must return, -1 if it doesnt need to move
    def getCard(self):
        if self.drawn == 15: self.Shuffle()
        self.drawn += 1
        if self.cards[self.drawn] == 1:
            # Go to jail
            return 10
        elif self.cards[self.drawn] == 2:
            # Go to Start:
            return 0
        else: return -1
# cartas de chance : Advance to go, mv to Illinoi, move to St. Charles,mv to neares utility,to nearest railroad,
# atras 3 sitios,to jail, Reading railroad,boardwalk .
class ChanceCards(SetOfCards):
    def __init__(self):
        self.cards = [0] * 7
        self.cards += [1,2,3,4,5,6,7,8,9]
        self.Shuffle()
    def getCard(self,pos):
        if self.drawn == 15: self.Shuffle()
        self.drawn += 1
        if self.cards[self.drawn] == 1:
            #go to Start
            return 0
        elif self.cards[self.drawn] == 2:
            #got to Illinoi
            return 24
        elif self.cards[self.drawn] == 3:
            #go to nearest utility
            if pos == 7: return 12
            elif pos == 22: return 28
            elif pos == 36: return 28
            else: return -2
        elif self.cards[self.drawn] == 4:
            if pos == 7: return 5
            elif pos == 22: return 25
            elif pos == 36: return 35
            else: return -2
        elif self.cards[self.drawn] == 5:
            return pos-3
        elif self.cards[self.drawn] == 6:
            return 10
        elif self.cards[self.drawn] == 7:
            return 5
        elif self.cards[self.drawn] == 8:
            return 39
        else: return -1

class BoardGame:
    def __init__(self,players):
        self.players = [0] * players
        self.board = [[]] * 40
        self.board[0] = [i for i in range(players)]
        self.caidas = [0] * 40
        self.movimientos = 0
        self.comm = CommCards()
        self.chance = ChanceCards()

    def getPlayerPos(self,playerID):
        return self.players[playerID]

    def movePlayer(self,playerID,offset):
        pos = self.players[playerID]
        pos += offset
        if pos >=40: pos -= 40
        auxpos = pos
        self.caidas[pos] += 1
        self.movimientos += 1
        #caigo en comunidad
        if (pos == 2 or pos == 17 or pos == 33):
            card = self.comm.getCard()
            if card != -1: pos = card
        #caigo en suerte
        if (pos == 7 or pos == 22 or pos == 36):
            card = self.chance.getCard(pos)
            if card > 0: pos = card
            elif card == -2: print 'ERROR'
        #Go to jail
        if pos == 30: pos = 10

        if auxpos != pos: self.caidas[pos];self.movimientos += 1
        self.players[playerID] = pos
    def printInfoPlayer(self,playerID):
        print 'Player ',playerID,' is in cell ',self.players[playerID]

    def printInfoCaidas(self):
        print 'Los jugadores han caido este numero de veces, en estas casillas'
        print [self.caidas[i] for i in range(0,11)],[self.caidas[i] for i in range(11,21)],\
            [self.caidas[i] for i in range(21,31)],[self.caidas[i] for i in range(31,40)]


    def printEnForma(self):
        print [self.caidas[i] for i in range(20,31)]
        for i in range(1,10):
            print '[',self.caidas[20-i],'                                ',self.caidas[30+i],']'
        print [self.caidas[10-i] for i in range(11)]
    def printEnFormaPorcentaje(self,pasadas):
        self.caidas = [float(elem)/float(self.movimientos) for elem in self.caidas]
        self.printEnForma()
players = 4
tiradas = 2000000
board = BoardGame(players)
for _ in range(tiradas):
    for i in range(players):
        board.movePlayer(0,RollDice())
board.printInfoCaidas()
maxpopulated = []
for _ in range(40):
    maxpos = board.caidas.index(max(board.caidas))
    maxpopulated += [maxpos]
    board.caidas[maxpos] = -1
print maxpopulated