import abc

# abstraktni trida reprezentujici hru
class AbstractGameClass(abc.ABC):

    # kazda trida dedici od teto tridy musi implementovat start
    @abc.abstractmethod
    def start(self) -> None:
        pass
    
    # kazda trida dedici od teto tridy musi implementovat getGameName
    @abc.abstractmethod
    def getGameName(self) -> str:
        pass