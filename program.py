from dataclasses import dataclass
from typing import Optional
from PyQt6.QtCore import QPoint, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

def load_image(path):
    label = QLabel()
    label.setPixmap(QPixmap(path))
    return label

class Fnoof(QMainWindow):

    def __init__(self):
        super().__init__()

        self.head_anims = []

        for 
        anim = QPropertyAnimation(self.child, b"pos")
        anim.setEndValue(QPoint(400, 400))
        anim.setDuration(1500)
        anim.start()

app = QApplication([])

window
