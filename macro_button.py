import os
from PySide6 import QtCore
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from custom_events import MacroButtonClicked


class MacroButton(QLabel):
    def __init__(self, row, col):
        super().__init__()
        self._button_width = 96
        self.macro_button_clicked = MacroButtonClicked()
        self.clicked = self.macro_button_clicked.clicked

        self.regular_image = QPixmap(os.path.normpath(os.path.join('images', 'keycap.png')))
        self.regular_image = self.regular_image.scaledToWidth(self._button_width)
        self.hovered_image = QPixmap(os.path.normpath(os.path.join('images', 'keycap-hover.png')))
        self.hovered_image = self.hovered_image.scaledToWidth(self._button_width)
        self.idle_image = self.regular_image

        self.setMouseTracking(True)
        self.row = row
        self.col = col
        self.setPixmap(self.regular_image)

        self.setMaximumSize(QtCore.QSize(self._button_width, self._button_width))

        self.is_pressed = False

    def click(self):
        self.idle_image = self.hovered_image
        self.setPixmap(self.idle_image)

    def release(self):
        self.idle_image = self.regular_image
        self.setPixmap(self.idle_image)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setPixmap(self.hovered_image)
        return super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.setPixmap(self.idle_image)
        return super().leaveEvent(event)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.is_pressed = True

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if self.is_pressed:
            self.clicked.emit(self.row, self.col)
        self.is_pressed = False
