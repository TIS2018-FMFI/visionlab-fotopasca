from Src.GUI.button import Button
from Src.GUI.window import Window


class RunningWindow(Window):

    onButton: Button = Button()
    offButton: Button = Button()
    recordButton: Button = Button()
    cameraFeed = None