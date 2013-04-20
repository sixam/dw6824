from PyQt4 import QtCore, QtGui
from utils.utils import Utils

from dp.src.protocol.Operation import Operation
from dp.src.protocol.InsertOperation import InsertOperation

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

        op = InsertOperation.unmarshall(packet)
        done = self.state.receiveOp(op)

        if self.dead:
            return 

        #if self.unreliable:
            #pass

        return done

