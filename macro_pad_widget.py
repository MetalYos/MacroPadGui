from PySide6.QtGui import *
from PySide6.QtWidgets import *
from macro_button import MacroButton
from pubsub import Events, pubsub_service

class MacroPadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.buttons = []
        self.selected_button = None
        self.is_pressed = False

        self.macro_pad_status_label = None
        self.macro_pad_bind_button = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.create_macro_pad_status_widget(main_layout)
        self.create_macro_pad_widget(main_layout)
        self.create_macro_pad_controll_widget(main_layout)
        self.setLayout(main_layout)

    def create_macro_pad_status_widget(self, main_layout):
        macro_pad_status_widget = QWidget(self)
        layout = QVBoxLayout(macro_pad_status_widget)

        self.macro_pad_status_label = QLabel(macro_pad_status_widget)

        layout.addWidget(self.macro_pad_status_label)
        macro_pad_status_widget.setLayout(layout)

        main_layout.addWidget(macro_pad_status_widget)

    def create_macro_pad_widget(self, main_layout):
        macro_pad_widget = QWidget(self)
        grid = QGridLayout(macro_pad_widget)

        for i in range(9):
            row = i // 3
            col = i % 3
            button = MacroButton(row, col)
            button.clicked.connect(self.macro_pad_button_clicked)
            grid.addWidget(button, row + 1, col + 1)
            grid.setRowStretch(row + 1, 0)
            grid.setColumnStretch(col + 1, 0)
            self.buttons.append(button)

        grid.setRowStretch(0, 1)
        grid.setColumnStretch(0, 1)
        grid.setRowStretch(4, 1)
        grid.setColumnStretch(4, 1)

        macro_pad_widget.setLayout(grid)
        main_layout.addWidget(macro_pad_widget)

    def create_macro_pad_controll_widget(self, main_layout):
        macro_pad_controll_widget = QWidget(self)
        macro_pad_controll_layout = QHBoxLayout(macro_pad_controll_widget)

        self.macro_pad_bind_button = QPushButton('Bind', macro_pad_controll_widget)
        self.macro_pad_bind_button.clicked.connect(self.macro_pad_bind_button_clicked)
        self.macro_pad_bind_button.setEnabled(False)
        self.macro_pad_bind_button.setMinimumHeight(60)

        macro_pad_controll_layout.addWidget(self.macro_pad_bind_button)
        macro_pad_controll_widget.setLayout(macro_pad_controll_layout)
        main_layout.addWidget(macro_pad_controll_widget)

    def macro_pad_button_clicked(self, row, col):
        index = row * 3 + col
        if self.selected_button is not None:
            self.selected_button.release()
        self.selected_button = self.buttons[index]
        self.selected_button.click()

        self.macro_pad_bind_button.setEnabled(True) 

        pubsub_service.subscribe(Events.EVENT_KEYBOARD_KEY_SELECTED, 
                                 self.keyboard_key_selected_event_handler)

        
        label_text = f'Macro Pad Key ({row}, {col}) selected.'
        if self.selected_button.selected_key is not None:
            label_text += f' Key is binded to {self.selected_button.selected_key}.'
        self.macro_pad_status_label.setText(label_text)

        pubsub_service.publish(Events.EVENT_MACRO_BUTTON_SELECTED, self.selected_button)

    def macro_pad_bind_button_clicked(self):
        pubsub_service.publish(Events.EVENT_BIND_BUTTON_CLICKED, self.selected_button)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.is_pressed = True

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if self.is_pressed:
            if self.selected_button is not None:
                self.selected_button.release()
            self.selected_button = None
            self.macro_pad_bind_button.setEnabled(False)
        self.is_pressed = False

    def keyboard_key_selected_event_handler(self, key):
        label_text = f'Macro Pad Key ({self.selected_button.row}, {self.selected_button.col}) selected.'
        if self.selected_button.selected_key is not None:
            label_text += f' Key is binded to {self.selected_button.selected_key}.'
        self.macro_pad_status_label.setText(label_text)

        pubsub_service.unsubscribe(Events.EVENT_KEYBOARD_KEY_SELECTED, 
                                   self.keyboard_key_selected_event_handler)

