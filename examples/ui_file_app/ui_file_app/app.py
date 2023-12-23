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
from PySide6 import QtWidgets

from ui_file_app import ui_form


class Widget(QtWidgets.QWidget, ui_form.Ui_Form):
    def __init__(self):
        super(Widget, self).__init__()
        self.setupUi(self)
        self.submit_button.clicked.connect(self._submit)

    def _submit(self):
        print(f"Your name is: {self.name_lineedit.text()}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Widget()
    win.show()
    sys.exit(app.exec())
