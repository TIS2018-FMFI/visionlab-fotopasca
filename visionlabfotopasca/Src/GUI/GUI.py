from Src.Configuration.conf import Configuration
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

    def configurationWindow(self):
        self.window = ConfigurationWindow(self)

    def roiWindow(self):
        self.window = RoiWindow(self)

    def runtimeWindow(self):
        self.window = RuntimeWindow(self)


