from dataclasses import dataclass
from typing import List, Tuple
import pickle

@dataclass
class Point:
    X: int
    Y: int

@dataclass
class RegionOfInterest:
    sensitivity: int
    ignored_areas: List[Tuple[Point, Point]]
    start: Point = Point(0, 0)
    end: Point = Point(0, 0)

@dataclass
class TimelapseSettings:
    enabled: bool
    capture_speed: int

@dataclass
class VideoSettings:
    enabled: bool
    
@dataclass
class EmailSettings:
    enabled: bool
    email: str

@dataclass
class AlarmSettings:
    enabled: bool
    delay: int
    duration: int

@dataclass
class SystemSettings:
    skip: bool
    password: str
    initDelay: int
    resolution: Tuple[int, int]
    videoFolder: str
    fps: int


#@dataclass
class Configuration:

    def __init__(self):
        self.system: SystemSettings = SystemSettings(False, "pass", 10, (1280, 720), "video", 40)
        self.timelapse: TimelapseSettings = TimelapseSettings(True, 30)
        self.video: VideoSettings = VideoSettings(True)
        self.email: EmailSettings = EmailSettings(False, None)
        self.alarm: AlarmSettings = AlarmSettings(True, 5, 10)
        self.regions_of_interest: List[RegionOfInterest] = [RegionOfInterest(0,[])]

CONF_FILE = "../../res/conf.obj"

def save(c: Configuration):
    with open(CONF_FILE, "wb") as output:
        pickle.dump(c, output, pickle.HIGHEST_PROTOCOL)

def load() -> Configuration:
    conf = None
    with open(CONF_FILE, "rb") as file:
        conf = pickle.load(file)

    return conf




# demonstration of saving configration
if __name__ == "__main__":
    conf = Configuration()


    save(conf)
    conf2 = load()

    print(conf2.email)
        
    







    
