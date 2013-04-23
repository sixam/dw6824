from ui.stroke import Stroke
from threading import Lock
from PyQt4 import QtCore, QtGui
from dp.src.utils.log import Log
import copy

from dp.src.protocol.OperationEngine import OperationEngine
from dp.src.protocol.Queue import Queue

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
        self.processed_ops = []

        # attached ui
        self.window = None

        self.lock = Lock()

        # site log file
        self.log = log

        self.engine = OperationEngine(self.id,log)
        self.queue  = Queue(log)
        self.log.Print("yo",self.queue)
    
    def thaw(self, sid):
        self.lock.acquire()
        self.engine.thawSite(sid)
        self.lock.release()


    def freeze(self, sid):
        self.lock.acquire()
        self.engine.freezeSite(sid)
        self.lock.release()

    def performOperation(self,op):
        if op.type == 'insert':
            m = len(self.strokes)
            for i in range(m, op.position+1):
                self.strokes.insert(i,None)
            if self.strokes[op.position]:
                self.strokes.insert(op.position,Stroke(**op.value))
            else: # none: replace
                self.strokes[op.position]=Stroke(**op.value)

        if op.type == 'delete':
            del self.strokes[op.position]

        if op.type == 'update':
            self.strokes[op.position] = Stroke(**op.value)

        if self.window: #Dont call UI (for the tester)
            pass
            # Send signal to UI

    def createOp(self,otype,stroke=None,pos=-1):
        self.log.Print( 'new op (lock)')
        self.lock.acquire()
        self.log.Print( 'new op (locked)')

        key = 'strokes'
        if otype == 'insert':
            val = stroke.marshall()
            position = len(self.strokes)
        elif otype == 'delete':
            val = Stroke().marshall()
            position = pos
        elif otype == 'update':
            val = stroke.marshall()
            position = pos

        op = self.engine.createOp(True,key,val,otype,position)

        self.log.blue('created op :',op)

        self.engine.pushLocalOp(op)
        self.processed_ops.append(op)

        self.performOperation(op)
        self.lock.release()
        if self.window: #Dont call UI (for the tester)
            self.newStrokesSignal.emit()
        self.log.Print( 'new op (unlock)\n')
        return op


    def receiveOp(self, op):
        self.log.Print( 'receive op (lock)')
        self.lock.acquire()
        self.log.Print( 'receive op (locked)')

        # check duplicates
        seen = self.engine.hasProcessedOp(op)
        if seen:
            self.log.orange('already seen')
            self.lock.release()
            self.log.Print('receive op (unlock)\n')
            return True
        self.queue.enqueue(op)

        self.log.blue('after enqueue')
        self.printQueue()
        added = 0
        cv = self.engine.copyContextVector()
        while True:
            cv = self.engine.copyContextVector()
            processable = self.queue.getProcessable(cv)
            if not processable:
                break
            new_op = self.engine.pushRemoteOp(processable)
            self.processed_ops.append(new_op)
            self.performOperation(new_op)
            added += 1

        self.log.blue('after dequeue')
        self.printQueue()

        self.log.green('receive: added',added,'operations')
        self.lock.release()
        self.log.Print( 'receive op (unlock)\n')

        #Dont call UI (for the tester)
        if self.window: 
            self.newStrokesSignal.emit()

        self.log.Print( 'receive op (unlock)\n')
        return True

    def getStrokes(self):
        self.log.Print( 'get strokes (lock)')
        self.lock.acquire()
        self.log.Print( 'get strokes (locked)')
        cp = copy.deepcopy(self.strokes)
        self.lock.release()
        self.log.Print( 'get strokes (unlock)\n')

        self.printFinalState()
        return cp

    def printFinalState(self):
        self.printProcessedOps()
        self.printHistoryBuffer()
        self.printStrokes()
        self.printQueue()

    def printProcessedOps(self):
        self.log.blue( '\n-------------------- PROCESSED  -------------------------------------------')
        self.log.Print( len(self.processed_ops), 'operations')
        for i,op in enumerate(self.processed_ops):
            self.log.Print(op)
        self.log.blue( '----------------------------------------------------------------------\n')

    def printHistoryBuffer(self):
        self.log.blue( '\n-------------------- HISTORY BUFFER  -------------------------------------------')
        self.log.Print( len(self.engine.hb.ops), 'operations')
        for op in self.engine.hb.ops:
            self.log.Print(self.engine.hb.ops[op])
        self.log.blue( '----------------------------------------------------------------------\n')

    def printQueue(self):
        self.log.blue( '\n-------------------- QUEUE  -------------------------------------------')
        self.log.Print( len(self.queue.ops), 'operations | ds:',self.engine.copyContextVector())
        for op in self.queue.ops:
            self.log.Print(self.queue.ops[op])
        self.log.blue( '----------------------------------------------------------------------\n')

    def printStrokes(self):
        self.log.blue( '\n-------------------- STROKES ---------------------------------------------')
        self.log.Print( len(self.strokes), 'strokes')
        for i,s in enumerate(self.strokes):
            self.log.Print( i,'-',s)
        self.log.blue( '--------------------------------------------------------------------------')



