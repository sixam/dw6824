import xmlrpclib
from threading import Thread
from rpc.common import PeerState,Request,Operation,OpType
import time

class Clerk:
    """ Clerk for the UI thread, handles the emission of RPC calls"""
    def __init__(self,state):
        self.state = state

    def _increase_vt(self):
        self.state.vt[self.state.id] += 1
        
    def addStroke(self,s):
        id = 0
        self._increase_vt()

        op = Operation(type=OpType.ADD,stroke_id = id, stroke = s)
        print 'adding',op

        rq = Request(sender = self.state.id, vt = self.state.vt, op = op,
                priority = self._calculatePriority(op), request_id = 0)
        print 'sending',rq

        self.state.queue.append(rq)

        # broadcast
        self._send(rq)

    def _calculatePriority(self,op):
        return self.state.id

    def _send(self,rq):
        for srv in self.state.peers:
            print srv
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
                pass
            time.sleep(.01)

    def moveStroke(self,id,offset):
        pass

    def editStroke(self,id,stroke):
        pass

    def deleteStroke(self,id):
        for srv in self.peers:
            srv.deleteStroke(id)
