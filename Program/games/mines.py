import random
from enum import Enum

from AbstractGameClass import AbstractGameClass

# enum pro reprezentaci policka
class Icon(Enum):
    MINE = "B"
    FLAG = "F"
    NUMBER = "X"
    NOTOPENED = "N"

# trida reprezentujici dvouprvkovou mnozinu cisel(x, y)
class Point:

    __x:int
    __y:int   

    def __init__(self, x:int, y:int) -> None:
        self.__x = x
        self.__y = y
        
    # funkce vrati aktualni pozici x
    def getX(self) -> int:
        return self.__x
    
    # funkce vrati aktualni pozici y    
    def getY(self) -> int:
        return self.__y
    
    # metoda nastavi novou aktualni pozici x 
    def setX(self, newX:int) -> None:
        self.__x = newX
    
    # metoda nastavi novou aktualni pozici y 
    def setY(self, newY:int) -> None:
        self.__y = newY

# trida reprezentujici policko na desce
class Square():

    # zda policko obsahuje minu
    __hasMine:bool
    # zda policko byl oznacen vlajkou
    __hasFlag:bool
    # zda policko bylo otevreno
    __isOpened:bool
    # kolik je v okoli min
    __number:int
    # kde se nachazi policko
    __position:Point
    # ikonka policka
    __icon:Icon

    def __init__(self, position:Point) -> None:
        self.__hasMine = False
        self.__hasFlag = False
        self.__isOpened = False
        self.__number = 0
        self.__position = position
        self.__icon = Icon.NOTOPENED

    # funkce vrati informaci, zda policko ma v sobe minu
    def getHasMine(self) -> bool:
        return self.__hasMine
    
    # funkce vrati informaci, zda policko je oznacen vlajkou
    def getHasFlag(self) -> bool:
        return self.__hasFlag
    
    # funkce vrati informaci, zda policko bylo otevreno
    def getIsOpened(self) -> bool:
        return self.__isOpened
    
    # funkce vrati aktulni pocet min, ktere se nachazi okolo policka
    def getNumber(self) -> int:
        return self.__number
    
    # funkce vrati aktualni pozici policka
    def getPosition(self) -> Point:
        return self.__position
    
    # funkce vrati aktualni ikonku policka
    def getIcon(self) -> Icon:
        return self.__icon
    
    # metoda nastavi, zda policko obsahuje minu
    def sethasMine(self, hasMine:bool) -> None:
        self.__hasMine = hasMine
    
    # metoda nastavi, zda policko je oznacene vlajkou
    def setHasFlag(self, hasFlag:bool) -> None:
        self.__hasFlag = hasFlag
    
    # metoda nastavi, zda policko je otevrene
    def setIsOpened(self, isOpened:bool) -> None:
        self.__isOpened = isOpened
    
    # metoda nastavi pocet min v okoli policka
    def setNumber(self, newNumber:int) -> None:
        self.__number = newNumber
    
    # metoda nastavi novou aktualni pozici policka
    def setPosition(self, newPosition:Point) -> None:
        self.__position = newPosition   

    # metoda nastavi novou ikonku policka
    def setIcon(self, newIcon:Icon) -> None:
        self.__icon = newIcon

# trida reprezentujici desku
class Board():

    # velikost desky
    __sizeX:int
    __sizeY:int
    # kolik jiz bylo otevrenych policek na desce
    __countOpened:int
    # kolik se nachazi min na desce
    __countMine:int
    # seznam vsech policek
    __listSquares:list[Square]

    def __init__(self, sizeX:int, sizeY:int) -> None:
        self.__sizeX = sizeX
        self.__sizeY = sizeY
        self.__countOpened = 0
        self.__listSquares = []

    # funkce vrati aktualni delku desky
    def getSizeX(self) -> int:
        return self.__sizeX
    
    # funkce vrati aktualni vysku desky 
    def getSizeY(self) -> int:
        return self.__sizeY
    
    # funkce vrati aktualni velikost desky
    def getSizeBoard(self) -> int:
        return self.__sizeX*self.__sizeY
    
    # funkce vrati aktualni pocet otevrenych policek
    def getCountOpened(self) -> int:
        return self.__countOpened
    
    # funkce vrati aktualni pocet min, ktere nachazi na desce
    def getCountMine(self) -> int:
        return self.__countMine

    # funkce vrati seznam vsech policek na desce
    def getListSquares(self) -> list[Square]:
        return self.__listSquares

    # funkce vrati vybrane policko ze seznamu vsech policek na desce
    def getSquare(self, index:int) -> Square:
        return self.getListSquares()[index]

    # metoda nastavi novy aktualni pocet otevrenych policek
    def setCountOpened(self, newCountOpened:int) -> None:
        self.__countOpened = newCountOpened
    
    # metoda nastavi novy aktualni pocet min, ktere se nachazeji na desce
    def setCountMine(self, newCountMine:int) -> int:
        self.__countMine = newCountMine

    # metoda vytvori novou prazdnou desku bez policek
    def createEmptyBoard(self) -> None:

        # ziskej referenci desky 
        board = self.getListSquares()

        # postupne pridavej policka az do maximalni velikosti desky
        for i in range(0, self.getSizeY()):
            for j in range(0, self.getSizeX()):
                board.append(Square(Point(j,i)))

    # funkce vrati seznam sousedu, ktere se nachazeji blizkosti policka
    def getNeighbours(self, square:Square) -> list[Square]:
        
        # ziskej referenci pozice policka
        x = square.getPosition().getX()
        y = square.getPosition().getY()

        # seznam pro postupnemu pridavani sousedu
        listSquares:list[Square] = []
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                
                # vyber policko vzdalene o nejakou pozici u vybraneho policka
                indexX = x + i
                indexY = y + j

                # ignoruj policka, ktere jsou mimo desky
                if indexX > -1 and indexX < self.getSizeX():
                    if indexY > -1 and indexY < self.getSizeY():
                        # pridej sousedni policka, ktere v sobe nemaji oznacenou vlajku
                        square:Square = self.getSquare(indexY*self.getSizeX() + indexX)
                        if square.getHasFlag() == False:
                            listSquares.append(square)
        
        # vrat seznam sousedu u vybraneho policka
        return listSquares
    
    # metoda zvysi vsem sousedum hodnotu policka, ze v okoli byla nasazena nova mina
    def addNeighboursNumber(self, square:Square) -> None:

        # ziskej referenci seznamu policek
        squares:list[Square] = self.getNeighbours(square)

        # postupne zvetsi hodnotu policka o +1
        for i in range(0, squares.__len__()):
            squares[i].setNumber(squares[i].getNumber() + 1)
    
    # metoda otevre vybrane policko na desce
    def openSquare(self, square:Square) -> None:

        # zkontroluj, zda policko ma minu
        if square.getHasMine() == True:
            # Nastav novou ikonku z neotvreneho policka na minu
            square.setIcon(Icon.MINE)
            square.setIsOpened(True)
        else: 
            # Nastav, ze dane policko je otevrene
            square.setIsOpened(True)
            # Nastav novou ikonku z neotvreneho policka na cislo 
            square.setIcon(Icon.NUMBER)
            # Nastav novou hodnotu, ze se otevrela nove policko
            self.setCountOpened(self.getCountOpened() + 1)
            # Otevri i sve sousedy
            self.openOthers(square)

    # metoda otevre policka, ktere sousedi s vybranym polickem
    def openOthers(self, square:Square) -> None:

        # zkontroluj, zda policko ma v okoli minu, pokud ano, zadne sousedy neotvirej
        if square.getNumber() > 0:
            square.setIsOpened(True)
            square.setIcon(Icon.NUMBER)
            return

        # algoritmus BFS
        queue = [ square ]
        history = []

        while queue:
            square = queue.pop()

            if not history.__contains__(square):
                history.append(square)

                squareList:list[Square] = self.getNeighbours(square)

                for i in range(0, squareList.__len__()):
                    
                    # zkontroluj, zda sousedni policko nema v okoli minu - pridej toto policko do fronty pro dalsi otevirani policku
                    if squareList[i].getNumber() == 0 and squareList[i].getIsOpened() == False:
                        squareList[i].setIsOpened(True)
                        squareList[i].setIcon(Icon.NUMBER)
                        self.setCountOpened(self.getCountOpened() + 1)
                        queue.append(squareList[i])
                    
                    # zkontroluj, zda sousedni policko hranici s nejakou minou - otevri ji a nehledej pro toto policko dalsi sousedy
                    if squareList[i].getIsOpened() == False:
                        squareList[i].setIsOpened(True)
                        squareList[i].setIcon(Icon.NUMBER)
                        self.setCountOpened(self.getCountOpened() + 1)
    
    # metoda vymaze vsechny policka, nastavi inicialni hodnoty, ktere byly predtim nastavene
    def reset(self) -> None:
        self.getListSquares().clear()
        self.setCountOpened(0)
        self.createEmptyBoard()

