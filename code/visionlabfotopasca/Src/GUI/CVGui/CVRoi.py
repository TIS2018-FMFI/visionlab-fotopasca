import cv2


class CVRoi:
    """ Class for cv2 GUI representation of region of interest. """

    def __init__(self, color=(0, 255, 0), width: int = 3, sensitivity: int = 50):
        """
        Constructs a roi.

        :param color: triplet of RGB values for the color of the border
        :param width: width of the border
        :param sensitivity: sensitivity of this region of interest
        """
        self.x1: int = -1
        self.y1: int = -1
        self.x2: int = -1
        self.y2: int = -1
        self.color = color
        self.width: int = width
        self.sensitivity = sensitivity
        self.ignored = False

    def draw(self, root, sel=False):
        """
        Re-draw function of this region of interest.
        Call this every frame to update the selected-look of this roi.
        :param root: cv2 root (ie. an image/frame of video) where the roi will be drawn
        :param sel: true if this roi is currently selected, false otherwise
        :return:
        """
        if self.isValid():
            if sel:
                cv2.rectangle(root, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 255), 3)
            elif self.ignored:
                cv2.rectangle(root, (self.x1, self.y1), (self.x2, self.y2), (255, 0, 255), 3)
            else:
                cv2.rectangle(root, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 0), 3)

    def isValid(self):
        """
        Check if this region of interest is valid (ie. it's area is > 0)
        :return: true if this roi is valid, else otherwise
        """
        return self.x1 != self.x2 and self.y1 != self.y2

    def isInside(self, x, y):
        """
        Returns a boolean, whether an mouse event was inside of this button.

        :param x: x-coordinate of the mouse event
        :param y: y-coordinate of the mouse event
        :return: whether event occurred within this roi
        """
        if self.x1 <= self.x2 and self.y1 <= self.y2:
            return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
        elif self.x1 <= self.x2 and self.y1 >= self.y2:
            return self.x1 <= x <= self.x2 and self.y1 >= y >= self.y2
        elif self.x1 >= self.x2 and self.y1 <= self.y2:
            return self.x1 >= x >= self.x2 and self.y1 <= y <= self.y2
        else:
            return self.x1 >= x >= self.x2 and self.y1 >= y >= self.y2

