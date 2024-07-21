import win32com.client
from threading import Thread


class TTS:
    def __init__(self):
        self.tts = win32com.client.Dispatch("SAPI.SpVoice")
        # self.tts.set_rate(1)  # Sets the speaking rate slightly faster than normal
        # self.tts.set_volume(80)  # Sets the volume to 80%
        self.tts.Speak("")

    def Speak(self, text):
        Thread(target=self.Speak_sync, args=(text,)).start()

    def Speak_sync(self, text):
        self.tts.Speak(text)
