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
        self.alarmStartTime = []
        self.alarmEndTime = []

    def clear(self):
        self.events = [(-1, -1, None, None) for i in range(len(self.config.regions_of_interest))]

    def process(self, frame, movements):
        now = time()
        delay = self.config.alarm.delay
        duration = self.config.alarm.duration

        for idx in range(len(movements)):
            if self.hasEventStarted(movements,idx):
                self.processStartOfEvent(frame, idx, now)
                self.alarmStartTime.append(now + delay)

            elif self.hasEventEnded(movements, idx):
                self.processEndOfEvent(idx, now)
                self.alarmEndTime.append(now + duration)

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
        datetime_now = datetime.now()
        event = Event(datetime_now, float(0), roi, self.count, roiFrame)
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
                roi = event.roi
                rec.append(frame[roi.start.Y:roi.end.Y, roi.start.X:roi.end.X])

        now = time()

        end = None
        start = None

        if self.config.alarm.enabled:

            while len(self.alarmStartTime) > 0:
                start = self.alarmStartTime[0]

                if len(self.alarmEndTime) > 0:
                    end = self.alarmEndTime[0]

                if end is not None and end < now:
                    self.alarmEndTime.pop(0)
                    self.alarmStartTime.pop(0)
                    end = None
                    start = None
                else:
                    break

            if start is not None and start < now:
                if end is None or end > now:
                    self.alarm.play()











