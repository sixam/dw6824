import unittest
import sys
import datetime
import time
import random
from threading import Thread

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


    def doStuff(self,ck):
        s1 = Stroke(path=[[10,10],[10,20]])
        print s1
        time.sleep(float(random.randint(1,10))/1000)
        ck.addStroke(s1)

# Test basic add/move/delete strokes
    def test_basic(self):
        s1 = Stroke(path=[[10,10],[10,20]])
        s2 = Stroke(path=[[30,10],[30,20]])
        print s1.path
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)

        t0 = Thread(target=self.doStuff,args=[ck0])
        t0.daemon = True
        t1 = Thread(target=self.doStuff,args=[ck1])
        t1.daemon = True
        
        t0.start()
        t1.start()

        time.sleep(1)

        self.assertEqual(len(p0.state.strokes),2)
        #raise NameError('bob')
        pass

# Test concurrent add/move/delete strokes
    #def test_concurrent_add_delete(self):
        #print 'incorrect ordering, got: wanted:'
        #pass

# Test unreliable add/move/delete strokes
    #def test_unreliable_add_delete(self):
        #print 'incorrect ordering, got: wanted:'
        #pass

# Test basic join/leave peers

# Test unreliable join/leave



