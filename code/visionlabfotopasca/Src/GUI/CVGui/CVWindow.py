import cv2


class CVWindow:
    def __init__(self, gui):
        self.gui = gui
        self.width, self.height = gui.config.system.resolution
        cv2.namedWindow('Fotopasca')
        self.root = None

    def loop(self, frame):
        """
        SystemManager should call this every frame to redraw the GUI.

        :param frame: cv2 frame (ie. an image/frame of video) containing this window
        """
        self.root = frame
        self.drawUI()
        cv2.imshow('Fotopasca', self.root)

    def drawUI(self):
        """Internal method called by loop() drawing the GUI of this window."""
        cv2.rectangle(self.root, (0, self.height - 80), (self.width, self.height), (50, 50, 50), -1)  # bar
        cv2.putText(self.root, 'Zavri s Q...', (20, self.height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
