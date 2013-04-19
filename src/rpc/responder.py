from PyQt4 import QtCore, QtGui
from dp.src.rpc.commontypes import Request, Operation
from utils.utils import Utils

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
    def enq(self,rqData):
        """ Unmarshalls the request and add it to the queue"""

        if self.dead:
            print 'I am dead dude, fuck off'
            return 
            pass

        if self.unreliable:
            print 'I am unreliable dude, ahah'
            pass

        rq = Request(**rqData)

        #print 'Responder, rq:', rq
        appended = self.state.appendToQueue(rq)
        if not appended:
            return True
        self.state.executeOperations()
        return True
