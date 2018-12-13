from typing import Dict
import cv2
import numpy as np

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

        flag = False

        # ak uz boli dva framy a teda mame frame na porovnanie
        if self.lastFrame is not None:

            # spravime rozdiel pixelov v obrazkoch
            diff = cv2.absdiff(self.lastFrame, gray_frame)

            for roi in self.config.regions_of_interest:
                # vybereme oblast roi
                rio_img = diff[roi.start.Y:roi.end.Y, roi.start.X:roi.end.X]

                # TODO: odstranit z roi oblasti ktore tam nechceme

                # spravime treshlold podla sensitivity
                ret, thresh = cv2.threshold(rio_img,roi.sensitivity,255,cv2.THRESH_BINARY)
                cv2.imshow("test", thresh)
                # percentualna zmena
                count = np.sum(thresh)
                count = int(count)
                percentage_change = (count / 255) / ((roi.end.Y - roi.start.Y) * (roi.end.X - roi.start.X)) * 1000

                print(percentage_change)
                # aka zmena presiahla 30 percent nastala udalost co zaznacime
                if percentage_change > 100 - roi.sensitivity:
                    flag = True

        self.lastFrame = gray_frame

        return flag


