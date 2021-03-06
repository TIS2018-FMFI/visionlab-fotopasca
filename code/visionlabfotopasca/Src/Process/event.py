from dataclasses import dataclass
from datetime import datetime as datetime
import numpy as np
from Src.Configuration import conf


@dataclass
class Event:
    time: datetime
    duration: float
    roi: conf.RegionOfInterest
    pictureNumber: int
    image: np.array
