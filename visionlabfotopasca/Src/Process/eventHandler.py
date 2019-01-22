from Src.Configuration.conf import Configuration
from Src.GUI.Alarm import Alarm
from Src.Process.event import Event
from time import time
from datetime import datetime as datetime

from Src.Saver.logger import Logger
from Src.Saver.recorder import EmergencyRecorder


class EventHandler:

    def __init__(self, config: Configuration, logger: Logger):
        self.config: Configuration = config
        self.alarm: Alarm = Alarm()
        self.logger: Logger = logger
        self.recording = list()
        self.events = list()
        self.count = 0

    def clear(self):
        self.events = [(-1, -1, None, None) for i in range(len(self.config.regions_of_interest))]

    def process(self, frame, movements):

        now = time()
        delay = self.config.alarm.delay

        for idx in range(len(movements)):
            if self.hasEventStarted(movements,idx):
                self.processStartOfEvent(frame, idx, now)

            elif self.hasEventEnded(movements, idx):
                self.processEndOfEvent(idx, now)

        self.alarmSignalization(delay, now, frame)

    def hasEventStarted(self, movements, idx):
        return movements[idx] is True and self.events[idx][0] == -1

    def hasEventEnded(self, movements, idx):
        return movements[idx] is False and self.events[idx][0] != -1

    def processEndOfEvent(self, idx, now):
        event = self.events[idx][2]
        event.duration = (now - self.events[idx][0])
        self.logger.log(event)
        rec: EmergencyRecorder = self.events[idx][3]

        if rec is not None:
            rec.save()

        print("stop")

        self.events[idx] = (-1, -1, None, None)

    def processStartOfEvent(self, frame, idx, now):
        roi = self.config.regions_of_interest[idx]
        roiFrame = frame[roi.start.Y:roi.end.Y, roi.start.X:roi.end.X]
        event = Event(datetime.now(), float(0), roi, self.count, roiFrame)
        rec: EmergencyRecorder = None
        if self.config.video.enabled:
            rec = EmergencyRecorder(self.config, event)

        self.events[idx] = (now, -1, event, rec)
        self.count += 1
        print("start")

    def alarmSignalization(self, delay, now, frame):

        for e in self.events:
            start, end, event, rec = e

            if rec is not None:
                rec.append(frame)

            if not self.config.alarm.enabled:
                continue
            if start != -1:
                diff = now - start
                if diff >= delay:
                    self.alarm.play()







