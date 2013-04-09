from PyQt4 import QtCore, QtGui
from utils.utils import utils
import sys
from rpc.peer import Peer

if __name__ == '__main__':
    # init QtGUI
    config = utils.getConfig()
    app = QtGui.QApplication(sys.argv)

    # init node 
    ip = config.get(sys.argv[1],'ip');
    port = int(config.get(sys.argv[1],'port'))
    peer = Peer(ip,port)

    sys.exit(app.exec_())

