from typing import Dict

from Src.Configuration.conf import Configuration

class Controller:

    def __init__(self,c : Configuration):

        self.lastFrame = None
        self.config: Configuration = c

    def isMovement(self, frame) -> Dict[int: bool] :
        res = dict() ## kluc je id oblasti hodnota je bool

        self.lastFrame = frame
        return res


