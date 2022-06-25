from PySide6.QtGui import *
from PySide6.QtWidgets import *
from macro_button import MacroButton


class MacroPadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.buttons = []
        self.selected_button = None
        self.is_pressed = False

        self.init_ui()

    def init_ui(self):
        grid = QGridLayout(self)

        for i in range(9):
            row = i // 3
            col = i % 3
            button = MacroButton(row, col)
            button.clicked.connect(self.button_clicked)
            grid.addWidget(button, row + 1, col + 1)
            grid.setRowStretch(row + 1, 0)
            grid.setColumnStretch(col + 1, 0)
            self.buttons.append(button)

        grid.setRowStretch(0, 1)
        grid.setColumnStretch(0, 1)
        grid.setRowStretch(4, 1)
        grid.setColumnStretch(4, 1)

    def button_clicked(self, row, col):
        index = row * 3 + col
        if self.selected_button is not None:
            self.selected_button.release()
        self.selected_button = self.buttons[index]
        self.selected_button.click()
        print(f'Clicked! ({row}, {col})')

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.is_pressed = True

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if self.is_pressed:
            if self.selected_button is not None:
                self.selected_button.release()
            self.selected_button = None
        self.is_pressed = False
