from PySide6.QtGui import *
from PySide6.QtWidgets import *
from macro_pad_widget import MacroPadWidget
from keyboard_widget import KeyboardWidget


class MainWidget(QSplitter):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        
        top_frame = MacroPadWidget()
        bottom_frame = self.create_macro_tabs()

        self.addWidget(top_frame)
        self.addWidget(bottom_frame)
        self.setSizes([100, 200])
        self.setChildrenCollapsible(False)

    @staticmethod
    def create_macro_tabs():
        bottom_frame = QTabWidget()
        bottom_frame.addTab(KeyboardWidget(), 'Keyboard')
        bottom_frame.addTab(QWidget(), 'Macro Recorder')

        return bottom_frame
