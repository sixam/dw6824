import xmlrpclib
class MoveOp:
    def __init__(self,id,offset):
        self.id = id
        self.offset = offset


class Clerk:
    """ Clerk for the UI thread, handles the emission of RPC calls"""
    def __init__(self,state):
        self.peers         = state.peers
        
    def addStroke(self,s):
        # compute operation priority

        # add op to the queue

        print self.peers

        # broadcast to peers
        for srv in self.peers:
            srv.addStroke(s)
            print srv,'sent stroke:',s

    def moveStroke(self,id,offset):
        for srv in self.peers:
            off = [offset.x(), offset.y()]
            mOp = MoveOp(id,off)
            srv.moveStroke(mOp)

    def deleteStroke(self):
        pass
