from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

class Fnoof(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # self.setWindowFlag(Qt.WindowType.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.old_pointer_position = None
        self.bodies = QPixmap("images/bodies.png")
        self.heads = QPixmap("images/heads.png")
        self.foreground = QPixmap("images/foreground.png")
        width = 300
        height = int(self.bodies.height() / self.bodies.width() * width)
        x, y = 0, 0
        self.setGeometry(x, y, width, height)
        self.setProperty("heads_y", 0)
        self.animation = QPropertyAnimation(self, b"heads_y")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setEndValue(-100)
        self.animation.setDuration(1500)
        self.animation.start()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        heads_rect = self.rect()
        print(self.property("heads_y"))
        heads_rect.setY(heads_rect.y() + self.property("heads_y"))
        painter.drawPixmap(self.rect(), self.bodies)
        painter.drawPixmap(heads_rect, self.heads)
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
