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


#@dataclass
class Configuration:
    system : SystemSettings = SystemSettings(False, None, 10, None, "video")
    timelaps : TimelapsSettings = TimelapsSettings(False, 10)
    video : VideoSettings = VideoSettings(False, 25)
    email : EmailSettings = None
    alarm : AlarmSettings = None
    
    regions_of_interest : List[RegionOfInterest] = []


CONF_FILE = "..\\res\conf.obj"

def save(c : Configuration) :
    with open(CONF_FILE, "wb") as output:
        pickle.dump(conf, output, pickle.HIGHEST_PROTOCOL)

def load() -> Configuration:
    conf = None
    with open(CONF_FILE, "rb") as file:
        conf = pickle.load(file)

    return conf




# demonstration of saving configration
if __name__ == "__main__":
    conf = Configuration()
    conf.timelaps = TimelapsSettings(False, 10)
    conf.video = VideoSettings(False,20)
    conf.email = EmailSettings(False, "somefake@email.miro")
    conf.alarm = AlarmSettings(False, False,0,0)
    conf.system = SystemSettings(False,"",0,(0,0),"")
    conf.regions_of_interest = [RegionOfInterest(Point(0,0),Point(0,0),[],10)]

    save(conf)
    conf2 = load()

    print(conf2.email)
        
    







    
