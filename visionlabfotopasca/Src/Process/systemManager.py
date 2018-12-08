import cv2
from typing import List

from Src.Configuration.conf import Configuration, load, save
from Src.GUI.GUI import GUI
from Src.Process.controller import Controller
from Src.Saver.logger import Logger
from Src.Saver.recorder import Recorder


class SystemManager:

    def __init__(self):
        self.config: Configuration = load()
        self.logger: Logger = Logger()
        self.recorder: Recorder = Recorder(self.config)
        self.controller: Controller = Controller(self.config)
        self.gui: GUI = GUI(self, self.config)
        self.cap = cv2.VideoCapture(0)

    def start(self, fps: int, functions: List):
        while(self.gui.STATE != self.gui.TERMINATE_STATE):
            if self.gui.STATE == self.gui.CONFIG_STATE:
                cv2.destroyAllWindows()
                self.gui.configurationWindow()
                save(self.config)
            elif self.gui.STATE == self.gui.ROI_STATE:
                self.roiMenu()
                save(self.config)
            elif self.gui.STATE == self.gui.RUNTIME_STATE:
                self.runtimeMenu()

        self.cap.release()
        cv2.destroyAllWindows()

    def roiMenu(self):
        self.gui.roiWindow()

        while (self.gui.STATE == self.gui.ROI_STATE):
            ret, frame = self.cap.read()
            self.gui.window.loop(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def runtimeMenu(self):
        self.gui.runtimeWindow()

        while (self.gui.STATE == self.gui.RUNTIME_STATE):
            ret, frame = self.cap.read()
            self.gui.window.loop(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def sendFrame(self, frame):
        '''posli recorderovi a controlerovi'''
        self.recorder.append(frame)
        movements = self.controller.isMovement(frame)
        ## for id, isMovement in movements:

SystemManager().start(10, [])