# trida reprezentujici generator min do desky
class MinesGenerator():

    # metoda pro vybranou desku nasazi podle pocet min do nahodnych policek minu
    def sampleMines(self, countMine:int, board:Board) -> None:
        
        # nastav aktualni pocet min pro vybranou desku
        board.setCountMine(countMine)

        # postupne pridavej miny do desky
        while countMine >= 1:
            
            # vyber nahodne policko z desky
            randomSquare:Square = random.choice(board.getListSquares())

            # zkontroluj, zda policko je volne - pokud ne, najdi nove volne policko
            if randomSquare.getHasMine() == False:
                randomSquare.sethasMine(True)
                board.addNeighboursNumber(randomSquare)
                countMine -= 1

# trida reprezentujici hru min
class MinesGameClass(AbstractGameClass):
    
    # hra skoncila nebo ne
    __gameOver:bool = False
    # zda hrac se hrat znovu
    __playAgain:bool = True
    # deska, na ktere hrac hraje
    __board:Board

    # metoda zapne hru a vybere specifikaci pro hru
    def start(self) -> None:
        self.__playAgain = True
        print("Would you like to use default settings for mines? (y/n)")
        
        # vyber urcitou specifikaci desky
        self.loadSpec()
        
        input("Press ENTER to play!")

        # hraje hru
        while self.__playAgain == True:
            self.game()
            self.playAgain()
    
    # metoda prubezne aktualizuje desku
    def game(self) -> None:
        
        # vyrenderuj vygenerovanou desku
        self.renderBoard()

        # prubezne aktualizuj a renderuj desku. 
        while self.__gameOver == False:
            
            # ziskej infomarci, jake tlacitko bylo kliknuto a jake policko bylo vybrane
            command = self.getCommand()

            # aplikuj leve a prave tlacitko na vybrane policko
            if command[1] == "r":
                self.rightClick(command[0])
            else:
                self.leftClick(command[0])

            self.renderBoard()

            # zkontroluj vysledek tlacitka
            self.checkGame(command[0])

    # funkce vrati vybrane policko a jaky druh tlacitka byl pouzit
    def getCommand(self) -> Square:
        
        # hlidej spravnej format vyberu policka a tlacitka
        while True:
            try:
                x, y, click = input().split()
                x = int(x)
                y = int(y)

                # zkontroluj, zda x hodnota neni mimo desky 
                if x < 0 or x >= self.__board.getSizeBoard():
                    raise Exception 
                
                # zkontroluj, zda y hodnota neni mimo desky 
                if y < 0 or y >= self.__board.getSizeBoard():
                    raise Exception 
                
                # zkontroluj, zda je to spravny druh tlacitka
                if click not in ['r', 'l']:
                    raise Exception
                
                # vrat uvedeny format prikazu 
                return [self.__board.getSquare(y*self.__board.getSizeX() + x), click]
            except:
                print("Invalid command, again! command format: (X position, Y position, (r/l click)) Example: 1 1 l")

    # metoda nastavi/odstrani vlajecku na vybranem policku
    def rightClick(self, square:Square) -> None:
        
        if square.getIsOpened() == True:
            print("The square was already opened!")
            return

        if square.getHasFlag() == True:
            square.setHasFlag(False)
            square.setIcon(Icon.NOTOPENED)
        else:
            square.setHasFlag(True)
            square.setIcon(Icon.FLAG)

    # metoda otevre vybrane policko
    def leftClick(self, square:Square) -> None:
        
        # zkontroluj, zda policko nema vlajecku a zaroven neni otevrena
        if square.getHasFlag() == False and square.getIsOpened() == False:
            self.__board.openSquare(square)
        elif square.getIsOpened() == True:
            print("This square is already opened!")
        else:  
            print("You cant open flagged square!")

    # funkce vrati jmeno hry
    def getGameName(self) -> str:
        return "Mine"
    
    # metoda nastavi specifikaci desky
    def loadSpec(self) -> None:
        
        # hrace se pta tak dlouho, dokud nedostane svoji odpoved pro druh vyberu specifikace - y/n
        while True:
            choice = input().lower()        
            if choice == "y":
                self.defaultMine()
                break
            elif choice == "n":
                self.customMine()
                break
            else:
                print("Wrong choices, again! (y/n)")

    # metoda nacte zakladni specifikaci desky
    def defaultMine(self) -> None:
        self.__board = Board(10, 10)
        self.__board.createEmptyBoard()
        mineGenerator = MinesGenerator()
        mineGenerator.sampleMines(20, self.__board)

    # metoda vytvari specifikaci podle vyberu hrace
    def customMine(self) -> None:
        print("Please enter the parameters for the mines board settings (X size,Y size, Count mine):")

        while True:
            try:
                x, y, count = input().split()
                x = int(x)
                y = int(y)
                count = int(count)

                if x*y < count:
                    raise Exception

                self.__board = Board(x, y)
                self.__board.createEmptyBoard()
                mineGenerator = MinesGenerator()
                mineGenerator.sampleMines(count, self.__board)
                break
            except:
                print("Invalid format, again! format: (X size,Y size, Count mine) Example: 10 10 10")


    # metoda vyrenderuje do konzole aktualni stav desky
    def renderBoard(self) -> None:
        
        print(f"\nOpened Squares: {self.__board.getCountOpened()}", end=" ")
        print("\n     \n", end="    ")

        for i in range(self.__board.getSizeX()):
            print(f"{i:<2}", end=" ")
        print("\n")

        # pro kazde policko vyrenderuj do konzole aktualni ikonku
        for i in range(self.__board.getSizeY()):
            print(f"{i:<3}", end=" ")
            for j in range(self.__board.getSizeX()):
                if self.__board.getSquare(i*self.__board.getSizeX() + j).getIcon() == Icon.NUMBER:
                    print(self.__board.getSquare(i*self.__board.getSizeX() + j).getNumber(), end="  ")
                else:
                    print(self.__board.getSquare(i*self.__board.getSizeX() + j).getIcon().value, end="  ")
            print()
        print()

    # metoda kontroluje, zda hrac vyhral nebo prohral hru
    def checkGame(self, square:Square) -> None:
        
        # zkontroluj, zda vybrane policko se nenachazela mina
        if square.getHasMine() == True and square.getIsOpened() == True:
            print("You Lose")
            self.__gameOver = True

        # maximalni pocet, kolik muze dohromady hrac otevrit policek
        maxCount = self.__board.getSizeBoard() - self.__board.getCountMine()

        # zkontroluj, zda hrac neotevrel vsechny bezpecne policka
        if maxCount == self.__board.getCountOpened():
            print("You Win")
            self.__gameOver = True

    # metoda se zepta hrace, zda chce hrat znovu na stejne desce
    def playAgain(self) -> None:
        
        print("Wanna play the mines again? (y/n)")
        
        # hrace se pta tak dlouho, dokud nedostane svoji odpoved, jestli chce hrat znovu nebo ne - y/n
        while True:
            choice = input().lower()
           
            if choice == "y":
                self.__board.reset()
                mineGenerator = MinesGenerator()
                mineGenerator.sampleMines(self.__board.getCountMine(), self.__board)
                print(self.__board.getCountMine())
                break
            elif choice == "n":
                self.__playAgain = False
                break
            else:
                print("Wrong choices, again! (y/n)")

        self.__gameOver = False
