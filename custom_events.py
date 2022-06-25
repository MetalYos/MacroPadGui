from PySide6 import QtCore


class MacroButtonClicked(QtCore.QObject):
    clicked = QtCore.Signal((int, int))

    def __init__(self):
        super().__init__()
