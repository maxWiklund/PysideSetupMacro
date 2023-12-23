import sys
from PySide6 import QtGui, QtWidgets

import email_app.icons.qresource


class SendMailWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        self.create_email_button = QtWidgets.QPushButton()
        self.send_email_button = QtWidgets.QPushButton()

        self.create_email_button.setIcon(QtGui.QIcon(":/icons/mail.png"))
        self.send_email_button.setIcon(QtGui.QIcon(":/icons/send.png"))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.create_email_button)
        layout.addWidget(self.send_email_button)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = SendMailWidget()
    win.show()
    sys.exit(app.exec())
