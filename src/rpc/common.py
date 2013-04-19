from ui.stroke import Stroke
from rpc.priority import Priority
from rpc.vt import VT
from dp.src.rpc.cot import COT
from threading import Lock
from PyQt4 import QtCore, QtGui
from dp.src.rpc.commontypes import Request, Operation, OpType
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
        self.prqs    = []
        self.context = {}

        self.window = None

        self.lock = Lock()


    def executeOperations(self):
        #NOTE: should be locking

        #print '\033[32m--execute\033[0m'

        #print '\tcurrent vt:',self.vt
        print 'execute (lock)'
        self.lock.acquire()
        print 'execute (locked)'
        print '\n===== EXECUTE ==============='
        print 'state', self.vt
        self.printQueue()

        to_del = []
        for i, rq in enumerate(self.queue):
            if i in to_del:
                continue
            print 'RQ context (exec)',rq.context
            print 'LOCAL context (exec)', self.context.keys()
            if COT.issublist(rq.context, self.context.keys()):
                to_del.append(i)
                cd = COT.contextsdiff(self.context.keys(), rq.context)
                COT.depth = 0
                COT.transform(rq, cd, self.context)
                self.performOperation(rq.op)
                self.context[rq.request_id] = rq
            
        to_del.sort()
        to_del.reverse()

        for i in to_del:
            #print '\033[31m\t del:', self.queue[i].request_id, '\033[0m'
            del self.queue[i] 

        self.printQueue()
        self.printContext()
        self.printStrokes()
        self.lock.release()
        print 'execute (unlock)'

        # Send signal to UI
        self.newStrokesSignal.emit()


        print '========================= END EXECUTE\n'



    def printQueue(self):
        print '\n-------------------- QUEUE -------------------------------------------'
        print len(self.queue), 'requests'
        for i,rq in enumerate(self.queue):
            if rq.op.type == OpType.ADD:
                print '\033[32m',i,'-',rq,'\033[0m'
            elif rq.op.type == OpType.DEL:
                print '\033[31m',i,'-',rq,'\033[0m'
            else:
                print '\033[33m',i,'-',rq,'\033[0m'
        print '----------------------------------------------------------------------\n'

    def printContext(self):
        print '\n-------------------- CONTEXT  ---------------------------------------------'
        print len(self.context), 'ops in context'
        for i,rq in enumerate(self.context):
                print '\033[32m',i,'-',rq,'\033[0m'
        print '----------------------------------------------------------------------\n'

    def printStrokes(self):
        print '\n-------------------- STROKES ---------------------------------------------'
        print len(self.strokes), 'strokes'
        for i,s in enumerate(self.strokes):
            print i,'-',s
        print '--------------------------------------------------------------------------'


    def performOperation(self,op):
        if op.type == OpType.ADD:
            m = len(self.strokes)
            for i in range(m, op.pos+1):
                self.strokes.insert(i,None)
            if self.strokes[op.pos]:
                self.strokes.insert(op.pos,op.stroke)
            else: # none: replace
                self.strokes[op.pos]=op.stroke
            for s in self.strokes:
                if s:
                    print '\t',s
                else:
                    print '\t',none
            print '\n'

        if op.type == OpType.DEL:
            print self.strokes
            del self.strokes[op.pos]
            print self.strokes
        if op.type == OpType.MOVE:
            self.strokes[op.pos].moveTo(op.offset)
            print self.strokes
            
        if self.window: #Dont call UI (for the tester)
            self.window.scribbleArea.draw()

    def getPastRequests(self):
        self.lock.acquire()
        cp = copy.deepcopy(self.prqs);
        self.lock.release()
        return cp

    def getSnapshot(self):
        print 'snapshot (lock)'
        self.lock.acquire()
        print 'snapshot (locked)'
        cp = PeerState(0);
        cp.id = self.id
        cp.queue = copy.deepcopy(self.queue)
        cp.log = []
        cp.vt = self.vt[:]
        cp.strokes = copy.deepcopy(self.strokes)
        cp.context = copy.deepcopy(self.context)
        self.lock.release()
        print 'snapshot (unlock)'
        return cp


    def appendToQueue(self, rq):
        print 'append (lock)'
        self.lock.acquire()
        print 'append (locked)'
        rid = rq.request_id

        if rid in self.prqs:
            print 'already seen'
            self.lock.release()
            print 'append (unlock)'
            return False

        self.prqs.append(rq.request_id);
        self.queue.append(rq)
        self.lock.release()
        print 'append (unlock)'
        return True

    def getStrokes(self):
        print 'get strokes (lock)'
        self.lock.acquire()
        print 'get strokes (locked)'
        cp = copy.deepcopy(self.strokes)
        self.lock.release()
        print 'get strokes (unlock)'
        return cp
