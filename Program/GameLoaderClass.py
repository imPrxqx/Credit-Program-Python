import os
import importlib.util
import inspect
from AbstractGameClass import AbstractGameClass

# trida slouzici pro hledani her
class GameLoaderClass():
    
    def __init__(self, folder):
        self.folder = folder

    # funkce nacita moduly z daneho souboru a ziska pristup k jeho obsahu a funkcim
    def loadModule(self, filePath) -> any:
        # ziskej jmeno modulu z cesty k souboru
        moduleName = os.path.splitext(os.path.basename(filePath))[0]
        # vytvor specifikaci modulu z cesty k souboru
        spec = importlib.util.spec_from_file_location(moduleName, filePath)
        # nacti modul z jeho speficikace
        module = importlib.util.module_from_spec(spec)
        # spust modul
        spec.loader.exec_module(module)
        return module

    # funkce vyhledava podtridy zadane zakladni tridy v danem modulu a vytvari jeji instanci, pokud je to mozne
    def findSubclassInModule(self, module, baseClass) -> any:
        # postupne prochazej vsechny objekty ve specifikovanem modulu
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # zkontroluj, zda je objekt podtridou zakladni tridy a zda neni totozny s baseClass
            if issubclass(obj, baseClass) and obj is not baseClass:
                print(f'Found game: {obj.__name__} in {module.__name__}.py')
                try:
                    # vytvor nalezene podtridy instanci
                    instance = obj()
                    return instance
                except TypeError as e:
                    print(f"Failed to instantiate {obj.__name__}: {e}")
        return None

    # funkce vyhledava a nacita moduly her z urceneho adresare a vytvari jejich instance, ktere pak vrati ve forme seznamu
    def loadGames(self) -> list:
        # seznam nactenych instanci her
        loadedGameObjects = []
        
        print("Searching for games...")
        # postupne prochazej vsechny soubory v danem adresari
        for filename in os.listdir(self.folder):
            # zkontroluj, zda soubor konci s koncovkou .py
            if filename.endswith('.py'):
                # vytvor cestu k souboru
                filePath = os.path.join(self.folder, filename)
                try:
                    # nacti modul
                    module = self.loadModule(filePath)
                    # hledej ty, co maji podtridu AbstractGameClass
                    obj = self.findSubclassInModule(module, AbstractGameClass)
                    if obj:
                        # Pridej nalezene instance do seznamu
                        loadedGameObjects.append(obj)
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")
        print("Stop searching...")
        # vrat seznam nactenych instanci her
        return loadedGameObjects
