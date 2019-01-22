from Src.Configuration.conf import Configuration, RegionOfInterest, Point
from Src.GUI.CVGui.CVRoi import CVRoi
from Src.GUI.TKGui.ConfigurationWindow import ConfigurationWindow
from Src.GUI.CVGui.RuntimeWindow import RuntimeWindow
from Src.GUI.CVGui.RoiWindow import RoiWindow


class GUI:
    """ Class for managing the GUI """
    STATE = 0
    CONFIG_STATE = 0
    ROI_STATE = 1
    RUNTIME_STATE = 2
    TERMINATE_STATE = -1

    def __init__(self, manager, config: Configuration):
        """
        GUI class constructor.
        :param manager: reference to the main SystemManager instance
        :param config: contains system configuration
        """
        self.manager = manager
        self.config: Configuration = config
        self.window = None
        self.rois: list = list()
        self.loadRois()

    def configurationWindow(self):
        """Opens the configuration window."""
        self.window = ConfigurationWindow(self)

    def roiWindow(self):
        """Opens the roi selection window."""
        self.window = RoiWindow(self)

    def runtimeWindow(self):
        """Opens the runtime window."""
        self.window = RuntimeWindow(self)

    def loadRois(self):
        """Loads region of interests from configuration."""
        self.rois = list()
        for roi in self.config.regions_of_interest:
            r = CVRoi()
            r.x1 = roi.start.X
            r.y1 = roi.start.Y
            r.x2 = roi.end.X
            r.y2 = roi.end.Y
            r.sensitivity = roi.sensitivity
            self.rois.append(r)
        for ignored in self.config.ignored_areas:
            i = CVRoi()
            i.x1 = ignored.start.X
            i.y1 = ignored.start.Y
            i.x2 = ignored.end.X
            i.y2 = ignored.end.Y
            i.ignored = True
            self.rois.append(i)

    def saveRois(self):
        """Saves region of interests to configuration."""
        regions = list()
        ignored = list()
        for roi in self.rois:
            r = RegionOfInterest(roi.sensitivity, Point(roi.x1, roi.y1), Point(roi.x2, roi.y2))
            if roi.ignored:
                ignored.append(r)
            else:
                regions.append(r)
        self.config.regions_of_interest = regions
        self.config.ignored_areas = ignored


