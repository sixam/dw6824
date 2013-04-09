import xmlrpclib
class Client:
    def __init__(self):
        self.peers         = []
        self.request_queue = []
        self.request_log   = []
        self.state_vector  = []
        self.x = 0
        
    def add(self):
        self.x += 1
    def addPeer(self,srv_name):
        srv = xmlrpclib.Server(srv_name)
        self.peers.append(srv)
        print 'added peer:',srv_name

    def addStroke(self,s):
        # compute operation priority

        # add op to the queue

        for srv in self.peers:
            srv.add_stroke(s)
            print srv,'sent stroke:',s

    def moveStroke(self):
        pass

    def deleteStroke(self):
        pass

        
