from PyQt4 import QtCore, QtGui
from dp.src.utils.utils import Utils
import sys
from dp.src.rpc.peer import Peer
import datetime
from dp.src.utils.log import Log

if __name__ == '__main__':
    # init QtGUI
    app = QtGui.QApplication(sys.argv)

    # init node 
    peer = Peer()

    sys.exit(app.exec_())
