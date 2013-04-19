import xmlrpclib
from dp.src.rpc.commontypes import Request, Operation, OpType
from threading import Thread
from rpc.common import PeerState
import time
from utils.utils import Utils
from rpc.priority import Priority
from ui.stroke import Stroke
import copy
from dp.src.utils.log import Log

class Clerk:
    """ Clerk for the UI thread, handles the emission of RPC calls"""
    def __init__(self,state):
        self.state = state
        self.log = state.log

        
    def addStroke(self,s):
        self.log.Print( 'sent', s)
        rq = self._genAdd(s)
        rq_send = copy.copy(rq)
        self.log.Print( 'REQUESTS',rq, rq_send )
        self.state.appendToQueue(rq)
        self.state.executeOperations()
        self._send(rq_send)

    def deleteStroke(self,s_pos):
        rq = self._genDel(s_pos)
        rq_send = copy.copy(rq)
        self.state.appendToQueue(rq)
        self.state.executeOperations()
        self._send(rq_send)

    def moveStroke(self,s_pos,offset):
        rq = self._genMove(s_pos, offset)
        rq_send = copy.copy(rq)
        self.state.appendToQueue(rq)
        self.state.executeOperations()
        self._send(rq_send)

    def _genAdd(self, s):
        sp = self.state.getSnapshot()
        pos = len(sp.strokes)
        op = Operation(type=OpType.ADD,stroke_id = s.id, stroke = s,pos =
                pos)
        p = Priority(op=op,state=sp)
        rq = Request(sender = sp.id, vt = sp.vt[:], op = op,
                priority = p, 
                request_id = Utils.generateID(),context=sp.context.keys())

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
                self.log.Print( 'looping')
                pass
            time.sleep(.1)

