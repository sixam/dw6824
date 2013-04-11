import xmlrpclib
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
            srv.add_stroke(s)
            print srv,'sent stroke:',s

    def moveStroke(self):
        pass

    def deleteStroke(self):
        pass
