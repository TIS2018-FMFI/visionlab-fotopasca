from Src.Configuration.conf import Configuration, RegionOfInterest, Point
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
            r.x1 = roi.start.X
            r.y1 = roi.start.Y
            r.x2 = roi.end.X
            r.y2 = roi.end.Y
            r.sensitivity = roi.sensitivity
            self.rois.append(r)

    def saveRois(self):
        regions = list()
        for roi in self.rois:
            r = RegionOfInterest(roi.sensitivity, [], Point(roi.x1, roi.y1), Point(roi.x2, roi.y2))
            regions.append(r)
        self.config.regions_of_interest = regions


