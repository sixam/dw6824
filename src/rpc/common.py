from ui.stroke import Stroke
from threading import Lock
from PyQt4 import QtCore, QtGui
from dp.src.utils.log import Log
import copy

from dp.src.protocol.OperationEngine import OperationEngine
from dp.src.protocol.Queue import Queue
from dp.src.protocol.OperationEngineException import OperationEngineException

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

        # logging options
    
    def thaw(self, sid):
        self.log.lock( 'thaw (lock)')
        self.lock.acquire()
        self.log.lock( 'thaw (locked)')
        self.engine.thawSite(sid)
        self.lock.release()
        self.log.lock( 'thaw (unlock)')


    def freeze(self, sid):
        self.log.lock( 'freeze (lock)')
        self.lock.acquire()
        self.log.lock( 'freeze (locked)')
        self.engine.freezeSite(sid)
        self.log.lock( 'freeze (unlock)')
        self.lock.release()

    def performOperation(self,op):
        if not op:
            self.log.red('ERROR: trying to perform a none op')
            return
        if op.type == 'insert':
            m = len(self.strokes)
            for i in range(m, op.position+1):
                self.strokes.insert(i,None)
            if self.strokes[op.position]:
                self.strokes.insert(op.position,Stroke(**op.value))
            else: # none: replace
                self.strokes[op.position]=Stroke(**op.value)

        if op.position not in range(0,len(self.strokes)):
            self.log.orange("can't move/delete stroke that doesn't exist, asked:",op.position,'max',len(self.strokes)-1)
            return

        if op.type == 'delete':
            del self.strokes[op.position]

        if op.type == 'update':
            self.strokes[op.position] = Stroke(**op.value)

        if self.window: #Dont call UI (for the tester)
            pass
            # Send signal to UI

    def createOp(self,otype,stroke=None,pos=-1,order=-1):
        self.log.lock( 'create op (lock)')
        self.lock.acquire()
        self.log.lock( 'create op (locked)')

        key = 'strokes'
        val = stroke.marshall()
        if otype == 'insert':
            position = len(self.strokes)
        elif otype == 'delete':
            position = pos
        elif otype == 'update':
            position = pos

        op = self.engine.createOp(True,key,val,otype,position)
        if order >= 0:
            op.order = order

        self.engine.pushLocalOp(op)
        self.processed_ops.append(op)

        self.performOperation(op)
        self.lock.release()
        self.log.lock( 'create op (unlock)\n')
        if self.window: #Dont call UI (for the tester)
            self.newStrokesSignal.emit()
        return op


    def receiveOp(self, op):
        self.log.lock( 'receive op (lock)')
        self.lock.acquire()
        self.log.lock( 'receive op (locked)')

        # check duplicates
        seen = self.engine.hasProcessedOp(op)
        if seen:
            self.log.engine('refused,already seen:',op)
            self.lock.release()
            self.log.lock('receive op (unlock)\n')
            return True
        self.queue.enqueue(op)

        added = 0
        cv = self.engine.copyContextVector()
        while True:
            cv = self.engine.copyContextVector()
            processable = self.queue.getProcessable(cv)
            if not processable:
                break
            new_op = self.engine.pushRemoteOp(processable)
            self.performOperation(new_op)
            self.processed_ops.append(new_op)
            added += 1


        self.lock.release()
        self.log.lock( 'receive op (unlock)\n')

        #Dont call UI (for the tester)
        if self.window: 
            self.newStrokesSignal.emit()

        return True

    def getStrokes(self):
        self.log.lock( 'get strokes (lock)')
        self.lock.acquire()
        self.log.lock( 'get strokes (locked)')
        cp = copy.deepcopy(self.strokes)
        self.lock.release()
        self.log.lock( 'get strokes (unlock)\n')

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
        ops = self.engine.hb.getMorrisSortedOperations()
        for op in ops:
            self.log.Print(op)
        self.log.blue( '----------------------------------------------------------------------\n')

    def printQueue(self):
        self.log.blue( '\n-------------------- QUEUE  -------------------------------------------')
        self.log.Print( len(self.queue.ops), 'operations | ds:',self.engine.copyContextVector())
        ops = self.queue.getMorrisSortedOperations()
        for op in ops:
            self.log.Print(op)
        self.log.blue( '----------------------------------------------------------------------\n')

    def printStrokes(self):
        self.log.blue( '\n-------------------- STROKES ---------------------------------------------')
        self.log.Print( len(self.strokes), 'strokes')
        for i,s in enumerate(self.strokes):
            self.log.Print( i,'-',s)
        self.log.blue( '--------------------------------------------------------------------------')



