#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
from dp.src.utils.utils import Utils
import sys
from dp.src.rpc.peer import Peer
import datetime
from dp.src.utils.log import Log


if __name__ == '__main__':
    # init QtGUI
    n = datetime.datetime.now().__str__()
    config = Utils.getConfig()
    local_id = sys.argv[1]

    print "New Run: %s\n" % n
    app = QtGui.QApplication(sys.argv)

    # init node 

    log = Log(local_id)

    ip = config.get(local_id,'ip')
    port = int(config.get(local_id,'port'))
    id = int(config.get(local_id,'id'));
    build_ui = True
    
    peer = Peer(ip, port, id, build_ui, log)
    peer.thaw(id)

    if len(sys.argv) >= 3:
        for i in range(2,len(sys.argv)):
            remote_id = sys.argv[i]
            ip_r   = config.get(remote_id,'ip')
            port_r = int(config.get(remote_id,'port'))
            id_r = int(config.get(remote_id,'id'));
            peer.addPeer(ip_r,port_r)
            peer.thaw(id_r)

    sys.exit(app.exec_())
