from threading import Lock, Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import time
import dp.src.protocol.Operation
from dp.src.protocol.Operation import Operation
from dp.src.protocol.InsertOperation import InsertOperation

class ServerResponder:
    def __init__(self, log):
        self.lock = Lock()
        self.log = log

        self.hosts         = []
        self.ports         = []

        self.participants  = []

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

    def join(self, session, ip, port):
        """ Starts a 2PC with all participants to commit a new peer"""
        self.log.red('Join Called')
        self.lock.acquire()
        count = len(self.hosts)
        self.log.red('COUNT:', count)
        if count  == 0:
            for i in range(session + 1):
                self.hosts = [[]]
                self.ports = [[]]
                self.participants = [[]]
                self.hosts[session]         = []
                self.ports[session]         = []
                self.participants[session]  = []

            srv = xmlrpclib.Server('http://%s:%s' % (ip, port))
            self.hosts[session].append(ip)
            self.ports[session].append(port)
            self.participants[session].append(srv)
            self.lock.release()
            return True


        # Send vote requests
        v = True
        self.log.blue(self.participants)
        self.log.blue(self.hosts)
        self.log.blue(self.ports)
        for srv in self.participants[session]:
            run = True
            while run :
                try:
                    v = srv.vote('join',count, ip, port)
                    run = False
                except:
                    pass
                time.sleep(1)
            self.log.purple(v)
            if v == False:
                break
        # Commit or abort
        for srv in self.participants[session]:
            run = True
            while run :
                self.log.purple('commit round')
                try:
                   v = srv.commit('join',count, v, ip, port)
                   run = False
                except:
                   pass
                time.sleep(1)
        if v == True:
            m = len(self.hosts)
            for i in range(m, session + 1):
               self.hosts[session]         = []
               self.ports[session]         = []
               self.participants[session]  = []
            srv = xmlrpclib.Server('http://%s:%s' % (ip, port))
            self.hosts[session].append(ip)
            self.ports[session].append(port)
            self.participants[session].append(srv)
        self.log.green('woot')
        self.log.blue(self.participants)
        self.log.blue(self.hosts)
        self.log.blue(self.ports)

        self.lock.release()
        return True
        



class CentralServer:
    def __init__(self, ip, port, log=None):
        # Node state
        self.log = log

        # Handler for the RPC requests
        self.responder = ServerResponder(log)

        # Accept incoming connections in a background thread
        self.server = SimpleXMLRPCServer((ip,port),logRequests=False,bind_and_activate=False)
        self.server.server_bind()
        self.server.server_activate()
        self.server.register_introspection_functions()
        self.server.register_instance(self.responder)
        t = Thread(target = self._run,name='{0}:{1}'.format(ip,port))
        t.daemon = True
        t.start()


    def _run(self):
        """ Accept incoming connection till exit  """
        self.server.serve_forever()
