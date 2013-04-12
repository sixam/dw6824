from PyQt4 import QtCore, QtGui
from rpc.common import Request

class RPCresponder:
    """ Handles the processing of RPC requests"""
    def __init__(self, state, window):
        # make all of the string functions available through
        # string.func_name
        import string
        self.string = string
        self.window = window
        self.state = state

    def _listMethods(self):
        # implement this method so that system.listMethods
        # knows to advertise the strings methods
        return list_public_methods(self) + \
                ['string.' + method for method in list_public_methods(self.string)]

    # RPC methods
    def enq(self,rqData):
        """ Unmarshalls the request and add it to the queue"""
        # NOTE : this should be lock-secured

        rq = Request(**rqData)
        print 'received', rq
        self.state.queue.append(rq)

        self.state.executeOperations()
        return True
