import xmlrpclib
from threading import Thread
from rpc.common import PeerState,Request,Operation,OpType
import time
from utils.utils import Utils
from rpc.priority import Priority
from ui.stroke import Stroke
import copy

class Clerk:
    """ Clerk for the UI thread, handles the emission of RPC calls"""
    def __init__(self,state):
        self.state = state

        
    def addStroke(self,s):
        rq = self._genAdd(s)
        self.state.appendToQueue(rq)
        self.state.executeOperations()
        self._send(rq)

    def deleteStroke(self,s_pos):
        rq = self._genDel(s_pos)
        self.state.appendToQueue(rq)
        self.state.executeOperations()
        self._send(rq)

    def moveStroke(self,s_pos,offset):
        rq = self._genMove(s_pos, offset)
        self.state.appendToQueue(rq)
        self.state.executeOperations()
        self._send(rq)

    def _genAdd(self, s):
        sp = self.state.getSnapshot()
        pos = len(sp.strokes)
        op = Operation(type=OpType.ADD,stroke_id = s.id, stroke = s,pos =
                pos)
        p = Priority(op=op,state=sp)
        rq = Request(sender = sp.id, vt = sp.vt[:], op = op,
                priority = p, 
                request_id = Utils.generateID())

        return rq


    def _genDel(self, s_pos):
        sp = self.state.getSnapshot()
        s_id = sp.strokes[s_pos].id
        op = Operation(type=OpType.DEL, stroke_id=s_id, pos=s_pos, stroke=sp.strokes[s_pos])
        p = Priority(op=op,state=sp)

        rq = Request(sender = sp.id, vt = sp.vt[:], op = op,
                priority = p, 
                request_id = Utils.generateID())
        return rq


    def _genMove(self, s_pos, offset):
        sp = self.state.getSnapshot()
        s_id = sp.strokes[s_pos].id
        op = Operation(type=OpType.MOVE, stroke_id=s_id, pos=s_pos,
                stroke=sp.strokes[s_pos], offset=offset)
        p = Priority(op=op,state=sp)
        rq = Request(sender = sp.id, vt = sp.vt[:], op = op,
                priority = p,
                request_id = Utils.generateID())

        return rq

    def _send(self,rq):
        for srv in self.state.peers:
            t = Thread(target=self._send_worker,args=(rq,srv))
            t.daemon = True
            t.start()

    def _send_worker(self,rq,srv):
        keep_running = True
        while keep_running :
            try:
                srv.enq(rq)
                keep_running = False
            except:
                print 'looping'
                print 'Sending rq:', rq
                pass
            time.sleep(1)

