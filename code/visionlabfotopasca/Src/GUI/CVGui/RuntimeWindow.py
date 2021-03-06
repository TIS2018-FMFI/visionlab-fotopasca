import cv2
from Src.GUI.CVGui.CVButton import CVButton
from Src.GUI.CVGui.CVWindow import CVWindow


class RuntimeWindow(CVWindow):
    """
    Class for cv2 based GUI of the runtime window.
    Extends an CVWindow abstract class.
    """

    def __init__(self, gui):
        """
        Construction of the runtime window.

        :param gui: reference to the parent gui manager
        """
        super().__init__(gui)
        self.btnRecord = CVButton(self.width - 300, self.height - 60, self.width - 170, self.height - 20, 'Record', 23)
        self.btnOff = CVButton(self.width - 150, self.height - 60, self.width - 20, self.height - 20, 'OFF', 42)
        self.__mouseEvent()

    def drawUI(self):
        """ Internal method called by loop() drawing the GUI of this window. """
        super().drawUI()

        timelapse = "on" if self.gui.manager.recorder.timelapse else "off"
        video = "on" if self.gui.manager.recorder.recording else "off"
        info = "timelapse: " + timelapse + " video: " + video
        cv2.putText(self.root, info, (self.width - 605, self.height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        self.btnOff.draw(self.root)
        if video == "on":
            self.btnRecord.draw(self.root, (0, 0, 255))
        else:
            self.btnRecord.draw(self.root)

        for roi in self.gui.rois:
            roi.draw(self.root)

    def __mouseEvent(self):
        """ Called by constructor to set-up mouse callbacks. """
        def event(e, x, y, flags, param):
            if e == cv2.EVENT_MOUSEMOVE:
                self.__mouseMove(x, y)
            elif e == cv2.EVENT_LBUTTONDOWN:
                self.__leftMouseButtonDown(x, y)

        cv2.setMouseCallback('Fotopasca', event)

    def __leftMouseButtonDown(self, x, y):
        if self.btnOff.mouseClick(x, y):
            self.gui.STATE = self.gui.ROI_STATE
        if self.btnRecord.mouseClick(x, y):
            self.gui.manager.recorder.toggle()

    def __mouseMove(self, x, y):
        self.btnOff.mouseHover(x, y)
        self.btnRecord.mouseHover(x, y)


