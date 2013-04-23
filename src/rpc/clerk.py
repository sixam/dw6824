import xmlrpclib
from threading import Thread
from rpc.common import PeerState
import time
from utils.utils import Utils
from ui.stroke import Stroke
import copy
from dp.src.utils.log import Log

class Clerk:
    """ Clerk for the UI thread, handles the emission of RPC calls"""
    def __init__(self,state):
        self.state = state
        self.log = state.log

    def thaw(self, sid):
        self.state.thaw(sid)

    def freeze(self, sid):
        self.state.freeze(sid)
        
    def addStroke(self,s):
        op = self.state.createOp('insert',stroke=s)
        self._send(op.copy())

    def deleteStroke(self,s_pos):
        op = self.state.createOp('delete',pos=s_pos)
        self._send(op.copy())

    def moveStroke(self,s_pos,offset):
        pass

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
                self.log.purple('send op:', op, 'to srv:', srv)
                done = srv.enq(packet)
                if done:
                    break
            except:
                self.log.Print( 'looping')
                pass
            time.sleep(1)
