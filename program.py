from dataclasses import dataclass
from typing import Optional
from PyQt6.QtCore import QPoint, QPropertyAnimation, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

def load_image(path):
    label = QLabel()
    label.setPixmap(QPixmap(path))
    return label

class Fnoof(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

app = QApplication([])

window = Fnoof()

window.show()

app.exec()
