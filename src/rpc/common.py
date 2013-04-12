from ui.stroke import Stroke
from rpc.priority import Priority

class PeerState:
    """Stores all data concerning a peer's state

    Contains:
        - list of other peers
        - dOPT structures
        - drawn objects (strokes)

    Is shared between UI and Network threads
    
    """
    # NOTE: lock around access to the structure?
    def __init__(self):
        self.id      = 0
        self.peers   = []
        self.queue   = []
        self.log     = []
        self.vt      = [0 for x in range(3)]
        self.strokes = []

    def executeOperations(self):
        #NOTE: should be locking
        for i,request in enumerate(self.queue):
            del self.queue[i]


            
        
class Request:
    def __init__(self,sender=-1,vt=None,op=None,priority=0,request_id=0):
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
        return "< sd:{4} | vt:{3} | op:{2} | p:{1} | rid:{0} >".format(
                self.request_id,self.priority,self.op,self.vt,self.sender)

class Operation:
    def __init__(self,type=None,stroke_id=None,stroke=None,pos=-1,opos=-1):
        if isinstance(stroke,dict):
            self.stroke = Stroke(**stroke)
        else:
            self.stroke = stroke

        self.type = type
        self.stroke_id = stroke_id
        self.stroke = stroke
        self.pos = pos
        if opos == -1:
            self.opos = pos
        else: # unmarshalling
            self.opos = opos

    def __str__(self):
        return "{{ {0} {1} at }}".format(
                self.type,self.stroke_id)

class OpType:
    ADD = 'ADD'
    DEL = 'DEL'
