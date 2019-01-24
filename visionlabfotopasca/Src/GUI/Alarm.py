from os import path
import simpleaudio as sa


class Alarm:
    """ Class for playing a sound alarm. """
    SOUND_FILE = path.join(path.dirname(path.dirname(path.dirname(path.realpath(__file__)))), "res/alarm.wav")

    def __init__(self):
        self.__wave_obj = sa.WaveObject.from_wave_file(self.SOUND_FILE)
        self.__play_obj = None

    def play(self):
        """ Plays one beep of the alarm. """
        if self.__play_obj is None:
            self.__play_obj = self.__wave_obj.play()

        if self.__play_obj.is_playing() is False:
            self.__play_obj = None

    def stop(self):
        """ Stops the alarm immediately. """
        if self.__play_obj is not None and self.__play_obj.is_playing():
            self.__play_obj.stop()
            self.__play_obj = None

