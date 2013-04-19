import copy
from ui.stroke import Stroke
from rpc.priority import Priority

class Request:
    def __init__(self,sender=-1,vt=[],op=None,priority=0,request_id='none',context=[]):
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
        self.context = context

    def __str__(self):
        return "< sd:{4} | ct:{3} | op:{2} | {1} |  rid:{0} >".format(
                self.request_id[0:5], self.priority,self.op,self.context,self.sender)
    def __copy__(self):
        new = Request()
        new.op = copy.copy(self.op)
        new.vt = copy.copy(self.vt)
        new.priority = copy.copy(self.priority)
        new.sender = copy.copy(self.sender)
        new.request_id = copy.copy(self.request_id)
        new.context = self.context
        return new
       

class Operation:
    def __init__(self,type=None,stroke_id='none',stroke=None,pos=-1,opos=-1,offset=[0,0]):
        if isinstance(stroke,dict):
            self.stroke = Stroke(**stroke)
        else:
            self.stroke = stroke

        self.type      = type
        self.stroke_id = stroke_id
        self.pos       = pos
        self.offset    = offset

        if opos == -1:
            self.opos = pos
        else: # unmarshalling
            self.opos = opos

    def __str__(self):
        return "{{ {0} {1} at {2}({3})}} - {4}".format(
                self.type,self.stroke_id[0:5],self.pos,self.opos,self.offset)

    def __copy__(self):
        new = Operation()
        new.stroke = copy.copy(self.stroke)
        new.type = copy.copy(self.type)
        new.stroke_id = copy.copy(self.stroke_id)
        new.pos = copy.copy(self.pos)
        new.opos = copy.copy(self.opos)
        new.offset = self.offset
        return new

class OpType:
    ADD = 'ADD'
    DEL = 'DEL'
    MOVE = 'MOV'
    NoOp = 'NoOp'
