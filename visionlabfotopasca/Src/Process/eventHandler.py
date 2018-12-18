from Src.Configuration.conf import Configuration
from Src.GUI.Alarm import Alarm
from Src.Process.event import Event
from time import time

from Src.Saver.logger import Logger


class EventHandler:

    def __init__(self, config: Configuration, logger: Logger):
        self.config: Configuration = config
        self.alarm: Alarm = Alarm()
        self.logger: Logger = logger
        self.events = dict()
        self.toPlay = list()
        self.count = 0

    def process(self, frame, movements):

        self.count += 1

        if not self.config.alarm.enabled:
            return

        now = time()
        delay = self.config.alarm.delay
        duration = self.config.alarm.duration

        for idx in len(movements):
            if movements[idx] == True and idx not in self.events:
                event = Event(now, 0, idx, self.count, frame)
                self.events[idx] = (now, event)
                self.toPlay.append(now)

            elif movements[idx] == False and idx in self.events:
                event = self.events[idx][1]
                event.duration = (now - self.events[0])
                self.logger.log(event)

            elif idx in self.events:
                del self.events[idx]

        for t in self.toPlay:
            diff = t - now

            if duration >= diff >= delay:
                self.alarm.play()







