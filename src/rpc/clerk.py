import xmlrpclib
from threading import Thread
from rpc.common import PeerState
import time
from utils.utils import Utils
from ui.stroke import Stroke
import copy
from dp.src.utils.log import Log

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

    def join(self, session, ip, port=9011):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('google.com',80))
        ip = s.getsockname()[0]
        s.close()

        peers = self.state.cs.join(session, ip, port)
        self.state.id = len(peers)

        for p in peers:
            self.state.addPeer(p[0],p[1])
            self.thaw(peers.index(p))


    def start(self, ip, port):
        session_num = self.state.cs.start(ip, port)
        self.state.id = 0 
        self.thaw(0)
        return session_num

    def lock(self, session):
        return self.state.cs.lockSession(session)
