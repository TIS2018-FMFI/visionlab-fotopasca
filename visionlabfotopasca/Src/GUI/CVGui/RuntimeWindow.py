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

    def loop(self, frame):
        """
        SystemManager should call this every frame to redraw the GUI.

        :param frame: cv2 frame (ie. an image/frame of video) containing this window
        """
        self.root = frame
        self.__drawUI()
        cv2.imshow('PhotoTrap', self.root)

    def __drawUI(self):
        """ Internal method called by loop() drawing the GUI of this window. """
        cv2.rectangle(self.root, (0, self.height - 80), (self.width, self.height), (50, 50, 50), -1)  # bar
        cv2.putText(self.root, 'Q pre zavretie...', (20, self.height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        self.btnOff.draw(self.root)
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

        cv2.setMouseCallback('PhotoTrap', event)

    def __leftMouseButtonDown(self, x, y):
        if self.btnOff.mouseClick(x, y):
            self.gui.STATE = self.gui.ROI_STATE
        if self.btnRecord.mouseClick(x, y):
            self.gui.manager.recorder.toggle()

    def __mouseMove(self, x, y):
        self.btnOff.mouseHover(x, y)
        self.btnRecord.mouseHover(x, y)


