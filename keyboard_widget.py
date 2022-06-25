import os
import json
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class KeyboardLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard_meta = []

        self.keyboard_image = QPixmap(os.path.normpath(os.path.join('images', 'keyboard.png')))
        with open(os.path.normpath(os.path.join('images', 'keyboard_meta.json')), 'r') as f:
            self.keyboard_meta = json.loads(f.read())
        self.setPixmap(self.keyboard_image)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        key = self._get_key_from_moise_pos(event.pos())
        if key is not None:
            print(key)
            rect = self.keyboard_meta[key]
            self.keyboard_image = QPixmap(os.path.normpath(os.path.join('images', 'keyboard.png')))

            # create painter instance with pixmap
            painter_instance = QPainter(self.keyboard_image)

            # set rectangle color and thickness
            pen_rectangle = QPen(Qt.red)
            pen_rectangle.setWidth(3)

            # draw rectangle on painter
            painter_instance.setPen(pen_rectangle)
            painter_instance.drawRect(rect[0], rect[1], rect[2], rect[3])

            # set pixmap onto the label widget
            self.setPixmap(self.keyboard_image)
        else:
            self.keyboard_image = QPixmap(os.path.normpath(os.path.join('images', 'keyboard.png')))
            self.setPixmap(self.keyboard_image)

    def _get_key_from_moise_pos(self, mouse_pos):
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()
        for key in self.keyboard_meta:
            x, y, width, height = self.keyboard_meta[key]
            if x <= mouse_x < (x + width) and y <= mouse_y < (y + height):
                return key


class KeyboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard_meta = []

        self.init_ui()

    def init_ui(self):
        grid = QGridLayout(self)

        grid.addWidget(KeyboardLabel(), 1, 1)

        # Define column stretches (0 - spacer, 1 - keyboard, 2 - spacer)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 0)
        grid.setColumnStretch(2, 1)

        # Define row stretches (0 - spacer, 1 - keyboard, 2 - spacer)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 0)
        grid.setRowStretch(2, 1)

        self.setLayout(grid)
