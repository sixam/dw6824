from ui.stroke import Stroke
from threading import Lock
from PyQt4 import QtCore, QtGui
from dp.src.utils.log import Log
import copy

from dp.src.protocol.OperationEngine import OperationEngine

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
    def __init__(self, peer_id, log=None):
        super(PeerState, self).__init__()
        self.id      = peer_id # site ID
        self.peers   = [] # known peers
        self.strokes = [] # currently drawn strokes
        self.prqs    = [] # past requests

        # attached ui
        self.window = None

        self.lock = Lock()

        # site log file
        self.log = log

        self.engine = OperationEngine(self.id)
        self.engine.freezeSite(self.id)


    def executeOperations(self):
        #NOTE: should be locking

        self.log.Print( 'execute (lock)')
        self.lock.acquire()
        self.log.Print( 'execute (locked)')
        self.log.Print( '\n===== EXECUTE ===============')
        self.log.Print( 'state', self.vt)
        self.printQueue()

        to_del = []
        for i, rq in enumerate(self.queue):
            if i in to_del:
                continue
            self.log.Print( 'RQ context (exec)',rq.context)
            self.log.Print( 'LOCAL context (exec)', self.context.keys())
            if self.cot.issublist(rq.context, self.context.keys()):
                to_del.append(i)
                cd = self.cot.contextsdiff(self.context.keys(), rq.context)
                self.cot.depth = 0
                self.cot.transform(rq, cd, self.context)
                self.performOperation(rq.op)
                self.context[rq.request_id] = rq
            
        to_del.sort()
        to_del.reverse()

        for i in to_del:
            del self.queue[i] 

        self.printQueue()
        self.printContext()
        self.printStrokes()
        self.lock.release()
        self.log.Print( 'execute (unlock)')

        # Send signal to UI
        self.newStrokesSignal.emit()


        self.log.Print( '========================= END EXECUTE\n')

    def printQueue(self):
        self.log.Print( '\n-------------------- QUEUE -------------------------------------------')
        self.log.Print( len(self.queue), 'requests')
        for i,rq in enumerate(self.queue):
            if rq.op.type == OpType.ADD:
                self.log.Print( '\033[32m',i,'-',rq,'\033[0m')
            elif rq.op.type == OpType.DEL:
                self.log.Print( '\033[31m',i,'-',rq,'\033[0m')
            else:
                self.log.Print( '\033[33m',i,'-',rq,'\033[0m')
        self.log.Print( '----------------------------------------------------------------------\n')

    def printContext(self):
        self.log.Print( '\n-------------------- CONTEXT  ---------------------------------------------')
        self.log.Print( len(self.context), 'ops in context')
        for i,rq in enumerate(self.context):
                self.log.Print( '\033[32m',i,'-',rq,'\033[0m')
        self.log.Print( '----------------------------------------------------------------------\n')

    def printStrokes(self):
        self.log.Print( '\n-------------------- STROKES ---------------------------------------------')
        self.log.Print( len(self.strokes), 'strokes')
        for i,s in enumerate(self.strokes):
            self.log.Print( i,'-',s)
        self.log.Print( '--------------------------------------------------------------------------')


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
                    self.log.Print( '\t',s)
                else:
                    self.log.Print( '\t',none)
            self.log.Print( '\n')

        if op.type == OpType.DEL:
            self.log.Print( self.strokes)
            del self.strokes[op.pos]
            self.log.Print( self.strokes)
        if op.type == OpType.MOVE:
            self.strokes[op.pos].moveTo(op.offset)
            self.log.Print( self.strokes)
            
        if self.window: #Dont call UI (for the tester)
            self.window.scribbleArea.draw()

    def getPastRequests(self):
        self.lock.acquire()
        cp = copy.deepcopy(self.prqs);
        self.lock.release()
        return cp

    def getSnapshot(self):
        self.log.Print( 'snapshot (lock)')
        self.lock.acquire()
        self.log.Print( 'snapshot (locked)')
        cp = PeerState(0);
        cp.id = self.id
        cp.queue = copy.deepcopy(self.queue)
        cp.log = []
        cp.vt = self.vt[:]
        cp.strokes = copy.deepcopy(self.strokes)
        cp.context = copy.deepcopy(self.context)
        self.lock.release()
        self.log.Print( 'snapshot (unlock)')
        return cp


    def appendToQueue(self, rq):
        self.log.Print( 'append (lock)')
        self.lock.acquire()
        self.log.Print( 'append (locked)')
        rid = rq.request_id

        if rid in self.prqs:
            self.log.Print( 'already seen')
            self.lock.release()
            self.log.Print( 'append (unlock)')
            return False

        self.prqs.append(rq.request_id);
        self.queue.append(rq)
        self.lock.release()
        self.log.Print( 'append (unlock)')
        return True

    def getStrokes(self):
        self.log.Print( 'get strokes (lock)')
        self.lock.acquire()
        self.log.Print( 'get strokes (locked)')
        cp = copy.deepcopy(self.strokes)
        self.lock.release()
        self.log.Print( 'get strokes (unlock)')
        return cp
