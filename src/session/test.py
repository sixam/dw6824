import xmlrpclib
import random
from math import floor
from dp.src.session.central import CentralServer
from dp.src.session.dummyclient import DummyClient
from dp.src.utils.log import Log

if __name__ == '__main__':
    sp              = 9005
    pbase           = 8005

    lc              = Log(100)
    cs              = CentralServer('localhost', sp, lc)
    csrv            = xmlrpclib.Server('http://%s:%s' % ('localhost', sp))

    n = 10
    dc = []
    cssrv = []
    l = []
    for i in range(n):
        l.append(Log(i))
        cssrv.append(xmlrpclib.Server('http://%s:%s' % ('localhost', sp)))
        dc.append(DummyClient('localhost', pbase + i, l[i], cssrv[i]))

#    s = dc[0].cstart('localhost', pbase)
#    dc[1].cjoin(s, 'localhost', pbase + 1)
#
#    s = dc[2].cstart('localhost', pbase + 2)
#    dc[3].cjoin(s, 'localhost', pbase + 3)
#
#
    sessions = []
    for i in range(int(floor(n/2))):
        sessions.append(dc[i].cstart('localhost', pbase + i))
    m = len(sessions)
    for i in range(m,n):
        s = random.randint(m,n - 1)
        dc[i].cjoin(sessions[i - m], 'localhost',pbase + i)
