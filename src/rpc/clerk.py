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
        # NOTE : this should be lock-secured
        #st = Stroke(**s)
        print '\033[31m-acquire Clerk add s\033[0m'

        pos = len(self.state.strokes)

        op = Operation(type=OpType.ADD,stroke_id = s.id, stroke = s,pos =
                pos)
        p = Priority(op=op,state=self.state)

        rq = Request(sender = self.state.id, vt = self.state.vt[:], op = op,
                priority = p, 
                request_id = Utils.generateID())

        self.state.appendToQueue(rq)

        # broadcast
        print 'sending', rq
        self.state.executeOperations()
        print '\033[31m-reloease Clerk add s\033[0m'

        self._send(rq)


    def deleteStroke(self,s_pos):
        """ Be careful when copying the state'vt : pointers ... """
        # NOTE : this should be lock-secured
        print '\033[31m-acquire Clerk del s\033[0m'

        s_id = self.state.strokes[s_pos].id
        op = Operation(type=OpType.DEL, stroke_id=s_id, pos=s_pos, stroke=self.state.strokes[s_pos])
        p = Priority(op=op,state=self.state)

        rq = Request(sender = self.state.id, vt = self.state.vt[:], op = op,
                priority = p, 
                request_id = Utils.generateID())

        self.state.appendToQueue(rq)

        # broadcast
        print 'rq.op', rq.op
        print 'rq.op.stroke', rq.op.stroke
        print 'sending', rq
        self.state.executeOperations()
        print '\033[31m-reloease Clerk del s\033[0m'

        self._send(rq)

    def moveStroke(self,s_pos,offset):
        stroke = copy.copy(self.state.strokes[s_pos])
        self.deleteStroke(s_pos)
        stroke.offsetPosBy(offset)
        self.addStroke(stroke)
        pass

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
                pass
            time.sleep(1)

