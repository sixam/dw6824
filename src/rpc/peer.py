from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4 import QtCore, QtGui
import sys
from rpc.common import PeerState,Request,Operation,OpType
from threading import Thread
from dp.src.rpc.clerk import Clerk
from dp.src.rpc.responder import RPCresponder
import xmlrpclib

class Peer:
    def __init__(self,ip,port,peer_id):
        # Node state
        self.state = PeerState(peer_id)

        # Init main UI

        # Handler for the RPC requests
        self.RPCresponder = RPCresponder(self.state)

        # Accept incoming connections in a background thread
        self.server = SimpleXMLRPCServer((ip,port),allow_none = True)
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

