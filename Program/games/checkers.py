from enum import Enum
from AbstractGameClass import AbstractGameClass

# enum pro reprezentaci dvou barev
class Color(Enum):
    WHITE = "w"
    BLACK = "b"

# enum pro reprezentaci dvou hracu
class Player(Enum):
    ONE = "1"
    TWO = "2"

# trida reprezentujici dvouprvkovou mnozinu cisel(bod, vektor)
class Point():
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    # posun bodu o x a y
    def move(self, x, y):
        self.x += x
        self.y += y
        return self
    
    # vytvoreni klonu
    def clone(self):
        return Point(self.x, self.y)

    # vytvoreni klonu a posun(vytvoreni relativniho klonu dle bodu)
    def cloneAndMove(self, x, y):
        return self.clone().move(x, y)
    
    # pretizeny equals
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Figure():
    def __init__(self, color:Color, isQueen = False):
        self.color = color
        self.isQueen = isQueen
    
    # funkce pro zjisk spravneho symbolu pri renderu
    def getIcon(self):
        if self.isQueen:
            return self.color.value.upper()
        return self.color.value

    # funkce pocita mozne tahy dle bodu a fugurky
    def getPossibleMoves(self, point:Point):
        if self.isQueen:
            return [point.cloneAndMove(-1, 1), 
                    point.cloneAndMove(1, -1), 
                    point.cloneAndMove(1, 1), 
                    point.cloneAndMove(-1, -1)]

        if self.color.value == Color.WHITE.value:
            return [point.cloneAndMove(-1, -1), 
                    point.cloneAndMove(1, -1)]

        if self.color.value == Color.BLACK.value:
            return [point.cloneAndMove(1, 1), 
                    point.cloneAndMove(-1, 1)]

