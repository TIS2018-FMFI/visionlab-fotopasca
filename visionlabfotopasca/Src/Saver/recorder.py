from datetime import *
import cv2

from Src.Configuration.conf import RegionOfInterest, Configuration


class Recorder:
    def __init__(self, config):
        self.SAVE_PATH = "../../videos/"
        self.config = config
        self.recording = False


    def toggle(self):
        if self.recording:
            self.save()
        else:
            self.start()

    def start(self):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.name = datetime.now().strftime("%H-%M-%S") + ".avi"
        self.out = cv2.VideoWriter(self.SAVE_PATH + self.name, fourcc, self.config.system.fps, self.config.system.resolution)
        self.recording = True

    def append(self, frame):
        if self.recording:
            self.out.write(frame)

    def save(self):
        if self.recording:
            self.out.release()
            self.recording = False

count = 0

class EmergencyRecorder:

    SAVE_PATH = "../../events/videos/"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    def __init__(self,config: Configuration, roi: RegionOfInterest):
        self.roi: RegionOfInterest = roi
        path = self.getPathToVideo()
        self.resolution = self.getResolution()
        self.out = cv2.VideoWriter(path, self.fourcc, config.system.fps, self.resolution)
        self.recording = True

    def getResolution(self):
        width = self.roi.end.X - self.roi.start.X
        height = self.roi.end.Y - self.roi.start.Y
        return (width, height)

    def getPathToVideo(self):
        global count
        count += 1
        return self.SAVE_PATH + str(self.event.time).replace(':', '-') + "#" + count + ".mp4"

    def append(self, frame):
        if self.recording:
            frame = cv2.resize(frame, self.resolution)
            self.out.write(frame)

    def save(self):
        if self.recording:
            self.out.release()
            self.recording = False