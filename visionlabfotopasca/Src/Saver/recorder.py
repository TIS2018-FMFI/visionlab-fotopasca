from datetime import *
from os import path
import cv2
from time import time

from Src.Configuration.conf import RegionOfInterest, Configuration
from Src.Process.event import Event


class Recorder:
    def __init__(self, config):
        self.VIDEO_PATH = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "videos/")
        self.TIMELAPSE_PATH = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "timelapse/")
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
        if self.recording:
            self.save()
        else:
            self.start()

    def start(self):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.name = datetime.now().strftime("%H-%M-%S") + ".avi"
        self.out = cv2.VideoWriter(self.VIDEO_PATH + self.name, fourcc, self.config.system.fps, self.config.system.resolution)
        self.recording = True

    def append(self, frame):
        if self.recording:
            self.out.write(frame)

        if self.timelapse:
            if self.lastTime is None or time() - self.lastTime > self.config.timelapse.capture_speed:
                self.outTimelapse.write(frame)
                self.lastTime = time()

    def save(self):
        if self.recording:
            self.out.release()
            self.recording = False

    def endTimelapse(self):
        if self.timelapse:
            self.outTimelapse.release()

count = 0

class EmergencyRecorder:
    SAVE_PATH = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "events/videos/")
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    def __init__(self,config: Configuration, event: Event):
        self.roi: RegionOfInterest = event.roi
        self.event = event
        filePath = self.getPathToVideo()
        self.resolution = self.getResolution()
        self.out = cv2.VideoWriter(filePath, self.fourcc, config.system.fps, self.resolution)
        self.recording = True

    def getResolution(self):
        width = self.roi.end.X - self.roi.start.X
        height = self.roi.end.Y - self.roi.start.Y
        return (width, height)

    def getPathToVideo(self):
        global count
        count += 1
        return self.SAVE_PATH + str(self.event.time).replace(':', '-') + "#" + str(count) + ".avi"

    def append(self, frame):
        if self.recording:
            self.out.write(frame)

    def save(self):
        if self.recording:
            self.out.release()
            self.recording = False