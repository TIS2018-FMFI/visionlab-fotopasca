import cv2
import numpy

from time import time
from os import path
from Src.Configuration.conf import Configuration, load, save
from Src.GUI.GUI import GUI
from Src.Process.controller import Controller
from Src.Process.eventHandler import EventHandler
from Src.Saver.logger import Logger
from Src.Saver.recorder import Recorder


class SystemManager:
    PATH_TO_VIDEO = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "testVideo.avi")
    INTERNAL_CAMERA = 0
    EXTERNAL_CAMERA = 1
    CV_CAP_PROP_FRAME_WIDTH = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4
    CV_CAP_PROP_FPS = 5
    INPUT = EXTERNAL_CAMERA

    def __init__(self):
        self.config: Configuration = load()
        self.logger: Logger = Logger()
        self.recorder: Recorder = Recorder(self.config)
        self.controller: Controller = Controller(self.config)
        self.gui: GUI = GUI(self, self.config)
        self.eventHandler: EventHandler = EventHandler(self.config, self.logger)
        self.startTime = None

    def start(self):
        if self.config.system.skip:
            self.gui.STATE = self.gui.ROI_STATE

        while self.gui.STATE != self.gui.TERMINATE_STATE:
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
                self.setCamera()
                self.runtimeMenu()
                self.recorder.endTimelapse()

        self.cap.release()
        cv2.destroyAllWindows()

    def setCamera(self):
        self.cap = cv2.VideoCapture(self.INPUT)
        width, height = self.config.system.resolution
        self.cap.set(self.CV_CAP_PROP_FPS, self.config.system.fps)
        self.cap.set(self.CV_CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(self.CV_CAP_PROP_FRAME_HEIGHT, height)

    def roiMenu(self):
        self.gui.roiWindow()
        while self.gui.STATE == self.gui.ROI_STATE:
            frame = self.getFrame()
            self.gui.window.loop(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def runtimeMenu(self):
        self.gui.runtimeWindow()
        self.eventHandler.clear()
        while self.gui.STATE == self.gui.RUNTIME_STATE:
            frame = self.getFrame()

            if self.startTime is None:
                self.startTime = time()
            if time() - self.startTime > self.config.system.initDelay:
                movements = self.controller.isMovement(frame)
                self.eventHandler.process(frame, movements)

            self.recorder.append(frame)
            self.gui.window.loop(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def getFrame(self):
        width, height = self.config.system.resolution
        ret, frame = self.cap.read()
        if ret is False:
            self.setCamera()
            ret, frame = self.cap.read()
        if frame is None:
            frame = self.noFeedScreen()
        frame = cv2.resize(frame, (width, height))
        return frame


    def noFeedScreen(self):
        width, height = self.config.system.resolution
        frame = numpy.zeros((height, width, 3), numpy.uint8)
        cv2.putText(frame, "CHYBA VSTUPU", (int(width/2) - 220, 200), cv2.FONT_HERSHEY_PLAIN, 4,
                    (255, 255, 255), 1, cv2.LINE_AA)
        return frame

