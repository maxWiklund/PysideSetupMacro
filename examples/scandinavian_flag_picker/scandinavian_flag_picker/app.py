# Copyright (C) 2023  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from PySide6 import QtCore, QtGui, QtWidgets

import scandinavian_flag_picker.icons.qresource


class FlagPicker(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        pen_label = QtWidgets.QLabel()
        pen_label.setPixmap(QtGui.QPixmap(":pen.png").scaled(QtCore.QSize(20, 20)))
        self.flags_combobox = QtWidgets.QComboBox()
        for flag_file in QtCore.QDir(":flags").entryList():
            self.flags_combobox.addItem(
                QtGui.QIcon(f":flags/{flag_file}"),
                flag_file.replace(".png", "").capitalize(),
            )

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
