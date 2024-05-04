import random
from enum import Enum
from AbstractGameClass import AbstractGameClass

# enum pro reprezentaci zbrani
class Weapons(Enum):
    NONE = []
    ROCK = [ "SCISSORS" ]
    PAPER = ["ROCK" ]
    SCISSORS = [ "PAPER" ]
    # BANAN = [ "SCISSORS", "PAPER", "ROCK" ] # ukazka pridani dalsi zbrane

# enum pro reprezentaci vysledku dvou hracu
class Results(Enum):
    TIE = "TIE"
    PLAYERONEWIN = "PLAYERONEWIN"
    PLAYERTWOWIN = "PLAYERTWOWIN"

# trida reprezentujici hrace
class Player:

    # kolikrat vyhral ve hre hrac
    __score:int
    # jmeno hrace
    __name:str
    # je Ai nebo ne
    __isAi:bool
    # vybrana zbran hrace
    __selectedWeapon:Weapons

    def __init__(self, score:int, name:str, isAi:bool=False) -> None:
        self.__score = score
        self.__name = name
        self.__isAi = isAi
        self.__selectedWeapon = Weapons.NONE
    
    # funkce vrati aktualni skore hrace
    def getPlayerScore(self) -> int:
        return self.__score

    # funkce vrati aktualni jmeno hrace
    def getPlayerName(self) -> str:
        return self.__name

    # funkce vrati aktualni mod hrace
    def getPlayerMode(self) -> bool:
        return self.__isAi
    
    # funkce vrati aktualne vybranou zbran hrace
    def getPlayerSelectedWeapon(self) -> Weapons:
        return self.__selectedWeapon

    # metoda nastavi skore na novou hodnotu
    def setPlayerScore(self, newScore:int) -> None:
        self.__score = newScore

    # metoda nastavi jmeno hrace na nove jmeno
    def setPlayerName(self, newName:str) -> None:
        self.__name = newName
    
    # metoda nastavi mod hrace na ai/hrac
    def setPlayerMode(self, isAi:bool) -> None:
        self.__isAi = isAi

    # metoda nastavi vybranou zbran na novou aktualni zbran
    def setPlayerSelectedWeapon(self, newWeapon:Weapons) -> None:
        self.__selectedWeapon = newWeapon

