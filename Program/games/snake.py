import msvcrt
import time
import os
import random
from enum import Enum

from AbstractGameClass import AbstractGameClass

# enum pro reprezentaci pohybu hada
class Movement(Enum):
    UP = "W"
    LEFT = "A"
    DOWN = "S"
    RIGHT = "D"

# trida reprezentujici hrace 
class Player:
    
    # celkovy skore hrace
    __score:int

    def __init__(self, initScore:int) -> None:
        self.__score = initScore

    # funkce vrati aktualni skore
    def getScore(self) -> int:
        return self.__score
        
    # metoda nastavi novy aktualni skore
    def setScore(self, newScore:int) -> None:
        self.__score = newScore

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

# trida reprezentujici jidlo pro hada 
class Fruit:
    
    # hodnota jidla po sezrani
    __foodValue:int
    # aktualni hodnota jidla na nejake pozici
    __position:Point

    def __init__(self, foodValue:int) -> None:
        self.__foodValue = foodValue
        self.__position = Point(0,0)

    # funkce vrati aktualni hodnotu jidla
    def getFoodValue(self) -> int:
        return self.__foodValue
    
    # funkce vrati aktualni pozici jidla 
    def getPosition(self) -> Point:
        return self.__position

    # metoda nastavi novou aktualni hodnotu jidla
    def setFoodValue(self, newFoodValue:int) -> None:
        self.__foodValue = newFoodValue
    
    # metoda nastavi novou aktualni pozici jidla
    def setPosition(self, newPosition:Point) -> None:
        self.__position = Point(newPosition.getX(), newPosition.getY())

# trida reprezentujici hada
class Snake:
    
    # velikost aktualniho hada
    __bodyCount:int
    # zda had sezral nejake jidlo
    __hasEaten:bool = False
    # zda had je zivy
    __isAlive:bool = True
    # seznam tel hada
    __bodyList:list[Point]

    def __init__(self, bodyCount:int) -> None:
        self.__bodyCount = bodyCount
        self.__bodyList = []

    # funkce vrati aktualni pocet tel
    def getBodyCount(self) -> int:
        return self.__bodyCount
    
    # funkce vrati, zda had sezral nejake jidlo
    def getHasEaten(self) -> bool:
        return self.__hasEaten

    # funkce vrati, zda had je zivy
    def getIsAlive(self) -> bool:
        return self.__isAlive

    # funkce vrati seznam tel hada
    def getBodyList(self) -> list[Point]:
        return self.__bodyList
    
    # metoda nastavi novy aktualni pocet tel
    def setBodyCount(self, newBodyCount:int) -> None:
        self.__bodyCount = newBodyCount

    # metoda nastavi, zda had sezral nejake jidlo
    def setHasEaten(self, hasEaten:bool) -> None:
        self.__hasEaten = hasEaten
    
    # metoda nastavi, zda had je zivy
    def setIsAlive(self, isAlive:bool) -> None:
        self.__isAlive = isAlive

    # metoda prida novou cast tela hadovi
    def addNewBody(self, newBody:Point) -> None:
        self.getBodyList().append(newBody)

    # metoda nastavi novy smer hada - nahoru, dolu, doleva, doprava
    def setMove(self, newPosition:Point) -> None:
        
        # ziskej referenci hada
        bodyList = self.getBodyList()
        bodyCount = self.getBodyCount()
        headPosition = bodyList[0]

        # uloz si predchozi pozici hlavy hada
        oldPoint = Point(headPosition.getX(), headPosition.getY())

        # nastav hlavu hada na novou pozici
        headPosition.setX(newPosition.getX())
        headPosition.setY(newPosition.getY())

        # nastav novou pozici pro prvni cast tela
        newPoint = Point(oldPoint.getX(), oldPoint.getY())

        # postupne nastav casti tela na nove pozice
        for i in range(1, bodyCount + 1):

            oldPoint = Point(bodyList[i].getX(), bodyList[i].getY())

            bodyList[i].setX(newPoint.getX())
            bodyList[i].setY(newPoint.getY())
            
            newPoint = Point(oldPoint.getX(), oldPoint.getY())

        # kontrola, zda had sezral jidlo
        if self.getHasEaten()  == True:
            self.setHasEaten(False)
            self.addNewBody(Point(oldPoint.getX(), oldPoint.getY()))
            self.setBodyCount(bodyCount + 1)

