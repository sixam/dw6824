from SimpleXMLRPCServer import SimpleXMLRPCServer
from dp.src.ui.main_window import MainWindow
from PyQt4 import QtCore, QtGui
import sys
from threading import Thread
from dp.src.rpc.client import Client
from dp.src.rpc.responder import RPCresponder

class Peer:
    def __init__(self,identifier,port):
        # Node state
        self.peers         = []
        self.request_queue = []
        self.request_log   = []
        self.state_vector  = []

        self.server = SimpleXMLRPCServer((identifier,port))
        self.server.register_introspection_functions()

        self.client = Client()

        self.window = MainWindow(self.client)
        self.window.show()

        self.client.add()

        self.RPCresponder = RPCresponder(self.window)
        self.server.register_instance(self.RPCresponder)

        t = Thread(target = self.run)
        t.daemon = True
        t.start()

    def run(self):
        self.server.serve_forever()

    def addPeer(self,srv_name):
        srv = xmlrpclib.Server(srv_name)
        self.peers.append(srv)
        print 'added peer:',srv_name

