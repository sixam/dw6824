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
from dp.src.session.central import CentralServer

from .test_common import GenericTestCase

import xmlrpclib

class CentralServerTest(GenericTestCase):
    def setUp(self):
        """ Prepares a simple situation with two test servers """
        self.servers = []
        self.peers   = []
        self.ips     = []
        self.ports   = []
        self.ids     = []
        self.clerks  = []
        self.logs    = []

        self.cs_proxies   = []

    
        app = QtGui.QApplication(sys.argv)

        # setup central server
        lc = Log(100)
        while True:
            try:
                port = random.randint(1,8000)
                self.csport = port
                self.cs = CentralServer('localhost',port , lc)
                break
            except:
                continue

    def addSite(self):
        log = Log(len(self.peers))
        self.logs.append(log)
        self.cs_proxies.append(xmlrpclib.Server('http://%s:%s' % ('localhost', self.csport)))
        ip = 'localhost'
        while True:
            try:
                port = random.randint(1,8000)
                log.Print('got that port')
                peer = Peer(ip, port, build_ui = False, log=log)
                log.Print('got that peer')
                self.peers.append(peer)
                self.ports.append(port)
                self.ips.append(ip)
                self.clerks.append(Clerk(peer.state))
                break
            except:
                continue

    def addMultipleSites(self,n=1):
        """ Adds n test servers """
        for i in range(n):
            self.addSite()

    def test_basic_central(self):
        """ Central - Basic server"""
        self.addSite()
        self.addSite()
        self.addSite()
        ck = self.clerks

        for c in self.clerks:
            print self.clerks.index(c)
            c.state.cs = self.cs_proxies[self.clerks.index(c)]

        sess_num = ck[0].start(self.ips[0],self.ports[0])
        time.sleep(1)

        for i in range(1,len(ck)):
            ck[i].join(sess_num,self.ips[i],self.ports[i])
        time.sleep(1)

        for i,c in enumerate(self.clerks):
            self.logs[i].blue(c.state.peers)
            self.logs[i].blue(c.state.id)

        s = self.genRandomStrokes(3)

        ck[0].addStroke(s[0])
        ck[1].addStroke(s[1])
        #ck[2].addStroke(s[2])
        time.sleep(1)


        self.assertStrokesEqual()






