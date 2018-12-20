from Src.Configuration.conf import Configuration
from Src.GUI.Alarm import Alarm
from Src.Process.event import Event
from time import time
from datetime import datetime as datetime

from Src.Saver.logger import Logger


class EventHandler:

    def __init__(self, config: Configuration, logger: Logger):
        self.config: Configuration = config
        self.alarm: Alarm = Alarm()
        self.logger: Logger = logger
        self.events = list()
        self.count = 0

    def clear(self):
        self.events = [(-1, -1, None) for i in range(len(self.config.regions_of_interest))]

    def process(self, frame, movements):


        #if not self.config.alarm.enabled:
        #    return

        now = time()
        delay = self.config.alarm.delay

        for idx in range(len(movements)):

            if movements[idx] is True and self.events[idx][0] == -1:
                event = Event(datetime.now(), float(0), self.config.regions_of_interest[idx], self.count, frame)
                self.events[idx] = (now, -1, event)
                self.count += 1

            elif movements[idx] is False and self.events[idx][0] != -1:
                event = self.events[idx][2]
                event.duration = (now - self.events[idx][0])
                self.logger.log(event)
                self.events[idx] = (-1, -1, None)

        for t in self.events:
            if t[0] != -1:
                diff = now - t[0]
                #print(diff)
                if diff >= delay:
                    self.alarm.play()







