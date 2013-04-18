from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4 import QtCore, QtGui
import sys
from rpc.common import PeerState,Request,Operation,OpType
from dp.src.ui.main_window import MainWindow
from threading import Thread
from dp.src.rpc.clerk import Clerk
from dp.src.rpc.responder import RPCresponder
import xmlrpclib

class Peer:
    def __init__(self,ip,port,peer_id,build_ui = True):
        # Node state
        self.id = peer_id
        self.state = PeerState(peer_id)
        self.name = '{0}:{1}'.format(ip,port)
        
        print ip,port

        # Init main UI
        if build_ui:
            self.window = MainWindow(self.state)
            self.window.show()
            self.window.raise_()
            self.state.window = self.window
            self.state.newStrokesSignal.connect(self.window.scribbleArea.strokesSignalHandler)

        # Handler for the RPC requests
        self.RPCresponder = RPCresponder(self.state)

        # Accept incoming connections in a background thread
        self.server = SimpleXMLRPCServer((ip,port),logRequests=True,bind_and_activate=False)
        self.server.allow_reuse_address=True
        self.server.register_introspection_functions()
        self.server.register_instance(self.RPCresponder)
        t = Thread(target = self._run,name='{0}:{1}'.format(ip,port))
        t.daemon = True
        t.start()

    def __str__(self):
        return 'peer {0} : {1}'.format(self.id,self.name)

    def _run(self):
        """ Accept incoming connection till exit  """
        try:
            self.server.serve_forever()
        finally:
            self.server.server_close()
            print 'server closed'

    def __del__(self):
        pass
        #self.server.server_close()
        #del self.server

    def addPeer(self,ip,port):
        """ Add a new peer """

        srv_name = 'http://%s:%s' % (ip, port)
        srv = xmlrpclib.Server(srv_name)
        self.state.peers.append(srv)
        print 'added peer:',srv_name

