import cv2

from Src.Configuration.conf import RegionOfInterest, Point
from Src.GUI.CVGui.CVButton import CVButton
from Src.GUI.CVGui.CVRoi import CVRoi
from Src.GUI.CVGui.CVWindow import CVWindow


class RoiWindow(CVWindow):

    def __init__(self, gui):
        super().__init__(gui)
        self.drawing = False
        self.btnDel = CVButton(self.width - 450, self.height - 60, self.width - 320, self.height - 20, 'Delete', 26)
        self.btnConfig = CVButton(self.width - 300, self.height - 60, self.width - 170, self.height - 20, 'Config', 25)
        self.btnOn = CVButton(self.width - 150, self.height - 60, self.width - 20, self.height - 20, 'ON', 46)
        self.loadRois()
        self.new = CVRoi()
        self.sel = None
        self.mouseEvent()

    def loop(self, frame):
        self.root = frame
        self.prepareFrame()
        self.drawUI()
        cv2.imshow('PhotoTrap', self.root)

    def prepareFrame(self):
        self.root = cv2.resize(self.root, (self.width, self.height))

    def drawUI(self):
        cv2.rectangle(self.root, (0, self.height - 80), (self.width, self.height), (50, 50, 50), -1)
        cv2.putText(self.root, 'Terminate the app with Q...', (20, self.height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        if self.sel is not None:
            self.btnDel.draw(self.root)
            info = "ux:" + str(self.sel.ux) + " uy:" + str(self.sel.uy) + " dx:" + str(self.sel.dx) + " dy:" + str(self.sel.dy)
            cv2.putText(self.root, info, (20, self.height - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        self.new.draw(self.root)
        for roi in self.rois:
            if roi == self.sel:
                roi.draw(self.root, sel=True)
            else:
                roi.draw(self.root)
        self.btnConfig.draw(self.root)
        self.btnOn.draw(self.root)

    def loadRois(self):
        self.rois = list()
        for roi in self.gui.config.regions_of_interest:
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
        self.gui.config.regions_of_interest = regions

    def mouseEvent(self):
        def event(e, x, y, flags, param):
            if e == cv2.EVENT_MOUSEMOVE:
                self.mouseMove(x, y)
            elif e == cv2.EVENT_LBUTTONDOWN:
                self.leftMouseButtonDown(x, y)
            elif e == cv2.EVENT_LBUTTONUP:
                self.leftMouseButtonUp()
            elif e == cv2.EVENT_LBUTTONDBLCLK:
                self.leftMouseButtonDoubleClick(x, y)

        cv2.setMouseCallback('PhotoTrap', event)

    def leftMouseButtonDown(self, x, y):
        if self.btnConfig.mouseClick(x, y):
            self.saveRois()
            self.gui.STATE = self.gui.CONFIG_STATE

        elif self.btnOn.mouseClick(x, y):
            self.saveRois()
            self.gui.STATE = self.gui.RUNTIME_STATE

        elif self.btnDel.mouseClick(x, y):
            if self.sel is not None:
                self.rois.remove(self.sel)
                self.sel = None

        else:
            self.drawing = True
            self.new.ux = self.new.dx = x
            self.new.uy = self.new.dy = y

    def leftMouseButtonUp(self):
        if self.new.isValid():
            self.rois.append(self.new)
            self.new = CVRoi()
        self.drawing = False

    def leftMouseButtonDoubleClick(self, x, y):
        self.sel = None
        for roi in reversed(self.rois):
            if roi.isInside(x, y):
                self.sel = roi
                break

    def mouseMove(self, x, y):
        self.btnConfig.mouseHover(x, y)
        self.btnOn.mouseHover(x, y)
        self.btnDel.mouseHover(x, y)
        if self.drawing:
            self.new.dx = x
            self.new.dy = y