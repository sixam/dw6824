from SimpleXMLRPCServer import SimpleXMLRPCServer
from dp.src.ui.main_window import MainWindow
from PyQt4 import QtCore, QtGui
import sys
from threading import Thread
from dp.src.rpc.client import Client
from dp.src.rpc.responder import RPCresponder
import xmlrpclib

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
        self.peers         = []
        self.request_queue = []
        self.request_log   = []
        self.state_vector  = []
        self.strokes       = []
        

class Peer:
    def __init__(self,ip,port):
        # Node state
        self.state = PeerState()

        # Init main UI
        self.window = MainWindow(self.state)
        self.window.show()

        # Handler for the RPC requests
        self.RPCresponder = RPCresponder(self.state,self.window)

        # Accept incoming connections in a background thread
        self.server = SimpleXMLRPCServer((ip,port))
        self.server.register_introspection_functions()
        self.server.register_instance(self.RPCresponder)
        t = Thread(target = self._run)
        t.daemon = True
        t.start()

    def _run(self):
        """ Accept incoming connection till exit  """
        self.server.serve_forever()

    def addPeer(self,ip,port):
        """ Add a new peer """

        srv_name = 'http://%s:%s' % (ip, port)
        srv = xmlrpclib.Server(srv_name)
        self.state.peers.append(srv)
        print 'added peer:',srv_name

