import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import qdarktheme
from macro_pad_connection_widget import MacroPadConnectionWidget
from main_widget import MainWidget
from serialport import SerialPort
from settings import Settings

settings = Settings()
settings.load_settings()

serial_port = SerialPort(settings["SerialPort"], settings["BaudRate"], settings["SerialTimeout"])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(MacroPadConnectionWidget(serial_port))
        vbox.addWidget(MainWidget(Qt.Vertical))

        program_frame = QWidget(self)
        hbox = QHBoxLayout()
        program_btn = QPushButton(text='Program')
        program_btn.setEnabled(False)
        program_btn.setMinimumWidth(200)
        program_btn.setMinimumHeight(50)
        hbox.addStretch()
        hbox.addWidget(program_btn)
        program_frame.setLayout(hbox)
        vbox.addWidget(program_frame)

        central_widget.setLayout(vbox)

        self.setCentralWidget(central_widget)

        self.setWindowTitle('Macro Pad Controller')
        self.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Apply dark theme to Qt application
    app.setStyleSheet(qdarktheme.load_stylesheet())

    widget = MainWindow()
    sys.exit(app.exec())
