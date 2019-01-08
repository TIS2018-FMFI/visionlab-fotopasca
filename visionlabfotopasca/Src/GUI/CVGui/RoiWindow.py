import cv2

from Src.GUI.CVGui.CVButton import CVButton
from Src.GUI.CVGui.CVRoi import CVRoi
from Src.GUI.CVGui.CVSlider import CVSlider
from Src.GUI.CVGui.CVWindow import CVWindow


class RoiWindow(CVWindow):
    """
    Class for cv2 based GUI of the region of interest selection window.
    Extends an CVWindow abstract class.
    """

    def __init__(self, gui):
        """
        Construction of the region of interest selection window.

        :param gui: reference to the parent gui manager
        """
        super().__init__(gui)
        self.drawing = False
        self.btnDel = CVButton(self.width - 450, self.height - 60, self.width - 320, self.height - 20, 'Delete', 26)
        self.btnConfig = CVButton(self.width - 300, self.height - 60, self.width - 170, self.height - 20, 'Config', 25)
        self.btnOn = CVButton(self.width - 150, self.height - 60, self.width - 20, self.height - 20, 'ON', 46)
        self.slider = CVSlider(self.width - 605, self.height - 40, self.width - 475, self.height - 40)
        self.new = CVRoi()
        self.sel = None
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
        cv2.rectangle(self.root, (0, self.height - 80), (self.width, self.height), (50, 50, 50), -1)
        cv2.putText(self.root, 'Q pre zavretie...', (20, self.height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        if self.sel is not None:
            self.btnDel.draw(self.root)
            info = "x1:" + str(self.sel.x1) + " y1:" + str(self.sel.y1) + " x2:" + str(self.sel.x2) + " y2:" + str(self.sel.y2)
            cv2.putText(self.root, info, (20, self.height - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        self.new.draw(self.root)
        for roi in self.gui.rois:
            if roi == self.sel:
                roi.draw(self.root, sel=True)
                self.slider.draw(self.root)
            else:
                roi.draw(self.root)
        self.btnConfig.draw(self.root)
        self.btnOn.draw(self.root)

    def __mouseEvent(self):
        """ Called by constructor to set-up mouse callbacks. """
        def event(e, x, y, flags, param):
            if e == cv2.EVENT_MOUSEMOVE:
                self.__mouseMove(x, y)
            elif e == cv2.EVENT_LBUTTONDOWN:
                self.__leftMouseButtonDown(x, y)
            elif e == cv2.EVENT_LBUTTONUP:
                self.__leftMouseButtonUp()
            elif e == cv2.EVENT_LBUTTONDBLCLK:
                self.__leftMouseButtonDoubleClick(x, y)

        cv2.setMouseCallback('PhotoTrap', event)

    def __leftMouseButtonDown(self, x, y):
        if self.btnConfig.mouseClick(x, y):
            self.gui.saveRois()
            self.gui.STATE = self.gui.CONFIG_STATE

        elif self.btnOn.mouseClick(x, y):
            self.gui.saveRois()
            self.gui.STATE = self.gui.RUNTIME_STATE

        elif self.btnDel.mouseClick(x, y):
            if self.sel is not None:
                self.gui.rois.remove(self.sel)
                self.sel = None

        elif self.slider.mouseClick(x, y):
            self.slider.active = True

        else:
            self.drawing = True
            self.new.x1 = self.new.x2 = x
            self.new.y1 = self.new.y2 = y

    def __leftMouseButtonUp(self):
        if self.new.isValid():
            self.gui.rois.append(self.new)
            self.new = CVRoi()
        self.drawing = False
        self.slider.active = False

    def __leftMouseButtonDoubleClick(self, x, y):
        self.sel = None
        for roi in reversed(self.gui.rois):
            if roi.isInside(x, y):
                self.sel = roi
                self.slider.setValue(roi.sensitivity)
                break

    def __mouseMove(self, x, y):
        if x < 0 or y < 0 or x > self.width or y > self.height:
            return
        if self.drawing and y < self.height - 80:
            self.new.x2 = x
            self.new.y2 = y
        self.btnConfig.mouseHover(x, y)
        self.btnOn.mouseHover(x, y)
        self.btnDel.mouseHover(x, y)
        self.slider.mouseMove(x, y, self.sel)
