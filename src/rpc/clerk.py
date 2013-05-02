import xmlrpclib
from threading import Thread
from rpc.common import PeerState
import time
from utils.utils import Utils
from ui.stroke import Stroke
import copy
from utils.log import Log

import socket

class Clerk:
    """ Clerk for the UI thread, handles the emission of RPC calls"""
    def __init__(self,state):
        self.state = state
        self.log = state.log

    def thaw(self, sid):
        self.state.thaw(sid)

    def freeze(self, sid):
        self.state.freeze(sid)
        
    def addStroke(self,s,order=-1):
        op = self.state.createOp('insert',stroke=s,order=order)
        self._send(op.copy())

    def deleteStroke(self,s,s_pos):
        new_s = copy.copy(s)
        op = self.state.createOp('delete',stroke=s,pos=s_pos)
        self._send(op.copy())

    def updateStroke(self,s,s_pos):
        op = self.state.createOp('update',stroke=s, pos=s_pos)
        self._send(op.copy())

    def moveStroke(self,s,s_pos,offset):
        new_s = copy.copy(s)
        new_s.offsetPosBy(offset)
        self.updateStroke(new_s,s_pos)

    def getStrokes(self):
        return self.state.getStrokes()

    def _send(self,op):
        for srv in self.state.peers:
            t = Thread(target=self._send_worker,args=(op,srv))
            t.daemon = True
            t.start()

    def _send_worker(self,op,srv):
        keep_running = True
        packet = op.marshall()
        while True :
            try:
                done = srv.enq(packet)
                if done:
                    self.log.rpc('sent:',op)
                    break
            except:
                pass
            time.sleep(1)

    def join(self, session):
        if self.state.session >= 0:
            self.log.red("Already in a session, restart to change.")
            return False
        ip   = self.state.ip
        port = self.state.port

        # Contact server
        self.log.green('Contacting',self.state.cs,'for a join')
        peers = self.state.cs.join(session, ip, port, self.state.uid)

        # Check we got the right to join
        if not peers:
            self.log.red("Could not join session", session,": it might be locked")
            return False

        self.state.id = len(peers)-1
        self.state.createEngine()
        self.thaw(self.state.id)
        self.state.session = session

        for i,p in enumerate(peers):
            self.log.orange('thawing', i)
            self.thaw(i)
            if p[0] == ip and p[1] == port:
                continue
            self.state.addPeer(p[0],p[1])

        self.log.Print("Joined session",self.state.session)
        return True

    def start(self):
        ip   = self.state.ip
        port = self.state.port

        session_num = self.state.cs.start(ip, port, self.state.uid)
        self.state.session = session_num
        self.state.id = 0 
        self.state.createEngine()
        self.thaw(0)
        return session_num

    def lock(self):
        if self.state.session < 0:
            self.log.Print("Cannot log a session I never joined")
            return False
        self.log.Print("Locked session",self.state.session)
        return self.state.cs.lockSession(self.state.session)
