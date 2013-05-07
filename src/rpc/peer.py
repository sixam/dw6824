from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4 import QtCore, QtGui
import sys
from utils.log import Log
from rpc.common import PeerState
from ui.main_window import MainWindow
from threading import Thread
from rpc.clerk import Clerk
from rpc.responder import RPCresponder
import xmlrpclib
import socket

class Peer:
    def __init__(self,ip='',port=9011,peer_id=-1,build_ui = True, log = None):
        # Node state
        if ip == '':
            self.ip = self._getIP()
        else:
            self.ip = ip
        if not log:
            log = Log('livesession')

        self.id         = peer_id
        self.port       = port
        self.log        = log
        self.name       = '{0}:{1}'.format(self.ip,port)
        self.state      = PeerState(peer_id, self.log)
        self.state.ip   = self.ip
        self.state.port = self.port
        self.state.ips.append(self.state.ip)
        self.state.ports.append(self.state.port)

        # Print start
        log.blue('\n\nINIT', self.id)
        log.blue('-'*(len(self.ip.__str__())+len(self.port.__str__())+3))
        self.log.blue(self.ip, ":", self.port)
        log.blue('-'*(len(self.ip.__str__())+len(self.port.__str__())+3))

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

    def _getIP(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('google.com',80))
        ip = s.getsockname()[0]
        s.close()
        return ip

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
