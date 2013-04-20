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
        self.processed_ops = []

        # attached ui
        self.window = None

        self.lock = Lock()

        # site log file
        self.log = log

        self.engine = OperationEngine(self.id,log)


    def performOperation(self,op):
        if op.type == 'insert':
            m = len(self.strokes)
            for i in range(m, op.position+1):
                self.strokes.insert(i,None)
            if self.strokes[op.position]:
                self.strokes.insert(op.position,Stroke(**op.value))
            else: # none: replace
                self.strokes[op.position]=Stroke(**op.value)

        #if op.type == OpType.DEL:
            #self.log.Print( self.strokes)
            #del self.strokes[op.pos]
            #self.log.Print( self.strokes)
        #if op.type == OpType.MOVE:
            #self.strokes[op.pos].moveTo(op.offset)
            #self.log.Print( self.strokes)
            
        if self.window: #Dont call UI (for the tester)
            # Send signal to UI
            self.newStrokesSignal.emit()
            self.window.scribbleArea.draw()

    def createOp(self,otype,stroke=None):
        self.log.Print( 'new op (lock)')
        self.lock.acquire()
        self.log.Print( 'new op (locked)')

        key = 'a'
        val = stroke.marshall()
        self.log.red('STROKE',val)

        op = self.engine.createOp(True,key,val,otype,self.id)

        self.engine.pushLocalOp(op)
        self.processed_ops.append(op)
        self.log.Print('buffer size:',self.engine.getBufferSize())

        self.lock.release()
        self.log.Print( 'new op (unlock)\n')
        self.log.red('CREATE: Perfom op')
        self.performOperation(op)
        return op


    def receiveOp(self, op):
        self.log.Print( 'receive op (lock)')
        self.lock.acquire()
        self.log.Print( 'receive op (locked)')

        # check duplicates
        self.log.orange('has processed?')
        seen = self.engine.hasProcessedOp(op)
        self.log.orange('has processed?returned')
        if not seen:
            self.log.green('not seen:push')
            new_op = self.engine.pushRemoteOp(op)
            self.processed_ops.append(new_op)
            self.log.green('not seen:pushed')
            self.log.Print('buffer size:',self.engine.getBufferSize())
        else:
            self.log.Print( 'already seen')
            self.lock.release()
            self.log.Print( 'receiv op (unlock)\n')
            return False

        self.lock.release()
        self.log.red('RECEIVE: Perfom op')
        self.performOperation(new_op)
        self.log.Print( 'receive op (unlock)\n')
        return True

    def getStrokes(self):
        self.log.Print( 'get strokes (lock)')
        self.lock.acquire()
        self.log.Print( 'get strokes (locked)')
        cp = copy.deepcopy(self.strokes)
        self.lock.release()
        self.log.Print( 'get strokes (unlock)\n')

        self.log.purple(self.engine.getBufferSize())

        self.printProcessedOps()
        self.printHistoryBuffer()
        self.printStrokes()

        self.log.purple('current context:',self.engine.copyContextVector())

        return cp

    def printProcessedOps(self):
        self.log.blue( '\n-------------------- PROCESSED  -------------------------------------------')
        self.log.Print( len(self.processed_ops), 'operations')
        for i,op in enumerate(self.processed_ops):
            self.log.Print(op)
        self.log.blue( '----------------------------------------------------------------------\n')

    def printHistoryBuffer(self):
        self.log.blue( '\n-------------------- HISTORY BUFFER  -------------------------------------------')
        self.log.Print( len(self.engine.hb.ops), 'operations')
        for i,op in enumerate(self.engine.hb.ops):
            self.log.Print(op)
        self.log.blue( '----------------------------------------------------------------------\n')

    def printStrokes(self):
        self.log.blue( '\n-------------------- STROKES ---------------------------------------------')
        self.log.Print( len(self.strokes), 'strokes')
        for i,s in enumerate(self.strokes):
            self.log.Print( i,'-',s)
        self.log.blue( '--------------------------------------------------------------------------')


