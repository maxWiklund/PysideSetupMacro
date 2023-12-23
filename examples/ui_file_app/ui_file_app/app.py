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
