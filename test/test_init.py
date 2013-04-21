import unittest
import sys
import datetime
import time
import random
from threading import Thread

from PyQt4 import QtCore, QtGui

from dp.src.utils.log import Log
from dp.src.utils.utils import Utils
from dp.src.rpc.peer import Peer
from dp.src.ui.stroke import Stroke
from dp.src.rpc.clerk import Clerk

from nose.tools import *




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
            log = Log(local_id)
            while True:
                try:
                    port = random.randint(1,8000)
                    noUI = False
                    build_ui = False
                    peer = Peer(ip,port, local_id,build_ui, log)
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

    def addMultipleServers(self,n=1):
        for i in range(n):
            self.addServer()

    def addServer(self,server=''):
        local_id = len(self.servers)
        self.ids.append(local_id)
        self.servers.append(server)
        log = Log(local_id)
        ip = 'localhost'
        while True:
            try:
                port = random.randint(1,8000)
                noUI = False
                build_ui = False
                peer = Peer(ip,port, local_id,build_ui,log)
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
#    def test_basic(self):
#        p0 = self.peers[0]
#        p1 = self.peers[1]
#        ck0 = Clerk(p0.state)
#        ck1 = Clerk(p1.state)
#
#        s1 = Stroke(path=[[10,10],[10,20]])
#        s2 = Stroke(path=[[10,10],[10,20]])
#
#        ck0.addStroke(s1)
#        time.sleep(1)
#        ck1.addStroke(s2)
#        time.sleep(1)
#
#        self.assertStrokesEqual()
#
#    def test_delay_01(self):
#        p0 = self.peers[0]
#        p1 = self.peers[1]
#        ck0 = Clerk(p0.state)
#        ck1 = Clerk(p1.state)
#        
#        s = self.genRandomStrokes(12)
#
#        ck0.addStroke(s[0]);
#        ck1.addStroke(s[1])
#        time.sleep(1)
#        
#        p0.kill()
#        p1.kill()
#        
#        ck0.addStroke(s[2]);
#        ck1.addStroke(s[4])
#        time.sleep(1)
#        
#        p0.revive()
#        p1.revive()
#        time.sleep(1)
#
#        #ck0.addStroke(s[6]);
#        #ck1.addStroke(s[7])
#        time.sleep(1)
#
#        self.assertStrokesEqual()
#
#    def test_delay_02(self):
#        p0 = self.peers[0]
#        p1 = self.peers[1]
#        ck0 = Clerk(p0.state)
#        ck1 = Clerk(p1.state)
#
#        s = self.genRandomStrokes(12)
#
#        ck0.addStroke(s[0]);
#        ck1.addStroke(s[1])
#        time.sleep(1)
#        
#        p0.kill()
#        p1.kill()
#        
#        ck0.addStroke(s[2]);
#        ck0.addStroke(s[3]);
#        ck1.addStroke(s[4])
#        time.sleep(1)
#        
#        p0.revive()
#        p1.revive()
#        time.sleep(1)
#
#        ck0.addStroke(s[5])
#        ck1.addStroke(s[6])
#
#        time.sleep(2)
#        print 'timed out'
#
#        self.assertStrokesEqual()

#    def test_manystrokes(self):
#        #self.addMultipleServers(1)
#        cks = []
#        for i in range(len(self.peers)):
#            cks.append(Clerk(self.peers[i].state));
#        s = self.genRandomStrokes(18)
#        for stroke in s:
#            i = random.randint(0,1024) % len(self.peers)
#            cks[i].addStroke(stroke)
#            #time.sleep(0.1)
#        time.sleep(30)
#        self.assertStrokesEqual()

    def test_manypeers(self):
        self.addMultipleServers(1)
        cks = []
        for i in range(len(self.peers)):
            cks.append(Clerk(self.peers[i].state));
        s = self.genRandomStrokes(10)
        for stroke in s:
            i = random.randint(0,1024) % len(self.peers)
            cks[i].addStroke(stroke)
#time.sleep(0.1)
        time.sleep(15)
        self.assertStrokesEqual()

    #def test_manypeers(self):
        #self.addMultipleServers(20)
        #cks = []
        #for i in range(len(self.peers)):
            #cks.append(Clerk(self.peers[i].state));
        #s = self.genRandomStrokes(30)
        #for stroke in s:
            #i = random.randint(0,1024) % len(self.peers)
            #cks[i].addStroke(stroke)
        #time.sleep(10)
        #self.assertStrokesEqual()

#    def test_manydeath(self):
#        self.addMultipleServers(20)
#        for i in range(len(self.peers)):
#            cks.append(Clerk(self.peers[i].state));
#        s = self.genRandomStrokes(30)



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