class Board():
    def __init__(self, size:int = 8):
        self.size = size
        # vytvorit dvoudimenzionalni list reprezentujici desku o rozmerech size x size
        self.board = [[None] * self.size for i in range(0, self.size)]
        # hrac jedna je natahu
        self.playerOnTurn = Player.ONE
        # ikona pro prazdny pole
        self.emptyIcon = "0"

        #vytvorit cerne figurky
        for i in range(1, self.size, 2):
            self.board[0][i] = Figure(Color.BLACK)
        for i in range(0, self.size, 2):
            self.board[1][i] = Figure(Color.BLACK)
        for i in range(1, self.size, 2):
            self.board[2][i] = Figure(Color.BLACK)
        
        #vytvorit bile figurky
        for i in range(0, self.size, 2):
            self.board[5][i] = Figure(Color.WHITE)
        for i in range(1, self.size, 2):
            self.board[6][i] = Figure(Color.WHITE)
        for i in range(0, self.size, 2):
            self.board[7][i] = Figure(Color.WHITE)
        

       

        self.render()

    def render(self):

        print("\n   ", end = " ")
        for i in range(0, self.size):
            print(i, end = "  ")
        print("\n")

        for i in range(0, self.size):
            print(i, end = "   ")

            for j in range(0, self.size):
                if self.board[i][j]:
                    print(self.board[i][j].getIcon(), end = "  ")
                else:
                    print(self.emptyIcon, end = "  ")
            print() 

        print(f"\nPlayer {self.playerOnTurn.value} is on turn [default 0 0 0 0]:", end = " ")
    
    def getPossibleMovesForCell(self, point:Point):
        possibleAutomaticMoves = []
        figure = self.getFigure(point)
        # najdi mozne tahy pro konkretni figurku
        possibleMoves = figure.getPossibleMoves(point)

        # pro kazdy mozny tah zjisti zda je vevnitr desky a zda je blizko figurky jine barvy
        for move in possibleMoves:
            if self.isInsideBoard(move) and self.getFigure(move) and self.getFigure(move).color.value != figure.color.value:
                # spocti movementVector = figurka_soupere - figurka
                movementVector = Point(move.x - point.x, move.y - point.y)
                # najdi policko po preskoceni figurky protihrace
                afterJumpPoint = Point(move.x + movementVector.x, move.y + movementVector.y)
                # zjisti zda je po preskoceni vevnitr desky a zda zatim neni zadna figurka
                if self.isInsideBoard(afterJumpPoint) and self.getFigure(afterJumpPoint) == None:
                    possibleAutomaticMoves.append([point, move, afterJumpPoint])

        return possibleAutomaticMoves

    def makeAutomaticMoves(self):
        possibleAutomaticMoves = []
        # najdi mozne autotahy pro kazdou figurku; barva zalezi na hraci, ktery je na tahu
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell and \
                ((cell.color.value == Color.WHITE.value and self.playerOnTurn.value == Player.ONE.value) or \
                (cell.color.value == Color.BLACK.value and self.playerOnTurn.value == Player.TWO.value)):
                    # najdi mozne autotahy pro konkretni figurku
                    possibleAutomaticMoves += self.getPossibleMovesForCell(Point(j, i))

        # zadne autotahy nejsou
        if len(possibleAutomaticMoves) == 0:
            return

        # aplikuj autotahy
        appliedTurn = self.applyAutomaticTurns(possibleAutomaticMoves)
        while True:
            # figurka po autotahu
            figurePoint = appliedTurn[2]
            # najdi mozne autotahy pro konkretni figurku
            possibleAutomaticMoves = self.getPossibleMovesForCell(figurePoint)

            # zadne autotahy nejsou -> zmen hrace a hledej autotahy pro nej
            if len(possibleAutomaticMoves) == 0:
                self.switchPlayer()
                return self.makeAutomaticMoves()
            
            # aplikuj autotahy
            appliedTurn = self.applyAutomaticTurns(possibleAutomaticMoves)

    # funkce pro zjisteni zda je bod uvnitr desky
    def isInsideBoard(self, point:Point) -> bool:
        if point.x < 0 or point.x > self.size - 1:
            return False
        if point.y < 0 or point.y > self.size - 1:
            return False
        return True
    
    # funkce pro zjisk figurky z desky dle bodu
    def getFigure(self, point:Point) -> Figure:
        return self.board[point.y][point.x]
    
    # funkce pro kontrolu rucneho tahu 
    def turn(self, figurePoint:Point, targetPoint:Point) -> bool:
        # kontrola zda je start a cil vevnitr desky
        if not self.isInsideBoard(figurePoint) or not self.isInsideBoard(targetPoint):
            return
        
        figure = self.getFigure(figurePoint)
        # kontrola zda je to figurka
        if figure == None:
            return
        
        # kontrola zda hrac muze tahnout touhle figurkou
        if self.playerOnTurn.value == Player.ONE.value and figure.color.value == Color.BLACK.value:
            return
        if self.playerOnTurn.value == Player.TWO.value and figure.color.value == Color.WHITE.value:
            return

        # kontrola zda cil patri mezi mozne tahy konkretni figurkou
        possibleMoves = figure.getPossibleMoves(figurePoint)
        if not (targetPoint in possibleMoves):
            return
        
        # kontrola zda je cilove polickp prazdne
        if self.getFigure(targetPoint):
            return
        
        # aplikuj tahy
        self.applyTurn(figurePoint, figurePoint, targetPoint, True)

    # funkce prohazuje hrace
    def switchPlayer(self):
        self.playerOnTurn = Player.TWO if self.playerOnTurn.value == Player.ONE.value else Player.ONE
        self.render()

    # funkce aplikuje tah
    def applyTurn(self, figurePoint:Point, middlePoint:Point, targetPoint:Point, hasSwitchPlayer:bool):
        figure = self.getFigure(figurePoint)
        self.board[figurePoint.y][figurePoint.x] = None
        self.board[middlePoint.y][middlePoint.x] = None
        self.board[targetPoint.y][targetPoint.x] = figure

        # pokud je cil na prvnim/poslednim radku -> zmen figurku na kralovnu
        if targetPoint.y in [0, 7]:
            figure.isQueen = True
        
        # dle parametru zmen hrace
        if hasSwitchPlayer:
            self.switchPlayer()
    
    def applyAutomaticTurns(self, possibleAutomaticMoves):
        appliedTurn = None
        # kdyz je jeden automaticky tah, aplikuj
        if len(possibleAutomaticMoves) == 1:
            appliedTurn = possibleAutomaticMoves[0]
            self.applyTurn(*possibleAutomaticMoves[0], False)
        else:
            print()
            print("Default 1")
            # kdyz je vice automatickych tahu, dej na vyber a defaultne vyber 1
            for i, possibleMove in enumerate(possibleAutomaticMoves):
                [figurePoint, middlePoint, targetPoint] = possibleMove
                print(f'{i + 1}) {figurePoint.x} {figurePoint.y} {targetPoint.x} {targetPoint.y}')
            
            moveIndex = int(input())
            moveIndex = moveIndex if moveIndex >= 1 and moveIndex <= len(possibleAutomaticMoves) else 1
            appliedTurn = possibleAutomaticMoves[moveIndex - 1]
            self.applyTurn(*possibleAutomaticMoves[moveIndex - 1], False)
        
        return appliedTurn
        
    # funkce urcuje zda je konec hry
    def isEndOfGame(self):
        whiteCount = 0
        blackCount = 0

        # pocita pocet bilych a cerny figurek na desce
        for row in self.board:
            for cell in row:
                if cell and cell.color.value == Color.WHITE.value:
                    whiteCount += 1
                if cell and cell.color.value == Color.BLACK.value:
                    blackCount += 1

                # staci mit alespon jednu od kazde barvy -> neni to konec
                if whiteCount > 0 and blackCount > 0:
                    return False

        # kdyz jednoumu hraci chybi figurky, je to konec hry
        return whiteCount == 0 or blackCount == 0


class DamaGameClass(AbstractGameClass):
    # funkce pro zpracovani vstupu
    def getCommand(self):
        try:
            [figureX, figureY, targetX, targetY] = [int(i) for i in input().split()]
            return [Point(figureX, figureY), Point(targetX, targetY)]
        except:
            # pokud je spatny vstup, vrat default [0,0,0,0]
            return [Point(0, 0), Point(0, 0)]
        
    def start(self):
        board = Board()

        # pokracuj dokud neni konec hry
        while not board.isEndOfGame():
            # proved vsechny automaticke tahy
            board.makeAutomaticMoves()
            # proved tah hrace
            board.turn(*self.getCommand())

    def getGameName(self):
        return "Checkers"