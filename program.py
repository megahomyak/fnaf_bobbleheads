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
        self.bodies = self.image_label("images/bodies.png")
        self.heads = self.image_label("images/heads.png")
        self.foreground = self.image_label("images/foreground.png")
        width = 300
        height = int(self.bodies.pixmap().height() / self.bodies.pixmap().width() * width)
        x, y = 0, 0
        self.setGeometry(x, y, width, height)
        self.animation = QPropertyAnimation(self.heads, b"pos")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setEndValue(self.heads.pos() + QPoint(0, 100))
        self.animation.setDuration(1500)
        self.animation.start()

    def image_label(self, path):
        label = QLabel(self)
        label.setGeometry(0, 0, 300, 238)
        pixmap = QPixmap(path).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        label.setPixmap(pixmap)
        return label

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
