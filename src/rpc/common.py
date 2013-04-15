import copy
from ui.stroke import Stroke
from rpc.priority import Priority
from rpc.vt import VT
from threading import Lock
from PyQt4 import QtCore, QtGui
import copy

class PeerState(QtCore.QObject):
    """Stores all data concerning a peer's state

    Contains:
        - list of other peers
        - dOPT structures
        - drawn objects (strokes)

    Is shared between UI and Network threads
    
    """

    newStrokesSignal = QtCore.pyqtSignal()

    # NOTE: lock around access to the structure?
    def __init__(self, peer_id):
        super(PeerState, self).__init__()
        self.id      = peer_id
        self.peers   = []
        self.queue   = []
        self.log     = []
        self.vt      = [0 for x in range(3)]
        self.strokes = []

        self.window = None


        self.lock = Lock()

    def appendToQueue(self, rq):
        self.lock.acquire()
        self.queue.append(rq)
        self.lock.release()

    def getStrokes(self):
        self.lock.acquire()
        cp = copy.deepcopy(self.strokes)
        self.lock.release()
        return cp

    def executeOperations(self):
        #NOTE: should be locking

        print '\033[32m--execute\033[0m'

        #print '\tcurrent vt:',self.vt
        self.lock.acquire()

        to_del = []
        for i, rq in enumerate(self.queue):
            if i in to_del:
                continue
            #print '\tunqueue vt:', rq.vt
            cmp = VT.cmp(rq.vt,self.vt)
            #print '\tcmp is:', cmp
            logcopy = copy.deepcopy(self.log)
            if  cmp ==0 or cmp == -1:
                #print rq.vt,'<=',self.vt
                to_del.append(i)
                if cmp==-1:
                    #print rq.vt,'<',self.vt
                    mr = self.mostRecent(rq.vt, logcopy)
                    print '\tmr', mr
                    print 'rq-op', rq.op
                    while mr and rq.op.type != OpType.NoOp:
                        if rq.vt[mr.sender] <= mr.vt[mr.sender]:
                            self.transform(rq,mr)
                        mrt = self.mostRecent(rq.vt, logcopy)


            self.performOperation(rq.op)
            self.log.append(rq)
            self.vt[rq.sender] += 1
            print '\tupdated vt', self.vt

        to_del.sort()
        to_del.reverse()

        print '\tdel', to_del

        for i in to_del:
           del self.queue[i] 
           
        print '\033[31m--done\033[0m\n'

        # Send signal to UI

        self.lock.release()
        self.newStrokesSignal.emit()




    def mostRecent(self,vt, logcopy):
        for i in range(len(logcopy)-1,-1,-1):
            if VT.cmp(logcopy[i].vt,vt) <= 0:
                del logcopy[i]
                return self.log[i]

        return None

    def performOperation(self,op):
        if op.type == OpType.ADD:
            print 'added', op.stroke
            self.strokes.insert(op.pos,op.stroke);
        if op.type == OpType.DEL:
            print 'deleted', op.pos
            print self.strokes
            del self.strokes[op.pos]
            print self.strokes
        self.window.scribbleArea.draw()
        pass

    def transform(self,ri,rj):
        oi = ri.op
        oj = rj.op
        PosI = oi.pos
        PosJ = oj.pos

        pi = ri.priority
        pj = rj.priority


        if oi.type == OpType.ADD and oj.type == OpType.ADD:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                oi.pos += 1
            else:
                if oi.stroke.id== oj.stroke.id:
                    op.type = OpType.NoOp
                else:
                    if pi > pj:
                        oi.pos += 1
                    else:
                        pass


        if oi.type == OpType.ADD and oj.type == OpType.DEL:
            if PosI < PosJ:
                pass
            else:
                oi.pos -= 1
                
            

        if oi.type == OpType.DEL and oj.type == OpType.ADD:
            if PosI < PosJ:
                pass
            else:
                oi.pos += 1

        if oi.type == OpType.DEL and oj.type == OpType.DEL:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                oi.pos -= 1
            else:
                oi.type = OpType.NoOp

        print '\033[32m--transformed\033[0m',ri,rj,'\n'

        
class Request:
    def __init__(self,sender=-1,vt=None,op=None,priority=0,request_id='none'):
        if isinstance(op,dict):
            self.op = Operation(**op)
        else:
            self.op = op 

        if isinstance(priority,dict):
            self.priority = Priority(**priority)
        else:
            self.priority = priority

        self.sender = sender
        self.vt = vt
        self.request_id = request_id

    def __str__(self):
        return "< sd:{4} | vt:{3} | op:{2} | {1} | rid:{0} >".format(
                self.request_id[0:5],self.priority,self.op,self.vt,self.sender)
    def __copy__(self):
        new = Request()
        new.op = copy.copy(self.op)
        new.vt = copy.copy(self.vt)
        new.priority = copy.copy(self.priority)
        new.sender = copy.copy(self.sender)
        new.request_id = copy.copy(self.request_id)
        return new
       

class Operation:
    def __init__(self,type=None,stroke_id='none',stroke=None,pos=-1,opos=-1):
        if isinstance(stroke,dict):
            self.stroke = Stroke(**stroke)
        else:
            self.stroke = stroke

        self.type = type
        self.stroke_id = stroke_id
        self.pos = pos
        if opos == -1:
            self.opos = pos
        else: # unmarshalling
            self.opos = opos

    def __str__(self):
        return "{{ {0} {1} at {2}({3})}}".format(
                self.type,self.stroke_id[0:5],self.pos,self.opos)

    def __copy__(self):
        new = Operation()
        new.stroke = copy.copy(self.stroke)
        new.type = copy.copy(self.type)
        new.stroke_id = copy.copy(self.stroke_id)
        new.ops = copy.copy(self.pos)
        new.opos = copy.copy(self.opos)
        return new

class OpType:
    ADD = 'ADD'
    DEL = 'DEL'
    NoOp = 'NoOp'
