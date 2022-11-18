from PySide6.QtGui import *
from PySide6.QtWidgets import *
from macro_pad_widget import MacroPadWidget
from keyboard_widget import KeyboardWidget
from pubsub import pubsub_service, Events


class MainWidget(QSplitter):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

        self.selected_button = None
        
        self.top_frame = MacroPadWidget()
        self.bottom_frame = self.create_macro_tabs()
        self.bottom_frame.setEnabled(False)

        self.addWidget(self.top_frame)
        self.addWidget(self.bottom_frame)
        self.setSizes([100, 300])
        self.setChildrenCollapsible(False)

        pubsub_service.subscribe(Events.EVENT_BIND_BUTTON_CLICKED, 
                                 self.bind_button_clicked_event_handler) 
        pubsub_service.subscribe(Events.EVENT_KEYBOARD_KEY_SELECTED, 
                                 self.keyboard_key_selected_event_handler) 

    @staticmethod
    def create_macro_tabs():
        bottom_frame = QTabWidget()
        bottom_frame.addTab(KeyboardWidget(), 'Keyboard')
        bottom_frame.addTab(QWidget(), 'Macro Recorder')

        return bottom_frame

    def bind_button_clicked_event_handler(self, selected_button):
        print(f'({selected_button.row}, {selected_button.col})')
        self.bottom_frame.setEnabled(True)
        self.top_frame.setEnabled(False)
        self.selected_button = selected_button

    def keyboard_key_selected_event_handler(self, key):
        print(f'{key} was selected!')
        self.bottom_frame.setEnabled(False)
        self.top_frame.setEnabled(True)
        self.selected_button.selected_key = key
