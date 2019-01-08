import cv2


class CVWindow:
    def __init__(self, gui):
        self.gui = gui
        self.width, self.height = gui.config.system.resolution
        cv2.namedWindow('PhotoTrap')
        self.root = None

    def loop(self, frame):
        """
        SystemManager should call this every frame to redraw the GUI.

        :param frame: cv2 frame (ie. an image/frame of video) containing this window
        """
        return "Not Implemented!"

    def __drawUI(self):
        """Internal method called by loop() drawing the GUI of this window."""
        return "Not Implemented!"

    def __mouseEvent(self):
        """Called by constructor to set-up mouse callbacks."""
        def event(e, x, y, flags, param):
            pass
        cv2.setMouseCallback('PhotoTrap', event)
