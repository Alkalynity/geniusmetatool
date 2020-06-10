from PyQt5 import QtWidgets
from meta_gui import Ui_App
import sys


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_App()
        self.ui.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    application.setFixedSize(application.size())
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
