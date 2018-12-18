import cv2
from typing import List

from Src.Configuration.conf import Configuration, load, save
from Src.GUI.Alarm import Alarm
from Src.GUI.GUI import GUI
from Src.Process.controller import Controller
from Src.Process.eventHandler import EventHandler
from Src.Saver.logger import Logger
from Src.Saver.recorder import Recorder


class SystemManager:
    CV_CAP_PROP_FRAME_WIDTH = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4
    CV_CAP_PROP_FPS = 5

    def __init__(self):
        self.config: Configuration = load()
        self.logger: Logger = Logger()
        self.recorder: Recorder = Recorder(self.config)
        self.controller: Controller = Controller(self.config)
        self.gui: GUI = GUI(self, self.config)
        self.eventHandler : EventHandler = EventHandler(self.config, self.logger)


    def start(self):
        if self.config.system.skip:
            self.gui.STATE = self.gui.ROI_STATE

        while self.gui.STATE != self.gui.TERMINATE_STATE:
            if self.gui.STATE == self.gui.CONFIG_STATE:
                cv2.destroyAllWindows()
                self.gui.configurationWindow()
                save(self.config)
            elif self.gui.STATE == self.gui.ROI_STATE:
                self.cap = cv2.VideoCapture(0)
                self.setCamera()
                self.roiMenu()
                self.gui.saveRois()
                save(self.config)
            elif self.gui.STATE == self.gui.RUNTIME_STATE:
                self.cap = cv2.VideoCapture(0)
                self.runtimeMenu()

        self.cap.release()
        cv2.destroyAllWindows()

    def setCamera(self):
        self.cap.set(self.CV_CAP_PROP_FPS, self.config.system.fps)
        width, height = self.config.system.resolution
        self.cap.set(self.CV_CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(self.CV_CAP_PROP_FRAME_HEIGHT, height)

    def roiMenu(self):
        self.gui.roiWindow()

        while self.gui.STATE == self.gui.ROI_STATE:
            ret, frame = self.cap.read()
            self.gui.window.loop(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def runtimeMenu(self):
        self.gui.runtimeWindow()

        while self.gui.STATE == self.gui.RUNTIME_STATE:
            ret, frame = self.cap.read()
            self.gui.window.loop(frame)
            movements = self.controller.isMovement(frame)

            self.eventHandler.process(frame, movements)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE



SystemManager().start()
