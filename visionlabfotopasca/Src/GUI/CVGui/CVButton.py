import cv2


class CVButton:

    def __init__(self, ux: int, uy: int, dx: int, dy: int, text: str, pleft: int):
        self.hover: bool = False
        self.ux: int = ux
        self.dx: int = dx
        self.uy: int = uy
        self.dy: int = dy
        self.text: str = text
        self.pLeft: int = pleft
        self.pTop: int = int((dy - uy) * 0.675)

    def draw(self, root):
        if self.hover:
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 0, 0), -1)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (255, 255, 255), 2)
            cv2.putText(root, self.text, (self.ux + self.pLeft, self.uy + self.pTop), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (255, 255, 255), -1)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 0, 0), 2)
            cv2.putText(root, self.text, (self.ux + self.pLeft, self.uy + self.pTop), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 0), 1, cv2.LINE_AA)

    def mouseHover(self, x: int, y: int):
        self.hover = self.ux <= x <= self.dx and self.uy <= y <= self.dy

    def mouseClick(self, x: int, y: int):
        return self.ux <= x <= self.dx and self.uy <= y <= self.dy
