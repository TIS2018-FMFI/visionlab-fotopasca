import cv2


class CVRoi:

    def __init__(self, color=(0, 255, 0), width: int = 3, sensitivity: int = 50):
        self.x1: int = -1
        self.y1: int = -1
        self.x2: int = -1
        self.y2: int = -1
        self.color = color
        self.width: int = width
        self.sensitivity = sensitivity

    def draw(self, root, sel=False):
        if self.isValid():
            if sel:
                cv2.rectangle(root, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 255), 3)
            else:
                cv2.rectangle(root, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 0), 3)

    def isValid(self):
        return self.x1 != self.x2 and self.y1 != self.y2

    def isInside(self, x, y):
        if self.x1 <= self.x2 and self.y1 <= self.y2:
            return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
        elif self.x1 <= self.x2 and self.y1 >= self.y2:
            return self.x1 <= x <= self.x2 and self.y1 >= y >= self.y2
        elif self.x1 >= self.x2 and self.y1 <= self.y2:
            return self.x1 >= x >= self.x2 and self.y1 <= y <= self.y2
        else:
            return self.x1 >= x >= self.x2 and self.y1 >= y >= self.y2

