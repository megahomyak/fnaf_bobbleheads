from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QSizePolicy

class Fnoof(QMainWindow):

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
        x, y = 0, 0

        self.nod_duration_one_way = 200

        self.animation = QPropertyAnimation()

        self.setGeometry(x, y, self.win_width, self.win_height)

    def nod(self):
        self.animation.stop()
        self.heads.move(0, 0)
        self.animation = QPropertyAnimation(self.heads, b"pos")
        self.animation.setEndValue(self.heads.pos() + QPoint(0, 20))
        self.animation.setDuration(self.nod_duration_one_way)
        self.animation.finished.connect(self.unnod)
        self.animation.start()

    def unnod(self):
        self.animation = QPropertyAnimation(self.heads, b"pos")
        self.animation.setEndValue(self.heads.pos() + QPoint(0, -20))
        self.animation.setDuration(self.nod_duration_one_way)
        self.animation.start()

    def image_label(self, path):
        label = QLabel(self)
        label.setGeometry(0, 0, self.win_width, self.win_height)
        pixmap = QPixmap(path).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        label.setPixmap(pixmap)
        return label

    def mousePressEvent(self, event):
        self.nod()
        self.old_pointer_position = event.pos()

    def mouseMoveEvent(self, event):
        new_pointer_position = event.pos()
        difference = QPoint(new_pointer_position - self.old_pointer_position + self.pos())
        self.move(difference)

app = QApplication([])
window = Fnoof()
window.show()
app.exec()