# trida reprezentujici desky 
class Board:
    
    # velikost desky
    __sizeX:int
    __sizeY:int

    # aktualni pocet jidel na desce a jejich pozice
    __fruitCount:int
    __activeFruitList:list[Fruit]
    
    # aktualni had na desce
    __activeSnake:Snake

    # aktualni hrac, ktery vyuziva desku
    __player:Player

    def __init__(self, sizeX:int, sizeY:int, activeSnake:Snake, activeFruitList:list[Fruit], player) -> None:
        self.__sizeX = sizeX
        self.__sizeY = sizeY
        self.__activeSnake = activeSnake
        self.__activeFruitList = activeFruitList
        self.__fruitCount = activeFruitList.__len__()
        self.__player = player
    
    # funkce vrati aktualni delku desky
    def getSizeX(self) -> int:
        return self.__sizeX
    
    # funkce vrati aktualni vysku desky
    def getSizeY(self) -> int:
        return self.__sizeY
    
    # funkce vrati celkovou velikost desky
    def getSizeBoard(self) -> int:
        return self.__sizeX*self.__sizeY
    
    # funkce vrati aktualni pocet jidel na desce
    def getFruitCount(self) -> int:
        return self.__fruitCount
    
    # funkce vrati aktualni seznam pozic jidel na desce
    def getActiveFruitList(self) -> list[Fruit]:
        return self.__activeFruitList

    # funkce vrati aktualniho hada na desce
    def getActiveSnake(self) -> Snake:
        return self.__activeSnake
    
    def getPlayer(self) -> Player:
        return self.__player

    # funkce ziska volne policko na desce
    def getRandomAvailablePosition(self) -> Point:
        
        # zkus nahodne vybrat volne policko
        while True:
            
            # vyber nahodnou pozici x, y
            x = random.randint(0, self.getSizeX() - 1)
            y = random.randint(0, self.getSizeY() - 1)

            # zda je policko volne
            isFreePosition = True

            # zkontroluj, zda pozice neobsahuje cast tela hada
            for body in self.getActiveSnake().getBodyList():              
                
                if body.getX() == x and body.getY() == y:
                    isFreePosition = False
                    break
            
            # zkontroluj, zda pozice neobsahuje jidlo
            for fruit in self.getActiveFruitList():
                if fruit.getPosition().getX() == x and fruit.getPosition().getY() == y:
                    isFreePosition = False
                    break
            
            # overeni, zda je policko volne
            if isFreePosition == True:
                return Point(x, y)


    # metoda nastavi novy aktualni pocet jidel na desce
    def setFruitCount(self, newFruitCount:int) -> None:
        self.__fruitCount = newFruitCount

    # metoda odstrani jidlo z desky
    def removeFruit(self, removeFruit:Point) -> None:

        # ziskej aktualni pocet jidel
        fruitCount = self.getFruitCount()

        # kontrola, zda se muze odstranit jidlo
        if fruitCount > 0:
            self.getActiveFruitList().remove(removeFruit)
            self.setFruitCount(fruitCount - 1)

    # metoda vytvori zakladni telo hada podle specifikace
    def createSnakeBody(self) -> None:
        
        # ziskej aktualni seznam tela hada
        snakeBodyList = self.getActiveSnake().getBodyList()

        # ziskej pozici uprostred desky
        centerBoardPoint = Point(int(self.getSizeX() / 2 - 1), int(self.getSizeY() / 2 - 1))

        # pridej hlavicku hada uprostred desky
        snakeBodyList.append(centerBoardPoint)

        # pridavej postupne nove casti tela hadovi
        for i in range(1, self.getActiveSnake().getBodyCount() + 1):
            
            # sniz pozici o jedno doleva
            positionX = centerBoardPoint.getX() - i
            positionY = centerBoardPoint.getY() 
            
            # pridej novou cast na dane policko
            snakeBodyList.append(Point(positionX, positionY))
        
    # metoda vygeneruje jidla do desky
    def generateFruits(self) -> None:
        
        # pro kazde jidlo vyber dostupne policko a vloz tam jidlo
        for fruit in self.getActiveFruitList():
            point = self.getRandomAvailablePosition()
            fruit.setPosition(Point(point.getX(), point.getY()))

    # metoda zkontroluje, zda had do neceho nenaboural
    def checkColision(self) -> None:
        
        # ziskej reference hada a seznam jidel
        headSnake = self.getActiveSnake().getBodyList()[0]
        bodySnake = self.getActiveSnake().getBodyList()[1:]
        fruitList = self.getActiveFruitList()
        
        # ziskej referenci velikosti desky
        wallX = self.getSizeX()
        wallY = self.getSizeY()

        # zkontroluj, zda had je mimo desky v pozici x
        if headSnake.getX() < 0 or headSnake.getX() >= wallX:
            self.getActiveSnake().setIsAlive(False)
        
        # zkontroluj, zda had je mimo desky v pozici y
        if headSnake.getY() < 0 or headSnake.getY() >= wallY:            
            self.getActiveSnake().setIsAlive(False)

        # zkontroluj, zda nenarazil na jidlo
        for fruit in fruitList:
            if headSnake.getX() == fruit.getPosition().getX() and headSnake.getY() == fruit.getPosition().getY():
                
                # zkontroluj, zda had neni dost velky, ze se jiz nevejde nove jidlo
                if self.getActiveSnake().getBodyCount() + self.getFruitCount() + 1 > self.getSizeBoard():
                    self.removeFruit(fruit)
                    self.getPlayer().setScore(self.getPlayer().getScore() + fruit.getFoodValue())
                    self.getActiveSnake().setHasEaten(True)
                else:
                    point = self.getRandomAvailablePosition()
                    fruit.getPosition().setX(point.getX())
                    fruit.getPosition().setY(point.getY())
                    self.getPlayer().setScore(self.getPlayer().getScore() + fruit.getFoodValue())
                    self.getActiveSnake().setHasEaten(True)

        # zkontroluj, zda had nenaboural do sebe
        for body in bodySnake:
            if body.getX() == headSnake.getX() and body.getY() == headSnake.getY():
                self.getActiveSnake().setIsAlive(False)

