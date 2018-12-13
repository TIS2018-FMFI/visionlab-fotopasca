from tkinter import *

from Src.GUI import GUI


class ConfigurationWindow:

    def __init__(self, gui: GUI):
        self.gui: GUI = gui
        self.root = Tk()
        self.root.title("Config")
        self.root.resizable(0, 0)
        self.root.config(bg="lightgray")
        self.setupOptions()
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()

    def setupOptions(self):
        col1 = Frame(self.root, width=200, bg="lightgray")
        col1.grid(row=0, column=0, sticky=E+W)
        col2 = Frame(self.root, width=200, bg="lightgray")
        col2.grid(row=0, column=1, sticky=E+W)
        col3 = Frame(self.root, width=200, bg="lightgray")
        col3.grid(row=0, column=2, sticky=E+W)
        self.cameraOptions()
        self.modeOptions()
        self.alarmOptions()
        self.otherOptions()
        self.buttons()

    def cameraOptions(self):
        label = Label(self.root, text="NASTAVENIA KAMERY", bg="lightgray", pady=20)
        label.grid(row=1, columnspan=3)

        resFrame = Frame(self.root, bg="lightgray")
        resLabel = Label(resFrame, text="rozlíšenie:", bg="lightgray", width=10)
        resLabel.pack(side=LEFT)
        self.resVar = StringVar(self.root)
        resolution = str(self.gui.config.system.resolution[0]) + "x" + str(self.gui.config.system.resolution[1])
        self.resVar.set(resolution)
        self.resolution = OptionMenu(resFrame, self.resVar, "1280x720", "960x540")
        self.resolution.config(bg="lightgray")
        self.resolution.pack(side=LEFT)
        resFrame.grid(row=2, column=0, padx=10, pady=(0,20))

        rateFrame = Frame(self.root, bg="lightgray")
        rateLabel = Label(rateFrame, text="snímkovanie:", bg="lightgray", width=10)
        rateLabel.pack(side=LEFT)
        self.framerate = Scale(rateFrame, from_=10, to=60, orient=HORIZONTAL, resolution=10, bg="lightgray")
        self.framerate.set(self.gui.config.system.fps)
        self.framerate.pack(side=LEFT)
        rateFrame.grid(row=2, column=1, padx=10, pady=(0,20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=3, columnspan=3, sticky=E+W)

    def modeOptions(self):
        label = Label(self.root, text="NASTAVENIA REŽIMU", bg="lightgray", pady=20)
        label.grid(row=4, columnspan=3)

        lapseFrame = Frame(self.root, bg="lightgray")
        lapseLabel = Label(lapseFrame, text="časozber: ", bg="lightgray",  width=10)
        lapseLabel.pack(side=LEFT)
        self.timelapseVar = IntVar()
        self.timelapseVar.set(self.gui.config.timelapse.enabled)
        self.timelapse = Checkbutton(lapseFrame, variable=self.timelapseVar, bg="lightgray")
        self.timelapse.pack(side=LEFT)
        lapseFrame.grid(row=5, column=0, padx=10, pady=(0,20))

        freqFrame = Frame(self.root, bg="lightgray")
        freqLabel = Label(freqFrame, text="frekvencia\nčasozberu:", bg="lightgray",  width=10)
        freqLabel.pack(side=LEFT)
        self.frequency = Scale(freqFrame, from_=1, to=30, orient=HORIZONTAL, resolution=1)
        self.frequency.set(self.gui.config.timelapse.capture_speed)
        self.frequency.pack(side=LEFT)
        self.frequency.config(bg="lightgray")
        freqFrame.grid(row=5, column=1, padx=10, pady=(0,20))

        recordFrame = Frame(self.root, bg="lightgray")
        recordLabel = Label(recordFrame, text="nahrávanie\npri poplachu:", bg="lightgray",  width=10)
        recordLabel.pack(side=LEFT)
        self.recordVar = IntVar()
        self.recordVar.set(self.gui.config.video.enabled)
        self.record = Checkbutton(recordFrame, variable=self.recordVar, bg="lightgray")
        self.record.pack(side=LEFT)
        recordFrame.grid(row=5, column=2, padx=10, pady=(0, 20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=6, columnspan=3, sticky=E+W)

    def alarmOptions(self):
        label = Label(self.root, text="NASTAVENIA ALARMU", bg="lightgray", pady=20)
        label.grid(row=7, columnspan=3)

        alarmFrame = Frame(self.root, bg="lightgray")
        alarmLabel = Label(alarmFrame, text="alarm pri\npoplachu:", bg="lightgray",  width=10)
        alarmLabel.pack(side=LEFT)
        self.alarmVar = IntVar()
        self.alarmVar.set(self.gui.config.alarm.enabled)
        self.alarm = Checkbutton(alarmFrame, variable=self.alarmVar, bg="lightgray")
        self.alarm.pack(side=LEFT)
        alarmFrame.grid(row=8, column=0, padx=10, pady=(0,20))

        delayFrame = Frame(self.root, bg="lightgray")
        delayLabel = Label(delayFrame, text="oneskorenie\nalarmu(s):", bg="lightgray",  width=10)
        delayLabel.pack(side=LEFT)
        self.delay = Scale(delayFrame, from_=1, to=30, orient=HORIZONTAL)
        self.delay.set(self.gui.config.alarm.delay)
        self.delay.config(bg="lightgray")
        self.delay.pack(side=LEFT)
        delayFrame.grid(row=8, column=1, padx=10, pady=(0,20))

        postFrame = Frame(self.root, bg="lightgray")
        postLabel = Label(postFrame, text="doznenie\nalarmu(s):", bg="lightgray",  width=10)
        postLabel.pack(side=LEFT)
        self.post = Scale(postFrame, from_=1, to=30, orient=HORIZONTAL, resolution=1)
        self.post.set(self.gui.config.alarm.duration)
        self.post.config(bg="lightgray")
        self.post.pack(side=LEFT)
        postFrame.grid(row=8, column=2, padx=10, pady=(0,20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=9, columnspan=3, sticky=E+W)

    def otherOptions(self):
        label = Label(self.root, text="OSTATNÉ NASTAVENIA", bg="lightgray", pady=20)
        label.grid(row=10, columnspan=3)

        autoFrame = Frame(self.root, bg="lightgray")
        autoLabel = Label(autoFrame, text="auto štart:", bg="lightgray",  width=10)
        autoLabel.pack(side=LEFT)
        self.autoVar = IntVar()
        self.autoVar.set(self.gui.config.system.skip)
        self.auto = Checkbutton(autoFrame, variable=self.autoVar, bg="lightgray")
        self.auto.pack(side=LEFT)
        autoFrame.grid(row=11, column=0, padx=10, pady=(0,20))

        passFrame = Frame(self.root, bg="lightgray")
        passLabel = Label(passFrame, text="heslo:", bg="lightgray",  width=10)
        passLabel.pack(side=LEFT)
        self.password = Entry(passFrame, width=10)
        self.password.pack(side=LEFT)
        passFrame.grid(row=11, column=1, padx=10, pady=(0,20))

        startDelayFrame = Frame(self.root, bg="lightgray")
        startDelayLabel = Label(startDelayFrame, text="oneskorenie\nštartu(s):", bg="lightgray",  width=10)
        startDelayLabel.pack(side=LEFT)
        self.startDelay = Scale(startDelayFrame, from_=1, to=60, orient=HORIZONTAL)
        self.startDelay.set(self.gui.config.system.initDelay)
        self.startDelay.config(bg="lightgray")
        self.startDelay.pack(side=LEFT)
        startDelayFrame.grid(row=11, column=2, padx=10, pady=(0,20))

        div = Frame(self.root, heigh=3, bg="gray")
        div.grid(row=12, columnspan=3, sticky=E+W)

    def save(self):
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
        self.gui.STATE = self.gui.ROI_STATE
        self.destroy()

    def buttons(self):
        self.save = Button(self.root, text="ulož nastavenia", height=2, width=20, command=self.save)
        self.save.grid(row=13, columnspan=3, padx=10, pady=(20, 8))
        def zobraz():
            print("----------NASTAVENIA----------")
            print("rozlíšenie: " + str(self.resVar.get()))
            print("snímkovanie: " + str(self.framerate.get()))
            print("časozber: " + str(self.timelapseVar.get()))
            print("alarm: " + str(self.alarmVar.get()))
            print("------------------------------")
        self.show = Button(self.root, text="zobraz nastavenia", height=2, width=20, command=zobraz)
        self.show.grid(row=14, columnspan=3, padx=10, pady=(8, 20))

