from PyQt4 import QtCore, QtGui
from rpc.common import Request

class RPCresponder:
    """ Handles the processing of RPC requests"""
    def __init__(self, state):
        # make all of the string functions available through
        # string.func_name
        import string
        self.string = string
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
        print '\033[31m-acquire Responder\033[0m'
        self.state.lock.acquire()

        rq = Request(**rqData)
        self.state.queue.append(rq)

        self.state.executeOperations()
        print '\033[31m-release Responder\033[0m'
        self.state.lock.release()
        return True