# trida reprezentujici hru - sprava hry 
class SnakeGameClass(AbstractGameClass):
    
    # deska, na ktere hrac hraje
    __board:Board
    # aktivni/neaktivni
    __gameStatus:bool = True

    # metoda zapne hru a vybere specifikaci pro hru
    def start(self) -> None:
        
        input("Press ENTER to play!")

        # nacti zakladni specifikaci hry
        self.loadInitSpec()

        # hraje hru
        while self.__gameStatus == True:

            self.game()
            self.playAgain()

    # funkce vrati jmeno hry
    def getGameName(self) -> str:
        return "Snake"
    
    # metoda se zepta, zda se ma hrat znova
    def playAgain(self) -> None:
        
        print("\nGAME OVER! \nWANNA PLAY AGAIN? (y/n)")

        # hrace se pta tak dlouho, dokud nedostane svoji odpoved - y/n
        while True:
            choice = input().lower()

            if choice == "y":
                self.loadInitSpec()                
                break
            elif choice == "n":
                self.__gameStatus = False
                break
            else:
                print("Wrong choice, again! (y/n)")

    # metoda nacte zakladni specifikaci hry
    def loadInitSpec(self) -> None:

        self.__gameStatus = True

        snake = Snake(3)
        
        commonFruit = Fruit(1)
        rareFruit = Fruit(2)
        luxuryFruit = Fruit(4)
        player = Player(0)
        self.__board = Board(10, 10, snake, [commonFruit, rareFruit, luxuryFruit], player)
        
        # vytvor hada na desku
        self.__board.createSnakeBody()
        # vytvor jidla do desky
        self.__board.generateFruits()

    # metoda prubezne aktualizuje desku a hrace
    def game(self) -> None:
        
        # nastav pocatecni smer hada
        direction = Movement.RIGHT

        # hra bezi tak dlouho, dokud je nazivu had
        while self.__board.getActiveSnake().getIsAlive() == True:
            
            # uklid predchozi render
            self.clearScreen()

            # ziskej aktualni smer hada
            direction = self.getDirection(direction)

            # aplikuj pohyb hada podle smeru
            self.setNewMove(direction)

            # zkontroluj stav hada, zda do neceho nenaboural
            self.__board.checkColision()
            
            # vyrenderuj desku, hada a jidla
            self.renderBoard()

            # zpomal hru
            time.sleep(0.1)

    # funkce vrati aktualni smer
    def getDirection(self, actualDirection:Movement) -> Movement:
        try: 
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 'w' and actualDirection != Movement.DOWN:
                    return Movement.UP
                elif key == 's' and actualDirection != Movement.UP:
                    return Movement.DOWN
                elif key == 'a' and actualDirection != Movement.RIGHT:
                    return Movement.LEFT
                elif key == 'd' and actualDirection != Movement.LEFT:
                    return Movement.RIGHT
        except:
            pass
        
        return actualDirection 

    # metoda uklidi konzoli
    def clearScreen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # metoda nastavi novy smer
    def setNewMove(self, newDirection:Movement) -> None:
        
        # ziskej referenci hlavy hada
        snakeHeadPosition = self.__board.getActiveSnake().getBodyList()[0]
        
        # aplikuj pohyb hada podle smeru
        if newDirection == Movement.UP:
            self.__board.getActiveSnake().setMove(Point(snakeHeadPosition.getX(), snakeHeadPosition.getY() - 1))
        elif newDirection ==  Movement.DOWN:
            self.__board.getActiveSnake().setMove(Point(snakeHeadPosition.getX(), snakeHeadPosition.getY() + 1))
        elif newDirection == Movement.LEFT:
            self.__board.getActiveSnake().setMove(Point(snakeHeadPosition.getX() - 1, snakeHeadPosition.getY()))
        elif newDirection == Movement.RIGHT:
            self.__board.getActiveSnake().setMove(Point(snakeHeadPosition.getX() + 1, snakeHeadPosition.getY()))
            
    # metoda vyrenderuje desku, hada a jidla
    def renderBoard(self) -> None:
        
        print(f"Skore: {self.__board.getPlayer().getScore()}")
        print("■ " * (self.__board.getSizeX() + 2))

        # ziskej referenci hada a seznam jidel
        bodyList = self.__board.getActiveSnake().getBodyList()
        fruitList = self.__board.getActiveFruitList()

        # postupne vyrenderuj desku        
        for y in range(0, self.__board.getSizeY()):
            print("■", end="")

            for x in range(0, self.__board.getSizeX()):
                
                # zda byla jiz vyrenderovana policko
                foundIcon = False
                
                # zkontroluj, zda na dane policku lezi cast tela
                for body in bodyList[1:]:
                    if body.getX() == x and body.getY() == y:
                        print(" U", end="")
                        foundIcon = True
                        break
                
                # zkontroluj, zda na dane policku lezi hlava hada
                if foundIcon == False and bodyList[0].getX() == x and bodyList[0].getY() == y:
                    print(" X", end="")   
                    foundIcon = True

                # zkontroluj, zda na dane policku lezi jidlo
                for fruit in fruitList:
                    if fruit.getPosition().getX() == x and fruit.getPosition().getY() == y:
                        print(" F", end="")   
                        foundIcon = True
                        break
                
                # zkontroluj, zda neco nebylo vyrenderovano    
                if foundIcon == False:
                    print("  ", end="")
            
            print(" ■")
        print("■ " * (self.__board.getSizeX() + 2))
