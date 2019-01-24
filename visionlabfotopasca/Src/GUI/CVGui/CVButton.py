import cv2


class CVButton:
    """ Custom implementation of button for openCV based GUI. """

    def __init__(self, ux: int, uy: int, dx: int, dy: int, text: str, pleft: int = 0):
        """
        Button constructor.

        :param ux: top-Left X-coordinate
        :param uy: top-Left Y-coordinate
        :param dx: bottom-Right X-coordinate
        :param dy: bottom-Right Y-coordinate
        :param text: text to be displayed on the button (CAUTION: text exceeding the width of button will overflow)
        :param pleft: left inner padding for the offset of text (0 by default)
        """
        self.hover: bool = False
        self.ux: int = ux
        self.dx: int = dx
        self.uy: int = uy
        self.dy: int = dy
        self.text: str = text
        self.pLeft: int = pleft
        self.pTop: int = int((dy - uy) * 0.675)

    def draw(self, root, bg=(255, 255, 255)):
        """
        Re-draw function of the button. Call this every frame to update the hover look of the button.

        :param root: cv2 root (ie. an image/frame of video) where the button will be drawn
        """
        if self.hover:
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 0, 0), -1)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (255, 255, 255), 2)
            cv2.putText(root, self.text, (self.ux + self.pLeft, self.uy + self.pTop), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), bg, -1)
            cv2.rectangle(root, (self.ux, self.uy), (self.dx, self.dy), (0, 0, 0), 2)
            cv2.putText(root, self.text, (self.ux + self.pLeft, self.uy + self.pTop), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 0), 1, cv2.LINE_AA)

    def mouseHover(self, x: int, y: int):
        """
        Mouse move callback of parent window should call this when event occurs.
        Button hover status updates accordingly.

        :param x: x-coordinate of mouse move event
        :param y: y-coordinate of mouse move event
        """
        self.hover = self.ux <= x <= self.dx and self.uy <= y <= self.dy

    def mouseClick(self, x: int, y: int):
        """
        Returns a boolean, whether a button click event was inside of this button.

        :param x: x-coordinate of the click event
        :param y: y-coordinate of the click event
        :return: whether click occurred inside of this button
        """
        return self.ux <= x <= self.dx and self.uy <= y <= self.dy
