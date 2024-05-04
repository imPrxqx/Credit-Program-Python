import random

from AbstractGameClass import AbstractGameClass

# trida reprezentujici stenu kostky 
class Side():

    # jmeno kostky
    __name:str
    # ikonka kostky
    __icon:str
    # sance padnuti strany
    __probability:float

    def __init__(self, name:str, icon:str, probability:float) -> None:
        self.__name = name
        self.__icon = icon
        self.__probability = probability
    
    # funkce vrati aktualni jmeno strany kostky
    def getName(self) -> str:
        return self.__name

    # funkce vrati aktualni ikonku strany kostky
    def getIcon(self) -> str:
        return self.__icon
    
    # funkce vrati aktualni sanci padnuti strany kostky
    def getProbability(self) -> int:
        return self.__probability

# trida reprezentujici kostku    
class Dice():

    # seznam stran kostky
    __sideList:list[Side]
    # aktualni strana kostky
    __currentSide:Side

    def __init__(self) -> None:
        self.__sideList = []
        self.__currentSide = None

    # funkce vrati aktualni seznam stran kostky
    def getSideList(self) -> list[Side]:
        return self.__sideList

    # funkce vrati aktualni stranu kostky
    def getCurrentSide(self) -> Side:
        return self.__currentSide
    
    # metoda nastavi novou aktualni stranu kostky
    def setCurrentSide(self, newCurrentSide:Side) -> None:
        self.__currentSide = newCurrentSide

    # metoda prida novou stranu do seznamu stran kostky 
    def addNewSide(self, newSide:Side) -> None:
        self.getSideList().append(newSide)
    
    # metoda hodi kostku a ziska padnutou stranu
    def rollDice(self) -> None:
        
        totalProbability = sum(side.getProbability() for side in self.getSideList())
        randomNumb = random.uniform(0, totalProbability)
        cumulativeProb = 0

        for side in self.getSideList():
            cumulativeProb += side.getProbability()
            if randomNumb < cumulativeProb:
                self.setCurrentSide(side)
                return

# trida reprezentujici hru  
class UniversalDiceGame(AbstractGameClass):

    # aktualne ulozena kostka
    __dice:Dice
    # haze se nebo ne
    __rollAgain:bool = True
   
    # metoda zapne hru a vybere specifikaci kostky pro hru
    def start(self) -> None:

        self.__rollAgain = True
        self.__dice = Dice()

        print("Would you like to use default settings for dice? (y/n)")
        
        # moznost nastaveni kostky podle sebe nebo predem nastavene hodnoty
        while True:
            choice = input().lower()
           
            if choice == "y":
                self.defaultDice()
                break
            elif choice == "n":
                self.customDice()
                break
            else:
                print("Wrong choices, again! (y/n)")
        
        input("Press ENTER to play!")

        # haze se kostka
        while self.__rollAgain == True:
            self.game()
            self.playAgain()
    
    # metoda nastavi aktualni kostku podle predem nastavenych hodnot
    def defaultDice(self) -> None:
        for i in range(1,7):
            self.__dice.addNewSide(Side(i, i, 1/6))

    # metoda nastavi aktualni kostku podle svych hodnot
    def customDice(self) -> None:
        
        print("Please enter the parameters for the universal settings:")
        print("Enter the number of sides on the dice:") 

        # nastaveni kolik bude mit kostka stran
        while True:
            try:
                countSide = int(input())

                if countSide <= 0:
                    raise Exception 

                break
            except:
                print("Invalid Number, again!")

        print("Please enter the parameters this format: (name:string icon:string probality:float) example: '1 1 0.5':")
        
        # pro kazdou stranu kostky se nastavi hodnoty
        for i in range(0, countSide):
                
            while True:
                side = input()
                side = side.split(' ')

                try: 
                    if len(side) != 3:
                        raise Exception
                        
                    name = str(side[0])
                    icon = str(side[1])     
                    probability = float(side[2])
                    
                    if probability < 0 or probability > 1:
                        raise Exception

                    self.__dice.addNewSide(Side(name, icon, probability))
                    break
                except:
                    print("Invalid format, again! (name:string icon:string probality:float) example: '1 1 0.5'")

    # metoda haze kostku a ziska hozenou stranu kostky
    def game(self) -> None:
        self.__dice.rollDice()
        print(f"Name: {self.__dice.getCurrentSide().getName()} Icon: {self.__dice.getCurrentSide().getIcon()} Probability: {self.__dice.getCurrentSide().getProbability()}")
    
    # metoda zepta hrace, zda chce hazet znovu nebo ne
    def playAgain(self) -> None:
        
        print("Wanna roll the dice again? (y/n)")

        while True:
            choice = input().lower()
           
            if choice == "y":
                break
            elif choice == "n":
                self.__rollAgain = False
                break
            else:
                print("Wrong choices, again! (y/n)")

    # funkce vrati jmeno hry
    def getGameName(self) -> str:
        return "Universal Dice"