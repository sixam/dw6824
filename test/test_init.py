import unittest
import sys
import datetime
import time

from PyQt4 import QtCore, QtGui

from dp.src.utils.utils import Utils
from dp.src.rpc.peer import Peer
from dp.src.ui.stroke import Stroke
from dp.src.rpc.clerk import Clerk



class TestSimple(unittest.TestCase):
    """simple test"""

    def setUp(self):
        # NOTE : problem with ports
        config = Utils.getConfig()
        servers = ['local1','local2']
        self.peers = []

        app = QtGui.QApplication(sys.argv)

        for server in servers:
            local_id = server
            ip = config.get(local_id,'ip')
            port = int(config.get(local_id,'port'))
            id = int(config.get(local_id,'id'));
            noUI = False
            build_ui = False
            peer = Peer(ip,port, id,build_ui)
            print 'added',peer
            for server2 in servers:
                if server2 != server:
                    remote_id = server2
                    ip_r   = config.get(remote_id,'ip')
                    port_r = int(config.get(remote_id,'port'))
                    peer.addPeer(ip_r,port_r)
            self.peers.append(peer)

    def tearDown(self):
        pass


# Test basic add/move/delete strokes
    def test_basic(self):
        s1 = Stroke(path=[[10,10],[10,20]])
        print s1
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)

        ck1.addStroke(s1)
        print ck1

        time.sleep(1)
        print 'waited'
        print 'incorrect ordering, got: wanted:'
        raise NameError('bob')
        pass

# Test concurrent add/move/delete strokes
    def test_concurrent_add_delete(self):
        print 'incorrect ordering, got: wanted:'
        pass

# Test unreliable add/move/delete strokes
    def test_unreliable_add_delete(self):
        print 'incorrect ordering, got: wanted:'
        pass

# Test basic join/leave peers

# Test unreliable join/leave



