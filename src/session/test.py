import xmlrpclib
from dp.src.session.central import CentralServer
from dp.src.session.dummyclient import DummyClient
from dp.src.utils.log import Log

if __name__ == '__main__':
    sp              = 9005
    pbase           = 8005

    lc              = Log(100)
    cs              = CentralServer('localhost', sp, lc)
    csrv            = xmlrpclib.Server('http://%s:%s' % ('localhost', sp))

    n = 4
    dc = []
    cssrv = []
    l = []
    for i in range(4):
        l.append(Log(i))
        cssrv.append(xmlrpclib.Server('http://%s:%s' % ('localhost', sp)))
        dc.append(DummyClient('localhost', pbase + i, l[i], cssrv[i])
    sessions = []
    for i in range(floor(n/2)):
        sessions.append(dc[i].cstart('localhost', pbase + 1))
    m = len(sessions)
    for i in range(m,n):
        dc[i].cjoin(session[i - m], 'localhost',pbase + i)
