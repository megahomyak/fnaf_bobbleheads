from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

class Fnoof(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # self.setWindowFlag(Qt.WindowType.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.old_pointer_position = None
        self.bodies = self.image_label("images/bodies.png")
        self.heads = self.image_label("images/heads.png")
        self.foreground = self.image_label("images/foreground.png")
        width = 300
        height = int(self.bodies.height() / self.bodies.width() * width)
        x, y = 0, 0
        self.setGeometry(x, y, width, height)
        self.animation = QPropertyAnimation(self.heads, b"y")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setEndValue(self.heads)
        self.animation.setDuration(1500)
        self.animation.start()

    def image_label(self, path):
        pixmap = QPixmap(path)
        label = QLabel(self)
        label.setPixmap(pixmap)
        return label

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bodies)
        painter.drawPixmap(self.rect(), self.heads)
        painter.drawPixmap(self.rect(), self.foreground)

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
