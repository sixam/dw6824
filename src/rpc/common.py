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
        self.vt      = [0 for x in range(64)]
        self.strokes = []
        
class Request:
    def __init__(self,sender=-1,vt=None,op=None,priority=0,request_id=0, pos = 0, opos = 0):
        self.sender = sender
        self.vt = vt
        self.op = op 
        self.priority = priority
        self.request_id = request_id
		self.pos = pos
		self.opos = opos

class Operation:
    def __init__(self,type=None,stroke_id=None,stroke=None):
        self.type = type
        self.stroke_id = stroke_id
        self.stroke = stroke

class OpType:
    ADD = 'Add'
    DEL = 'Delete'
