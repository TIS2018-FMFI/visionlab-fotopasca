import cv2


class CVSlider:

    def __init__(self, lx: int, ly: int, rx: int, ry: int):
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
        return self.ux <= x <= self.dx and self.uy <= y <= self.dy

    def setValue(self, val):
        print(val)
        length = self.rx - self.lx - 16
        pos = int(length / 100 * val)
        self.ux = self.lx + pos
        self.dx = self.lx + 16 + pos

    def getValue(self):
        length = self.rx - self.lx - 16
        pos = self.ux - self.lx
        return int((pos/length) * 100)

