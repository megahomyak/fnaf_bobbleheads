from PyQt6.QtCore import QPoint, Qt
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
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.old_pointer_position = None

    def mousePressEvent(self, event):
        self.old_pointer_position = event.pos()

    def mouseMoveEvent(self, event):
        new_pointer_position = event.pos()
        difference = QPoint(new_pointer_position - self.old_pointer_position + self.pos())
        self.move(difference)

app = QApplication([])

window = Fnoof()

window.show()

app.exec()
