import unittest
import sys
import time
import random

from PyQt4 import QtCore, QtGui

from dp.src.utils.log import Log
from dp.src.utils.utils import Utils
from dp.src.rpc.peer import Peer
from dp.src.ui.stroke import Stroke
from dp.src.rpc.clerk import Clerk


class GenericTestCase(unittest.TestCase):
    """Generic test stub

        implements helper methods useful to all tests

    """

    def setUp(self):
        """ Prepares a simple situation with two test servers """
        self.servers = []
        self.peers   = []
        self.ips     = []
        self.ports   = []
        self.ids     = []
        self.clerks  = []

        app = QtGui.QApplication(sys.argv)
        self.addMultipleServers(2)

    def tearDown(self):
        pass

    def genRandomStrokes(self, n):
        """ Generates n random strokes """
        s = []
        for i in range(n):
            a = [random.randint(0,1024), random.randint(0,768)]
            b = [random.randint(0,1024), random.randint(0,768)]
            s.append(Stroke(path = [a,b]));
        return s

    def addMultipleServers(self,n=1):
        """ Adds n test servers """
        for i in range(n):
            self.addServer()

    def addServer(self):
        """ Adds 1 test servers """
        server = Utils.generateID()
        local_id = len(self.servers)
        self.ids.append(local_id)
        self.servers.append(server)
        log = Log(local_id)
        ip = 'localhost'
        while True:
            try:
                port = random.randint(1,8000)
                build_ui = False
                peer = Peer(ip,port, local_id,build_ui,log)
                self.peers.append(peer)
                self.ports.append(port)
                self.ips.append(ip)
                self.clerks.append(Clerk(peer.state))
                break
            except:
                continue
                
        for i,s in enumerate(self.servers):
            for j,server2 in enumerate(self.servers):
                if server2 != s and (s==server or server2 == server):
                    self.peers[i].addPeer(self.ips[j],self.ports[j])

    def assertStrokesEqual(self):
        """ Checks the final stroke lists are coherent between peers """
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
