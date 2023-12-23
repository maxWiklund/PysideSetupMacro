import sys
from PySide6 import QtCore, QtGui, QtWidgets

import skandinavia_flag_picker.icons.qresource


class FlagPicker(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        pen_label = QtWidgets.QLabel()
        pen_label.setPixmap(QtGui.QPixmap(":pen.png").scaled(QtCore.QSize(20, 20)))
        self.flags_combobox = QtWidgets.QComboBox()
        for flag_file in QtCore.QDir(":flags").entryList():
            self.flags_combobox.addItem(QtGui.QIcon(f":flags/{flag_file}"), flag_file.replace(".png", "").capitalize())

        self.flags_combobox.setCurrentText("Sweden")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pen_label)
        layout.addWidget(self.flags_combobox)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = FlagPicker()
    win.show()
    sys.exit(app.exec())
