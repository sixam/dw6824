from threading import Lock, Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import time
from dp.src.session.central import CentralServer

class Incoming:
    def __init__(self):
        self.id = -1
        self.ip = ''
        self.port = 0

class ClientResponder:
    def __init__(self, log):
        self.lock = Lock()
        self.log = log

        self.peers = []
        self.incoming = Incoming()

    def _dispatch(self, method, args):
        try:
            return getattr(self, method)(*args)
        except:
            self.log.exception('FFFFFFFFUUUUUUUCCCKKKK')


    def _listMethods(self):
        # implement this method so that system.listMethods
        # knows to advertise the strings methods
        return list_public_methods(self) + \
                ['string.' + method for method in list_public_methods(self.string)]

    def vote(self, t, id, ip, port):
        self.log.green('vote asked')
        self.lock.acquire()
        self.incoming.id = id
        self.incoming.ip = ip
        self.incoming.port = port
        self.lock.release()
        self.log.green('Vote OK')
        return True

    def commit(self, t, id, vote, ip, port):
        self.log.green('commit received')
        self.lock.acquire()
        if vote == True:
            srv = xmlrpclib.Server('http://%s:%s' % (self.incoming.ip, self.incoming.port))
            m = len(self.peers)
            for i in range(m, id + 1):
                self.peers.insert(i, None)
            self.peers[id] = srv
        self.lock.release()
        return True
        

class DummyClient:
    def __init__(self, ip, port, log=None, cs=None):
        # Node state
        self.log = log

        # Handler for the RPC requests
        self.responder = ClientResponder(log)

        # Accept incoming connections in a background thread
        self.server = SimpleXMLRPCServer((ip,port),logRequests=False,bind_and_activate=False)
        self.server.server_bind()
        self.server.server_activate()
        self.server.register_introspection_functions()
        self.server.register_instance(self.responder)
        t = Thread(target = self._run,name='{0}:{1}'.format(ip,port))
        t.daemon = True
        self.cs = cs
        t.start()


    def cjoin(self, session, ip, port):
        self.cs.join(session, ip, port)

    def cstart(self, ip, port):
        return self.cs.start(ip, port)
        


    def _run(self):
        """ Accept incoming connection till exit  """
        self.server.serve_forever()
