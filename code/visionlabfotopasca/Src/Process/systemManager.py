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
    """ System manager - controls the system. """
    PATH_TO_VIDEO = path.join(path.dirname(path.dirname(path.dirname(path.dirname(path.realpath(__file__))))), "testVideo.avi")
    INTERNAL_CAMERA = 0
    EXTERNAL_CAMERA = 1
    CV_CAP_PROP_FRAME_WIDTH = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4
    CV_CAP_PROP_FPS = 5
    INPUT = EXTERNAL_CAMERA

    def __init__(self):
        """ Initialize attributes - configuration, logger, recorder, controller, gui, event-handler. """
        self.config: Configuration = load()
        self.logger: Logger = Logger()
        self.recorder: Recorder = Recorder(self.config)
        self.controller: Controller = Controller(self.config)
        self.gui: GUI = GUI(self, self.config)
        self.eventHandler: EventHandler = EventHandler(self.config, self.logger)
        self.startTime = None

    def start(self):
        """
        Main program - switches between three states:
         1) config state
         2) roi config state
         3) running state
        """
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
        """ Set attributes and set the feed from camera. """
        self.cap = cv2.VideoCapture(self.INPUT)

    def roiMenu(self):
        """ Region of interest config menu loop. """
        self.gui.roiWindow()
        while self.gui.STATE == self.gui.ROI_STATE:
            frame = self.getFrame()
            self.gui.window.loop(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def runtimeMenu(self):
        """ Runtime loop, sends frame to GUI and to controller and takes care of fps count. """
        self.gui.runtimeWindow()
        self.eventHandler.clear()

        oneTickTime = 1000/self.config.system.fps

        while self.gui.STATE == self.gui.RUNTIME_STATE:
            t1 = time()
            frame = self.getFrame()

            if self.startTime is None:
                self.startTime = time()
            if time() - self.startTime > self.config.system.initDelay:
                movements = self.controller.isMovement(frame)
                self.eventHandler.process(frame, movements)

            self.recorder.append(frame)
            self.gui.window.loop(frame)

            duration = (time() - t1) * 1000  # in millis
            waitTime = 1
            if duration < oneTickTime:
                waitTime  = int(oneTickTime - duration)

            if cv2.waitKey(waitTime) & 0xFF == ord('q'):
                self.gui.STATE = self.gui.TERMINATE_STATE

    def getFrame(self):
        """
        Read frame from camera in set resolution.
        :return: frame: numpy.array representing a frame from camera
        """
        width, height = self.config.system.resolution
        ret, frame = self.cap.read()
        if ret is False:
            self.setCamera()
            ret, frame = self.cap.read()
        if frame is None:
            frame = self.noFeedScreen()
        else:
            frame = self.blackBarsCrop(frame)
        frame = cv2.resize(frame, (width, height))
        return frame

    def noFeedScreen(self):
        """
        Black screen with error message in case of wrong input from camera.
        :return: black_screen: numpy.array
        """
        width, height = self.config.system.resolution
        frame = numpy.zeros((height, width, 3), numpy.uint8)
        cv2.putText(frame, "CHYBA VSTUPU", (int(width/2) - 220, 200), cv2.FONT_HERSHEY_PLAIN, 4,
                    (255, 255, 255), 1, cv2.LINE_AA)
        return frame

    def blackBarsCrop(self, frame):
        """
        Remove the black bars from frame.
        :param frame: input frame from camera
        :return: new_frame: numpy.array
        """
        rows = numpy.where(numpy.max(frame, 0) > 0)[0]
        if rows.size:
            cols = numpy.where(numpy.max(frame, 1) > 0)[0]
            frame = frame[cols[0]: cols[-1] + 1, rows[0]: rows[-1] + 1]
        else:
            frame = frame[:1, :1]
        return frame
