from enum import Enum
from GameLoaderClass import GameLoaderClass

# enum pro reprezentaci stavu hlavniho menu
class MenuState(Enum):
    LOAD = 0
    MAIN_MENU = 1
    SELECTED_GAME = 2

# nastav pocatecni stav na nacteni her
state = MenuState.LOAD
# pripava seznamu pro ulozeni instanci her
loadedGameObjects = []

# metoda vybira nejakou hru, ktera se nachazi na adresari ./games
def main() -> None:
    global state, loadedGameObjects
    # nastav pocatecni stav na nacteni her
    state = MenuState.LOAD
    # vytvor instanci tridy slouzici pro nacitani her, ktere se nachazi na adrese ./games
    loader = GameLoaderClass('./games')
    # nacti hry, ktere se nachazi na adrese ./games 
    loadedGameObjects = loader.loadGames()

    # zkontroluj, zda se nasli nejake hry
    if len(loadedGameObjects) == 0:
        print("No games found.")
        return

    # nastav stav na vyber her
    state = MenuState.MAIN_MENU
    # oznaceni nevybrane hry
    selectedGame = -1
    # vzdy ukazuj nabidku her od 1 az do n + dej moznost vyberu hry
    while True:
        # zkontroluj, zda jsme porad nevybrali hru
        if state == MenuState.MAIN_MENU:
            # vzdy nastav na -1, abychom vedeli, ze nemame porad vybranou hru
            selectedGame = -1
            print("-----------------------------------------------------")
            print("Game list:")
            # vypis vsechny mozne hry, ktere lze vybrat
            for i, gameObject in enumerate(loadedGameObjects):
                # vypis jmeno hry, ktera je ulozena v souboru, ve kterem je hlavni kod hry
                print(f"[{i + 1}] {gameObject.getGameName()}")
            print(f"Total {len(loadedGameObjects)}")

            try:
                if len(loadedGameObjects) == 1:
                    # precti, co hrac vybral za hru
                    selectedGame = input(f"Select game [1]: ")
                else:
                    # precti, co hrac vybral za hru
                    selectedGame = input(f"Select game [1-{len(loadedGameObjects)}]: ")
                
                # zkontroluj, zda je to cislo
                selectedGame = int(selectedGame)
                # zkontroluj, zda patri do intervalu pro vyber her
                if selectedGame < 1 or selectedGame > len(loadedGameObjects):
                    raise Exception
                # prepni se do stavu, kdy hrajeme nejakou hru
                state = MenuState.SELECTED_GAME
            except:
                # zkontroluj, zda do hlavniho menu nenapsal hrac quit - po napsani quit ukonci program
                if selectedGame == "quit":
                    print("Goodbye.")
                    exit(0)

                # po spatnem vyberu nastav stav na vyberu nejake hry 
                state = MenuState.MAIN_MENU
                print(f"Wrong game number {selectedGame}.")
            
        if state == MenuState.SELECTED_GAME:
            print("Game starting...")
            # zavolej metodu start, ktera se nachazi v hlavnim kodu nejake hry
            game = loadedGameObjects[selectedGame - 1]
            game.start()
            # po skonceni u dane hry se prepni znovu do vyberu nejake dalsi hry
            state = MenuState.MAIN_MENU

if __name__ == '__main__':
    main()    