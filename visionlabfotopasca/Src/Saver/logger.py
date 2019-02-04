from os import path
import cv2

from Src.Process.event import Event


class Logger:

    LOGFILE = path.join(path.dirname(path.dirname(path.dirname(path.dirname(path.realpath(__file__))))), "events/log/log.txt")
    PATH_TO_PICTURE_FILE = path.join(path.dirname(path.dirname(path.dirname(path.dirname(path.realpath(__file__))))), "events/images/")
    
    def log(self,event : Event):
        with open(self.LOGFILE,'a') as f:
            f.write(f'\"{event.time}\";{event.duration};\"{event.roi}\";{event.pictureNumber}\n')
            
        imgName = self.PATH_TO_PICTURE_FILE + \
                  str(event.time).replace(':','-') +\
                  "#" + str(event.pictureNumber) + ".jpg"
        
        print("logujem")
        cv2.imwrite(imgName, event.image)

