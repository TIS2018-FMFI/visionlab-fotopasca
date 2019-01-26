from datetime import *
from os import path
import cv2
from time import time

from Src.Configuration.conf import RegionOfInterest, Configuration
from Src.Process.event import Event


class Recorder:
    VIDEO_PATH = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "videos/")
    TIMELAPSE_PATH = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "timelapse/")

    def __init__(self, config):
        """
        initialize recorder for timelapse and video
        :param config:
        """
        self.config = config
        self.recording = False

        self.timelapse = self.config.timelapse.enabled

        if self.timelapse:
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            nameTimelapse = datetime.now().strftime("%H-%M-%S") + ".avi"
            self.outTimelapse = cv2.VideoWriter(self.TIMELAPSE_PATH + nameTimelapse, fourcc, self.config.system.fps,
                                                self.config.system.resolution)

        self.lastTime = None

    def toggle(self):
        """
        toggle
        :return None:
        """
        if self.recording:
            self.save()
        else:
            self.start()

    def start(self):
        """
        start recording initialize writer
        :return None:
        """
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.name = datetime.now().strftime("%H-%M-%S") + ".avi"
        self.out = cv2.VideoWriter(self.VIDEO_PATH + self.name, fourcc, self.config.system.fps, self.config.system.resolution)
        self.recording = True

    def append(self, frame):
        """
        add actuall frame to video file and timelapse file
        :param frame:
        :return None:
        """
        if self.recording:
            self.out.write(frame)

        if self.timelapse:
            if self.lastTime is None or time() - self.lastTime > self.config.timelapse.capture_speed:
                self.outTimelapse.write(frame)
                self.lastTime = time()

    def save(self):
        """
        finish recording and save result to file
        :return None:
        """
        if self.recording:
            self.out.release()
            self.recording = False

    def endTimelapse(self):
        """
        finish timelapse recording and save result to file
        :return None:
        """
        if self.timelapse:
            self.outTimelapse.release()


count = 0


class EmergencyRecorder:
    """recorder for event recording"""
    SAVE_PATH = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "events/videos/")

    def __init__(self,config: Configuration, event: Event):
        self.roi: RegionOfInterest = event.roi
        self.event = event
        self.config = config
        filePath = self.getPathToVideo()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

        resolution = self.count_resolution()

        self.out = cv2.VideoWriter(filePath, fourcc, config.system.fps, resolution)
        self.recording = True

    def count_resolution(self):
        """ get resolution - if cut flag is set in configuration count it
            :return resolution : tuple of integers (width, height)
        """
        if self.config.system.cut:
            resolution = (self.event.roi.end.X - self.event.roi.start.X, self.event.roi.end.Y - self.event.roi.start.Y)
        else:
            resolution = self.config.system.resolution
        return resolution

    def getPathToVideo(self):
        """
        create new name for next video file
        :return path: string path to new video file
        """
        global count
        count += 1
        return self.SAVE_PATH + str(self.event.time).replace(':', '-') + "#" + str(count) + ".avi"

    def append(self, f):
        """
        Write frame to video
        :param f: acctual frame from camera
        :return None:
        """
        if self.recording:
            if self.config.system.cut:
                frame = f[self.roi.start.Y:self.roi.end.Y, self.roi.start.X:self.roi.end.X]
            else:
                frame = f
            self.out.write(frame)

    def save(self):
        """
        finish the recording and save it to file
        :return None:
        """
        if self.recording:
            self.out.release()
            self.recording = False
