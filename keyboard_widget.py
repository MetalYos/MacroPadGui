import os
import json
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from pubsub import Events, pubsub_service

class KeyboardLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard_meta = []

        self.keyboard_image = QPixmap(os.path.normpath(os.path.join('images', 'keyboard.png')))
        with open(os.path.normpath(os.path.join('images', 'keyboard_meta.json')), 'r') as f:
            self.keyboard_meta = json.loads(f.read())
        self.setPixmap(self.keyboard_image)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        key = self._get_key_from_mouse_pos(event.pos())
        if key is not None:
            self._draw_selected_key_rect(key)

            # Publish event to indicate that a key was selected
            pubsub_service.publish(Events.EVENT_KEYBOARD_KEY_SELECTED, key)
        else:
            self.keyboard_image = QPixmap(os.path.normpath(os.path.join('images', 'keyboard.png')))
            self.setPixmap(self.keyboard_image)

    def select_key(self, key):
        self._draw_selected_key_rect(key)

    def clear_selected_key(self):
        self.keyboard_image = QPixmap(os.path.normpath(os.path.join('images', 'keyboard.png')))
        self.setPixmap(self.keyboard_image)

    def _get_key_from_mouse_pos(self, mouse_pos):
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()
        for key in self.keyboard_meta:
            x, y, width, height = self.keyboard_meta[key]
            if x <= mouse_x < (x + width) and y <= mouse_y < (y + height):
                return key

    def _draw_selected_key_rect(self, key):
        rect = self.keyboard_meta[key]
        self.keyboard_image = QPixmap(os.path.normpath(os.path.join('images', 'keyboard.png')))

        # create painter instance with pixmap
        painter_instance = QPainter(self.keyboard_image)

        brush = QBrush(QColor(255, 0, 0, 100))
        painter_instance.fillRect(rect[0], rect[1], rect[2], rect[3], brush)

        # set pixmap onto the label widget
        self.setPixmap(self.keyboard_image)


class KeyboardWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard_meta = []

        self.init_ui()

        pubsub_service.subscribe(Events.EVENT_MACRO_BUTTON_SELECTED, 
                                 self.macro_button_selected_event_handler) 
 
    def init_ui(self):
        self. keyboard_label = KeyboardLabel()
        self.setWidget(self.keyboard_label)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter);

    def macro_button_selected_event_handler(self, selected_button):
        if selected_button is not None:
            if selected_button.selected_key is not None:
                self.keyboard_label.select_key(selected_button.selected_key)
            else:
                self.keyboard_label.clear_selected_key()