# trida reprezentujici mistnost, kde hraji hraci
class RoomGame:

    # hraci, kteri se nachazi v teto mistnosti
    __playerList:list[Player]
    # seznam zbrani, ktere hraci mohou hrat
    __weaponList:list[Weapons]
    # aktualni hrac, ktery vybira zbran
    __playerTurn:Player

    def __init__(self, playerList:list[Player], weapons:list[Weapons]) -> None:
        self.__playerList = playerList
        self.__weaponList = weapons
        self.__playerTurn = playerList[0]

    # funkce vrati aktualni seznam hracu, kteri hraji
    def getPlayerList(self) -> list[Player]:
        return self.__playerList  
    
    # funkce vrati aktualni seznam zbrani, ktere lze hrat
    def getWeaponList(self) -> list[Weapons]:
        return self.__weaponList  
    
    # funkce vrati aktualniho hrace, ktery je na rade
    def getPlayerTurn(self) -> Player:
        return self.__playerTurn
    
    # funkce vrati nahodne vybranou zbran ze seznamu zbrani
    def getRandomWeapon(self) -> Weapons:
        return random.choice(self.getWeaponList())

    # funkce vrati vysledek dvou hracu, kdo vyhral na zaklade zbrani
    def whoDidWin(self, players:list[Player]) -> Results:

        # podivej se zda prvni hrac vyhral podle toho, jestli jeho zbran vyhrava proti druhemu hraci
        weaponListAdvantagesPlayerOne = self.isInWeaponAdvantagesList(players[0].getPlayerSelectedWeapon(), players[1].getPlayerSelectedWeapon())
        # podivej se zda druhy hrac vyhral podle toho, jestli jeho zbran vyhrava proti prvnimu hraci
        weaponListAdvantagesPlayerTwo = self.isInWeaponAdvantagesList(players[1].getPlayerSelectedWeapon(), players[0].getPlayerSelectedWeapon())
        
        print(f"Player: {players[0].getPlayerName()} Weapon: {players[0].getPlayerSelectedWeapon().name}")
        print("VS")
        print(f"Player: {players[1].getPlayerName()} Weapon: {players[1].getPlayerSelectedWeapon().name}")
        
        # nastav u obou hracu na nevybranou zbran
        players[0].setPlayerSelectedWeapon(Weapons.NONE)
        players[1].setPlayerSelectedWeapon(Weapons.NONE)

        # zkontroluj, kdo vyhral a vrat vysledek hry
        if(weaponListAdvantagesPlayerOne == True):
            return Results.PLAYERONEWIN
        elif(weaponListAdvantagesPlayerTwo == True):
            return Results.PLAYERTWOWIN
        else:
            return Results.TIE
    
    # funkce vrati, zda vybrana zbran ma ve seznamu vyhod uvnitr druhou zbran
    def isInWeaponAdvantagesList(self, weaponNamePlayerOne:Weapons, weaponNamePlayerTwo:Weapons) -> bool:
        # postupne zkontroluj, zda je uvnitr zbran nad kterou vyhrava
        for weapon in Weapons:
            if weaponNamePlayerOne == weapon:
                for advantages in weapon.value:
                    if weaponNamePlayerTwo.name == advantages:
                        return True
                return False
        return False

    # metoda zmeni poradi hracu pro vyber zbrani
    def changeTurn(self) -> None:
        
        if self.__playerTurn == self.getPlayerList()[0]:
            self.__playerTurn = self.getPlayerList()[1]
        elif self.__playerTurn == self.getPlayerList()[1]:
            self.__playerTurn =  self.getPlayerList()[0]
    
    # metoda nastavi aktualniho hrace, ktery je ted na rade
    def setPlayerTurn(self, playerTurn:Player) -> None:
        self.__playerTurn = playerTurn
    
    # metoda prida hraci skore +1
    def addScore(self, player:Player) -> None:
        player.setPlayerScore(player.getPlayerScore() + 1)

