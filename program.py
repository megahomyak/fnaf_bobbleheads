from PyQt6 import QtCore
from PyQt6.QtCore import QPoint, QPropertyAnimation, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QSizePolicy
from threading import Event, Thread
import time
from io import BytesIO
import librosa
import soundcard
import soundfile

class Fnoof(QMainWindow):
    nod_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # self.setWindowFlag(Qt.WindowType.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.old_pointer_position = None

        image_size = QPixmap("images/foreground.png").size()
        self.win_width = 300
        self.win_height = int(image_size.height() / image_size.width() * self.win_width)

        self.bodies = self.image_label("images/bodies.png")
        self.heads = self.image_label("images/heads.png")
        self.foreground = self.image_label("images/foreground.png")

        self.nodding_stopper = Event()

        self.RECORDING_TIME = 5 # In seconds

        self.animation = QPropertyAnimation()

        x, y = 0, 0
        self.setGeometry(x, y, self.win_width, self.win_height)

        self.nod_signal.connect(self.nod)

    @QtCore.pyqtSlot(int)
    def nod(self, duration):
        print("nod", duration)
        print(time.time())
        self.heads.move(0, 0)
        self.animation = QPropertyAnimation(self.heads, b"pos")
        self.animation.setEndValue(self.heads.pos() + QPoint(0, 20))
        self.animation.setDuration(duration)
        self.animation.finished.connect(lambda: self.unnod(duration))
        self.animation.start()

    def unnod(self, duration):
        print("unnod", duration)
        self.animation = QPropertyAnimation(self.heads, b"pos")
        self.animation.setEndValue(self.heads.pos() + QPoint(0, -20))
        self.animation.setDuration(duration)
        self.animation.start()

    def image_label(self, path):
        label = QLabel(self)
        label.setGeometry(0, 0, self.win_width, self.win_height)
        pixmap = QPixmap(path).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        label.setPixmap(pixmap)
        return label

    def update_nods(self):
        SAMPLE_RATE = 48000
        recording = BytesIO()
        measure_time = time.time()
        with soundcard.get_microphone(
                id=str(soundcard.default_speaker().name),
                include_loopback=True
        ).recorder(samplerate=SAMPLE_RATE) as mic:
            data = mic.record(numframes=SAMPLE_RATE * self.RECORDING_TIME)
            soundfile.write(file=recording, data=data[:, 0], samplerate=SAMPLE_RATE, format="wav")
        recording.seek(0)

        waveform, sample_rate = librosa.load(recording)
        tempo, beat_frames = librosa.beat.beat_track(y=waveform, sr=sample_rate)
        beat_times = librosa.frames_to_time(frames=beat_frames, sr=sample_rate)

        self.nodding_stopper.set()
        nodding_stopper = Event()
        self.nodding_stopper = nodding_stopper

        if tempo:
            seconds_per_beat = 60 / tempo

            first_beat_time = measure_time + beat_times[0]

            Thread(target=lambda: self.run_nodding_thread(
                first_beat_time, seconds_per_beat, nodding_stopper
            )).start()

    def run_nodding_thread(self, first_beat_time, seconds_per_beat, nodding_stopper):
        while True:
            if nodding_stopper.is_set():
                break
            current_time = time.time()
            diff = current_time - first_beat_time
            print(current_time, first_beat_time, seconds_per_beat)
            wait_time = diff % seconds_per_beat
            time.sleep(wait_time)
            nod_interval = int(seconds_per_beat * 1000 // 2)
            self.nod_signal.emit(nod_interval)

    def mousePressEvent(self, event):
        self.old_pointer_position = event.pos()

    def mouseMoveEvent(self, event):
        new_pointer_position = event.pos()
        difference = QPoint(new_pointer_position - self.old_pointer_position + self.pos())
        self.move(difference)

app = QApplication([])
window = Fnoof()
window.show()

def update_nods_regularly():
    ESTIMATED_PROCESSING_DELAY = 1 # In seconds
    while True:
        Thread(target=window.update_nods).start()
        time.sleep(window.RECORDING_TIME - ESTIMATED_PROCESSING_DELAY)

Thread(target=update_nods_regularly).start()
app.exec()
