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

    print "New Run: %s\n" % n
    app = QtGui.QApplication(sys.argv)

    # init node 


#    ip = config.get(local_id,'ip')
#    port = int(config.get(local_id,'port'))
#    id = int(config.get(local_id,'id'));
    build_ui = True
    
    peer = Peer()
    sys.exit(app.exec_())
