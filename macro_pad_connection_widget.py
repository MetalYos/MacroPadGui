from PySide6.QtGui import *
from PySide6.QtWidgets import *


class MacroPadConnectionWidget(QWidget):
    def __init__(self, serial_port, parent=None):
        super().__init__(parent)

        self.serial_port = serial_port

        hbox = QHBoxLayout(self)
        hbox.addWidget(QLabel('Macro Pad:'))

        self.connection_label = QLabel('NOT CONNECTED')
        self.connection_label.setStyleSheet('QLabel { color: red }')
        hbox.addWidget(self.connection_label)
        hbox.addStretch()

        connect_btn = QPushButton(text='Connect')
        connect_btn.clicked.connect(self.connect_button_clicked)
        hbox.addWidget(connect_btn)

        disconnect_btn = QPushButton(text='Disconnect')
        disconnect_btn.clicked.connect(self.disconnect_button_clicked)
        hbox.addWidget(disconnect_btn)

        self.setLayout(hbox)

    def connect_button_clicked(self):
        self.serial_port.open()
        if self.serial_port.is_open():
            self.connection_label.setText('CONNECTED')
            self.connection_label.setStyleSheet('QLabel { color: green }')

    def disconnect_button_clicked(self):
        self.serial_port.close()
        if self.serial_port.is_open() is False:
            self.connection_label.setText('NOT CONNECTED')
            self.connection_label.setStyleSheet('QLabel { color: red }')
