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

        
    def addStroke(self,s):
        op = self.state.createOp('insert',stroke=s)
        self._send(op.copy())

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

