from PyQt4 import QtCore, QtGui
from utils.utils import Utils

from dp.src.protocol.Operation import Operation

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

        self.log.Print("received",packet)

        op = Operation.unmarshall(packet)
        self.log.Print('unmarshalled op',op.siteId,op.seqId,op.contextVector)

        self.state.receiveOp(op)

        return True

        #if self.dead:
            #self.log.Print( 'I am dead dude, fuck off')
            #return 
            #pass

        #if self.unreliable:
            #self.log.Print( 'I am unreliable dude, ahah')
            #pass

