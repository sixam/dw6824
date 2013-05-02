from PyQt4 import QtCore, QtGui
import sys
from rpc.peer import Peer
import datetime

if __name__ == '__main__':
    # init QtGUI
    app = QtGui.QApplication(sys.argv)

    # init node 
    peer = Peer()

    sys.exit(app.exec_())
