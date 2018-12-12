from typing import Dict
import cv2

from Src.Configuration.conf import Configuration

class Controller:

    def __init__(self,c : Configuration):

        self.lastFrame = None
        self.config: Configuration = c

    def isMovement(self, frame):
        ## kluc je id oblasti hodnota je bool
        res = dict()

        # konvezria na gray scale img
        gray_img = gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ak uz boli dva framy a teda mame frame na porovnanie
        if self.lastFrame is not None:

            # spravime rozdiel pixelov v obrazkoch
            diff = cv2.absdiff(self.lastFrame, gray_frame)

            for rio in self.config.regions_of_interest:
                # vybereme oblast roi
                rio_img = diff[rio.start.Y:rio.end.Y, rio.start.Y:rio.end.Y]

                # TODO: odstranit z rio oblasti ktore tam nechceme

                # spravime treshlold podla sensitivity
                thresh = cv2.threshold(rio_img,rio.sensitivity,255,cv2.THRESH_BINARY)

                # percentualna zmena
                percentage_change = (cv2.sumElems(thresh)/255) / ((rio.end.Y - rio.start.Y)\
                                    * (rio.end.Y-rio.start.Y)) * 100

                # aka zmena presiahla 30 percent nastala udalost co zaznacime
                if percentage_change > 30:
                    res[rio] = True
                else:
                    res[rio] = False

        self.lastFrame = frame
        return res


