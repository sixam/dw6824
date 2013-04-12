import xmlrpclib
from threading import Thread
from rpc.common import PeerState,Request,Operation,OpType
import time
from utils.utils import Utils
from rpc.priority import Priority

class Clerk:
    """ Clerk for the UI thread, handles the emission of RPC calls"""
    def __init__(self,state):
        self.state = state

        
    def addStroke(self,s):
        # NOTE : this should be lock-secured
        stroke_id = Utils.generateID()
        self._increase_vt()

        op = Operation(type=OpType.ADD,stroke_id = stroke_id, stroke = s)
        p = Priority(op=op,state=self.state)

        rq = Request(sender = self.state.id, vt = self.state.vt, op = op,
                priority = p, 
                request_id = Utils.generateID())

        self.state.queue.append(rq)

        # broadcast
        self._send(rq)

        self.state.executeOperations()

    def deleteStroke(self,id):
        # NOTE : this should be lock-secured
        stroke_id = Utils.generateID()
        self._increase_vt()

        op = Operation(type=OpType.DEL,stroke_id = id)

        rq = Request(sender = self.state.id, vt = self.state.vt, op = op,
                priority = self._calculatePriority(op), 
                request_id = Utils.generateID())

        self.state.queue.append(rq)

        # broadcast
        self._send(rq)
 
    def moveStroke(self,id,offset):
        pass

    def editStroke(self,id,stroke):
        pass

    def _calculatePriority(self,op):
        return self.state.id


    def _increase_vt(self):
        self.state.vt[self.state.id] += 1

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
                print 'sent', rq
            except:
                print 'looping'
                pass
            time.sleep(1)

