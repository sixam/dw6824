from PyQt4 import QtCore, QtGui
from utils.utils import Utils

from protocol.Operation import Operation
from protocol.InsertOperation import InsertOperation
from protocol.DeleteOperation import DeleteOperation
from protocol.UpdateOperation import UpdateOperation

import xmlrpclib

class Incoming:
    """ Represents the incoming peer trying to join """
    def __init__(self):
        self.id = -1
        self.ip = ''
        self.port = 0

class RPCresponder:
    """ Handles the processing of RPC requests"""
    def __init__(self, state):
        # make all of the string functions available through
        # string.func_name
        import string
        self.string = string
        self.state = state
        self.unreliable = False
        self.dead = False
        self.log = state.log
        self.knownids = []

        # join related
        self.incoming = Incoming()

    def _dispatch(self, method, args):
        try:
            return getattr(self, method)(*args)
        except:
            self.log.exception('DISPATCH EXCEPTION (rpc responder)')


    def _listMethods(self):
        # implement this method so that system.listMethods
        # knows to advertise the strings methods
        return list_public_methods(self) + \
                ['string.' + method for method in list_public_methods(self.string)]

    def setUnreliable(self):
        self.unreliable = True

    def setReliable(self):
        self.unreliable = False

    def kill(self):
        self.dead = True

    def revive(self):
        self.dead = False

    # RPC methods
    def enq(self,packet):
        """ Unmarshalls the request and add it to the queue"""
        if self.dead:
            return 

        otype = packet['type'] if 'type' in packet else None

        if otype == 'insert':
            op = InsertOperation.unmarshall(packet)
        elif otype == 'delete':
            op = DeleteOperation.unmarshall(packet)
        elif otype == 'update':
            op = UpdateOperation.unmarshall(packet)

        self.log.rpc('received:',op)
        if op.key != self.state.session:
            return False

        for ip in op.ips:
            if ip == self.state.ip and op.ports[op.ips.index(ip)] == self.state.port :
                continue
            if ip not in self.state.ips:
                port = op.ports[op.ips.index(ip)]
                id = op.siteId
                srv = xmlrpclib.Server('http://%s:%s' % (ip, port))
                self.log.Print(' added peer:',srv,'\n')
                self.state.peers.append(srv)
                self.state.thaw(id)
                self.state.ips.append(ip)
                self.state.ports.append(port)
                

        accepted = self.state.receiveOp(op)

        if accepted:
            return True
        else:
            return False

    def vote(self, t, id, ip, port):
        self.log.green('vote asked')
        #self.lock.acquire()
        if id in self.knownids:
            return True
        self.incoming.id = id
        self.incoming.ip = ip
        self.incoming.port = port
        #self.lock.release()
        srv = xmlrpclib.Server('http://%s:%s' % (self.incoming.ip, self.incoming.port))
        self.state.peers.append(srv)
        self.state.ips.append(ip)
        self.state.ports.append(port)
        self.log.orange('thawing', id)
        self.state.thaw(id)
        self.log.Print(' added peer:',srv,'\n')
        self.knownids.append(id)

        return True

    def join(self, ip, port,bl):
        self.log.red('fucked up dude')
