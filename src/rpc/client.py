import xmlrpclib
class Client:
    def __init__(self,peers):
        self.request_queue = []
        self.request_log   = []
        self.state_vector  = []
        self.peers         = peers
        
    def addStroke(self,s):
        # compute operation priority

        # add op to the queue
        print self.peers

        for srv in self.peers:
            srv.add_stroke(s)
            print srv,'sent stroke:',s

    def moveStroke(self):
        pass

    def deleteStroke(self):
        pass
