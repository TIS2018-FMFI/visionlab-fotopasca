import cv2
from typing import List

from Src.Configuration.conf import Configuration, load
from Src.GUI.window import Window
from Src.Process.controller import Controller
from Src.Saver.logger import Logger
from Src.Saver.recorder import Recorder


class SystemManager:
    config: Configuration = Configuration()
    logger: Logger = Logger()
    recorder: Recorder = Recorder()
    controller: Controller = Controller()
    guiElem: Window = Window()

    def __init__(self):
        pass


    def start(self, fps: int, functions: List):
        cap = cv2.VideoCapture(1)

        while (True):
            ret, frame = cap.read()
        
            self.sendFrame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cap.release()
        cv2.destroyAllWindows()

        self.timelaps.save()

    def sendFrame(self, frame):
        '''posli recorderovi a controlerovi'''
        self.recorder.append(frame)
        movements = self.controller.isMovement(frame)
        ## for id, isMovement in movements:
