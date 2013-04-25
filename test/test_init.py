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

    def genRandomStrokes(self, n):
        s = []
        for i in range(n):
            a = [random.randint(0,1024), random.randint(0,768)]
            b = [random.randint(0,1024), random.randint(0,768)]
            s.append(Stroke(path = [a,b]));
        return s

    def addMultipleServers(self,n=1):
        for i in range(n):
            self.addServer()

    def addServer(self):
        server = Utils.generateID()
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
                self.assertTrue(Pass,msg="different length")
            else:   
                for i, stroke in enumerate(s):
                    if strokes[i] != stroke:
                        Pass = False
                        self.assertTrue(Pass,msg="Peer {0} has a different stroke at {1}".format(p.__str__(),i))

    def test_basic(self):
        """ Basic - add strokes """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)

        s = self.genRandomStrokes(2)

        ck0.addStroke(s[0])
        time.sleep(1)
        ck1.addStroke(s[1])
        time.sleep(1)

        self.assertStrokesEqual()

    def test_basic_delete(self):
        """ Basic - delete strokes """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)

        s = self.genRandomStrokes(2)

        ck0.addStroke(s[0])
        time.sleep(1)
        ck1.addStroke(s[1])
        time.sleep(1)
        ck0.deleteStroke(0)
        time.sleep(1)

        self.assertStrokesEqual()

    def test_basic_move(self):
        """ Basic - move strokes """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)

        s = self.genRandomStrokes(4)

        ck0.addStroke(s[0])
        ck0.addStroke(s[1])
        time.sleep(1)
        ck1.addStroke(s[2])
        ck1.addStroke(s[3])
        time.sleep(1)

        strokes = ck0.getStrokes()
        index = 0
        offset = [10,10]
        ck0.moveStroke(strokes[index],index,offset)

        self.assertStrokesEqual()

    def test_delay_01(self):
        """ Delay - simple """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)
        
        s = self.genRandomStrokes(12)

        ck0.addStroke(s[0]);
        ck1.addStroke(s[1])
        time.sleep(1)
        
        p0.kill()
        p1.kill()
        
        ck0.addStroke(s[2]);
        ck1.addStroke(s[4])
        time.sleep(1)
        
        p0.revive()
        p1.revive()
        time.sleep(1)

        #ck0.addStroke(s[6]);
        #ck1.addStroke(s[7])
        time.sleep(1)

        self.assertStrokesEqual()

    def test_delay_02(self):
        """ Delay - dOPT puzzle """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = Clerk(p0.state)
        ck1 = Clerk(p1.state)

        s = self.genRandomStrokes(12)

        ck0.addStroke(s[0]);
        ck1.addStroke(s[1])
        time.sleep(1)
        
        p0.kill()
        p1.kill()
        
        ck0.addStroke(s[2]);
        ck0.addStroke(s[3]);
        ck1.addStroke(s[4])
        time.sleep(1)
        
        p0.revive()
        p1.revive()
        time.sleep(1)

        ck0.addStroke(s[5])
        ck1.addStroke(s[6])

        time.sleep(2)
        self.assertStrokesEqual()

    def test_manystrokes(self):
        """ Many - strokes """
        cks = []
        for i in range(len(self.peers)):
            cks.append(Clerk(self.peers[i].state));
        s = self.genRandomStrokes(100)
        for stroke in s:
            i = random.randint(0,1024) % len(self.peers)
            cks[i].addStroke(stroke)
        time.sleep(30)
        self.assertStrokesEqual()


    def test_manypeers(self):
        """ Many - peers """
        self.addMultipleServers(2)
        cks = []
        for i in range(len(self.peers)):
            cks.append(Clerk(self.peers[i].state));
        for ck in cks:
            for sid in self.ids:
                ck.thaw(sid)

        s = self.genRandomStrokes(20)
        for stroke in s:
            i = random.randint(0,len(self.peers)-1)
            cks[i].addStroke(stroke)
        time.sleep(10)

        for ck in cks:
            ck.state.getStrokes()

        self.assertStrokesEqual()

    def test_manypeers02(self):
        """ Many - peers, strokes, operations """
        #self.addMultipleServers(1)
        cks = []
        for i in range(len(self.peers)):
            cks.append(Clerk(self.peers[i].state));
        for ck in cks:
            for sid in self.ids:
                ck.thaw(sid)

        n_strokes = 12
        s = self.genRandomStrokes(n_strokes)
        for stroke in s:
            i = random.randint(0,len(self.peers)-1)
            cks[i].addStroke(stroke)

        for s in range(n_strokes/2):
            i = random.randint(0,len(self.peers)-1)
            strokes = cks[i].getStrokes()
            if not strokes:
                continue
            m = random.randint(0, len(strokes) - 1)
            if not strokes[m]:
                continue
            if random.randint(0,1) :
                offset = [random.randint(1,200),random.randint(1,200)]
                cks[i].moveStroke(strokes[m],m,offset)
            else:
                cks[i].deleteStroke(strokes[m],m)
        time.sleep(25)

        self.assertStrokesEqual()

    #def test_manydead(self):
        #""" Many - peers dying"""
        #self.addMultipleServers(3)
        #cks = []
        #for i in range(len(self.peers)):
            #cks.append(Clerk(self.peers[i].state));
        #for ck in cks:
            #for sid in self.ids:
                #ck.thaw(sid)

        #s = self.genRandomStrokes(9)
        #for stroke in s:
            #i = random.randint(0,1024) % len(self.peers)
            #cks[i].addStroke(stroke)
        #time.sleep(5)
        
        #dead = []
        #s = self.genRandomStrokes(15)
        #for stroke in s:
            #i = random.randint(0,1024) % len(self.peers)
            #cks[i].addStroke(stroke)
            #if random.randint(0,1) > 0 and i not in dead:
                #self.peers[i].kill()
                #dead.append(i)
        #time.sleep(5)

        #for p in dead:
            #self.peers[p].revive()
        #time.sleep(25)

        #self.assertStrokesEqual()
