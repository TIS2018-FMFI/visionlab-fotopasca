import cv2


class CVRoi:

    def __init__(self, color=(0, 255, 0), width: int = 3, sensitivity: int = 50):
        self.ux: int = -1
        self.uy: int = -1
        self.dx: int = -1
        self.dy: int = -1
        self.color = color
        self.width: int = width
        self.sensitivity = sensitivity

    def draw(self, root, sel=False):
        if self.isValid():
            if sel:
                cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 255, 255), 3)
            else:
                cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 255, 0), 3)

    def isValid(self):
        return self.ux != self.dx and self.uy != self.dy

    def isInside(self, x, y):
        return self.ux <= x <= self.dx and self.uy <= y <= self.dy

