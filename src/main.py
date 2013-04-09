from PyQt4 import QtCore, QtGui
from dp.src.utils.utils import utils
import sys
from dp.src.rpc.peer import Peer

if __name__ == '__main__':
    # init QtGUI
    config = utils.getConfig()
    sys.stdout = open(utils.getLogPath('mainlog'),'a')
    sys.stderr = open(utils.getLogPath('errorlog'),'a')
    app = QtGui.QApplication(sys.argv)

    # init node 

    ip = config.get(sys.argv[1],'ip');
    port = int(config.get(sys.argv[1],'port'))
    peer = Peer(ip,port)

    sys.exit(app.exec_())

