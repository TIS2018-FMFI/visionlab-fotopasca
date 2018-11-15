from datetime import datetime as datetime
import numpy as np
import cv2

from Main.event import Event
from Main import conf



class Logger:

    LOGFILE = "..\events\log\log.txt"
    PATH_TO_PICTURE_FILE = "..\events\images\\"
    
    def log(self,event : Event):
        with open(self.LOGFILE,'a') as f:
            f.write(f'{event.time}_{event.duration}_{event.roi}#{event.pictureNumber}\n')
            
        imgName = self.PATH_TO_PICTURE_FILE + \
                  str(event.time).replace(':','-') +\
                  "#" + str(event.pictureNumber) +  ".jpg"
        
        
        cv2.imwrite(imgName,event.image)

        
if __name__ == "__main__":
    roi = conf.RegionOfInterest(conf.Point(0,0),conf.Point(0,0),[],10)
    img = np.zeros((100,100,3), np.uint8)
    event = Event(datetime.now(),10.5,roi,1,img)

    logger = Logger()

    logger.log(event)


    
   
