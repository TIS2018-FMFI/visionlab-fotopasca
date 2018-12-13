import cv2
from typing import List

from Src.Configuration.conf import Configuration, load, save
from Src.GUI.Alarm import Alarm
from Src.GUI.GUI import GUI
from Src.Process.controller import Controller
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
        self.cap = cv2.VideoCapture(0)
        self.alarm = Alarm()

    def start(self, fps: int, functions: List):

        if self.config.system.skip:
            self.gui.STATE = self.gui.ROI_STATE

        while(self.gui.STATE != self.gui.TERMINATE_STATE):
            if self.gui.STATE == self.gui.CONFIG_STATE:
                cv2.destroyAllWindows()
                self.gui.configurationWindow()
                save(self.config)
            elif self.gui.STATE == self.gui.ROI_STATE:
                self.setCamera()
                self.roiMenu()
                self.gui.saveRois()
                save(self.config)
            elif self.gui.STATE == self.gui.RUNTIME_STATE:
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
            move = self.controller.isMovement(frame)
            if move:
                self.alarm.play()
                print("alarm")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def sendFrame(self, frame):
        '''posli recorderovi a controlerovi'''
        self.recorder.append(frame)
        movements = self.controller.isMovement(frame)
        ## for id, isMovement in movements:

SystemManager().start(10, [])
