from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4 import QtCore, QtGui
import sys
from dp.src.utils.log import Log
from rpc.common import PeerState
from dp.src.ui.main_window import MainWindow
from threading import Thread
from dp.src.rpc.clerk import Clerk
from dp.src.rpc.responder import RPCresponder
import xmlrpclib
import socket

class Peer:
    def __init__(self,ip='',port=9011,peer_id=-1,build_ui = True, log = None):
        # Node state
        if ip == '':
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(('google.com',80))
            ip = s.getsockname()[0]
            s.close()
        if not log:
            log = Log('livesession')

        self.id = peer_id
        self.log = log
        self.state = PeerState(peer_id, self.log)
        self.name = '{0}:{1}'.format(ip,port)

        log.blue('\n\nINIT', peer_id)
        log.blue('----------------')
        self.log.blue(ip,port)
        log.blue('----------------')

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
        self.server = SimpleXMLRPCServer((ip,port),logRequests=False,bind_and_activate=False)
        self.server.server_bind()
        self.server.server_activate()
        self.server.register_introspection_functions()
        self.server.register_instance(self.RPCresponder)
        t = Thread(target = self._run,name='{0}:{1}'.format(ip,port))
        t.daemon = True
        t.start()

    def __str__(self):
        return 'peer {0} - {1}'.format(self.id,self.name)

    def _run(self):
        """ Accept incoming connection till exit  """
        self.server.serve_forever()

    def kill(self):
        self.log.red( self,'=> killed')
        self.RPCresponder.kill()

    def revive(self):
        self.log.green( self,'=> revived')
        self.RPCresponder.revive()

    def setUnreliable(self):
        self.log.red( self,'=> unreliable')
        self.RPCresponder.setUnreliable()

    def setReliable(self):
        self.log.green( self,'=> reliable')
        self.RPCresponder.setReliable()

    def addPeer(self,ip,port):
        """ Add a new peer """
        self.state.addPeer(ip,port)

    def getStrokes(self):
        return self.state.getStrokes()

    def thaw(self, sid):
        self.state.thaw(sid)

    def freeze(self, sid):
        self.state.freeze(sid)
