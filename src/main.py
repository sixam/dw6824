from PyQt4 import QtCore, QtGui
from dp.src.utils.utils import utils
import sys
from dp.src.rpc.peer import Peer
import datetime

if __name__ == '__main__':
    # init QtGUI
    n = datetime.datetime.now().__str__()
    config = utils.getConfig()
    local_id = sys.argv[1]
    #sys.stdout = open(utils.getLogPath('mainlog',local_id),'a')
    #sys.stderr = open(utils.getLogPath('errorlog',local_id),'a')

    print "New Run: %s\n" % n
    sys.stderr.write("New Run: %s\n" % n)
    app = QtGui.QApplication(sys.argv)

    # init node 

    ip = config.get(local_id,'ip')
    port = int(config.get(local_id,'port'))
    peer = Peer(ip,port)

    if len(sys.argv) >= 3:
        for i in range(2,len(sys.argv)):
            remote_id = sys.argv[i]
            ip_r   = config.get(remote_id,'ip')
            port_r = int(config.get(remote_id,'port'))
            peer.addPeer(ip_r,port_r)

    sys.exit(app.exec_())

