from ui import ui
from PyQt4 import QtCore, QtGui

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = ui.MainWindow()
    window.show()
    sys.exit(app.exec_())
