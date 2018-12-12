from Src.Configuration.conf import Configuration, RegionOfInterest, Point
from Src.GUI.Alarm import Alarm
from Src.GUI.CVGui.CVRoi import CVRoi
from Src.GUI.TKGui.ConfigurationWindow import ConfigurationWindow
from Src.GUI.CVGui.RuntimeWindow import RuntimeWindow
from Src.GUI.CVGui.RoiWindow import RoiWindow


class GUI:
    STATE = 0
    CONFIG_STATE = 0
    ROI_STATE = 1
    RUNTIME_STATE = 2
    TERMINATE_STATE = -1

    def __init__(self, manager, config: Configuration):
        self.manager = manager
        self.config: Configuration = config
        self.window = None
        self.rois = list()
        self.loadRois()
        self.alarm = Alarm()

    def configurationWindow(self):
        self.window = ConfigurationWindow(self)

    def roiWindow(self):
        self.window = RoiWindow(self)

    def runtimeWindow(self):
        self.window = RuntimeWindow(self)

    def loadRois(self):
        self.rois = list()
        for roi in self.config.regions_of_interest:
            r = CVRoi()
            r.ux = roi.start.X
            r.uy = roi.start.Y
            r.dx = roi.end.X
            r.dy = roi.end.Y
            self.rois.append(r)

    def saveRois(self):
        regions = list()
        for roi in self.rois:
            r = RegionOfInterest(0, [], Point(roi.ux, roi.uy), Point(roi.dx, roi.dy))
            regions.append(r)
        self.config.regions_of_interest = regions


