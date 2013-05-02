from threading import Lock, Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import time
from dp.src.protocol.Operation import Operation
from dp.src.protocol.InsertOperation import InsertOperation

class ServerResponder:
    def __init__(self, log):
        self.lock = Lock()
        self.log = log

        self.hosts         = []
        self.ports         = []
        self.locked        = []

        self.participants  = []

        self.startops = []
        self.joinops = []
        self.lockops = []

    def _dispatch(self, method, args):
        try:
            return getattr(self, method)(*args)
        except:
            self.log.exception('Dispatch crashed')

    def _listMethods(self):
        # implement this method so that system.listMethods
        # knows to advertise the strings methods
        return list_public_methods(self) + \
                ['string.' + method for method in list_public_methods(self.string)]

    def checkreplock(self, session):
        return session in self.lockops

    def getLocked(self, session):
        return True

    def checkrepstart(self, ip, port, uid):
        for op in self.startops:
            if op[0] == ip and op[1] == port and op[2] == uid:
                return True
        return False

    def checkrepjoin(self, ip, port, uid, session):
        for op in self.joinops:
            if op[0] == ip and op[1] == port and op[2] == session and op[3] == uid:
                return True
        return False

    def getsession(self, ip, port, uid):
         for op in self.startops:
            if op[0] == ip and op[1] == port and op[2] == uid:
                return op[3]
         return -1

    def getpeers(self, ip, port, uid, session):
        for op in self.joinops:
            if op[0] == ip and op[1] == port and op[2] == session and op[3] == uid:
                return op[4]
        self.log.red('ERROR in cs.getpeers, not found')
        return []


    def start(self, ip, port, uid):
        self.log.red('start called')
        self.lock.acquire()
        count = len(self.hosts)
        self.log.red('COUNT:', count)
        if self.checkrepstart(ip, port, uid):
            self.log.purple('duplicate request')
            value = self.getsession(ip, port, uid)
            self.lock.release()
            return value
        if count  == 0:
            self.hosts = [[]]
            self.ports = [[]]
            self.participants = [[]]
            srv = xmlrpclib.Server('http://%s:%s' % (ip, port))
            self.hosts[0].append(ip)
            self.ports[0].append(port)
            self.participants[0].append(srv)
            self.startops.append([ip, port, count, uid])
            self.locked.append(False)
            self.lock.release()
            return 0
        srv = xmlrpclib.Server('http://%s:%s' % (ip, port))
        self.hosts.append([ip])
        self.ports.append([port])
        self.participants.append([srv])
        self.locked.append(False)
        self.startops.append([ip, port, count, uid])
        self.lock.release()
        return count


    def lockSession(self, session):
        self.log.red('lock session called')
        self.lock.acquire()
        count  = len(self.hosts)
        if session >= count:
            self.lock.release()
            return False
        if self.checkreplock(session):
            self.log.purple('duplicate request')
            value = self.getLocked(session)
            self.lock.release()
            return value
        self.lockops.append(session)
        self.locked[session] = True
        self.lock.release()
        return True

    def join(self, session, ip, port, uid):
        self.log.red('Join Called')
        self.lock.acquire()
        count = len(self.hosts)
        if session >= count:
            self.lock.release()
            return False
        if self.checkrepjoin(ip, port, uid, session):
            self.log.purple('duplicate request')
            value = self.getpeers(ip, port, uid, session)
            self.lock.release()
            return value

        if self.locked[session]:
            self.lock.release()
            return False
                
        # Send vote requests
        self.log.blue(self.participants)
        self.log.blue(self.hosts)
        self.log.blue(self.ports)
        site_count = len(self.hosts[session])
        for srv in self.participants[session]:
            run = True
            count = 0
            while run and count < 10:
                try:
                    v = srv.vote('join',site_count, ip, port)
                    run = False
                except:
                    count += 1
                time.sleep(1)
            self.log.purple(v)
        # Commit or abort
        self.log.red('SITE COUNT:', site_count)
        srv = xmlrpclib.Server('http://%s:%s' % (ip, port))
        self.hosts[session].append(ip)
        self.ports[session].append(port)
        self.participants[session].append(srv)
        # return list of ip,ports,ids
        value = zip(self.hosts[session],self.ports[session])
        self.joinops.append([ip, port, session, uid, value])

        self.log.green('woot')
        self.log.blue(self.participants)
        self.log.blue(self.hosts)
        self.log.blue(self.ports)

        self.lock.release()
        return value
        



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

        log.blue('\n\nINIT - server')
        log.blue('----------------')
        self.log.blue( ip,port)
        log.blue('----------------')


    def _run(self):
        """ Accept incoming connection till exit  """
        self.server.serve_forever()
