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
        self.ips   = []
        self.ports = []

        app = QtGui.QApplication(sys.argv)

        for server in servers:
            local_id = server
            ip = 'localhost'
            #port = int(config.get(local_id,'port'))
            while True:
                try:
                    port = random.randint(1,8000)
                    id = int(config.get(local_id,'id'));
                    noUI = False
                    build_ui = False
                    peer = Peer(ip,port, id,build_ui)
                    self.peers.append(peer)
                    self.ports.append(port)
                    self.ips.append(ip)
                    break
                except:
                    continue
                
        for i,server in enumerate(servers):
            for j,server2 in enumerate(servers):
                if server2 != server:
                    self.peers[i].addPeer(self.ips[j],self.ports[j])

    def tearDown(self):
        pass


    def doStuff(self,ck):
        s1 = Stroke(path=[[10,10],[10,20]])
        ck.addStroke(s1)
    def assertStrokesEqual(self):
        Pass = True
        strokes = self.peers[0].getStrokes()
        for p in self.peers:
            s = p.getStrokes()
            if len(s) != len(strokes):
                Pass = False
            else:   
                for i, stroke in enumerate(s):
                    if strokes[i] != stroke:
                        Pass = False
        self.assertTrue(Pass)
                
                

# Test basic add/move/delete strokes
    def test_basic(self):
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)

        s1 = Stroke(path=[[10,10],[10,20]])
        s2 = Stroke(path=[[10,10],[10,20]])

        ck0.addStroke(s1)
        ck1.addStroke(s2)

        time.sleep(2)
        self.assertStrokesEqual()
        pass

 #Test concurrent add/move/delete strokes
    def test_concurrent_add_delete(self):
        print 'incorrect ordering, got: wanted:'
        pass

# Test unreliable add/move/delete strokes
    #def test_unreliable_add_delete(self):
        #print 'incorrect ordering, got: wanted:'
        #pass

# Test basic join/leave peers

# Test unreliable join/leave