# trida reprezentujici hru 
class RockScissorsPaperGameClass(AbstractGameClass):
    
    # mistnost, ve kterem se hraje
    __game:RoomGame
    # zda hraci chteji hrat znovu hru
    __playAgain:bool = True

    # metoda zapne hru a vybere specifikaci pro hru
    def start(self) -> None:
        
        self.__playAgain = True
        # nacti specifikaci hracu
        self.loadSpec()
        
        input("Press ENTER to play!")

        print("----------------------------------------")
        
        while self.__playAgain == True:
            self.game()
            self.playAgain()

    # metoda nacte specifikace hracu      
    def loadSpec(self) -> None:
        
        # priprav si seznam hracu, kteri budou chtit hrat
        playerList:list[Player] = []
        print("Set player for this game:")
        
        # ziskej specifikace dvou hracu
        for i in range(0,2):
  
            while True:
                try:
                    # ziskej hodnoty z konzole
                    mode, score, name = input(f"Player {i} format: [ [y/n - Ai Mode] [int - Score] [str - Name] ]\n").split()
                    
                    # zkontroluj, zda hodnota patri do y nebo n, jinak hod vyjimku
                    if mode in {"y"}:
                        mode = True
                    elif mode in {"n"}:
                        mode = False
                    else: 
                        raise Exception
                    
                    score = int(score)
                    name = str(name)

                    # pridej nove vytvoreneho hrace
                    playerList.append(Player(score, name, mode))
                    break
                except:
                    print("Invalid format, again! Player format: [ [y/n - Ai Mode] [int - Score] [str - Name] ] Example True 0 Jan")

        # nacti za pomoci enum konfiguraci zbrani
        weapons = [weapon for weapon in Weapons if weapon != Weapons.NONE]
        # vytvor mistnost, kde budou hrat hraci s vybranym seznamem zbrani
        self.__game = RoomGame( playerList, weapons) 
    
    # metoda prubezne aktualizuje hru
    def game(self) -> None:
        
        # postupne ziskavej od vsech hracu vybranou zbran a pak na zaklade vybranych zbran vypis vysledek
        while True:
            # zkontroluj, zda nejaky hrac nema jeste vybranou zbran
            if(self.__game.getPlayerTurn().getPlayerSelectedWeapon() == Weapons.NONE):
                print(f"Player: {self.__game.getPlayerTurn().getPlayerName()} Turn!")
                # zkontroluj, zda se jedna o Ai nebo ne
                if(self.__game.getPlayerTurn().getPlayerMode() == True):
                    # Ai si nahodne vybere ze seznamu nejakou zbran
                    self.__game.getPlayerTurn().setPlayerSelectedWeapon(self.__game.getRandomWeapon())
                else:  
                    # hrac si vybere z konzole nejakou zbran, ktera se nachazi ve seznamu zbrani           
                    try:
                        print("Weapons List:", ', '.join(weapon.name for weapon in self.__game.getWeaponList()) + ".")
                        weapon = input()
                        # zkontroluj, ze si nevybral NONE, protoze patri take do seznamu zbrani
                        if (weapon != "NONE"):
                            self.__game.getPlayerTurn().setPlayerSelectedWeapon(Weapons[weapon])
                        else:
                            raise Exception
                    except:
                        print("Invalid weapons, again! Weapons List:", ', '.join(weapon.name for weapon in self.__game.getWeaponList()) + ".")
                        continue

                print(f"Player: {self.__game.getPlayerTurn().getPlayerName()} got weapon: {self.__game.getPlayerTurn().getPlayerSelectedWeapon().name}")
                # po vyberu zbrane zmen kolo hrace
                self.__game.changeTurn()
            else:
                # jakmile vsichni hraci si vybrali zbran, zkontroluj vysledek hry na zaklade vybranych zbrani
                print("----------------------------------------")
                # zkontroluj, kdo z hracu vyhral
                result = self.__game.whoDidWin(self.__game.getPlayerList())
                print("----------------------------------------")

                # na zaklade vysledku pripis skore vyhranemu hraci
                if(result == Results.PLAYERONEWIN):
                    self.__game.addScore(self.__game.getPlayerList()[0])
                    print(f"Player: {self.__game.getPlayerList()[0].getPlayerName()} WON!")
                elif(result == Results.PLAYERTWOWIN):
                    self.__game.addScore(self.__game.getPlayerList()[1])
                    print(f"Player: {self.__game.getPlayerList()[1].getPlayerName()} WON!")
                else:
                    print("Game was TIE!")

                print("----------------------------------------")
                print("Skore:")
                print(self.__game.getPlayerList()[0].getPlayerName(), self.__game.getPlayerList()[0].getPlayerScore())
                print(self.__game.getPlayerList()[1].getPlayerName(), self.__game.getPlayerList()[1].getPlayerScore())
                print("----------------------------------------")
                print("Would you like to play this game again? (y/n)")
                break

    # metoda se zepta hracu, zda chteji hrat znovu
    def playAgain(self) -> None:
        # ptej se tak dlouho, dokud nedostane svoji odpoved (y/n), zda chteji hrat znovu
        while True:
            choice = input().lower()

            if choice == "y":
                break
            elif choice == "n":
                self.__playAgain = False
                break
            else:
                print("Wrong choices, again! (y/n)")

    # funkce vrati jmeno hry
    def getGameName(self) -> str:
        return "Rock Paper Scissors"