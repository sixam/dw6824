from ui import ui
from PyQt4 import QtCore, QtGui
import sys
from rpc import server

if __name__ == '__main__':
    # init QtGUI
    app = QtGui.QApplication(sys.argv)

    # init RPC server
    server = server.Server('localhost',8000)

    sys.exit(app.exec_())

