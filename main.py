import time
import pyaudio
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image
import wave


class SoundPlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
        self.playing = False
        self.exit_event = threading.Event()
        self.thread = threading.Thread(target=self.play_sound)
        self.start_playing()  

    def play_sound(self):
        wf = wave.open("beep.wav", 'rb')
        CHUNK = 1024
        data = wf.readframes(CHUNK)
        while not self.exit_event.is_set():
            if self.playing:
                self.stream.write(data)
                data = wf.readframes(CHUNK)
                if data == b'':
                    wf.rewind()
                    data = wf.readframes(CHUNK)
            time.sleep(1)  

    def start_playing(self):
        self.playing = True
        if not self.thread.is_alive():
            self.thread.start()

    def stop_playing(self):
        self.playing = False

    def cleanup(self):
        self.exit_event.set()
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


def on_clicked(icon, item):
    if item == quit_item:
        icon.stop()
        sound_player.cleanup()
    elif item == toggle_item:
        if sound_player.playing:
            sound_player.stop_playing()
        else:
            sound_player.start_playing()



image = Image.open("icon.png")

sound_player = SoundPlayer()

menu = (item('Toggle Sound', on_clicked, default=True),
        item('Quit', on_clicked))

quit_item = menu[1]
toggle_item = menu[0]

icon = pystray.Icon("sound_icon", image, "Sound Player", menu=menu)


icon.run()
