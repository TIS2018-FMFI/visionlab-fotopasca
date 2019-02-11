from datetime import *
from os import path
import cv2
from time import time

from Src.Configuration.conf import RegionOfInterest, Configuration
from Src.Process.event import Event


class Recorder:
    VIDEO_PATH = path.join(path.dirname(path.dirname(path.dirname(path.dirname(path.realpath(__file__))))), "videos/")
    TIMELAPSE_PATH = path.join(path.dirname(path.dirname(path.dirname(path.dirname(path.realpath(__file__))))), "timelapse/")

    def __init__(self, config):
        """
        Initialize recorder for time-lapse and video.
        :param config: reference to the system configuration
        """
        self.config = config
        self.recording = False

        self.timelapse = self.config.timelapse.enabled

        if self.timelapse:
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            nameTimelapse = datetime.now().strftime("%H-%M-%S") + ".mp4"
            self.outTimelapse = cv2.VideoWriter(self.TIMELAPSE_PATH + nameTimelapse, fourcc, self.config.system.fps,
                                                self.config.system.resolution)

        self.lastTime = None

    def toggle(self):
        """
        Toggle for recording a manual video.
        :return None:
        """
        if self.recording:
            self.save()
        else:
            self.start()

    def start(self):
        """ Start recording, initialize writer. """
        self.name = datetime.now().strftime("%H-%M-%S") + ".avi"
        self.out = cv2.VideoWriter(self.VIDEO_PATH + self.name, -1, self.config.system.fps, self.config.system.resolution)
        self.recording = True

    def append(self, frame):
        """
        Add actual frame to video file and time-lapse file.
        :param frame: frame to add
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
        Finish recording and save result to a file.
        :return None:
        """
        if self.recording:
            self.out.release()
            self.recording = False

    def endTimelapse(self):
        """
        Finish time-lapse recording and save result to a file.
        :return None:
        """
        if self.timelapse:
            self.outTimelapse.release()


count = 0


class EmergencyRecorder:
    """ Recorder class for event recording. """
    SAVE_PATH = path.join(path.dirname(path.dirname(path.dirname(path.dirname(path.realpath(__file__))))), "events/videos/")

    def __init__(self,config: Configuration, event: Event):
        self.roi: RegionOfInterest = event.roi
        self.event = event
        self.config = config
        filePath = self.getPathToVideo()
        fourcc = cv2.VideoWriter_fourcc(*'H264')

        resolution = self.count_resolution()
        self.out = cv2.VideoWriter(filePath, fourcc, config.system.fps, resolution)
        self.recording = True

    def count_resolution(self):
        """
        Get resolution - if cut flag is set in configuration count it.
        :return resolution : tuple of integers (width, height)
        """
        if self.config.system.cut:
            resolution = (self.event.roi.end.X - self.event.roi.start.X, self.event.roi.end.Y - self.event.roi.start.Y)
        else:
            resolution = self.config.system.resolution
        return resolution

    def getPathToVideo(self):
        """
        Create new name for next video file.
        :return path: string path to new video file
        """
        global count
        count += 1
        return self.SAVE_PATH + str(self.event.time).replace(':', '-') + "#" + str(count) + ".mp4"

    def append(self, f):
        """
        Write frame to video.
        :param f: actual frame from camera
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
        Finish the recording and save it to a file.
        :return None:
        """
        if self.recording:
            self.out.release()
            self.recording = False
