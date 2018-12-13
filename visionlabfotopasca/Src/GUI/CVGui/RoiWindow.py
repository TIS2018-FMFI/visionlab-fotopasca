import cv2

from Src.GUI.CVGui.CVButton import CVButton
from Src.GUI.CVGui.CVRoi import CVRoi
from Src.GUI.CVGui.CVSlider import CVSlider
from Src.GUI.CVGui.CVWindow import CVWindow


class RoiWindow(CVWindow):

    def __init__(self, gui):
        super().__init__(gui)
        self.drawing = False
        self.btnDel = CVButton(self.width - 450, self.height - 60, self.width - 320, self.height - 20, 'Delete', 26)
        self.btnConfig = CVButton(self.width - 300, self.height - 60, self.width - 170, self.height - 20, 'Config', 25)
        self.btnOn = CVButton(self.width - 150, self.height - 60, self.width - 20, self.height - 20, 'ON', 46)
        self.slider = CVSlider(self.width - 605, self.height - 40, self.width - 475, self.height - 40)
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
        cv2.putText(self.root, 'Q pre zavretie...', (20, self.height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        if self.sel is not None:
            self.btnDel.draw(self.root)
            info = "ux:" + str(self.sel.ux) + " uy:" + str(self.sel.uy) + " dx:" + str(self.sel.dx) + " dy:" + str(self.sel.dy)
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
            self.new.ux = self.new.dx = x
            self.new.uy = self.new.dy = y

    def leftMouseButtonUp(self):
        if self.new.isValid():
            self.gui.rois.append(self.new)
            self.new = CVRoi()
        self.drawing = False
        self.slider.active = False

    def leftMouseButtonDoubleClick(self, x, y):
        self.sel = None
        for roi in reversed(self.gui.rois):
            #print("Roi: (" + str(roi.ux) + "," + str(roi.uy) + "), (" + str(roi.dx) + "," + str(roi.dy) + ")")
            #print("Click: " + str(x) + "," + str(y))
            if roi.isInside(x, y):
                self.sel = roi
                self.slider.setValue(roi.sensitivity)
                break

    def mouseMove(self, x, y):
        self.btnConfig.mouseHover(x, y)
        self.btnOn.mouseHover(x, y)
        self.btnDel.mouseHover(x, y)
        self.slider.mouseMove(x, y, self.sel)
        if self.drawing:
            self.new.dx = x
            self.new.dy = y