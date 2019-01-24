from tkinter import *

from Src.GUI import GUI


class ConfigurationWindow:
    AVAILABLE_RESOLUTIONS = ["1920x1080", "1600x900", "1366x768", "1280x720", "960x540"]
    """
    Class for tkinter based GUI of the configuration window.
    :param AVAILABLE_RESOLUTIONS : List of resolutions in format "WIDTHxHEIGHT" that will be available.
    """

    def __init__(self, gui: GUI):
        """
        Configuration window constructor.
        :param gui: reference to the parent gui manager
        """
        self.gui: GUI = gui
        self.root = Tk()
        self.root.title("Config")
        self.root.resizable(0, 0)
        self.root.config(bg="lightgray")
        self.__setupOptions()
        self.root.mainloop()

    def __setupOptions(self):
        self.__cameraOptions()
        self.__modeOptions()
        self.__alarmOptions()
        self.__otherOptions()
        self.__buttons()

    def __cameraOptions(self):
        label = Label(self.root, text="NASTAVENIA KAMERY", bg="lightgray", pady=20)
        label.grid(row=0, columnspan=3)

        resFrame = Frame(self.root, bg="lightgray")
        resLabel = Label(resFrame, text="rozlíšenie:", bg="lightgray", width=10)
        resLabel.pack(side=LEFT)
        self.resVar = StringVar(self.root)
        self.resVar.set(str(self.gui.config.system.resolution[0]) + "x" + str(self.gui.config.system.resolution[1]))
        self.resolution = OptionMenu(resFrame, self.resVar, *self.AVAILABLE_RESOLUTIONS)
        self.resolution.config(bg="lightgray")
        self.resolution.pack(side=LEFT)
        resFrame.grid(row=1, column=0, padx=10, pady=(0,20))

        rateFrame = Frame(self.root, bg="lightgray")
        rateLabel = Label(rateFrame, text="snímkovanie\n(fps):", bg="lightgray", width=10)
        rateLabel.pack(side=LEFT)
        self.framerate = Scale(rateFrame, from_=10, to=60, orient=HORIZONTAL, resolution=10, bg="lightgray")
        self.framerate.set(self.gui.config.system.fps)
        self.framerate.pack(side=LEFT)
        rateFrame.grid(row=1, column=1, padx=10, pady=(0,20))

        cutFrame = Frame(self.root, bg="lightgray")
        cutLabel = Label(cutFrame, text="záznam\nvýseku:", bg="lightgray", width=10)
        cutLabel.pack(side=LEFT)
        self.cutVar = IntVar()
        self.cutVar.set(self.gui.config.system.cut)
        self.cut = Checkbutton(cutFrame, variable=self.cutVar, bg="lightgray")
        self.cut.pack(side=LEFT)
        cutFrame.grid(row=1, column=2, padx=10, pady=(0,20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=2, columnspan=3, sticky=E+W)

    def __modeOptions(self):
        label = Label(self.root, text="NASTAVENIA REŽIMU", bg="lightgray", pady=20)
        label.grid(row=3, columnspan=3)

        lapseFrame = Frame(self.root, bg="lightgray")
        lapseLabel = Label(lapseFrame, text="časozber: ", bg="lightgray",  width=10)
        lapseLabel.pack(side=LEFT)
        self.timelapseVar = IntVar()
        self.timelapseVar.set(self.gui.config.timelapse.enabled)
        self.timelapse = Checkbutton(lapseFrame, variable=self.timelapseVar, bg="lightgray")
        self.timelapse.pack(side=LEFT)
        lapseFrame.grid(row=4, column=0, padx=10, pady=(0,20))

        freqFrame = Frame(self.root, bg="lightgray")
        freqLabel = Label(freqFrame, text="frekvencia\nčasozberu(s):", bg="lightgray",  width=10)
        freqLabel.pack(side=LEFT)
        self.frequency = Scale(freqFrame, from_=1, to=30, orient=HORIZONTAL, resolution=1)
        self.frequency.set(self.gui.config.timelapse.capture_speed)
        self.frequency.pack(side=LEFT)
        self.frequency.config(bg="lightgray")
        freqFrame.grid(row=4, column=1, padx=10, pady=(0,20))

        recordFrame = Frame(self.root, bg="lightgray")
        recordLabel = Label(recordFrame, text="nahrávanie\npri poplachu:", bg="lightgray",  width=10)
        recordLabel.pack(side=LEFT)
        self.recordVar = IntVar()
        self.recordVar.set(self.gui.config.video.enabled)
        self.record = Checkbutton(recordFrame, variable=self.recordVar, bg="lightgray")
        self.record.pack(side=LEFT)
        recordFrame.grid(row=4, column=2, padx=10, pady=(0, 20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=5, columnspan=3, sticky=E+W)

    def __alarmOptions(self):
        label = Label(self.root, text="NASTAVENIA ALARMU", bg="lightgray", pady=20)
        label.grid(row=6, columnspan=3)

        alarmFrame = Frame(self.root, bg="lightgray")
        alarmLabel = Label(alarmFrame, text="alarm pri\npoplachu:", bg="lightgray",  width=10)
        alarmLabel.pack(side=LEFT)
        self.alarmVar = IntVar()
        self.alarmVar.set(self.gui.config.alarm.enabled)
        self.alarm = Checkbutton(alarmFrame, variable=self.alarmVar, bg="lightgray")
        self.alarm.pack(side=LEFT)
        alarmFrame.grid(row=7, column=0, padx=10, pady=(0,20))

        delayFrame = Frame(self.root, bg="lightgray")
        delayLabel = Label(delayFrame, text="oneskorenie\nalarmu(s):", bg="lightgray",  width=10)
        delayLabel.pack(side=LEFT)
        self.delay = Scale(delayFrame, from_=0, to=30, orient=HORIZONTAL)
        self.delay.set(self.gui.config.alarm.delay)
        self.delay.config(bg="lightgray")
        self.delay.pack(side=LEFT)
        delayFrame.grid(row=7, column=1, padx=10, pady=(0,20))

        postFrame = Frame(self.root, bg="lightgray")
        postLabel = Label(postFrame, text="doznenie\nalarmu(s):", bg="lightgray",  width=10)
        postLabel.pack(side=LEFT)
        self.post = Scale(postFrame, from_=1, to=30, orient=HORIZONTAL, resolution=1)
        self.post.set(self.gui.config.alarm.duration)
        self.post.config(bg="lightgray")
        self.post.pack(side=LEFT)
        postFrame.grid(row=7, column=2, padx=10, pady=(0,20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=8, columnspan=3, sticky=E+W)

    def __otherOptions(self):
        label = Label(self.root, text="OSTATNÉ NASTAVENIA", bg="lightgray", pady=20)
        label.grid(row=9, columnspan=3)

        autoFrame = Frame(self.root, bg="lightgray")
        autoLabel = Label(autoFrame, text="auto štart:", bg="lightgray",  width=10)
        autoLabel.pack(side=LEFT)
        self.autoVar = IntVar()
        self.autoVar.set(self.gui.config.system.skip)
        self.auto = Checkbutton(autoFrame, variable=self.autoVar, bg="lightgray")
        self.auto.pack(side=LEFT)
        autoFrame.grid(row=10, column=0, padx=10, pady=(0,20))

        startDelayFrame = Frame(self.root, bg="lightgray")
        startDelayLabel = Label(startDelayFrame, text="oneskorenie\nštartu(s):", bg="lightgray",  width=10)
        startDelayLabel.pack(side=LEFT)
        self.startDelay = Scale(startDelayFrame, from_=1, to=60, orient=HORIZONTAL)
        self.startDelay.set(self.gui.config.system.initDelay)
        self.startDelay.config(bg="lightgray")
        self.startDelay.pack(side=LEFT)
        startDelayFrame.grid(row=10, column=1, padx=10, pady=(0,20))

        inputFrame = Frame(self.root, bg="lightgray")
        inputLabel = Label(inputFrame, text="vstup:", bg="lightgray",  width=10)
        inputLabel.pack(side=LEFT)
        self.input = Scale(inputFrame, from_=0, to=2, orient=HORIZONTAL)
        input = self.gui.manager.INPUT
        if type(input) is not int:
            input = 2
        self.input.set(input)
        self.input.config(bg="lightgray")
        self.input.pack(side=LEFT)
        inputFrame.grid(row=10, column=2, padx=10, pady=(0,20))
        # passFrame = Frame(self.root, bg="lightgray")
        # passLabel = Label(passFrame, text="heslo:", bg="lightgray",  width=10)
        # passLabel.pack(side=LEFT)
        # self.password = Entry(passFrame, width=10)
        # self.password.pack(side=LEFT)
        # passFrame.grid(row=10, column=2, padx=10, pady=(0,20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=11, columnspan=3, sticky=E+W)

    def __save(self):
        self.gui.config.system.resolution = tuple(map(int, self.resVar.get().split("x")))
        self.gui.config.system.fps = self.framerate.get()
        self.gui.config.timelapse.enabled = bool(self.timelapseVar.get())
        self.gui.config.timelapse.capture_speed = self.frequency.get()
        self.gui.config.video.enabled = bool(self.recordVar.get())
        self.gui.config.alarm.enabled = bool(self.alarmVar.get())
        self.gui.config.alarm.delay = self.delay.get()
        self.gui.config.alarm.duration = self.post.get()
        self.gui.config.system.skip = bool(self.autoVar.get())
        self.gui.config.system.initDelay = self.startDelay.get()
        self.gui.config.system.cut = bool(self.cutVar.get())
        self.gui.manager.INPUT = self.gui.manager.PATH_TO_VIDEO if self.input.get() == 2 else self.input.get()
        self.gui.STATE = self.gui.ROI_STATE
        self.root.destroy()

    def __buttons(self):
        self.save = Button(self.root, text="ulož nastavenia", height=2, width=20, command=self.__save)
        self.save.grid(row=12, columnspan=3, padx=10, pady=20)

