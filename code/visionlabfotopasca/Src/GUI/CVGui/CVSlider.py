import cv2


class CVSlider:
    """ Custom implementation of a slider for openCV based GUI. """

    def __init__(self, lx: int, ly: int, rx: int, ry: int):
        """
        Slider constructor.

        :param lx: top-left x-coordinate
        :param ly: top-left y-coordinate
        :param rx: bottom-right x-coordinate
        :param ry: bottom-right y-coordinate
        """
        self.hover: bool = False
        self.active: bool = False
        self.lx: int = lx
        self.rx: int = rx
        self.ly: int = ly
        self.ry: int = ry

        self.ux: int = lx + (rx - lx) // 3
        self.dx: int = self.ux + 16
        self.uy: int = ly - 16
        self.dy: int = ry + 16

    def draw(self, root):
        """
        Re-draw function of the slider. Call this every frame to update the look of this slider.

        :param root: cv2 root (ie. an image/frame of video) where the slider will be drawn
        """
        if self.active:
            cv2.line(root, (self.lx, self.ly), (self.rx, self.ry), (0, 0, 0), 10)
            cv2.line(root, (self.lx, self.ly), (self.rx, self.ry), (255, 255, 255), 4)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 0, 0), -1)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (255, 255, 255), 2)
        else:
            cv2.line(root, (self.lx, self.ly), (self.rx, self.ry), (0, 0, 0), 10)
            cv2.line(root, (self.lx, self.ly), (self.rx, self.ry), (255, 255, 255), 4)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (255, 255, 255), -1)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 0, 0), 2)

    def mouseMove(self, x: int, y: int, sel):
        """
        Mouse move callback of parent window should call this when event occurs.
        Slider value updates when it is active.

        :param x: x-coordinate of the mouse move event
        :param y: y-coordinate of the mouse move event
        :param sel: reference to the selected region of interest, its sensitivity is updated accordingly
        """
        if self.active:
            self.ux = x - 8
            self.dx = x + 8
            if self.ux < self.lx:
                self.ux = self.lx
                self.dx = self.ux + 16
            if self.dx > self.rx:
                self.dx = self.rx
                self.ux = self.dx - 16
            sel.sensitivity = self.getValue()

    def mouseClick(self, x: int, y: int):
        """
        Returns a boolean, whether a button click event was inside of this slider.

        :param x: x-coordinate of the click event
        :param y: y-coordinate of the click event
        :return: whether click occurred inside of this slider
        """
        return self.ux <= x <= self.dx and self.uy <= y <= self.dy

    def setValue(self, val):
        """
        Sets a new value for this slider.

        :param val: New value in the range of 0-100.
        """
        length = self.rx - self.lx - 16
        pos = int(length / 100 * val)
        self.ux = self.lx + pos
        self.dx = self.lx + 16 + pos

    def getValue(self):
        """ Gets the value of this slider, 0-100 range. """
        length = self.rx - self.lx - 16
        pos = self.ux - self.lx
        return int((pos/length) * 100)

