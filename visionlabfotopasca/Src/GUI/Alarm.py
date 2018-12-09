
import simpleaudio as sa


class Alarm:
    SOUND_FILE = "../../res/alarm.wav"

    def __init__(self):
        self.__wave_obj = sa.WaveObject.from_wave_file(self.SOUND_FILE)
        self.__play_obj = None

    def play(self):
        if self.__play_obj is None:
            self.__play_obj = self.__wave_obj.play()

        if self.__play_obj.is_playing() is False:
            self.__play_obj = None

    def stop(self):
        if self.__play_obj is not None and self.__play_obj.is_playing():
            self.__play_obj.stop()
            self.__play_obj = None
