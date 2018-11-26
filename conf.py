from dataclasses import dataclass
from typing import List, Tuple
import pickle

@dataclass
class Point:
    X :int
    Y :int

@dataclass
class RegionOfInterest:
    start : Point
    end : Point
    ignored_areas : List[Tuple[Point,Point]]
    sensitivity : int

@dataclass
class TimelapsSettings:
    enabled : bool
    capture_speed : int

@dataclass
class VideoSettings:
    enabled : bool
    capture_rate : int
    
@dataclass
class EmailSettings:
    enabled : bool
    email : str

@dataclass
class AlarmSettings:
    emergency_recording : bool
    sound_alarm : bool
    delay : int
    soundAfterEvent : int

@dataclass
class SystemSettings:
    skip_configuration : bool 
    password : str
    initDelay : int
    resolution : Tuple[int, int]
    videoFolder : str

class Configuration:
    system : SystemSettings = None
    timelaps : TimelapsSettings = None
    video : VideoSettings = None
    email : EmailSettings = None
    alarm : AlarmSettings = None
    
    regions_of_interest : List[RegionOfInterest] = []




# demonstration of saving configration
if __name__ == "__main__":
    conf = Configuration()
    conf.timelaps = TimelapsSettings(False, 10)
    conf.video = VideoSettings(False,20)
    conf.email = EmailSettings(False, "somefake@email.miro")
    conf.alarm = AlarmSettings(False, False,0,0)
    conf.system = SystemSettings(False,"",0,(0,0),"")
    conf.regions_of_interest = [RegionOfInterest(Point(0,0),Point(0,0),[],10)]
 
    with open("test.data", "wb") as output:
        pickle.dump(conf, output, pickle.HIGHEST_PROTOCOL)
    del conf
    conf2 = None
    with open("test.data", "rb") as f2:
        conf2 = pickle.load(f2)

    print(conf2.timelaps)
        
    







    
