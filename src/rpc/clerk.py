import xmlrpclib
class Clerk:
    def __init__(self,peers=[]):
        self.peers = peers
        
    def addPeer(self,srv_name):
        srv = xmlrpclib.Server(srv_name)
        self.peers.append(srv)
        print 'added peer:',srv_name

    def sendStroke(self,s):
        for srv in self.peers:
            srv.add_stroke(s)
            print srv,'sent stroke:',s

        
