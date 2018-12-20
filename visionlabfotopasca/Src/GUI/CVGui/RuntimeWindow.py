import cv2
from Src.GUI.CVGui.CVButton import CVButton
from Src.GUI.CVGui.CVWindow import CVWindow


class RuntimeWindow(CVWindow):

    def __init__(self, gui):
        super().__init__(gui)
        self.btnRecord = CVButton(self.width - 300, self.height - 60, self.width - 170, self.height - 20, 'Record', 23)
        self.btnOff = CVButton(self.width - 150, self.height - 60, self.width - 20, self.height - 20, 'OFF', 42)
        self.mouseEvent()

    def loop(self, frame):
        self.root = frame
        self.drawUI()
        cv2.imshow('PhotoTrap', self.root)

    def drawUI(self):
        cv2.rectangle(self.root, (0, self.height - 80), (self.width, self.height), (50, 50, 50), -1)  # bar
        cv2.putText(self.root, 'Q pre zavretie...', (20, self.height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        self.btnOff.draw(self.root)
        self.btnRecord.draw(self.root)
        for roi in self.gui.rois:
            roi.draw(self.root)

    def mouseEvent(self):
        def event(e, x, y, flags, param):
            if e == cv2.EVENT_MOUSEMOVE:
                self.mouseMove(x, y)
            elif e == cv2.EVENT_LBUTTONDOWN:
                self.leftMouseButtonDown(x, y)

        cv2.setMouseCallback('PhotoTrap', event)

    def leftMouseButtonDown(self, x, y):
        if self.btnOff.mouseClick(x, y):
            self.gui.STATE = self.gui.ROI_STATE
        if self.btnRecord.mouseClick(x, y):
            self.gui.manager.recorder.toggle()

    def mouseMove(self, x, y):
        self.btnOff.mouseHover(x, y)
        self.btnRecord.mouseHover(x, y)


