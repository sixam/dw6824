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
        self.servers = ['local1','local2']
        self.peers = []
        self.ips   = []
        self.ports = []
        self.ids   = [0,1]

        app = QtGui.QApplication(sys.argv)

        for i,server in enumerate(self.servers):
            local_id = self.ids[i]
            ip = 'localhost'
            while True:
                try:
                    port = random.randint(1,8000)
                    noUI = False
                    build_ui = False
                    peer = Peer(ip,port, local_id,build_ui)
                    self.peers.append(peer)
                    self.ports.append(port)
                    self.ips.append(ip)
                    break
                except:
                    continue
                
        for i,server in enumerate(self.servers):
            for j,server2 in enumerate(self.servers):
                if server2 != server:
                    self.peers[i].addPeer(self.ips[j],self.ports[j])

    def tearDown(self):
        pass

    def addServer(self,server):
        local_id = len(self.servers)
        self.ids.append(local_id)
        self.servers.append(server)
        ip = 'localhost'
        while True:
            try:
                port = random.randint(1,8000)
                noUI = False
                build_ui = False
                peer = Peer(ip,port, local_id,build_ui)
                self.peers.append(peer)
                self.ports.append(port)
                self.ips.append(ip)
                break
            except:
                continue
                
        for i,s in enumerate(self.servers):
            for j,server2 in enumerate(self.servers):
                if server2 != s and (s==server or server2 == server):
                    self.peers[i].addPeer(self.ips[j],self.ports[j])

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
        time.sleep(1)

        self.assertStrokesEqual()

    #def test_delay(self):
        #p0 = self.peers[0]
        #p1 = self.peers[1]
        #ck0 = Clerk(p0.state)
        #ck1 = Clerk(p1.state)
        
        #s = self.genRandomStrokes(8)
        #ck0.addStroke(s[0]);
        #time.sleep(1)
        #ck1.addStroke(s[1])

        #time.sleep(1)
        
        #p0.kill()
        #p1.kill()
        
        #ck0.addStroke(s[2]);
        #time.sleep(1)
        #ck0.addStroke(s[3]);
        #time.sleep(1)
        #ck1.addStroke(s[4])
        #time.sleep(1)
        #ck1.addStroke(s[5])
        
        #time.sleep(1)
        
        #p0.revive()
        #p1.revive()

        #time.sleep(1)

        #ck0.addStroke(s[6]);
        #time.sleep(1)
        #ck1.addStroke(s[7])
        
        #time.sleep(2)

        #self.assertStrokesEqual()


    def genRandomStrokes(self, n):
        s = []
        for i in range(n):
            a = [random.randint(0,100), random.randint(0,100)]
            b = [random.randint(0,100), random.randint(0,100)]
            s.append(Stroke(path = [a,b]));
        return s


 #Test concurrent add/move/delete strokes
#    def test_concurrent_add_delete(self):
#        print 'incorrect ordering, got: wanted:'
#        pass
#
## Test unreliable add/move/delete strokes
#    #def test_unreliable_add_delete(self):
#        #print 'incorrect ordering, got: wanted:'
#        #pass
#
## Test basic join/leave peers
#
## Test unreliable join/leave
#
#
#