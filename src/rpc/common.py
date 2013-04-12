from ui.stroke import Stroke
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
        
class Request:
    def __init__(self,sender=-1,vt=None,op=None,priority=0,request_id=0):
        if isinstance(op,dict):
            self.op = Operation(**op)
        else:
            self.op = op 

        self.sender = sender
        self.vt = vt
        self.priority = priority
        self.request_id = request_id

    def __str__(self):
        return "< sd:{4} | vt:{3} | op:{2} | p:{1} | rid:{0} >".format(
                self.request_id,self.priority,self.op,self.vt,self.sender)

class Operation:
    def __init__(self,type=None,stroke_id=None,stroke=None):
        if isinstance(stroke,dict):
            self.stroke = Stroke(**stroke)
        else:
            self.stroke = stroke

        self.type = type
        self.stroke_id = stroke_id

    def __str__(self):
        return "{{ {0} {1} at }}".format(
                self.type,self.stroke_id)

class OpType:
    ADD = 'ADD'
    DEL = 'DEL'
