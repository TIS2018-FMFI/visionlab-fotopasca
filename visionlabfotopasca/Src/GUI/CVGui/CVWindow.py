import cv2


class CVWindow:
    def __init__(self, gui):
        self.gui = gui
        self.width, self.height = gui.config.system.resolution
        cv2.namedWindow('PhotoTrap')
        self.root = None

    def loop(self, frame):
        return "Not Implemented!"

    def prepareFrame(self):
        return "Not Implemented!"

    def drawUI(self):
        return "Not Implemented!"

    def mouseEvent(self):
        def event(e, x, y, flags, param):
            pass
        cv2.setMouseCallback('PhotoTrap', event)
