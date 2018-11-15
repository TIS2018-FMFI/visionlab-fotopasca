from typing import List
import conf


import cv2

from timelapsRecorder import TimelapsRecorder

from videoRecorder import VideoRecorder

from logger import Logger


class ProcessVideo:

    def __init__(self, c :conf.Configuration):
        self.cap = cv2.VideoCapture(1)
        self.config : conf.Configuration = c
        self.timelaps : TimelapsRecorder = TimelapsRecorder(c)
        self.video : VideoRecorder = VideoRecorder(c)
        self.logger : Logger = Logger()

    def getFrame(self):
        ret, frame = self.cap.read()
        return frame

    def start(self, fps : int, functions : List):
        cap = cv2.VideoCapture(1)

        while (True):
            ret, frame = cap.read()

            self.timelaps.add(frame)

            isEvent, events = self.detectEvents(frame)

            for e in events:
                self.logger.log(e)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cap.release()
        cv2.destroyAllWindows()

        self.timelaps.save()

    def detectEvents(self, frame):
        return False, None