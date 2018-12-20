from datetime import *
import cv2


class Recorder:
    SAVE_PATH = "../../videos/"

    def __init__(self, config):
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
            print("ukladam", self.name)
            self.out.release()
            self.recording = False
