from PyQt4 import QtCore, QtGui
import sys
from rpc.peer import Peer

if __name__ == '__main__':
    # init QtGUI
    app = QtGui.QApplication(sys.argv)

    # init node 
    peer = Peer('localhost',8000)

    sys.exit(app.exec_())

